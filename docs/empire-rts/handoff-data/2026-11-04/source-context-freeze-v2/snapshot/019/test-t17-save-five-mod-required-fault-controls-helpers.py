# Purpose: preregistered memory-only helper observations for the new controller.
# Date: 2026-10-29. SPDX-License-Identifier: GPL-2.0-or-later
"""Inert import/default CLI. No producer, syscall observer, fixture or unit files."""
import importlib.util
import importlib.machinery
import hashlib
from pathlib import Path
import sys
import time

CONTROLLER = Path('/Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/0ad/tools/epoch-rts/test-t17-save-five-mod-required-fault-controls.py')


class CheckedControllerLoader(importlib.machinery.SourceFileLoader):
    """Normal import execution with code generated solely from checked bytes.

    No source reread, alternate origin or bytecode-cache read/write is available.
    This class is inert until root admits run_admitted's exact reviewed source.
    """
    def __init__(self, raw, expected_sha):
        if type(raw) is not bytes or len(raw) > 131072:
            raise ImportError('CHECKED_SOURCE_BOUND')
        if hashlib.sha256(raw).hexdigest() != expected_sha:
            raise ImportError('CHECKED_SOURCE_SHA')
        super().__init__('_required_fault_inert_helpers', str(CONTROLLER))
        self.checked_bytes = raw
        self.checked_sha = expected_sha
        self.used = False

    def get_code(self, fullname):
        if fullname != '_required_fault_inert_helpers' or self.path != str(CONTROLLER) or self.used:
            raise ImportError('CHECKED_SOURCE_ORIGIN_OR_REUSE')
        if hashlib.sha256(self.checked_bytes).hexdigest() != self.checked_sha:
            raise ImportError('CHECKED_SOURCE_CHANGED')
        self.used = True
        # Inherited source_to_code compiles this exact immutable byte object;
        # inherited exec_module consumes this get_code, not filesystem/cache.
        return self.source_to_code(self.checked_bytes, str(CONTROLLER), _optimize=0)

    def get_data(self, path):
        raise ImportError('SOURCE_AND_BYTECODE_REREAD_FORBIDDEN')

    def set_data(self, path, data, **kwargs):
        raise ImportError('BYTECODE_WRITE_FORBIDDEN')


def rejected(function):
    try:
        function()
    except Exception:
        return True
    return False


def observations(module):
    flags = module.os.O_WRONLY | module.os.O_CREAT | module.os.O_EXCL | module.os.O_NOFOLLOW
    return (
        ('H01_compact_json_literal', lambda: module.canonical({'v': 1, 'kind': 'ABORT'}) == b'{"v":1,"kind":"ABORT"}'),
        ('H02_empty_sha', lambda: module.digest(b'') == 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'),
        ('H03_strict_literal', lambda: module.strict(b'{"v":1}') == {'v': 1}),
        ('H04_duplicate_rejected', lambda: rejected(lambda: module.strict(b'{"v":1,"v":2}'))),
        ('H05_nan_rejected', lambda: rejected(lambda: module.strict(b'{"v":NaN}'))),
        ('H06_base64_literal', lambda: module.decode('YWJj') == b'abc'),
        ('H07_base64_malformed', lambda: rejected(lambda: module.decode('!!!!'))),
        ('H08_relative_parts', lambda: module.relative_parts('a/b.json') == ['a', 'b.json']),
        ('H09_parent_path_rejected', lambda: rejected(lambda: module.relative_parts('a/../b'))),
        ('H10_absolute_parent_rejected', lambda: rejected(lambda: module.absolute('/a/../b'))),
        ('H11_deadline_edge', lambda: module.future_deadline(1, 21, 20) == 21),
        ('H12_deadline_over', lambda: rejected(lambda: module.future_deadline(1, 21.001, 20))),
        ('H13_primary_retained', lambda: module.first_error('primary', 'secondary') == 'primary'),
        ('H14_first_error_selected', lambda: module.first_error(None, 'secondary') == 'secondary'),
        ('H15_fault_predicate', lambda: module.fault_match(module.IDS[0], 'capture-inputs.json', '/fixed', '/fixed', 7, 7, flags) is True),
        ('H16_generation_mismatch', lambda: module.fault_match(module.IDS[0], 'capture-inputs.json', '/fixed', '/fixed', 7, 8, flags) is False),
        ('H17_filename_mismatch', lambda: module.fault_match(module.IDS[0], 'other.json', '/fixed', '/fixed', 7, 7, flags) is False),
        ('H18_once_close_record', lambda: module.generation_closed({'closeAttempts': 1, 'closeStatus': 'OK'}) is True),
        ('H19_unknown_close_record', lambda: module.generation_closed({'closeAttempts': 1, 'closeStatus': 'UNKNOWN'}) is False),
        ('H20_binding_order', lambda: module.canonical_rows([{'path': '/z', 'bytes': 0, 'sha256': '0' * 64}, {'path': '/a', 'bytes': 1, 'sha256': '1' * 64}]) == [{'path': '/a', 'bytes': 1, 'sha256': '1' * 64}, {'path': '/z', 'bytes': 0, 'sha256': '0' * 64}]),
    )


def run_admitted(expected_sha):
    # Root must statically admit this exact source before calling this function.
    # Read-only bound source identity is outside individual memory-only test bodies.
    if not sys.dont_write_bytecode:
        raise RuntimeError('BYTECODE_WRITES_FORBIDDEN')
    started = time.monotonic()
    with CONTROLLER.open('rb') as source:
        raw = source.read(131073)
    if len(raw) > 131072:
        raise RuntimeError('CONTROLLER_SOURCE_BOUND')
    if hashlib.sha256(raw).hexdigest() != expected_sha:
        raise RuntimeError('CONTROLLER_SOURCE_CHANGED')
    loader = CheckedControllerLoader(raw, expected_sha)
    spec = importlib.util.spec_from_file_location('_required_fault_inert_helpers', str(CONTROLLER), loader=loader)
    if spec is None or spec.loader is not loader:
        raise ImportError('CHECKED_LOADER_SPEC')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # NEW inert controller only, never the producer.
    checks = observations(module)
    if len(checks) != 20:
        raise RuntimeError('HELPER_PLAN_COUNT')
    for name, check in checks:
        if not 0 <= time.monotonic() - started <= 20:
            raise RuntimeError('HELPER_DEADLINE')
        if check() is not True:
            print(name + ' FAIL', flush=True)
            return 1
        print(name + ' PASS_MEMORY_HELPER_ONLY', flush=True)
    if time.monotonic() - started > 20:
        raise RuntimeError('HELPER_DEADLINE')
    print('20 MEMORY_HELPERS_ONLY; F01/F02 NOT_RUN; producer NOT_IMPORTED', flush=True)
    return 0


def main(argv):
    if len(argv) != 3 or argv[1] != '--run-memory-only-after-root-admission':
        return 0
    return run_admitted(argv[2])


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
