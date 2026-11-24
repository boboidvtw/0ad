#!/usr/bin/env python3
"""Purpose: M7.2 AI-vs-AI Frontier Duel batch for game-length balance. Created: 2026-11-24.

SPDX-License-Identifier: GPL-2.0-or-later
Runs whole headless games (epoch_petra vs epoch_petra) and reads each outcome from the
replay metadata. Measures duration only; it says nothing about how a human experiences a game.
"""
import argparse
import json
import pathlib
import plistlib
import re
import statistics
import subprocess
import time

REPLAYS = pathlib.Path.home() / "Library/Application Support/0ad/replays/0.28.0"


def run_game(binary, seed, diff1, diff2, wall_limit, log_path):
    before = set(REPLAYS.glob("*/metadata.json"))
    command = [str(binary), "-mod=mod", "-mod=public", "-mod=epoch_rts",
               "-autostart=random/epoch_frontier_duel", "-autostart-players=2", "-autostart-size=192",
               f"-autostart-seed={seed}", f"-autostart-aiseed={seed}",
               "-autostart-civ=1:epoch", "-autostart-civ=2:epoch",
               "-autostart-ai=1:epoch_petra", f"-autostart-aidiff=1:{diff1}",
               "-autostart-ai=2:epoch_petra", f"-autostart-aidiff=2:{diff2}",
               "-autostart-nonvisual"]
    with log_path.open("x") as handle:
        process = subprocess.Popen(command, stdout=handle, stderr=subprocess.STDOUT)
        try:
            process.wait(timeout=wall_limit)
        except subprocess.TimeoutExpired:
            process.terminate()
            process.wait(timeout=10)
    text = log_path.read_text(errors="replace")
    errors = [line for line in text.splitlines() if re.search(r"ERROR|WARNING|uncaught exception", line)]
    new = sorted(set(REPLAYS.glob("*/metadata.json")) - before)
    seconds, states = None, None
    if len(new) == 1:
        meta = json.loads(new[0].read_text())
        seconds = meta["timeElapsed"] / 1000
        states = [player.get("state") for player in meta["playerStates"][1:]]
    finished = process.returncode == 0 and states is not None and "won" in states
    return {"seed": seed, "diff": [diff1, diff2], "seconds": seconds, "states": states,
            "finished": finished, "errors": errors[:5], "exit_code": process.returncode}


def summarize(games, low, high):
    done = [game["seconds"] for game in games if game["finished"] and not game["errors"]]
    return {"games": len(games), "finished_clean": len(done),
            "median_min": round(statistics.median(done) / 60, 1) if done else None,
            "min_min": round(min(done) / 60, 1) if done else None,
            "max_min": round(max(done) / 60, 1) if done else None,
            "in_range": sum(low * 60 <= s <= high * 60 for s in done)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app", required=True, type=pathlib.Path)
    parser.add_argument("--seeds", default="1-10", help="range like 1-10 or list like 7,42")
    parser.add_argument("--diffs", default="2:3,3:3", help="player1:player2 AI difficulty pairs")
    parser.add_argument("--wall-limit", type=int, default=180, help="real seconds per game")
    parser.add_argument("--output", type=pathlib.Path, default=pathlib.Path("work/duel-batch"))
    args = parser.parse_args()
    repo = pathlib.Path(__file__).resolve().parents[2]
    info = plistlib.loads((args.app / "Contents/Info.plist").read_bytes())
    if info.get("CFBundleShortVersionString") != "0.28.0":
        parser.error("Expected the official 0.28.0 runtime")
    link = pathlib.Path.home() / "Library/Application Support/0ad/mods/epoch_rts"
    if not link.is_symlink() or link.resolve() != repo / "binaries/data/mods/epoch_rts":
        parser.error("Run launch-macos.sh once to register this checkout's Mod")
    if subprocess.run(["pgrep", "-x", "pyrogenesis"], capture_output=True).returncode != 1:
        parser.error("Close running 0 A.D. instances first")
    if "-" in args.seeds:
        first, last = map(int, args.seeds.split("-"))
        seeds = list(range(first, last + 1))
    else:
        seeds = [int(seed) for seed in args.seeds.split(",")]
    pairs = [tuple(int(part) for part in pair.split(":")) for pair in args.diffs.split(",")]
    binary = args.app.resolve() / "Contents/MacOS" / info["CFBundleExecutable"]
    out = args.output / time.strftime("%Y%m%dT%H%M%S")
    out.mkdir(parents=True, exist_ok=False)
    games = []
    for diff1, diff2 in pairs:
        for seed in seeds:
            game = run_game(binary, seed, diff1, diff2, args.wall_limit, out / f"d{diff1}v{diff2}-s{seed}.log")
            games.append(game)
            print(json.dumps(game), flush=True)
    summary = {f"{d1}v{d2}": summarize([g for g in games if g["diff"] == [d1, d2]], 10, 20) for d1, d2 in pairs}
    (out / "result.json").write_text(json.dumps({"games": games, "summary": summary}, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    print(f"Local evidence: {out}")
    return 0 if all(g["finished"] and not g["errors"] for g in games) else 1


if __name__ == "__main__":
    raise SystemExit(main())
