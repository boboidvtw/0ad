#!/usr/bin/env python3
"""Purpose: Audit native R28 replay hashes through the final T13 turn. Created: 2026-09-28.
SPDX-License-Identifier: GPL-2.0-or-later
"""
import argparse
import hashlib
import json
import pathlib
import re
import shutil


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hashes(text):
    result = {}
    turn = None
    elapsed = 0
    for line in text.splitlines():
        if line.startswith('turn '):
            _, index, length = line.split()
            turn = int(index)
            elapsed += int(length)
        elif line.startswith(('hash ', 'hash-quick ')):
            kind, value = line.split()
            if turn is None or turn in result or not re.fullmatch('[0-9a-f]{32}', value):
                raise ValueError('Invalid or duplicate native hash')
            result[turn] = {'kind': kind, 'value': value, 'elapsed': elapsed}
    return result


def compare(a, b, final_time):
    needed = {turn for turn, row in a.items() if row['elapsed'] <= final_time}
    return bool(needed) and (max(a[t]['elapsed'] for t in needed) == final_time and
        needed == set(range(max(needed) + 1)) and
        all(t in b and a[t] == b[t] for t in needed))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', type=pathlib.Path)
    args = parser.parse_args()
    report = json.loads((args.run / 'result.json').read_text())
    rows, artifacts, errors = {}, {}, {}
    for role in ['host', 'client']:
        run = args.run / role
        log = (run / 'engine.log').read_text()
        match = re.search(r"Replay written to '([^']+)'", log)
        if not match:
            raise ValueError('Missing native replay path')
        replay = pathlib.Path(match[1]) / 'commands.txt'
        target = run / 'native-commands.txt'
        if target.exists() and sha(target) != sha(replay):
            raise ValueError('Refuse to replace different archived replay')
        if not target.exists():
            shutil.copy2(replay, target)
        rows[role] = hashes(target.read_text())
        pid = report['reports'][role]['pid']
        native_logs = list((pathlib.Path.home() / 'Library/Application Support/0ad/logs').glob('*_' + str(pid) + '.html'))
        artifacts[role] = {'replay_sha256': sha(target), 'native_logs': {},
                           'hash_count': len(rows[role]), 'full_hashes': sum(r['kind'] == 'hash' for r in rows[role].values())}
        errors[role] = []
        for path in native_logs:
            dest = run / path.name
            if not dest.exists():
                shutil.copy2(path, dest)
            artifacts[role]['native_logs'][path.name] = sha(dest)
            errors[role] += [line for line in dest.read_text(errors='replace').splitlines()
                             if re.search(r'class=["\'](?:error|warning)|out.of.sync', line, re.I)]
    final = report['reports']['host']['frames']['network-final']['snapshot']['time']
    checks = {'run_passed': report['passed'], 'native_hashes_equal_through_final': compare(rows['host'], rows['client'], final),
              'native_logs_present': all(a['native_logs'] for a in artifacts.values()),
              'native_logs_clean': not any(errors.values())}
    result = {'final_time': final, 'checks': checks, 'passed': all(checks.values()), 'artifacts': artifacts, 'errors': errors}
    (args.run / 'native-audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
