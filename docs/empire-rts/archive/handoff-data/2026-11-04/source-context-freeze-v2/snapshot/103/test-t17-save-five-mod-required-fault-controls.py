# Purpose: reviewed three-case injected-errno controller; inert until stage C gates.
# Date: 2026-10-29. SPDX-License-Identifier: GPL-2.0-or-later
"""Only memory helpers before SOURCE approval. Never import a producer at import.
Negative source models, not real permission/Node/pipe/fullhost/native acceptance.
"""
import base64
import errno
import hashlib
import importlib.util
import io
import json
import math
import os
from pathlib import Path
import stat
import sys
import time

REPO = Path('/Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/0ad')
BASE = REPO / 'work/t17-save-five-mod-inventory-repair-preparation'
V1 = BASE / 'required-fault-controls-preparation-v1'
V2 = BASE / 'required-fault-controls-preparation-v2'
IMPL = BASE / 'required-fault-controls-implementation-v1'
EXEC = V1 / 'execution-v1'
PREP = IMPL / 'execution-preparation-v1'
SOURCE_FREEZE = IMPL / 'source-context-freeze-v1/manifest.json'
ORACLE = V1 / 'CASE-ORACLE-v1.json'
ORACLE_SHA = 'c29ae4c2b9cdd74d2ad9fde92c4867aea3921a07f6b77475ba28d854cb45c271'
FIXTURE = BASE / 'preservation-bridge-regression-preparation/implementation-v1/fixture-oracle.json'
FIXTURE_SHA = 'd3361786bd195f3596ea6785919e7715bc3af387c515dc90c9dd49538cb90310'
DESIGN_SHA = 'f597e8d5c5bcf214ccb6a74d7e0920914441c3dece4b6851aa895a5c4607b2d4'
COMPLETION_SHA = 'bae792e723440805f97024314bb5e4a3a02d80f677cce7f59a9929a45972bcdc'
IDS = ('F01_EACCES_CAPTURE_INPUT_RESERVE', 'F02_R_EACCES_FAULT_RESERVE',
       'F02_W_EACCES_FAULT_WRITE_PREFIX')
ROOTS = ('binaries/data/mods/epoch_rts', 'tools/epoch-rts/t16-harness',
         'tools/epoch-rts/t17-save-harness', 'tools/epoch-rts/t17-save-allocation-witness')
SOURCE_NAMES = ('t17-save-five-mod-capture.py', 't17-save-five-mod-source-inventory-v2.cjs',
                't17-save-five-mod-analysis-schema.json')
SOURCE_SHAS = ('d687c19c9be59ba4e241d0d6fc4d0b331cb7ec3555f2267b4fa125e56bdb5022',
               'e7100dd52b755cc7dedefa07624520dbacdd41ccf8e20428160ec2c588f2c3b1',
               '280357ab50426d73f1265cb07458d8d4f86f226ab3b02d68025d1762d7975191')
DESIGN_REPORTS = (
    ('CODE', 'required-fault-controls-design-code-review-v2.json', '729c7244721d05f39b2ee6c4593323ac28bab80f62f4ba7446ed3cf96aa6faeb'),
    ('Python', 'required-fault-controls-design-python-review-v2.json', '284d922e3b028353bfecfe6db36b090b882aebbb593376a5a8c456365aa7eb53'),
    ('JSAPI', 'required-fault-controls-design-js-review-v2/review.json', '06f6ceaa04033e2db6986835ba8ed7b0b8c2f9b376b04be4f5f8de99b7d198c5'))
LAUNCHER = Path('/Library/Developer/CommandLineTools/usr/bin/python3')
HOPS = ((LAUNCHER, '../../Library/Frameworks/Python3.framework/Versions/3.9/bin/python3'),
        (Path('/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3'), 'python3.9'))
PYTHON_TARGET = Path('/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9')
PYTHON_SHA = '6e7ae61f68a3838094fc56590f84c52069a97d7816f6bb79e0e85995b340e464'
RESOURCE_POLICY = {'availableDiskMin': 134217728, 'physicalRAMMin': 2147483648,
                   'reclaimableEstimateMin': 1073741824, 'softFDMin': 256}

class Rejected(Exception):
    pass


def require(value, code):
    if not value:
        raise Rejected(code)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=True, separators=(',', ':'), allow_nan=False).encode('ascii')


def strict(raw):
    require(type(raw) is bytes and len(raw) <= 2097152, 'JSON_BOUND')
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'DUPLICATE_KEY')
            result[key] = value
        return result
    def bad_number(value):
        raise Rejected('NONFINITE')
    value = json.loads(raw.decode('utf-8', 'strict'), object_pairs_hook=pairs,
                       parse_constant=bad_number)
    def finite(item, depth=0):
        require(depth <= 128, 'JSON_DEPTH')
        if type(item) is float:
            require(math.isfinite(item), 'NONFINITE')
        if type(item) is dict:
            for child in item.values():
                finite(child, depth + 1)
        elif type(item) is list:
            for child in item:
                finite(child, depth + 1)
    finite(value)
    return value


def decode(value):
    require(type(value) is str, 'BASE64_TYPE')
    raw = base64.b64decode(value, validate=True)
    require(base64.b64encode(raw).decode('ascii') == value, 'BASE64_CANONICAL')
    return raw


def relative_parts(value):
    require(type(value) is str and 0 < len(value.encode('utf-8')) <= 1024, 'PATH_BOUND')
    parts = value.split('/')
    require(all(x and x not in ('.', '..') and '\\' not in x and ':' not in x and '\x00' not in x for x in parts), 'PATH_COMPONENT')
    return parts


def identity(value):
    return [getattr(value, 'st_' + key) for key in
            ('dev', 'ino', 'mode', 'uid', 'gid', 'nlink', 'size', 'mtime_ns', 'ctime_ns')]


def absolute(value):
    require(type(value) is str and value.startswith('/') and '..' not in Path(value).parts, 'ABSOLUTE_PATH')
    return Path(value)


def physical_dir(path):
    path = absolute(str(path))
    current = os.open('/', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for part in path.parts[1:]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=current)
            previous, current = current, child
            os.close(previous)
        return current
    except BaseException:
        os.close(current)
        raise


