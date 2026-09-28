#!/usr/bin/env python3
"""Purpose: Reject incomplete or divergent native replay evidence. Created: 2026-09-28.
SPDX-License-Identifier: GPL-2.0-or-later
"""
import importlib.util
import pathlib
import unittest

spec = importlib.util.spec_from_file_location('audit', pathlib.Path(__file__).with_name('t13-audit-network.py'))
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class NativeHashes(unittest.TestCase):
    def test_complete_equal(self):
        text = 'turn 0 200\nhash ' + 'a'*32 + '\nturn 1 200\nhash-quick ' + 'b'*32 + '\n'
        rows = audit.hashes(text)
        self.assertTrue(audit.compare(rows, rows, 400))
        self.assertFalse(audit.compare(rows, rows, 600))

    def test_missing_and_divergent(self):
        a = {0: {'elapsed': 200, 'kind': 'hash', 'value': 'a'*32}}
        self.assertFalse(audit.compare(a, {}, 200))
        self.assertFalse(audit.compare(a, {0: {**a[0], 'value': 'b'*32}}, 200))
        self.assertFalse(audit.compare({}, {}, 200))
        self.assertFalse(audit.compare({1: a[0]}, {1: a[0]}, 200))

    def test_invalid_or_duplicate(self):
        for text in ['hash ' + 'a'*32, 'turn 0 200\nhash bad', 'turn 0 200\nhash ' + 'a'*32 + '\nhash ' + 'b'*32]:
            with self.assertRaises(ValueError):
                audit.hashes(text)


if __name__ == '__main__':
    unittest.main(verbosity=2)
