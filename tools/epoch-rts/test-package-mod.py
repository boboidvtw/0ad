#!/usr/bin/env python3
"""Purpose: M7.4 guards against a player package that cannot load or leaks validation maps. Created: 2026-11-24.
SPDX-License-Identifier: GPL-2.0-or-later
"""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

spec = importlib.util.spec_from_file_location("package_mod", Path(__file__).with_name("package-mod.py"))
package = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package)


class SelectFilesTests(unittest.TestCase):
    MAPS = {
        "maps/random/epoch_frontier.json": {"settings": {"Script": "epoch_frontier.js"}},
        "maps/random/epoch_frontier_duel.json": {"settings": {
            "Script": "epoch_frontier_duel.js", "TriggerScripts": ["scripts/epoch_rts/FrontierDuel.js"]}},
    }

    def test_keeps_player_maps_and_drops_validation_maps(self):
        files = set(self.MAPS) | {"mod.json", "maps/random/epoch_frontier.js", "maps/random/epoch_frontier_duel.js",
                                  "maps/scripts/epoch_rts/FrontierDuel.js", "maps/random/epoch_t06_full.json",
                                  "maps/scripts/epoch_rts/T06Validation.js"}
        kept = package.select_files(files, self.MAPS.__getitem__)
        self.assertIn("maps/scripts/epoch_rts/FrontierDuel.js", kept)
        self.assertIn("mod.json", kept)
        self.assertNotIn("maps/random/epoch_t06_full.json", kept)
        self.assertNotIn("maps/scripts/epoch_rts/T06Validation.js", kept)

    def test_missing_trigger_script_fails_the_build(self):
        files = set(self.MAPS) | {"maps/random/epoch_frontier.js", "maps/random/epoch_frontier_duel.js"}
        with self.assertRaisesRegex(ValueError, "FrontierDuel.js"):
            package.select_files(files, self.MAPS.__getitem__)


class BuildTests(unittest.TestCase):
    def test_real_package_is_loadable_and_reproducible(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            first, digest_a, _ = package.build(package.REPO, Path(a))
            _, digest_b, _ = package.build(package.REPO, Path(b))
            self.assertEqual(digest_a, digest_b)
            with zipfile.ZipFile(first) as zf:
                names = zf.namelist()
                manifest = json.loads(zf.read("mod.json"))  # R28 reads mod.json at the archive root
            self.assertEqual(manifest["name"], "epoch_rts")
            self.assertIn("0ad=0.28.0", manifest["dependencies"])
            self.assertIn("maps/random/epoch_frontier_duel.json", names)
            self.assertIn("simulation/ai/epoch_petra/_epochbot.js", names)
            maps = [n for n in names if n.startswith("maps/")]
            self.assertFalse([n for n in maps if "/epoch_t" in n or "validation" in n or "/T" in n], maps)


if __name__ == "__main__":
    unittest.main()