def read_file(path, cap=33554432):
    parent = physical_dir(Path(path).parent)
    fd = None
    primary = None
    try:
        before = os.stat(Path(path).name, dir_fd=parent, follow_symlinks=False)
        require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and before.st_size <= cap, 'FILE_BOUND_TYPE')
        fd = os.open(Path(path).name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=parent)
        require(identity(os.fstat(fd)) == identity(before), 'FILE_OPEN_IDENTITY')
        pieces, total = [], 0
        while True:
            chunk = os.read(fd, min(65536, cap - total + 1))
            if not chunk:
                break
            pieces.append(chunk)
            total += len(chunk)
            require(total <= cap, 'FILE_READ_BOUND')
        require(total == before.st_size and identity(os.fstat(fd)) == identity(before), 'FILE_READ_IDENTITY')
        require(identity(os.stat(Path(path).name, dir_fd=parent, follow_symlinks=False)) == identity(before), 'FILE_PATH_IDENTITY')
        return b''.join(pieces)
    except BaseException as error:
        primary = error
        raise
    finally:
        errors = []
        for owned in ([fd] if fd is not None else []) + [parent]:
            try:
                os.close(owned)
            except BaseException as error:
                errors.append(repr(error))
        if errors:
            if primary is not None:
                primary.cleanupUnknown = getattr(primary, 'cleanupUnknown', []) + errors
            else:
                raise Rejected('READ_CLOSE_UNKNOWN:' + repr(errors))


def checked_file(path, expected):
    raw = read_file(path)
    require(digest(raw) == expected, 'FILE_SHA:' + str(path))
    return raw


def canonical_rows(rows):
    result = []
    seen = set()
    for row in rows:
        path = str(absolute(row['path']))
        require(path not in seen and type(row['bytes']) is int and row['bytes'] >= 0, 'BINDING_DUPLICATE_TYPE')
        require(type(row['sha256']) is str and len(row['sha256']) == 64 and all(c in '0123456789abcdef' for c in row['sha256']), 'BINDING_SHA')
        seen.add(path)
        result.append({'path': path, 'bytes': row['bytes'], 'sha256': row['sha256']})
    return sorted(result, key=lambda row: row['path'].encode('utf-8'))


def binding_path(row):
    # Point-in-time history binds its frozen snapshot, never a mutable tracking file.
    value = row['path'] if row.get('requireCurrentMatchForDesignApproval', True) else row['snapshot']
    return absolute(value) if value.startswith('/') else REPO / value


def future_deadline(start, now, budget):
    require(type(start) in (int, float) and type(now) in (int, float) and math.isfinite(start) and math.isfinite(now), 'CLOCK_TYPE')
    require(start <= now <= start + budget, 'DEADLINE')
    return start + budget


def first_error(primary, secondary):
    return secondary if primary is None else primary


class FailureLedger:
    """Bounded memory observations, never a promise of durable final evidence."""
    def __init__(self):
        self.primary_error = None
        self.primary = None
        self.secondary = []
        self.bytes = 0
        self.incomplete = 0
        self.unknown_records = []
        self.unknown_bytes = 0

    def unknown_record(self, phase, error_type, cleanup):
        # A separate reserved bounded marker budget preserves phase/available close
        # facts when a full message cannot fit. Missing markers remain UNKNOWN.
        marker = {'phase': phase, 'type': error_type, 'cleanupUnknown': cleanup,
                  'message': 'UNKNOWN_LEDGER_RECORD_NOT_FULLY_RETAINED'}
        try:
            raw = canonical(marker)
            require(self.unknown_bytes + len(raw) <= 65536, 'UNKNOWN_MARKER_BOUND')
            marker = strict(raw)
            self.unknown_bytes += len(raw)
            self.unknown_records.append(marker)
        except BaseException:
            pass  # incomplete already counts this lost full event, never COMPLETE.
        return {'phase': phase, 'type': error_type,
                'message': 'UNKNOWN_LEDGER_RECORD_NOT_FULLY_RETAINED',
                'cleanupUnknown': 'UNKNOWN_SEE_BOUNDED_MARKERS'}

    def record(self, phase, error, cleanup_unknown=None):
        first = self.primary_error is None
        if first:
            self.primary_error = error  # Preserve the original object, not a wrapper.
        cleanup = 'UNKNOWN'
        try:
            cleanup = list(getattr(error, 'cleanupUnknown', []))
            if cleanup_unknown is not None:
                cleanup.extend(cleanup_unknown)
            event = {'phase': phase, 'type': type(error).__name__,
                     'message': str(error), 'cleanupUnknown': cleanup}
            raw = canonical(event)
            if self.bytes + len(raw) > 983040 or len(self.secondary) >= 16384:
                raise Rejected('LEDGER_BOUND')
            # Own a detached plain record so later cleanup mutation cannot erase it.
            event = strict(raw)
            self.bytes += len(raw)
        except BaseException:
            self.incomplete += 1
            event = self.unknown_record(phase, type(error).__name__, cleanup)
            # One bounded marker for the primary. Later dropped events are counted,
            # never presented as a complete ledger or silently declared healthy.
            if not first:
                return
        if first:
            self.primary = event
        else:
            self.secondary.append(event)

    def merge_case(self, case_id, other):
        if other.primary_error is None:
            return
        first = self.primary_error is None
        if first:
            self.primary_error = other.primary_error
        events = [other.primary] + other.secondary
        for event in events:
            try:
                merged = dict(event)
                merged['phase'] = case_id + ' / ' + event['phase']
                raw = canonical(merged)
                require(self.bytes + len(raw) <= 983040 and len(self.secondary) < 16384, 'LEDGER_BOUND')
                merged = strict(raw)
                self.bytes += len(raw)
                if first:
                    self.primary = merged
                    first = False
                else:
                    self.secondary.append(merged)
            except BaseException:
                self.incomplete += 1
                marker = self.unknown_record(case_id + ' / ' + event['phase'],
                                             event['type'], event['cleanupUnknown'])
                if first:
                    self.primary = marker
                    first = False
        self.incomplete += other.incomplete
        for marker in other.unknown_records:
            self.unknown_record(case_id + ' / ' + marker['phase'],
                                marker['type'], marker['cleanupUnknown'])

    def snapshot(self):
        return {'primary': self.primary, 'secondary': list(self.secondary),
                'ledgerCompleteness': 'UNKNOWN' if self.incomplete else 'COMPLETE_MEMORY_ONLY',
                'unretainedEvents': self.incomplete,
                'unknownRecords': list(self.unknown_records),
                'durableFinalLedger': 'NOT_ATTESTED'}

    def apply(self, result):
        result.update(self.snapshot())
        if self.primary_error is not None:
            result['status'] = 'UNKNOWN_OR_FAIL'


def diagnostic_bytes(ledger):
    """Pure serialization; a cap breach has a fixed explicit UNKNOWN payload."""
    raw = b'REQUIRED_FAULT_CONTROLS_UNKNOWN_OR_FAIL ' + canonical(ledger.snapshot()) + b'\n'
    require(len(raw) <= 1048576, 'DIAGNOSTIC_BOUND')
    return raw


