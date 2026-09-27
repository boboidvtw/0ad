#!/usr/bin/env python3
"""Purpose: Fail-closed T12 framing and historical-log regression. Created: 2026-09-26."""
import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location('t12_runner', pathlib.Path(__file__).with_name('t12-macos.py'))
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


def frame(value):
    data = json.dumps(value, ensure_ascii=False)
    chunks = [data[i:i + 30] for i in range(0, len(data), 30)]
    return ['EPOCH_T12_RESULT_CHUNK ' + json.dumps({'index': i, 'total': len(chunks), 'data': chunk})
            for i, chunk in enumerate(chunks)]


class FramingTests(unittest.TestCase):
    def setUp(self):
        self.suite = {'passed': True, 'checks': [{'id': '繁中', 'passed': True}]}
        self.frames = frame(self.suite)

    def test_roundtrip_with_log_noise(self):
        self.assertEqual(RUNNER.parse_result('start\n' + '\nINFO\n'.join(self.frames) + '\nend'), self.suite)

    def test_missing_duplicate_and_reordered(self):
        for frames in [self.frames[:-1], self.frames + self.frames[:1], self.frames[::-1]]:
            with self.subTest(frames=frames):
                self.assertIsNone(RUNNER.parse_result('\n'.join(frames)))

    def test_malformed_extra_frame_cannot_be_ignored(self):
        self.assertIsNone(RUNNER.parse_result('\n'.join(self.frames) + '\nEPOCH_T12_RESULT_CHUNK {'))

    def test_invalid_frame_types(self):
        for chunk in [None, [], {}, {'index': False, 'total': 1, 'data': '{}'},
                      {'index': 0, 'total': 1, 'data': 123}]:
            with self.subTest(chunk=chunk):
                self.assertIsNone(RUNNER.parse_result('EPOCH_T12_RESULT_CHUNK ' + json.dumps(chunk)))

    def test_truncated_payload_and_no_result(self):
        self.assertIsNone(RUNNER.parse_result('EPOCH_T12_RESULT_CHUNK {"index":0,"total":1,"data":"{"}'))
        self.assertIsNone(RUNNER.parse_result('normal engine log'))

    def test_inconsistent_pass_and_empty_checks(self):
        for suite in [[], {'passed': True, 'checks': []}, {'passed': True, 'checks': [{'passed': False}]},
                      {'passed': 'true', 'checks': [{'passed': True}]}, {'passed': True, 'checks': [None]}]:
            with self.subTest(suite=suite):
                self.assertIsNone(RUNNER.parse_result('\n'.join(frame(suite))))

    def test_failed_suite_is_retained(self):
        suite = {'passed': False, 'checks': [{'passed': False}]}
        self.assertEqual(RUNNER.parse_result('\n'.join(frame(suite))), suite)

    def test_archived_successful_logs(self):
        ids = ['20260922T093246827695Z-validation-42', '20260922T093300612186Z-validation-7',
               '20260922T093319002362Z-validation-42', '20260922T093340440180Z-validation-7',
               '20260922T093404473733Z-validation-42']
        paths = [ROOT / 'work/t12-validation' / name for name in ids]
        if not all((p / 'result.json').exists() for p in paths):
            self.skipTest('Local historical artifacts unavailable')
        for path in paths:
            with self.subTest(run=path.name):
                self.assertEqual(RUNNER.parse_result((path / 'engine.log').read_text()),
                                 json.loads((path / 'result.json').read_text())['suite'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
