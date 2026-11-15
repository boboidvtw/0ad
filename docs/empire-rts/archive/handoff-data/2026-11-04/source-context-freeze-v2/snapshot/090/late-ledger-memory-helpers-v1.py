# Purpose: four preregistered affected pure-memory late-ledger controls only.
# Date: 2026-10-29. SPDX-License-Identifier: GPL-2.0-or-later
"""No import/compile/run before fresh root and independent limited admission."""
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
        super().__init__('_required_fault_late_ledger_helpers', str(CONTROLLER))
        self.checked_bytes = raw
        self.checked_sha = expected_sha
        self.used = False

    def get_code(self, fullname):
        if fullname != '_required_fault_late_ledger_helpers' or self.path != str(CONTROLLER) or self.used:
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



def h21(module):
    original = ValueError('body')
    original.cleanupUnknown = ['body-close']
    case = module.FailureLedger()
    case.record('producer body', original)
    case.record('case result evidence', RuntimeError('result'))
    outer = module.FailureLedger()
    outer.merge_case('F01', case)
    snap = outer.snapshot()
    return {'originalPrimaryIdentity': outer.primary_error is original,
            'primaryPhase': snap['primary']['phase'],
            'primaryCleanup': snap['primary']['cleanupUnknown'],
            'secondaryPhases': [row['phase'] for row in snap['secondary']],
            'completeness': snap['ledgerCompleteness']} == {
                'originalPrimaryIdentity': True, 'primaryPhase': 'F01 / producer body',
                'primaryCleanup': ['body-close'],
                'secondaryPhases': ['F01 / case result evidence'],
                'completeness': 'COMPLETE_MEMORY_ONLY'}


def h22(module):
    original = RuntimeError('original')
    ledger = module.FailureLedger()
    ledger.record('case body', original)
    phases = ['post source /bound', 'post runtime readback', 'campaign result evidence',
              'store close', 'cleanup final deadline', 'campaign final deadline',
              'stderr diagnostic channel UNKNOWN']
    close = [{'fd': 7, 'status': 'CLOSE_UNKNOWN', 'error': 'fabricated close'}]
    for phase in phases:
        try:
            module.future_deadline(1, 121.001, 120)
        except module.Rejected as error:
            ledger.record(phase, error, close if phase == 'store close' else None)
    result = {'status': 'SHOULD_BECOME_UNKNOWN'}
    ledger.apply(result)
    return {'originalPrimaryIdentity': ledger.primary_error is original,
            'secondaryPhases': [row['phase'] for row in result['secondary']],
            'closeCleanup': result['secondary'][3]['cleanupUnknown'],
            'status': result['status'], 'durableFinalLedger': result['durableFinalLedger']} == {
                'originalPrimaryIdentity': True, 'secondaryPhases': phases,
                'closeCleanup': close, 'status': 'UNKNOWN_OR_FAIL',
                'durableFinalLedger': 'NOT_ATTESTED'}


def h23(module):
    original = ValueError('x' * 131072)
    ledger = module.FailureLedger()
    for unused in range(9):
        ledger.record('overflow', original)
    result = {'status': 'SHOULD_BECOME_UNKNOWN'}
    ledger.apply(result)
    return {'originalPrimaryIdentity': ledger.primary_error is original,
            'secondaryCount': len(result['secondary']),
            'unretainedEvents': result['unretainedEvents'],
            'ledgerCompleteness': result['ledgerCompleteness'],
            'status': result['status']} == {
                'originalPrimaryIdentity': True, 'secondaryCount': 6,
                'unretainedEvents': 2, 'ledgerCompleteness': 'UNKNOWN',
                'status': 'UNKNOWN_OR_FAIL'}


class Unprintable(Exception):
    def __str__(self):
        raise ValueError('fabricated serialization failure')


def h24(module):
    original = Unprintable()
    ledger = module.FailureLedger()
    ledger.record('case body', original)
    ledger.record('stdout fallback channel UNKNOWN', OSError('fabricated channel failure'))
    result = {'status': 'SHOULD_BECOME_UNKNOWN'}
    ledger.apply(result)
    return {'originalPrimaryIdentity': ledger.primary_error is original,
            'primaryPhase': result['primary']['phase'],
            'primaryMessage': result['primary']['message'],
            'primaryCleanup': result['primary']['cleanupUnknown'],
            'unretainedEvents': result['unretainedEvents'],
            'ledgerCompleteness': result['ledgerCompleteness'],
            'secondaryPhases': [row['phase'] for row in result['secondary']],
            'status': result['status']} == {
                'originalPrimaryIdentity': True, 'primaryPhase': 'case body',
                'primaryMessage': 'UNKNOWN_LEDGER_RECORD_NOT_FULLY_RETAINED',
                'primaryCleanup': 'UNKNOWN_SEE_BOUNDED_MARKERS', 'unretainedEvents': 1,
                'ledgerCompleteness': 'UNKNOWN',
                'secondaryPhases': ['stdout fallback channel UNKNOWN'],
                'status': 'UNKNOWN_OR_FAIL'}


def run_admitted(expected_sha):
    if not sys.dont_write_bytecode:
        raise RuntimeError('BYTECODE_WRITES_FORBIDDEN')
    started = time.monotonic()
    with CONTROLLER.open('rb') as source:
        raw = source.read(131073)
    if len(raw) > 131072 or hashlib.sha256(raw).hexdigest() != expected_sha:
        raise RuntimeError('CONTROLLER_SOURCE_BOUND_OR_CHANGED')
    loader = CheckedControllerLoader(raw, expected_sha)
    spec = importlib.util.spec_from_file_location('_required_fault_late_ledger_helpers', str(CONTROLLER), loader=loader)
    if spec is None or spec.loader is not loader:
        raise ImportError('CHECKED_LOADER_SPEC')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    checks = (('H21_case_merge_first_primary_and_secondary', h21),
              ('H22_all_late_phases_and_fd_unknown', h22),
              ('H23_bound_is_unknown_never_complete', h23),
              ('H24_serialization_failure_and_channel_bookkeeping', h24))
    for name, check in checks:
        if not 0 <= time.monotonic() - started <= 20:
            raise RuntimeError('HELPER_DEADLINE')
        if check(module) is not True:
            print(name + ' FAIL', flush=True)
            return 1
        print(name + ' PASS_MEMORY_HELPER_ONLY', flush=True)
    if time.monotonic() - started > 20:
        raise RuntimeError('HELPER_DEADLINE')
    print('4 NEW MEMORY_HELPERS_ONLY; old20 NOT_RERUN; producer/cases NOT_RUN', flush=True)
    return 0


def main(argv):
    if len(argv) != 3 or argv[1] != '--run-four-new-memory-only-after-root-admission':
        return 0
    return run_admitted(argv[2])


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
