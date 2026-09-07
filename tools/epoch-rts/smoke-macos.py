#!/usr/bin/env python3
"""Run a bounded real-engine M1 smoke test. Created: 2026-09-07.

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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app", required=True, type=pathlib.Path)
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
    command = [str(binary), "-mod=mod", "-mod=public", "-mod=epoch_rts",
               "-autostart=random/epoch_frontier", "-autostart-players=2", "-autostart-size=192",
               f"-autostart-seed={args.seed}", "-autostart-civ=1:athen", "-autostart-civ=2:athen",
               "-autostart-nonvisual", "-autostart-disable-replay"]
    reached_limit = False
    with log_path.open("x") as handle:
        process = subprocess.Popen(command, stdout=handle, stderr=subprocess.STDOUT)
        try:
            deadline = time.monotonic() + 30
            while process.poll() is None and time.monotonic() < deadline:
                text = log_path.read_text(errors="replace")
                turns = re.findall(r"Turn (\d+) \(", text)
                if turns and int(turns[-1]) >= 100:
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
    marker = "Epoch RTS M1: Frontier ready; players=2; pioneers=2;" in text
    report = {
        "runtime": "0.28.0", "mod": "epoch_rts 0.1.0", "seed": args.seed,
        "map": "random/epoch_frontier", "size": 192, "players": 2,
        "map_ready_marker": marker, "last_turn": int(turns[-1]) if turns else None,
        "stopped_after_turn_limit": reached_limit, "exit_code": process.returncode,
        "errors_or_warnings": errors, "engine_html_error_or_warning": html_errors,
        "visual_verified": False,
        "passed": (reached_limit and marker and not errors and not html_errors
                   and process.returncode in (0, -signal.SIGTERM)),
    }
    (output / "result.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    print(f"Local evidence: {output}")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
