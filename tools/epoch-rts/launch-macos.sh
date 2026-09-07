#!/bin/bash
# Purpose: Launch the M1 Mod against a pinned official macOS runtime. Created: 2026-09-06.
# SPDX-License-Identifier: GPL-2.0-or-later
set -euo pipefail

mode="${1:-frontier}"
if [[ "$#" -gt 1 || ( "$mode" != "frontier" && "$mode" != "duel" && "$mode" != "--menu" ) ]]; then
    echo "Usage: EPOCH_RTS_0AD_APP='/path/to/0 A.D..app' $0 [frontier|duel|--menu]" >&2
    exit 2
fi
if [[ "$(uname -s)" != "Darwin" ]]; then
    echo "This launcher supports macOS only. See docs/empire-rts/baseline.md." >&2
    exit 2
fi

repo_root="$(cd "$(dirname "$0")/../.." && pwd -P)"
app_path="${EPOCH_RTS_0AD_APP:-/Applications/0 A.D..app}"
plist="$app_path/Contents/Info.plist"
if [[ ! -f "$plist" ]]; then
    echo "Set EPOCH_RTS_0AD_APP to the official Release 28 app path." >&2
    exit 2
fi
version="$(/usr/libexec/PlistBuddy -c 'Print :CFBundleShortVersionString' "$plist")"
if [[ "$version" != "0.28.0" ]]; then
    echo "Expected 0.28.0; found $version. Other versions are not validated." >&2
    exit 2
fi
executable="$(/usr/libexec/PlistBuddy -c 'Print :CFBundleExecutable' "$plist")"
binary="$app_path/Contents/MacOS/$executable"
if [[ ! -x "$binary" ]]; then
    echo "The app executable is missing or not executable: $binary" >&2
    exit 2
fi

mod_source="$repo_root/binaries/data/mods/epoch_rts"
mod_parent="$HOME/Library/Application Support/0ad/mods"
mod_link="$mod_parent/epoch_rts"
if [[ -L "$mod_link" ]]; then
    if [[ "$(readlink "$mod_link")" != "$mod_source" ]]; then
        echo "Existing epoch_rts link points elsewhere; no files changed: $mod_link" >&2
        exit 2
    fi
elif [[ -e "$mod_link" ]]; then
    echo "Existing epoch_rts installation preserved; use it or relocate it explicitly: $mod_link" >&2
    exit 2
else
    mkdir -p "$mod_parent"
    ln -s "$mod_source" "$mod_link"
fi

args=(-mod=mod -mod=public -mod=epoch_rts -conf=windowed:true -xres=1280 -yres=800)
if [[ "$mode" == "frontier" ]]; then
    args+=(-autostart=random/epoch_frontier -autostart-players=2 -autostart-size=192
        -autostart-seed=42 -autostart-civ=1:athen -autostart-civ=2:athen
        -autostart-player=1 -autostart-playername=EpochTester)
fi
if [[ "$mode" == "duel" ]]; then
    args+=(-autostart=random/epoch_frontier_duel -autostart-players=2 -autostart-size=192
        -autostart-seed=42 -autostart-civ=1:epoch -autostart-civ=2:epoch
        -autostart-player=1 -autostart-playername=EpochTester)
fi
exec "$binary" "${args[@]}"
