#!/usr/bin/env python3
"""Purpose: T12 validation, replay and GUI runner against official R28. Created: 2026-09-22.
SPDX-License-Identifier: GPL-2.0-or-later
"""
import argparse
import datetime
import hashlib
import json
import pathlib
import plistlib
import re
import shutil
import subprocess
import time


def parse_result(text):
    """Reject missing, duplicate, malformed or out-of-order result frames."""
    parts = text.split('EPOCH_T12_RESULT_CHUNK ')[1:]
    if not parts:
        return None
    chunks = []
    try:
        for index, part in enumerate(parts):
            chunk = json.JSONDecoder().raw_decode(part)[0]
            if (not isinstance(chunk, dict) or type(chunk.get('index')) is not int
                    or type(chunk.get('total')) is not int
                    or chunk['index'] != index or chunk['total'] != len(parts)
                    or not isinstance(chunk.get('data'), str)):
                return None
            chunks.append(chunk['data'])
        suite = json.loads(''.join(chunks))
        if (not isinstance(suite, dict) or type(suite.get('passed')) is not bool
                or not isinstance(suite.get('checks'), list) or not suite['checks']
                or any(not isinstance(check, dict) or type(check.get('passed')) is not bool
                       for check in suite['checks'])
                or suite['passed'] != all(check['passed'] for check in suite['checks'])):
            return None
        return suite
    except (json.JSONDecodeError, TypeError, ValueError):
        return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--app', required=True, type=pathlib.Path)
    parser.add_argument('--mode', choices=['validation'], default='validation')
    parser.add_argument('--replay', type=pathlib.Path)
    parser.add_argument('--baseline', type=pathlib.Path)
    parser.add_argument('--visual', action='store_true')
    parser.add_argument('--timeout', type=int, default=120)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--ai', choices=['petra', 'epoch_petra'], default='epoch_petra')
    args = parser.parse_args()
    repo = pathlib.Path(__file__).resolve().parents[2]
    app = args.app.resolve()
    info = plistlib.loads((app / 'Contents/Info.plist').read_bytes())
    if info['CFBundleShortVersionString'] != '0.28.0':
        parser.error('Expected official 0.28.0')
    mod = repo / 'binaries/data/mods/epoch_rts'
    user = pathlib.Path.home() / 'Library/Application Support/0ad'
    link = user / 'mods/epoch_rts'
    if not link.is_symlink() or link.resolve() != mod:
        parser.error('Mod link must point to this checkout')
    if subprocess.run(['pgrep', '-x', 'pyrogenesis'], capture_output=True).returncode != 1:
        parser.error('Close other game instances first')
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    out = repo / 'work/t12-validation' / (stamp + '-' + args.mode + '-' + str(args.seed))
    out.mkdir(parents=True, exist_ok=False)
    source = {str(p.relative_to(repo)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(mod.rglob('*')) if p.is_file()}
    source[str(pathlib.Path(__file__).resolve().relative_to(repo))] = hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
    (out / 'source-manifest.json').write_text(json.dumps(source, indent=2) + '\n')
    command = [str(app / 'Contents/MacOS' / info['CFBundleExecutable']),
               '-mod=mod', '-mod=public', '-mod=epoch_rts']
    if args.replay:
        if not args.baseline:
            parser.error('--replay requires --baseline')
        command += ['-replay=' + str(args.replay.resolve()), '-replay-directory=' + str(out)]
    else:
        command += ['-autostart=random/epoch_t12_validation', '-autostart-players=2',
                    '-autostart-size=192', '-autostart-seed=' + str(args.seed),
                    '-autostart-aiseed=' + str(args.seed), '-autostart-civ=1:epoch',
                    '-autostart-civ=2:epoch', '-autostart-ai=2:' + args.ai, '-autostart-aidiff=2:3']
        if not args.visual:
            command += ['-autostart-nonvisual']
    if args.visual:
        command += ['-conf=windowed:true', '-xres=1280', '-yres=800',
                    '-conf=locale:zh_TW', '-conf=pauseonfocusloss:false']
        if not args.replay:
            command += ['-autostart-player=-1', '-autostart-speed=20']
    replays = user / 'replays/0.28.0'
    before = set(replays.glob('*/commands.txt'))
    log = out / 'engine.log'
    with log.open('x') as handle:
        process = subprocess.Popen(command, stdout=handle, stderr=subprocess.STDOUT)
        try:
            deadline = time.monotonic() + args.timeout
            while process.poll() is None and time.monotonic() < deadline:
                text = log.read_text(errors='replace')
                if 'ERROR' in text:
                    break
                time.sleep(0.1)
        finally:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
    text = log.read_text(errors='replace')
    suite = parse_result(text)
    errors = [line for line in text.splitlines() if re.search(r'ERROR|WARNING|uncaught exception', line)]
    html_path = user / 'logs/interestinglog.html'
    html = html_path.read_text(errors='replace') if html_path.exists() else ''
    (out / 'interestinglog.html').write_text(html)
    html_error = bool(re.search(r'class=[\"\'](?:error|warning)', html))
    new_replays = sorted(set(replays.glob('*/commands.txt')) - before)
    for index, replay in enumerate(new_replays):
        shutil.copy2(replay, out / ('commands-' + str(index) + '.txt'))
    unchanged = all(hashlib.sha256((repo / name).read_bytes()).hexdigest() == digest
                    for name, digest in source.items())
    baseline = json.loads(args.baseline.read_text()) if args.baseline else None
    replay_match = bool(baseline and suite == baseline.get('suite')) if args.replay else None
    replay_complete = bool(process.returncode == 0 and '# Final state:' in text) if args.replay else None
    public = app / 'Contents/Resources/data/mods/public/public.zip'
    report = {'mode': args.mode, 'seed': args.seed, 'ai': args.ai, 'command': command,
              'exit_code': process.returncode, 'errors': errors, 'html_error': html_error,
              'source_unchanged': unchanged, 'suite': suite, 'replay_count': len(new_replays),
              'visual_requested': args.visual, 'visual_verified': False,
              'replay_match': replay_match, 'replay_complete': replay_complete,
              'binary_sha256': hashlib.sha256(pathlib.Path(command[0]).read_bytes()).hexdigest(),
              'public_zip_sha256': hashlib.sha256(public.read_bytes()).hexdigest(),
              'passed': bool(suite and suite['passed'] and not errors and not html_error and unchanged
                             and process.returncode == 0 and (not args.replay or (replay_match and replay_complete)))}
    (out / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ['suite', 'command']}, indent=2))
    if suite:
        print(json.dumps({'passed': suite['passed'], 'time': suite['time'], 'checks': len(suite['checks']),
                          'failed': [c for c in suite['checks'] if not c['passed']]}, indent=2))
    print('Evidence:', out)
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
