#!/usr/bin/env python3
"""Purpose: Bounded read-only T12 AI probes against official R28. Created: 2026-09-22.
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--app', required=True, type=pathlib.Path)
    parser.add_argument('--mode', choices=['public', 'epoch'], required=True)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--ai', choices=['petra', 'epoch_petra'], default='petra')
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
    out = repo / 'work/t12-observed-probe' / (stamp + '-' + args.mode + '-' + str(args.seed))
    out.mkdir(parents=True, exist_ok=False)
    source = {str(p.relative_to(repo)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(mod.rglob('*')) if p.is_file()}
    source[str(pathlib.Path(__file__).resolve().relative_to(repo))] = hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
    (out / 'source-manifest.json').write_text(json.dumps(source, indent=2) + '\n')
    civ = 'athen' if args.mode == 'public' else 'epoch'
    command = [str(app / 'Contents/MacOS' / info['CFBundleExecutable']),
               '-mod=mod', '-mod=public', '-mod=epoch_rts',
               '-autostart=random/epoch_t12_' + args.mode + '_probe',
               '-autostart-players=2', '-autostart-size=192',
               '-autostart-seed=' + str(args.seed), '-autostart-aiseed=' + str(args.seed),
               '-autostart-civ=1:' + civ, '-autostart-civ=2:' + civ,
               '-autostart-ai=2:' + args.ai, '-autostart-aidiff=2:3', '-autostart-nonvisual']
    replays = user / 'replays/0.28.0'
    before = set(replays.glob('*/commands.txt'))
    log = out / 'engine.log'
    with log.open('x') as handle:
        process = subprocess.Popen(command, stdout=handle, stderr=subprocess.STDOUT)
        try:
            deadline = time.monotonic() + 120
            while process.poll() is None and time.monotonic() < deadline:
                text = log.read_text(errors='replace')
                if 'EPOCH_T12_PROBE_COMPLETE' in text or 'ERROR' in text:
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
    samples = []
    for part in text.split('EPOCH_T12_SAMPLE ')[1:]:
        try:
            samples.append(json.JSONDecoder().raw_decode(part)[0])
        except json.JSONDecodeError:
            pass
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
    report = {'mode': args.mode, 'seed': args.seed, 'ai': args.ai, 'command': command,
              'complete': 'EPOCH_T12_PROBE_COMPLETE' in text, 'exit_code': process.returncode,
              'errors': errors, 'html_error': html_error, 'source_unchanged': unchanged,
              'samples': samples, 'replay_count': len(new_replays),
              'scope': 'Read-only observation; not behavior acceptance'}
    (out / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ['samples', 'command']}, indent=2))
    for sample in samples[:1] + samples[-1:]:
        print(json.dumps({'time': sample['time'], 'players': [
            {k: v for k, v in p.items() if k != 'statistics'} for p in sample['players']]}, indent=2))
    print('Evidence:', out)
    return 0 if report['complete'] and not errors and not html_error and unchanged and samples and process.returncode in (0, -15) else 1


if __name__ == '__main__':
    raise SystemExit(main())