def emit_failure(ledger, started):
    """Once per channel; no retry, new file, or assumption a closed Store works."""
    channel_unknown = False
    try:
        raw = diagnostic_bytes(ledger)
    except BaseException as error:
        ledger.record('diagnostic serialization', error)
        channel_unknown = True
        raw = b'REQUIRED_FAULT_CONTROLS_UNKNOWN_OR_FAIL UNKNOWN_LEDGER_SERIALIZATION_OR_BOUND\n'
    try:
        text = raw.decode('ascii')
        require(sys.stderr.write(text) == len(text), 'DIAGNOSTIC_SHORT_WRITE_UNKNOWN')
        sys.stderr.flush()
    except BaseException as error:
        ledger.record('stderr diagnostic channel UNKNOWN', error)
        channel_unknown = True
    try:
        future_deadline(started, time.monotonic(), 120)
    except BaseException as error:
        ledger.record('post diagnostic final deadline', error)
        channel_unknown = True
    if channel_unknown:
        # Purpose/date: retain diagnostic-tail phases in the remaining channel;
        # 2026-10-29. Its own last write/flush failure cannot attest durability.
        try:
            # Fresh plain-record snapshot includes stderr/deadline failures above.
            fallback = diagnostic_bytes(ledger)
            # Reserve the entire possible earlier success write, including a
            # partial write. Aggregate stdout remains <=1MiB without a retry.
            success_bytes = len(b'ACCEPT_THREE_BOUNDED_NEGATIVE_SOURCE_MODELS_ONLY\n')
            require(len(fallback) + success_bytes <= 1048576, 'FALLBACK_AGGREGATE_BOUND')
        except BaseException as error:
            ledger.record('stdout fallback serialization or bound UNKNOWN', error)
            fallback = b'REQUIRED_FAULT_CONTROLS_UNKNOWN_OR_FAIL UNKNOWN_FINAL_LEDGER_SERIALIZATION_OR_BOUND\n'
        try:
            text = fallback.decode('ascii')
            require(sys.stdout.write(text) == len(text), 'FALLBACK_SHORT_WRITE_UNKNOWN')
            sys.stdout.flush()
        except BaseException as error:
            ledger.record('stdout fallback channel UNKNOWN', error)
    return 1


def fault_match(kind, name, parent_path, root_path, root_generation, actual_generation, flags):
    target = 'capture-inputs.json' if kind == IDS[0] else 'fault.json'
    return (name == target and parent_path == root_path and root_generation == actual_generation
            and root_generation is not None
            and flags == (os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW))


def generation_closed(row):
    return row['closeAttempts'] == 1 and row['closeStatus'] == 'OK'


def read_source_freeze(descriptor):
    require(set(descriptor) == {'path', 'sha256'} and descriptor['path'] == str(SOURCE_FREEZE), 'FREEZE_PATH')
    manifest = strict(checked_file(SOURCE_FREEZE, descriptor['sha256']))
    rows = manifest['bindings']
    require(type(rows) is list and len(rows) <= 128, 'FREEZE_COUNT')
    result, originals, total = [], {}, 0
    for row in rows:
        original = row['path']
        require(original not in originals, 'FREEZE_DUPLICATE')
        originals[original] = row
        snapshot = absolute(row['snapshot']) if row['snapshot'].startswith('/') else REPO / row['snapshot']
        raw = read_file(snapshot)
        require(len(raw) == row['bytes'] and digest(raw) == row['sha256'], 'SNAPSHOT_BINDING')
        path = binding_path(row)
        current = read_file(path)
        require(len(current) == row['bytes'] and digest(current) == row['sha256'], 'CURRENT_BINDING')
        total += len(raw)
        result.append({'path': str(path), 'bytes': len(current), 'sha256': digest(current)})
    require(total <= 33554432, 'FREEZE_BYTES')
    design = strict(checked_file(V2 / 'manifest.json', DESIGN_SHA))
    for required in design['bindings']:
        original = required['path']
        require(original in originals, 'MISSING_DESIGN_CONTEXT:' + original)
        actual = originals[original]
        require((actual['bytes'], actual['sha256']) == (required['bytes'], required['sha256']), 'DESIGN_CONTEXT_CHANGED')
        if not required.get('requireCurrentMatchForDesignApproval', True):
            require(actual.get('requireCurrentMatchForDesignApproval') is False, 'HISTORY_NOT_SNAPSHOT')
    mandatory = [Path(__file__).absolute(), IMPL / 'HELPER-PLAN-v1.json',
                 REPO / 'tools/epoch-rts/test-t17-save-five-mod-required-fault-controls-helpers.py',
                 V2 / 'manifest.json', BASE / 'required-fault-controls-design-completion-v2.json']
    mandatory.extend(BASE / row[1] for row in DESIGN_REPORTS)
    for path in mandatory:
        key = str(path.relative_to(REPO)) if str(path).startswith(str(REPO) + '/') else str(path)
        require(key in originals, 'MISSING_NEW_CONTEXT:' + key)
    normalized = canonical_rows(result)
    return manifest, normalized, digest(canonical(normalized))


def runtime_rows():
    result = []
    for path, link in HOPS:
        parent = physical_dir(path.parent)
        primary = None
        try:
            before = os.stat(path.name, dir_fd=parent, follow_symlinks=False)
            require(stat.S_ISLNK(before.st_mode) and os.readlink(path.name, dir_fd=parent) == link, 'LAUNCHER_LINK')
            after = os.stat(path.name, dir_fd=parent, follow_symlinks=False)
            require(identity(before) == identity(after) and os.readlink(path.name, dir_fd=parent) == link, 'LAUNCHER_CHANGED')
            result.append({'path': str(path), 'identity': identity(before), 'rawlink': link})
        except BaseException as error:
            primary = error
            raise
        finally:
            try:
                os.close(parent)
            except BaseException as error:
                if primary is not None:
                    primary.cleanupUnknown = getattr(primary, 'cleanupUnknown', []) + [repr(error)]
                else:
                    raise
    raw = checked_file(PYTHON_TARGET, PYTHON_SHA)
    result.append({'path': str(PYTHON_TARGET), 'identity': identity(os.stat(PYTHON_TARGET, follow_symlinks=False)), 'bytes': len(raw), 'sha256': digest(raw)})
    return result


def report_fresh(report, core_sha, rows, rows_sha, runtime, now):
    require(report['capsuleId'] == 't17-required-fault-controls-v1' and report['capsuleCoreSHA256'] == core_sha, 'REPORT_CORE')
    require(report['sourceBindings'] == rows and report['sourceBindingsSHA256'] == rows_sha, 'REPORT_BINDINGS')
    require(report['runtimeRows'] == runtime and report['resourcePolicy'] == RESOURCE_POLICY, 'REPORT_RUNTIME')
    checked, expires = report['checkedUnixSeconds'], report['expiresUnixSeconds']
    require(type(checked) in (int, float) and type(expires) in (int, float)
            and math.isfinite(checked) and math.isfinite(expires), 'REPORT_CLOCK')
    require(0 <= now - checked <= 60 and now + 120 <= expires and 120 <= expires - checked <= 600, 'REPORT_EXPIRED')
    require(report['runRoot'] == str(EXEC) and report['sourceFreezeSHA256'] == report['reviewedSourceFreezeSHA256'], 'REPORT_ROOT')
    require(report['status'] == 'MATCH' and report['fixedRootAbsent'] is True and report['scopedOwnerAbsent'] is True, 'REPORT_OBSERVATION')
    actual = report['resources']
    for key in RESOURCE_POLICY:
        require(type(actual[key]) is int and actual[key] >= RESOURCE_POLICY[key], 'REPORT_RESOURCE')


