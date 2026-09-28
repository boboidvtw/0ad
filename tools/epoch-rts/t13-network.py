#!/usr/bin/env python3
"""Purpose: Run two real local R28 clients and compare T13 evidence. Created: 2026-09-28.
SPDX-License-Identifier: GPL-2.0-or-later
"""
import argparse
import datetime
import importlib.util
import json
import pathlib
import re
import subprocess
import time

ROOT = pathlib.Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('t13', ROOT / 'tools/epoch-rts/t13-macos.py')
t13 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t13)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--timeout', type=int, default=480)
    args = parser.parse_args()
    if subprocess.run(['pgrep', '-x', 'pyrogenesis'], capture_output=True).returncode != 1:
        parser.error('Close existing game instances first')
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    out = ROOT / 'work/t13-network' / (stamp + '-' + str(args.seed))
    out.mkdir(parents=True)
    paths = [p for folder in [ROOT / 'binaries/data/mods/epoch_rts', ROOT / 'tools/epoch-rts/t13-harness']
             for p in folder.rglob('*') if p.is_file()]
    paths += [pathlib.Path(__file__).resolve(), ROOT / 'tools/epoch-rts/t13-macos.py']
    manifest = {str(p.relative_to(ROOT)): t13.digest(p) for p in sorted(paths)}
    (out / 'source-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    app = (ROOT / '../runtime/0 A.D..app').resolve()
    common = [str(app / 'Contents/MacOS/pyrogenesis'), '-mod=mod', '-mod=public',
              '-mod=epoch_rts', '-mod=epoch_t13_harness', '-unique-logs', '-nosound',
              '-conf=windowed:true', '-xres=960', '-yres=720', '-conf=pauseonfocusloss:false',
              '-conf=locale:zh_TW', '-conf=t13.mode:network', '-autostart-port=5073']
    commands = {
        'host': common + ['-autostart=random/epoch_t13_network', '-autostart-host',
                         '-autostart-host-players=2', '-autostart-playername=T13Host',
                         '-autostart-size=192', '-autostart-seed=' + str(args.seed),
                         '-autostart-aiseed=' + str(args.seed), '-autostart-civ=1:epoch',
                         '-autostart-civ=2:epoch', '-autostart-speed=2'],
        'client': common + ['-autostart-client=127.0.0.1', '-autostart-playername=T13Client']}
    processes, logs = {}, {}
    timed_out = False
    try:
        for role in ['host', 'client']:
            folder = out / role
            folder.mkdir()
            logs[role] = (folder / 'engine.log').open('x')
            processes[role] = subprocess.Popen(commands[role], cwd=folder, stdout=logs[role], stderr=subprocess.STDOUT)
            if role == 'host':
                time.sleep(3)
        (out / 'processes.json').write_text(json.dumps({r: p.pid for r, p in processes.items()}) + '\n')
        deadline = time.monotonic() + args.timeout
        while any(p.poll() is None for p in processes.values()):
            if time.monotonic() > deadline:
                timed_out = True
                break
            time.sleep(1)
    finally:
        for p in processes.values():
            if p.poll() is None:
                p.terminate()
                try:
                    p.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    p.kill()
                    p.wait()
        for log in logs.values():
            log.close()
    reports = {}
    for role, process in processes.items():
        text = (out / role / 'engine.log').read_text(errors='replace')
        error = None
        try:
            snapshots = t13.frames(text)
        except (ValueError, AssertionError, KeyError, TypeError) as exc:
            snapshots, error = {}, repr(exc)
        reports[role] = {'pid': process.pid, 'exit_code': process.returncode, 'frames': snapshots,
                         'parse_error': error,
                         'errors': [line for line in text.splitlines() if re.search(r'ERROR|WARNING|out.of.sync|OOS', line, re.I)]}
    host, client = (reports[r]['frames'] for r in ['host', 'client'])
    shared = lambda f: {k: v for k, v in f.items() if k != 'sent'}
    final = host.get('network-final', {})
    checks = {'not_timeout': not timed_out,
              'exit': all(r['exit_code'] == 0 for r in reports.values()),
              'no_errors': all(not r['errors'] and not r['parse_error'] for r in reports.values()),
              'sources_unchanged': all(t13.digest(ROOT / n) == h for n, h in manifest.items()),
              'complete': bool(final) and len([k for k in host if k.startswith('network-')]) > 10,
              'synchronized': bool(host) and shared(host) == shared(client),
              'both_senders': {host.get('sent', {}).get('player'), client.get('sent', {}).get('player')} == {1, 2},
              'both_commands_executed': all(host.get('command-' + str(p), {}).get('entities') and
                  all(e['owner'] == p and e['stance'] == 'standground' for e in host['command-' + str(p)]['entities']) for p in [1, 2]),
              'fixture_checks': bool(final.get('checks')) and all(c['passed'] for c in final.get('checks', [])),
              'winner': [p['state'] for p in final.get('snapshot', {}).get('players', [])] == ['won', 'defeated']}
    report = {'seed': args.seed, 'commands': commands, 'checks': checks, 'passed': all(checks.values()), 'reports': reports}
    (out / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'run': str(out), 'checks': checks, 'errors': {r: v['errors'] for r, v in reports.items()}}, indent=2))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
