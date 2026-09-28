#!/usr/bin/env python3
"""Purpose: Fail-closed evidence parser tests. Created: 2026-09-28.
SPDX-License-Identifier: GPL-2.0-or-later
"""
import importlib.util
import json
import pathlib
import unittest

spec = importlib.util.spec_from_file_location('t13', pathlib.Path(__file__).with_name('t13-macos.py'))
t13 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t13)


def frame(index, total, data, kind='snapshot'):
    return 'noise EPOCH_T13_FRAME ' + json.dumps(dict(kind=kind, index=index, total=total, data=data)) + '\n'


class Frames(unittest.TestCase):
    def reject(self, text):
        with self.assertRaises((ValueError, AssertionError, KeyError, TypeError)):
            t13.frames(text)

    def test_valid_multi_kind(self):
        self.assertEqual(t13.frames(frame(0, 2, '{"x":') + frame(1, 2, '1}') + frame(0, 1, '[]', 'other')),
                         {'snapshot': {'x': 1}, 'other': []})

    def test_missing_reordered_duplicate(self):
        for text in [frame(0, 2, '{}'), frame(1, 2, '{}'), frame(0, 1, '{}') * 2]:
            self.reject(text)

    def test_invalid_types(self):
        for text in [frame(True, 1, '{}'), frame(0, True, '{}'), frame(0, 0, '{}'), frame(0, 1, 5)]:
            self.reject(text)

    def test_truncation_and_extra_malformed(self):
        self.reject(frame(0, 1, '{'))
        self.reject(frame(0, 1, '{}') + 'EPOCH_T13_FRAME {')

    def test_no_frames_remains_empty(self):
        self.assertEqual(t13.frames('normal engine log'), {})


if __name__ == '__main__':
    unittest.main(verbosity=2)