def admit(capsule_path, expected_sha):
    require(Path(capsule_path) == PREP / 'capsule-v1.json', 'CAPSULE_PATH')
    capsule = strict(checked_file(capsule_path, expected_sha))
    keys = {'schema', 'capsuleId', 'scope', 'runRoot', 'caseIds', 'retry', 'seed', 'sourceFreeze',
            'sourceReviews', 'sourceBindings', 'runtimeRows', 'resourcePolicy', 'rootReadback', 'independentFreshGuard'}
    require(set(capsule) == keys and capsule['schema'] == 1 and type(capsule['schema']) is int, 'CAPSULE_KEYS')
    require(capsule['capsuleId'] == 't17-required-fault-controls-v1' and capsule['scope'] == 'INJECTED_ERRNO_HAND_AUTHORED_PROTOCOL_MODEL_ONLY', 'CAPSULE_SCOPE')
    require(capsule['runRoot'] == str(EXEC) and capsule['caseIds'] == list(IDS)
            and type(capsule['retry']) is int and capsule['retry'] == 0 and capsule['seed'] is False, 'CAPSULE_CASES')
    require(sys.version_info[:3] == (3, 9, 6) and Path(sys.executable) == LAUNCHER and sys.dont_write_bytecode, 'FIXED_PYTHON')
    manifest, rows, rows_sha = read_source_freeze(capsule['sourceFreeze'])
    require(capsule['sourceBindings'] == rows, 'CAPSULE_BINDINGS')
    require(checked_file(BASE / 'required-fault-controls-design-completion-v2.json', COMPLETION_SHA), 'DESIGN_COMPLETION')
    for role, path, sha in DESIGN_REPORTS:
        report = strict(checked_file(BASE / path, sha))
        require(report['verdict'] == 'APPROVE_DESIGN_ONLY', 'DESIGN_REVIEW')
    reviews = capsule['sourceReviews']
    require(type(reviews) is list and len(reviews) == 3, 'SOURCE_REVIEW_COUNT')
    review_paths = set()
    for role, desc in zip(('CODE', 'Python', 'JSAPI'), reviews):
        path = IMPL / ('source-review-' + role + '-v1.json')
        require(set(desc) == {'role', 'path', 'sha256'} and desc['role'] == role and desc['path'] == str(path), 'SOURCE_REVIEW_PATH')
        report = strict(checked_file(path, desc['sha256']))
        require(report['verdict'] == 'APPROVE_SOURCE_ONLY' and report['reviewerRole'] == role
                and report['inputManifestSHA256'] == capsule['sourceFreeze']['sha256']
                and report['reviewedBindingsSHA256'] == rows_sha, 'SOURCE_REVIEW_LINK')
        require(str(path) not in review_paths, 'SOURCE_REVIEW_DISTINCT')
        review_paths.add(str(path))
    runtime = runtime_rows()
    require(capsule['runtimeRows'] == runtime and capsule['resourcePolicy'] == RESOURCE_POLICY, 'CAPSULE_RUNTIME')
    core = {key: value for key, value in capsule.items() if key not in ('rootReadback', 'independentFreshGuard')}
    core_sha = digest(canonical(core))
    paths = []
    for key, filename in (('rootReadback', 'root-readback-v1.json'), ('independentFreshGuard', 'freshguard-v1.json')):
        desc = capsule[key]
        require(set(desc) == {'path', 'sha256'} and desc['path'] == str(PREP / filename), 'CURRENT_REPORT_PATH')
        report = strict(checked_file(desc['path'], desc['sha256']))
        require(report['sourceFreezeSHA256'] == capsule['sourceFreeze']['sha256'], 'REPORT_FREEZE')
        report_fresh(report, core_sha, rows, rows_sha, runtime, time.time())
        paths.append(desc['path'])
    require(len(set(paths)) == 2, 'INDEPENDENT_REPORT_DISTINCT')
    require(not os.path.lexists(EXEC), 'RUN_ROOT_EXISTS')
    # Actual available-disk observation supplements the two independent resource records.
    disk = os.statvfs(V1)
    require(disk.f_bavail * disk.f_frsize >= RESOURCE_POLICY['availableDiskMin'], 'CURRENT_DISK')
    return capsule, rows, rows_sha, runtime


class Store:
    """Exclusive physical tree; no unlink/rename/truncate or ownership retries."""
    def __init__(self):
        self.parent = physical_dir(V1)
        self.root = None
        self.dirs = {}
        self.bytes = 0
        self.files = 0
        self.close_errors = []
        try:
            os.mkdir('execution-v1', 0o700, dir_fd=self.parent)
            self.root = os.open('execution-v1', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=self.parent)
            self.dirs[''] = self.root
            self.root_identity = identity(os.fstat(self.root))[:2]
        except BaseException as error:
            for owned in ([self.root] if self.root is not None else []) + [self.parent]:
                try:
                    os.close(owned)
                except BaseException as secondary:
                    error.cleanupUnknown = getattr(error, 'cleanupUnknown', []) + [repr(secondary)]
            raise
    def check(self):
        reopened = physical_dir(V1)
        primary = None
        try:
            require(identity(os.fstat(reopened))[:2] == identity(os.fstat(self.parent))[:2], 'STORE_PARENT_ANCHOR')
            current = os.stat('execution-v1', dir_fd=reopened, follow_symlinks=False)
            held = os.fstat(self.root)
            require(identity(current)[:2] == self.root_identity == identity(held)[:2]
                    and stat.S_ISDIR(current.st_mode) and stat.S_IMODE(held.st_mode) == 0o700
                    and held.st_uid == os.getuid(), 'STORE_ANCHOR')
        except BaseException as error:
            primary = error
            raise
        finally:
            try:
                os.close(reopened)
            except BaseException as error:
                if primary is not None:
                    primary.cleanupUnknown = getattr(primary, 'cleanupUnknown', []) + [repr(error)]
                else:
                    raise
    def directory(self, name):
        self.check()
        path = ''
        fd = self.root
        for part in relative_parts(name):
            path = path + '/' + part if path else part
            if path not in self.dirs:
                os.mkdir(part, 0o700, dir_fd=fd)
                new = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                self.dirs[path] = new
            current = os.stat(part, dir_fd=fd, follow_symlinks=False)
            held = os.fstat(self.dirs[path])
            require(identity(current)[:2] == identity(held)[:2] and stat.S_ISDIR(held.st_mode)
                    and stat.S_IMODE(held.st_mode) == 0o700 and held.st_uid == os.getuid(), 'STORE_DIRECTORY')
            fd = self.dirs[path]
        return fd
    def put(self, name, raw, cap=8388608):
        require(type(raw) is bytes and len(raw) <= cap, 'EVIDENCE_FILE_BOUND')
        require(self.bytes + len(raw) <= 33554432 and self.files < 768, 'CAMPAIGN_EVIDENCE_BOUND')
        bits = relative_parts(name)
        parent = self.root if len(bits) == 1 else self.directory('/'.join(bits[:-1]))
        self.check()
        fd = os.open(bits[-1], os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=parent)
        primary = None
        try:
            view = memoryview(raw)
            while view:
                count = os.write(fd, view)
                require(count > 0, 'EVIDENCE_SHORT_WRITE')
                view = view[count:]
            os.fsync(fd)
        except BaseException as error:
            primary = error
            raise
        finally:
            try:
                os.close(fd)
            except BaseException as error:
                if primary is not None:
                    primary.cleanupUnknown = getattr(primary, 'cleanupUnknown', []) + [repr(error)]
                else:
                    raise
        require(read_file(EXEC / name, cap) == raw, 'EVIDENCE_READBACK')
        os.fsync(parent)
        self.bytes += len(raw)
        self.files += 1
    def close(self):
        owned = list(reversed(list(self.dirs.values()))) + [self.parent]
        self.dirs = {}
        self.parent = None
        for fd in owned:
            try:
                os.close(fd)
            except BaseException as error:
                self.close_errors.append({'fd': fd, 'status': 'CLOSE_UNKNOWN', 'error': repr(error)})
        require(not self.close_errors, 'STORE_CLOSE_UNKNOWN')


