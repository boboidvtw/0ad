#!/usr/bin/env python3
"""Purpose: isolated R28 T07 real-engine runs and replay checks. Created: 2026-09-13.
SPDX-License-Identifier: GPL-2.0-or-later
Raw logs/replays remain local; result.json contains no private paths.
"""
import argparse
import datetime
import hashlib
import importlib.util
import json
import pathlib
import plistlib
import re
import subprocess
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--app', required=True, type=pathlib.Path)
    parser.add_argument('--mode', choices=['probe','validation','demo'], required=True)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--replay', type=pathlib.Path)
    parser.add_argument('--visual', action='store_true')
    parser.add_argument('--baseline', type=pathlib.Path, help='Original result.json required for replay comparison')
    parser.add_argument('--timeout', type=int, default=120)
    args = parser.parse_args()
    repo = pathlib.Path(__file__).resolve().parents[2]
    spec = importlib.util.spec_from_file_location('smoke', pathlib.Path(__file__).with_name('smoke-macos.py'))
    smoke = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(smoke)
    info = plistlib.loads((args.app/'Contents/Info.plist').read_bytes())
    if info.get('CFBundleShortVersionString') != '0.28.0':
        parser.error('Expected official R28 0.28.0')
    if subprocess.run(['pgrep','-x','pyrogenesis'],capture_output=True).returncode != 1:
        parser.error('Close the existing game before starting; shared logs must not race')
    mod_link = pathlib.Path.home()/'Library/Application Support/0ad/mods/epoch_rts'
    if not mod_link.is_symlink() or mod_link.resolve() != repo/'binaries/data/mods/epoch_rts':
        parser.error('Mod symlink does not target this checkout')
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    out = repo/'work/epoch-rts-t07'/f'{stamp}-{args.mode}-seed-{args.seed}'
    out.mkdir(parents=True)
    command = [str(args.app.resolve()/'Contents/MacOS'/info['CFBundleExecutable']),'-mod=mod','-mod=public','-mod=epoch_rts']
    if args.replay:
        if not args.baseline:
            parser.error('--replay requires --baseline')
        metadata=json.loads(args.replay.read_text().splitlines()[0].removeprefix('start '))
        if metadata['settings']['Seed'] != args.seed or metadata['map'] != 'maps/random/epoch_t07_'+args.mode:
            parser.error('Replay map/seed do not match the requested case')
        command += [f'-{"replay-visual" if args.visual else "replay"}={args.replay.resolve()}', '-hashtest-quick=true']
    else:
        command += [f'-autostart=random/epoch_t07_{args.mode}','-autostart-players=2','-autostart-size=192',f'-autostart-seed={args.seed}','-autostart-civ=1:epoch','-autostart-civ=2:epoch','-autostart-player=1','-autostart-playername=EpochTester']
    if args.visual:
        command += ['-conf=windowed:true','-xres=1280','-yres=800','-conf=locale:zh_TW','-conf=pauseonfocusloss:false']
    elif not args.replay:
        command += ['-autostart-nonvisual']
    replay_root=pathlib.Path.home()/'Library/Application Support/0ad/replays/0.28.0'
    before=set(replay_root.glob('*/commands.txt'))
    source_root=repo/'binaries/data/mods/epoch_rts'
    def source_manifest():
        return {str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(source_root.rglob('*')) if p.is_file()}
    sources=source_manifest()
    log=out/'engine.log'
    suite=None
    with log.open('w') as handle:
        proc=subprocess.Popen(command,stdout=handle,stderr=subprocess.STDOUT)
        try:
            deadline=time.monotonic()+args.timeout
            while proc.poll() is None and time.monotonic()<deadline:
                suite=smoke.read_suite(log.read_text(errors='replace'))
                if suite and not args.visual and not args.replay:
                    break
                time.sleep(0.2)
        finally:
            if proc.poll() is None:
                proc.terminate()
                try: proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    proc.kill();proc.wait()
    text=log.read_text(errors='replace')
    suite=smoke.read_suite(text)
    source_changed=sources!=source_manifest()
    errors=[line for line in text.splitlines() if re.search(r'ERROR|WARNING|uncaught exception|Assertion failed|MISMATCH',line)]
    if source_changed:
        errors.append('Source changed during run; repeat validation against a fixed revision')
    interesting=pathlib.Path.home()/'Library/Application Support/0ad/logs/interestinglog.html'
    html_error=bool(re.search(r'<p[^>]+class=[\"\'](?:error|warning)',interesting.read_text(errors='replace'))) if interesting.exists() else None
    replays=sorted(set(replay_root.glob('*/commands.txt'))-before)
    (out/'local-replays.json').write_text(json.dumps([str(p) for p in replays],indent=2)+'\n')
    baseline=json.loads(args.baseline.read_text()) if args.baseline else None
    replay_match=bool(suite and baseline and baseline.get('passed') and sources==baseline.get('source_manifest') and suite==baseline.get('suite')) if args.replay else None
    replay_complete=bool(proc.returncode==0 and '# Final state:' in text) if args.replay and not args.visual else None
    report={'replay_matches_baseline':replay_match,'replay_completed':replay_complete,'hash_checks_ok':len(re.findall(r'hash(?:-quick)? ok',text)),'runtime':'0.28.0','mode':args.mode,'seed':args.seed,'size':192,'replay':bool(args.replay),'visual_requested':args.visual,'visual_verified':False,'exit_code':proc.returncode,'suite':suite,'errors_or_warnings':errors,'engine_html_error_or_warning':html_error,'passed':bool(suite and suite['passed'] and suite['checks'] and all(c['passed'] for c in suite['checks']) and suite.get('mode')==args.mode and not errors and not html_error and proc.returncode in (0,-15) and (not args.replay or (replay_match and (args.visual or replay_complete)))),'source_sha256':sources['binaries/data/mods/epoch_rts/maps/scripts/epoch_rts/T07Validation.js'],'source_manifest':sources,'source_changed_during_run':source_changed}
    (out/'result.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({**{k:v for k,v in report.items() if k!='source_manifest'},'suite':{k:v for k,v in suite.items() if k!='checks'} if suite else None},indent=2))
    print('Local evidence:',out)
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
