#!/usr/bin/env python3
"""Run a bounded real-engine prototype smoke test. Created: 2026-09-07.

SPDX-License-Identifier: GPL-2.0-or-later
This validates generation/simulation, not rendering or mouse interaction.
"""
import argparse
import datetime
import json
import pathlib
import plistlib
import re
import signal
import subprocess
import time


def read_suite(text):
    """Ignore a partially written result until the next poll; logs may append Turn text."""
    marker = "EPOCH_TEST_RESULT "
    if marker not in text:
        return None
    try:
        result, _ = json.JSONDecoder().raw_decode(text.rsplit(marker, 1)[1])
    except json.JSONDecodeError:
        return None
    if not isinstance(result, dict) or not isinstance(result.get("checks"), list):
        return None
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app", required=True, type=pathlib.Path)
    parser.add_argument("--scenario", choices=["m1", "duel", "t04", "t05"], default="m1")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=pathlib.Path, default=pathlib.Path("work/epoch-rts-smoke"))
    args = parser.parse_args()
    repo = pathlib.Path(__file__).resolve().parents[2]
    with (args.app / "Contents/Info.plist").open("rb") as handle:
        info = plistlib.load(handle)
    if info.get("CFBundleShortVersionString") != "0.28.0":
        parser.error("Expected the official 0.28.0 runtime")
    binary = args.app.resolve() / "Contents/MacOS" / info["CFBundleExecutable"]
    link = pathlib.Path.home() / "Library/Application Support/0ad/mods/epoch_rts"
    if not link.is_symlink() or link.resolve() != repo / "binaries/data/mods/epoch_rts":
        parser.error("Run launch-macos.sh once to register this checkout's Mod, then close the game")
    # All 0 A.D. instances share the normal log directory; do not race another game.
    running = subprocess.run(["pgrep", "-x", "pyrogenesis"], capture_output=True, check=False)
    if running.returncode != 1:
        parser.error("Close running 0 A.D. instances before this test (or check pgrep availability)")
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    output = args.output / f"{stamp}-seed-{args.seed}"
    output.mkdir(parents=True, exist_ok=False)
    log_path = output / "engine.log"
    scenario = {"m1": "epoch_frontier", "duel": "epoch_frontier_duel", "t04": "epoch_frontier_validation", "t05": "epoch_frontier_research_validation"}[args.scenario]
    civ = "athen" if args.scenario == "m1" else "epoch"
    command = [str(binary), "-mod=mod", "-mod=public", "-mod=epoch_rts",
               f"-autostart=random/{scenario}", "-autostart-players=2", "-autostart-size=192",
               f"-autostart-seed={args.seed}", f"-autostart-civ=1:{civ}", f"-autostart-civ=2:{civ}",
               "-autostart-nonvisual", "-autostart-disable-replay"]
    reached_limit = False
    with log_path.open("x") as handle:
        process = subprocess.Popen(command, stdout=handle, stderr=subprocess.STDOUT)
        try:
            deadline = time.monotonic() + 60
            while process.poll() is None and time.monotonic() < deadline:
                text = log_path.read_text(errors="replace")
                turns = re.findall(r"Turn (\d+) \(", text)
                if (read_suite(text) is not None if args.scenario in ("t04", "t05") else turns and int(turns[-1]) >= 100):
                    reached_limit = True
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
    text = log_path.read_text(errors="replace")
    turns = re.findall(r"Turn (\d+) \(", text)
    interesting_path = pathlib.Path.home() / "Library/Application Support/0ad/logs/interestinglog.html"
    interesting = interesting_path.read_text(errors="replace") if interesting_path.exists() else ""
    errors = [line for line in text.splitlines()
              if re.search(r"ERROR|WARNING|uncaught exception|Assertion failed", line)]
    html_errors = bool(re.search(r'<p[^>]+class=[\"\'](?:error|warning)', interesting))
    marker = ("Epoch RTS M1: Frontier ready;" if args.scenario == "m1" else "Epoch RTS T04: Duel ready;") in text
    suite = read_suite(text)
    suite_passed = args.scenario not in ("t04", "t05") or bool(suite and suite.get("passed") is True and suite["checks"] and all(check.get("passed") is True for check in suite["checks"]))
    mod_version = json.loads((repo / "binaries/data/mods/epoch_rts/mod.json").read_text())["version"]
    report = {
        "runtime": "0.28.0", "mod": f"epoch_rts {mod_version}", "seed": args.seed,
        "map": f"random/{scenario}", "suite": suite, "size": 192, "players": 2,
        "map_ready_marker": marker, "last_turn": int(turns[-1]) if turns else None,
        "stopped_after_turn_limit": reached_limit and args.scenario not in ("t04", "t05"),
        "stop_condition": "suite result" if args.scenario in ("t04", "t05") else "at least 100 turns", "exit_code": process.returncode,
        "errors_or_warnings": errors, "engine_html_error_or_warning": html_errors,
        "visual_verified": False,
        "passed": (reached_limit and marker and suite_passed and not errors and not html_errors
                   and process.returncode in (0, -signal.SIGTERM)),
    }
    (output / "result.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({**report, "suite": {"passed": suite["passed"], "checks": len(suite["checks"]), "failure": suite["failure"]} if suite else None}, indent=2))
    print(f"Local evidence: {output}")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