class BoundedBytes(io.BytesIO):
    def write(self, raw):
        require(self.tell() + len(raw) <= 1048576, 'SINK_BOUND')
        return super().write(raw)


class BoundedText(io.StringIO):
    def write(self, value):
        require(len(self.getvalue().encode('utf-8')) + len(value.encode('utf-8')) <= 1048576, 'STDERR_BOUND')
        return super().write(value)


class Observer:
    """Only preregistered errno effects; observations cannot attest hidden FDs."""
    def __init__(self, case_id, root):
        self.case_id, self.root = case_id, str(root)
        self.saved = (os.open, os.write, os.close)
        self.active, self.generations, self.events = {}, [], []
        self.sequence, self.injections = 0, 0
        self.root_generation = None
        self.partial = None
        self.installed = False
    def event(self, value):
        require(len(self.events) < 16384, 'EVENT_BOUND')
        self.events.append(value)
    def opened_path(self, path, kwargs):
        value = os.fspath(path)
        if value.startswith('/'):
            return value
        parent = self.active.get(kwargs.get('dir_fd'))
        return None if parent is None or parent['path'] is None else str(Path(parent['path']) / value)
    def target(self, name, flags, kwargs):
        parent = self.active.get(kwargs.get('dir_fd'))
        return (parent is not None and fault_match(self.case_id, name, parent['path'], self.root,
                self.root_generation, parent['generation'], flags)
                and identity(os.fstat(kwargs['dir_fd']))[:2] == parent['identity'][:2])
    def open(self, path, flags, *args, **kwargs):
        matched = self.target(path, flags, kwargs)
        if matched and self.case_id != IDS[2]:
            self.injections += 1
            self.event({'op': 'OPEN_EACCES', 'name': str(path), 'flags': flags,
                        'dirGeneration': self.root_generation, 'errno': errno.EACCES})
            raise OSError(errno.EACCES, 'preregistered injected permission control')
        fd = self.saved[0](path, flags, *args, **kwargs)
        # Ownership is registered immediately after successful open, before fstat.
        self.sequence += 1
        row = {'fd': fd, 'generation': self.sequence, 'path': self.opened_path(path, kwargs),
               'identity': None, 'closeAttempts': 0, 'closeStatus': 'NOT_ATTEMPTED', 'fault': matched}
        self.active[fd] = row
        self.generations.append(row)
        try:
            row['identity'] = identity(os.fstat(fd))
            self.event({'op': 'OPEN', 'fd': fd, 'generation': row['generation'], 'path': row['path'], 'flags': flags})
            if row['path'] == self.root and stat.S_ISDIR(row['identity'][2]):
                require(self.root_generation is None, 'ROOT_GENERATION_REOPEN')
                self.root_generation = row['generation']
        except BaseException as primary:
            # Caller has not received fd; transfer once-only cleanup to this wrapper.
            try:
                self.close(fd)
            except BaseException as error:
                primary.cleanupUnknown = getattr(primary, 'cleanupUnknown', []) + [repr(error)]
            raise
        return fd
    def write(self, fd, data):
        row = self.active.get(fd)
        if row is not None and row['fault'] and self.case_id == IDS[2]:
            require(self.injections == 0, 'REPEATED_FAULT_WRITE')
            self.injections += 1
            raw = bytes(data)
            require(raw.startswith(b'{"phase":') and len(raw) <= 1048576, 'FAULT_PREFIX_INPUT')
            count = self.saved[1](fd, b'{"phase":')
            self.partial = {'fd': fd, 'generation': row['generation'], 'attemptedBase64': base64.b64encode(raw).decode('ascii'),
                            'committedBase64': base64.b64encode(b'{"phase":'[:count]).decode('ascii'), 'actualWriteCount': count}
            self.event({'op': 'WRITE_PREFIX_EACCES', 'fd': fd, 'generation': row['generation'], 'actualWriteCount': count, 'errno': errno.EACCES})
            require(count == 9, 'PREFIX_SHORT_WRITE')
            raise OSError(errno.EACCES, 'preregistered injected permission control')
        return self.saved[1](fd, data)
    def close(self, fd):
        row = self.active.pop(fd, None)
        if row is not None:
            row['closeAttempts'] += 1
            row['closeStatus'] = 'UNKNOWN'
        try:
            self.saved[2](fd)
        except BaseException as error:
            if row is not None:
                row['closeError'] = repr(error)
            raise
        if row is not None:
            row['closeStatus'] = 'OK'
            self.event({'op': 'CLOSE', 'fd': fd, 'generation': row['generation'], 'status': 'OK'})
    def install(self):
        require(not self.installed, 'OBSERVER_REINSTALL')
        os.open, os.write, os.close = self.open, self.write, self.close
        self.installed = True
    def restore(self):
        if self.installed:
            os.open, os.write, os.close = self.saved
            self.installed = False
    def facts(self):
        return {'events': self.events, 'generations': self.generations, 'injections': self.injections,
                'partial': self.partial, 'unclosedObservedGenerations': [row['generation'] for row in self.active.values()],
                'scope': 'OBSERVED_OS_OPEN_CLOSE_GENERATIONS_ONLY_NOT_HIDDEN_OR_FULLHOST'}


