#!/usr/bin/env python3
"""Purpose: M7.4 build a reproducible player .pyromod of epoch_rts for official 0 A.D. R28. Created: 2026-11-24.
SPDX-License-Identifier: GPL-2.0-or-later

Only player-facing maps are packaged; T04-T12 validation and probe maps stay in the repo.
Files come from `git ls-files`, so untracked local experiments never ship.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

REPO = Path(__file__).resolve().parents[2]
MOD_DIR = "binaries/data/mods/epoch_rts"
PLAYER_MAPS = ("epoch_frontier", "epoch_frontier_duel")
FIXED_TIME = (2026, 1, 1, 0, 0, 0)  # zip entries need a fixed time for identical bytes


def tracked_files(repo):
    out = subprocess.run(["git", "ls-files", "-z", MOD_DIR], cwd=repo, check=True,
                         capture_output=True).stdout.decode()
    return sorted(Path(p).relative_to(MOD_DIR).as_posix() for p in out.split("\0") if p)


def select_files(files, read_json):
    """Return the packaged mod-relative paths: everything except non-player maps."""
    keep_maps = set()
    for name in PLAYER_MAPS:
        settings = read_json(f"maps/random/{name}.json")["settings"]
        keep_maps.update({f"maps/random/{name}.json", f"maps/random/{settings['Script']}"})
        keep_maps.update(f"maps/{script}" for script in settings.get("TriggerScripts", []))
    missing = sorted(p for p in keep_maps if p not in files)
    if missing:
        raise ValueError(f"player maps reference untracked files: {missing}")
    return [p for p in files if not p.startswith("maps/") or p in keep_maps]


def build(repo, output_dir):
    mod_root = repo / MOD_DIR
    files = tracked_files(repo)
    selected = select_files(set(files), lambda p: json.loads((mod_root / p).read_text(encoding="utf-8")))
    version = json.loads((mod_root / "mod.json").read_text(encoding="utf-8"))["version"]
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"epoch_rts-{version}.pyromod"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel in sorted(selected):
            info = zipfile.ZipInfo(rel, FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, (mod_root / rel).read_bytes())
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (output_dir / f"{archive.name}.sha256").write_text(f"{digest}  {archive.name}\n")
    return archive, digest, len(selected)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output", type=Path, default=REPO / "work/dist")
    args = parser.parse_args()
    archive, digest, count = build(REPO, args.output.resolve())
    print(json.dumps({"archive": str(archive), "files": count, "sha256": digest}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
