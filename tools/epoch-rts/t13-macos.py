#!/usr/bin/env python3
"""Purpose: Isolated native R28 save/load evidence runner. Created: 2026-09-27.
SPDX-License-Identifier: GPL-2.0-or-later
"""
import argparse
import datetime
import hashlib
import importlib.util
import json
import pathlib
import re
import subprocess
import time

ROOT = pathlib.Path(__file__).resolve().parents[2]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frames(text):
    grouped = {}
    for part in text.split('EPOCH_T13_FRAME ')[1:]:
        frame = json.JSONDecoder().raw_decode(part)[0]
        if not isinstance(frame, dict) or not isinstance(frame.get('kind'), str):
            raise ValueError('Invalid frame object or kind')
        group = grouped.setdefault(frame['kind'], [])
        if (type(frame['index']) is not int or frame['index'] != len(group) or
                type(frame['total']) is not int or frame['total'] <= 0 or
                not isinstance(frame['data'], str)):
            raise ValueError('Invalid frame index, total or data')
        group.append(frame)
    result = {}
    for kind, group in grouped.items():
        if not all(f['total'] == len(group) for f in group):
            raise ValueError('Incomplete or inconsistent frame group')
        result[kind] = json.loads(''.join(f['data'] for f in group))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scenario', choices=['epoch', 'public'], default='epoch')
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--load-run', type=pathlib.Path)
    parser.add_argument('--checkpoint', type=int, choices=[120000, 480000, 700000], default=480000)
    parser.add_argument('--timeout', type=int, default=150)
    args = parser.parse_args()
    if subprocess.run(['pgrep', '-x', 'pyrogenesis'], capture_output=True).returncode != 1:
        parser.error('Close existing game instances first')
    app = (ROOT / '../runtime/0 A.D..app').resolve()
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    mode = 'load' if args.load_run else 'save'
    out = ROOT / 'work/t13-save' / (stamp + '-' + mode + '-' + str(args.seed))
    out.mkdir(parents=True)
    prefix = 't13-' + stamp
    paths = [p for folder in [ROOT / 'binaries/data/mods/epoch_rts', ROOT / 'tools/epoch-rts/t13-harness']
             for p in folder.rglob('*') if p.is_file()]
    paths += [ROOT / 'tools/epoch-rts' / name for name in ['t13-macos.py', 't13-network.py',
              't12-macos.py', 'test-t13-tools.py', 'test-t13-payment.cjs']]
    manifest = {str(p.relative_to(ROOT)): digest(p) for p in sorted(paths)}
    (out / 'source-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    command = [str(app / 'Contents/MacOS/pyrogenesis'), '-mod=mod', '-mod=public',
               '-mod=epoch_rts', '-mod=epoch_t13_harness', '-conf=windowed:true', '-xres=1280', '-yres=800',
               '-unique-logs', '-conf=pauseonfocusloss:false', '-conf=locale:zh_TW', '-conf=t13.mode:' + mode,
               '-conf=t13.prefix:' + prefix, '-nosound']
    runtime = {str(p.relative_to(app)): digest(p) for p in [app / 'Contents/MacOS/pyrogenesis',
               app / 'Contents/Resources/data/mods/public/public.zip']}
    baseline = None
    if args.load_run:
        baseline = json.loads((args.load_run / 'result.json').read_text())
        if (baseline['seed'] != args.seed or baseline['scenario'] != args.scenario or
                baseline['mode'] != 'save' or not baseline['passed']):
            parser.error('Baseline must be a successful save run with matching seed and scenario')
        prefix = baseline['save_prefix']
        command.append('-conf=t13.load:' + prefix + '-' + str(args.checkpoint))
    else:
        command += ['-autostart=random/' + ('epoch_t12_validation' if args.scenario == 'epoch' else 'epoch_t12_public_probe'), '-autostart-players=2', '-autostart-size=192',
                    '-autostart-seed=' + str(args.seed), '-autostart-aiseed=' + str(args.seed),
                    '-autostart-civ=1:' + ('epoch' if args.scenario == 'epoch' else 'athen'),
                    '-autostart-civ=2:' + ('epoch' if args.scenario == 'epoch' else 'athen'),
                    '-autostart-ai=2:' + ('epoch_petra' if args.scenario == 'epoch' else 'petra'),
                    '-autostart-aidiff=2:3', '-autostart-player=-1', '-autostart-speed=20']
    with (out / 'engine.log').open('x') as log:
        process = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT, cwd=out)
        timed_out = False
        try:
            process.wait(timeout=args.timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
    text = (out / 'engine.log').read_text(errors='replace')
    errors = [line for line in text.splitlines() if re.search(r'ERROR|WARNING|uncaught exception', line)]
    parse_error = None
    try:
        snapshots = frames(text)
    except (ValueError, AssertionError, KeyError, TypeError) as error:
        snapshots = {}
        parse_error = repr(error)
    spec = importlib.util.spec_from_file_location('t12', ROOT / 'tools/epoch-rts/t12-macos.py')
    t12 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(t12)
    suite = t12.parse_result(text)
    checks = {'exit': process.returncode == 0, 'no_errors': not errors, 'not_timeout': not timed_out,
              'framing': not parse_error, 'suite': bool(suite and suite['passed']) if args.scenario == 'epoch' else 'final' in snapshots,
              'sources_unchanged': all((ROOT / n).exists() and digest(ROOT / n) == h for n, h in manifest.items()),
              'final_snapshot': 'final' in snapshots}
    observations = {}
    if baseline:
        saved = baseline['snapshots'].get('saved-' + str(args.checkpoint))
        checks['restored_snapshot'] = bool(saved) and snapshots.get('loaded') == saved
        checks['baseline_sources'] = manifest == json.loads((args.load_run / 'source-manifest.json').read_text())
        checks['baseline_runtime'] = runtime == baseline.get('runtime')
        observations['identical_continued_suite'] = suite == baseline['suite']
        observations['identical_continued_final_state'] = snapshots.get('final') == baseline['snapshots'].get('final')
    else:
        checks['three_checkpoints'] = all('saved-' + str(t) in snapshots for t in [120000,480000,700000])
    saves = pathlib.Path.home() / 'Library/Application Support/0ad/saves'
    artifacts = {p.name: digest(p) for p in saves.glob(prefix + '*.0adsave')}
    expected_saves = {prefix + '-' + str(t) + '.0adsave' for t in [120000, 480000, 700000]}
    checks['native_save_files'] = set(artifacts) == expected_saves
    if baseline:
        checks['save_hashes_unchanged'] = artifacts == baseline['save_hashes']
    checks['winner'] = [p['state'] for p in snapshots.get('final', {}).get('players', [])] == ['defeated', 'won']
    if not baseline and args.scenario == 'epoch':
        middle = snapshots.get('saved-480000', {}).get('players', [])
        checks['research_in_progress'] = len(middle) == 2 and any(q.get('technologyTemplate') == 'phase_epoch_iron' and 0 < q.get('progress', 0) < 1
            for e in middle[1]['entities'] for q in e.get('queue', []))
        checks['post_research_checkpoint'] = 'phase_epoch_iron' in snapshots.get('saved-700000', {}).get('players', [{}, {}])[1].get('researched', [])
    report = {'runtime': runtime, 'observations': observations, 'scenario': args.scenario, 'mode': mode, 'seed': args.seed, 'checkpoint': args.checkpoint if baseline else None,
              'save_prefix': prefix, 'command': command, 'exit_code': process.returncode, 'errors': errors,
              'parse_error': parse_error, 'checks': checks, 'passed': all(checks.values()),
              'snapshots': snapshots, 'suite': suite, 'save_hashes': artifacts}
    (out / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'run': str(out), 'checks': checks, 'errors': errors, 'parse_error': parse_error}, indent=2))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