def census(path, bytes_cap, files_cap=256):
    """Bounded physical walk, retain file identity/hash; never follow symlinks."""
    rows, count, total = [], 0, 0
    def walk(directory, prefix):
        nonlocal count, total
        fd = physical_dir(directory)
        primary = None
        try:
            iterator = os.scandir(fd)
            try:
                names = []
                for item in iterator:
                    count += 1
                    require(count <= files_cap, 'TREE_ENTRY_BOUND')
                    names.append(item.name)
            finally:
                iterator.close()
            for name in sorted(names, key=lambda value: value.encode('utf-8')):
                relative_parts(name)
                st = os.stat(name, dir_fd=fd, follow_symlinks=False)
                rel = prefix + '/' + name if prefix else name
                require(stat.S_ISDIR(st.st_mode) or stat.S_ISREG(st.st_mode), 'TREE_TYPE')
                if stat.S_ISDIR(st.st_mode):
                    walk(directory / name, rel)
                else:
                    total += st.st_size
                    require(total <= bytes_cap, 'TREE_BYTE_BOUND')
                    raw = read_file(directory / name, bytes_cap)
                    rows.append({'path': rel, 'bytes': len(raw), 'sha256': digest(raw), 'identity': identity(st)})
        except BaseException as error:
            primary = error
            raise
        finally:
            try:
                os.close(fd)
            except BaseException as error:
                if primary is not None:
                    primary.cleanupUnknown = getattr(primary, 'cleanupUnknown', []) + [repr(error)]
                else:
                    raise
    walk(path, '')
    return {'files': rows, 'entries': count, 'bytes': total}


def fixture_setup(store, case_id, fixture):
    prefix = case_id + '/fixture'
    store.directory(case_id + '/evidence')
    store.put(case_id + '/evidence/preexisting-sentinel.bin', b'F01F02 immutable prefix\n')
    store.put(prefix + '/synthetic-public.zip', decode(fixture['zipBase64']), 65536)
    for i, mod in enumerate(fixture['orderedMods'][1:]):
        store.directory(prefix + '/fixture-repo/' + ROOTS[i])
        for row in fixture['rows']:
            if row['mod'] == mod:
                store.put(prefix + '/fixture-repo/' + ROOTS[i] + '/' + row['vfs'], decode(row['bodyBase64']), 4096)
    store.directory(prefix + '/fixture-repo/work/t17-save-five-mod-inventory-repair-preparation')
    tooling = {}
    for name, expected in zip(SOURCE_NAMES, SOURCE_SHAS):
        raw = checked_file(REPO / 'tools/epoch-rts' / name, expected)
        store.put(prefix + '/tooling/' + name, raw, 131072)
        tooling[name] = EXEC / prefix / 'tooling' / name
    store.check()
    return tooling


def load_producer(tooling, case_id):
    # STAGE C ONLY. Never invoked by import/default CLI or memory helpers.
    path = tooling[SOURCE_NAMES[0]]
    spec = importlib.util.spec_from_file_location('_required_fault_' + case_id, str(path))
    require(spec is not None and spec.loader is not None, 'PRODUCER_SPEC')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    fixture_root = EXEC / case_id / 'fixture'
    config = {'REPO': fixture_root / 'fixture-repo', 'ARCHIVE_PATH': fixture_root / 'synthetic-public.zip',
              'ARCHIVE_SHA': 'cea88db14e39f8f6ef63c315a8f88d4fc18a0a6c12e33dca97d38d636849b132',
              'OUTPUT_PARENT': fixture_root / 'fixture-repo/work/t17-save-five-mod-inventory-repair-preparation/captures',
              'NODE_PATH': tooling[SOURCE_NAMES[1]], 'NODE_SOURCE_EXPECTED': SOURCE_SHAS[1],
              'SCHEMA_PATH': tooling[SOURCE_NAMES[2]]}
    for key, value in config.items():
        require(hasattr(module, key), 'PRIVATE_GLOBAL_MISSING')
        setattr(module, key, value)
    return module, config


def verify_case(case, output, sent, stderr, code, observer, fixture):
    require(code == 1 and sent == decode(case['expectedStdoutBase64'])
            and len(sent) == case['expectedStdoutBytes'] and digest(sent) == case['expectedStdoutSHA256'], 'RETURN_STDOUT_ORACLE')
    require(stderr == case['expectedStderr'], 'STDERR_PRIMARY_OR_CLEANUP_UNKNOWN')
    frames = [strict(line) for line in sent.splitlines()]
    require(frames == case['expectedFrames'] and frames[-1]['durableFault'] is False
            and not any(row['kind'] == 'COMPLETED' for row in frames), 'FRAME_ORACLE')
    require(read_file(output / 'protocol-input.ndjson', 1048576) == decode(case['_input']), 'INPUT_RAW')
    require(read_file(output / 'protocol-output.ndjson', 1048576) == sent, 'OUTPUT_RAW_SENT')
    for name in case['forbiddenFiles']:
        require(not os.path.lexists(output / name), 'UNEXPECTED_HEALTHY_FILE')
    expected_files = {'protocol-input.ndjson', 'protocol-output.ndjson', 'diagnostics.ndjson', 'archive-auth.json'}
    for row in fixture['rows']:
        names = ['layer-sources/' + row['mod'] + '/' + row['vfs']]
        if row['vfs'] == 'mod.json':
            names.append('layer-metadata/' + row['mod'] + '/mod.json')
        for name in names:
            raw = read_file(output / name, 1048576)
            require(raw == decode(row['bodyBase64']) and digest(raw) == row['sha256'], 'BODY_COPY_ORACLE')
            expected_files.add(name)
    selected = {}
    for row in fixture['rows']:
        selected[row['vfs']] = row
    for vfs in fixture['selectedVFS']:
        name = 'effective/' + vfs
        require(read_file(output / name) == decode(selected[vfs]['bodyBase64']), 'EFFECTIVE_ORACLE')
        expected_files.add(name)
    archive = strict(read_file(output / 'archive-auth.json', 1048576))
    archive_rows = [row for row in observer.generations if row['path'] == str(EXEC / case['id'] / 'fixture/synthetic-public.zip')]
    require(len(archive_rows) == 1, 'ARCHIVE_FD_OBSERVATION')
    observed_identity = archive_rows[0]['identity']
    require(archive['fdMetadata'] == [observed_identity[j] for j in (0, 1, 6, 7, 8)], 'ARCHIVE_FD_METADATA')
    require(archive['chunkBytes'] == 4194304 and archive['chunkCount'] == 1, 'ARCHIVE_CHUNK_CONTEXT')
    require(archive['expectedSHA'] == fixture['zipSHA256'] and archive['actualSHA'] == fixture['zipSHA256']
            and archive['chunkSHA256'] == [fixture['zipSHA256']] and archive['size'] == 517
            and archive['status'] == 'VERIFIED_HELD_FD_BYTES' and archive['authorityKind'] == 'VERIFIED_HELD_FD_BYTES', 'ARCHIVE_ORACLE')
    if case['id'] == IDS[0]:
        fault = strict(read_file(output / 'fault.json', 1048576))
        require(fault == {'phase': 'ARCHIVE_AND_SOURCES', 'code': 'SOURCE_TYPE', 'secondary': [],
                          'unknownCloseDescriptors': [], 'outputCleanupComplete': False, 'sourceClosure': False, 'native': False}, 'FAULT_ORACLE')
        require(not os.path.lexists(output / 'capture-inputs.json'), 'F01_TARGET_PRESENT')
        expected_files.add('fault.json')
    else:
        inputs = strict(read_file(output / 'capture-inputs.json', 1048576))
        require(inputs['captured'] == case['expectedCaptured'] and inputs['sourceClosure'] is False and inputs['native'] is False, 'CAPTURE_INPUT_ORACLE')
        require(inputs['nodeSource'] == {'path': str(EXEC / case['id'] / 'fixture/tooling' / SOURCE_NAMES[1]),
                                       'expectedSHA': SOURCE_SHAS[1], 'actualSHA': SOURCE_SHAS[1]}, 'NODE_SOURCE_ORACLE')
        context = inputs['runtime']
        require(set(context) == {'pythonExecutable', 'pythonVersion', 'launcher', 'dependencies', 'authority'}
                and context['pythonExecutable'] == sys.executable and context['pythonVersion'] == sys.version
                and context['authority'] == 'OBSERVED_RUNTIME_DEPENDENCIES_NOT_EXECUTION_ATTESTATION', 'RUNTIME_CONTEXT_KEYS')
        host_rows = runtime_rows()
        launcher = context['launcher']
        require(launcher['physicalTarget'] == str(PYTHON_TARGET) and launcher['targetSHA256'] == PYTHON_SHA
                and len(launcher['hops']) == 2, 'RUNTIME_LAUNCHER')
        for actual, observed in zip(launcher['hops'], host_rows[:2]):
            require(actual['path'] == observed['path'] and actual['rawlink'] == observed['rawlink'], 'RUNTIME_HOP_PATH')
            for name, index in (('dev', 0), ('ino', 1), ('mode', 2), ('uid', 3), ('gid', 4), ('size', 6), ('mtime_ns', 7), ('ctime_ns', 8)):
                require(actual[name] == observed['identity'][index], 'RUNTIME_HOP_IDENTITY')
        dependency_paths = [str(PYTHON_TARGET)] + [str(PYTHON_TARGET.parent.parent / 'lib/python3.9' / name) for name in
                            ('zipfile.py', 'hashlib.py', 'io.py', 'json/__init__.py', 'os.py',
                             'lib-dynload/_hashlib.cpython-39-darwin.so', 'lib-dynload/zlib.cpython-39-darwin.so')]
        require([row['path'] for row in context['dependencies']] == dependency_paths, 'RUNTIME_DEPENDENCY_PATHS')
        for row in context['dependencies']:
            raw = read_file(row['path'])
            require(set(row) == {'path', 'bytes', 'sha256'} and row['bytes'] == len(raw) and row['sha256'] == digest(raw), 'RUNTIME_DEPENDENCY_READBACK')
        expected_files.add('capture-inputs.json')
        if case['id'] == IDS[1]:
            require(not os.path.lexists(output / 'fault.json'), 'F02_RESERVE_FILE_PRESENT')
        else:
            require(read_file(output / 'fault.json', 1048576) == b'{"phase":', 'PARTIAL_FAULT_ORACLE')
            require(observer.partial is not None and observer.partial['actualWriteCount'] == 9, 'PARTIAL_WRITE_OBSERVATION')
            expected_files.add('fault.json')
    tree = census(output, 8388608)
    require({row['path'] for row in tree['files']} == expected_files, 'PRODUCER_TREE_BIJECTION')
    require(observer.injections == 1 and not observer.active
            and all(generation_closed(row) for row in observer.generations), 'OBSERVED_GENERATION_CLOSE_OR_INJECTION')
    return tree


def run_case(store, case, fixture, campaign_start):
    started = time.monotonic()
    result = {'caseId': case['id'], 'status': 'ADMISSION', 'consumed': False, 'producerCalls': 0,
              'primary': None, 'secondary': [], 'native': False, 'sourceClosure': False}
    ledger = FailureLedger()
    observer, saved_stderr = None, None
    sent, stderr = BoundedBytes(), BoundedText()
    before = None
    try:
        tooling = fixture_setup(store, case['id'], fixture)
        before = census(EXEC / case['id'] / 'fixture', 1048576 + 262144)
        require(before['bytes'] <= 1048576 + 262144, 'FIXTURE_PAYLOAD_BOUND')
        future_deadline(started, time.monotonic(), 20)
        future_deadline(campaign_start, time.monotonic(), 120)
        # Private producer import executes its module body and consumes the case.
        result['consumed'] = True
        store.put(case['id'] + '/evidence/producer-body-entry.json', canonical(result) + b'\n')
        module, config = load_producer(tooling, case['id'])
        output = config['OUTPUT_PARENT'] / 'fault_fixture_v1'
        observer = Observer(case['id'], output)
        saved_stderr = sys.stderr
        sys.stderr = stderr
        observer.install()
        try:
            result['producerCalls'] = 1
            code = module._run(io.BytesIO(decode(case['_input'])), sent)
            result['producerReturn'] = code
        except BaseException as error:
            ledger.record('producer body', error)
        finally:
            try:
                observer.restore()
            except BaseException as error:
                ledger.record('producer observer restore', error)
            sys.stderr = saved_stderr
            saved_stderr = None
        if ledger.primary_error is not None:
            raise ledger.primary_error
        future_deadline(started, time.monotonic(), 20)
        tree = verify_case(case, output, sent.getvalue(), stderr.getvalue(), code, observer, fixture)
        result['producerTree'] = tree
        after = census(EXEC / case['id'] / 'fixture', 1048576 + 262144 + 8388608)
        after_rows = {row['path']: row for row in after['files']}
        for row in before['files']:
            require(after_rows.get(row['path']) == row, 'FIXTURE_PREFIX_CHANGED')
        require(read_file(EXEC / case['id'] / 'evidence/preexisting-sentinel.bin') == b'F01F02 immutable prefix\n', 'SENTINEL_CHANGED')
        future_deadline(started, time.monotonic(), 20)
        result['status'] = 'ACCEPT_BOUNDED_INJECTED_ERRNO_HAND_AUTHORED_PROTOCOL_ONLY'
    except BaseException as error:
        if error is not ledger.primary_error:
            ledger.record('case body', error)
    finally:
        if observer is not None:
            try:
                observer.restore()
            except BaseException as error:
                ledger.record('observer restore', error)
        if saved_stderr is not None:
            sys.stderr = saved_stderr
        channels = [('outer-stdout.raw', lambda: sent.getvalue()),
                    ('outer-stderr.raw', lambda: stderr.getvalue().encode('utf-8'))]
        if observer is not None:
            channels.append(('observer.json', lambda: canonical(observer.facts()) + b'\n'))
        for name, create_raw in channels:
            try:
                store.put(case['id'] + '/evidence/' + name, create_raw())
            except BaseException as error:
                ledger.record(name, error)
        result['seconds'] = time.monotonic() - started
        for phase, action in (
                ('case evidence census', lambda: census(EXEC / case['id'] / 'evidence', 8388608)),
                ('case campaign census', lambda: census(EXEC, 33554432, 1552)),
                ('case final deadline', lambda: future_deadline(started, time.monotonic(), 20)),
                ('case campaign deadline', lambda: future_deadline(campaign_start, time.monotonic(), 120))):
            try:
                action()
            except BaseException as error:
                ledger.record(phase, error)
        ledger.apply(result)
        try:
            store.put(case['id'] + '/evidence/result.json', canonical(result) + b'\n')
        except BaseException as error:
            ledger.record('case result evidence', error)
        for phase, origin, budget in (('case post result deadline', started, 20),
                                      ('case post result campaign deadline', campaign_start, 120)):
            try:
                future_deadline(origin, time.monotonic(), budget)
            except BaseException as error:
                ledger.record(phase, error)
        ledger.apply(result)  # Returned memory includes failure of the result channel.
    return result, ledger


def campaign(capsule_path, capsule_sha):
    started = time.monotonic()
    store, result, rows, runtime = None, None, None, None
    ledger = FailureLedger()
    try:
        capsule, rows, rows_sha, runtime = admit(capsule_path, capsule_sha)
        oracle = strict(checked_file(ORACLE, ORACLE_SHA))
        fixture = strict(checked_file(FIXTURE, FIXTURE_SHA))
        require(oracle['caseCount'] == 3 and [row['id'] for row in oracle['cases']] == list(IDS), 'ORACLE_CASES')
        require(len(fixture['rows']) == 13 and fixture['layerCounts'] == [3, 2, 2, 2, 4], 'FIXTURE_COUNTS')
        for row in fixture['rows']:
            body = decode(row['bodyBase64'])
            require(len(body) == row['bytes'] <= 4096 and digest(body) == row['sha256'], 'FIXTURE_BODY')
        require(len(decode(fixture['zipBase64'])) == 517 and digest(decode(fixture['zipBase64'])) == fixture['zipSHA256'], 'FIXTURE_ZIP')
        future_deadline(started, time.monotonic(), 30)
        store = Store()
        store.put('capsule.json', read_file(capsule_path, 2097152))
        store.put('literal-case-oracle.json', checked_file(ORACLE, ORACLE_SHA), 2097152)
        store.put('literal-fixture-oracle.json', checked_file(FIXTURE, FIXTURE_SHA), 2097152)
        result = {'scope': capsule['scope'], 'retry': 0, 'seed': False, 'cases': [],
                  'sourceClosure': False, 'native': False, 'officialCaptureApproved': False}
        future_deadline(started, time.monotonic(), 30)
        for row in oracle['cases']:
            case = dict(row)
            case['_input'] = oracle['expectedInputBase64']
            observed, case_ledger = run_case(store, case, fixture, started)
            result['cases'].append(observed)
            if case_ledger.primary_error is not None:
                ledger.merge_case(case['id'], case_ledger)
                break
        result['status'] = 'ACCEPT_THREE_BOUNDED_NEGATIVE_SOURCE_MODELS_ONLY'
    except BaseException as error:
        ledger.record('campaign body', error)
    finally:
        cleanup_start = time.monotonic()
        if store is not None:
            if result is None:
                result = {'scope': 'INJECTED_ERRNO_HAND_AUTHORED_PROTOCOL_MODEL_ONLY', 'cases': [], 'native': False, 'sourceClosure': False}
            completed = {row['caseId'] for row in result['cases']}
            for case_id in IDS:
                if case_id not in completed:
                    result['cases'].append({'caseId': case_id, 'status': 'NOT_RUN', 'consumed': False})
            try:
                census(EXEC, 33554432, 1552)
            except BaseException as error:
                ledger.record('post campaign census', error)
            for row in rows:
                try:
                    raw = read_file(row['path'])
                    require(len(raw) == row['bytes'] and digest(raw) == row['sha256'], 'POST_SOURCE_CHANGED')
                except BaseException as error:
                    ledger.record('post source ' + row['path'], error)
            try:
                require(runtime_rows() == runtime, 'POST_RUNTIME_CHANGED')
            except BaseException as error:
                ledger.record('post runtime readback', error)
            ledger.apply(result)
            try:
                store.put('result.json', canonical(result) + b'\n')
            except BaseException as error:
                ledger.record('campaign result evidence', error)
            try:
                store.close()
            except BaseException as error:
                # Store.close has exhausted owned once-only closes. Keep every FD
                # detail in memory; never reopen a closed/uncertain evidence store.
                ledger.record('store close', error, store.close_errors)
        for phase, origin, budget in (('cleanup final deadline', cleanup_start, 30),
                                      ('campaign final deadline', started, 120)):
            try:
                future_deadline(origin, time.monotonic(), budget)
            except BaseException as error:
                ledger.record(phase, error)
        if result is not None:
            ledger.apply(result)  # Memory only; disk result necessarily predates close.
    if ledger.primary_error is not None:
        return emit_failure(ledger, started)
    try:
        text = 'ACCEPT_THREE_BOUNDED_NEGATIVE_SOURCE_MODELS_ONLY\n'
        require(sys.stdout.write(text) == len(text), 'SUCCESS_SHORT_WRITE_UNKNOWN')
        sys.stdout.flush()
    except BaseException as error:
        ledger.record('success stdout channel UNKNOWN', error)
    try:
        future_deadline(started, time.monotonic(), 120)
    except BaseException as error:
        ledger.record('post success diagnostic final deadline', error)
    if ledger.primary_error is not None:
        return emit_failure(ledger, started)
    return 0


def main(argv):
    if len(argv) != 4 or argv[1] != '--execute-reviewed':
        return 0  # Inert by default: no file access, probes, imports or fixture setup.
    return campaign(argv[2], argv[3])


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
