# Purpose: bounded CONFIG_ADAPTED preservation supervisor. Date: 2026-10-27.
# SPDX-License-Identifier: GPL-2.0-or-later
"""Author preparation only. No launch on import/default CLI.

The separately invoked execution entry requires externally frozen root evidence;
JSON consistency checks do not authenticate a human/reviewer or grant authority.
No helper test calls subprocess or the production capture entry point.
"""
import base64
import difflib
import hashlib
import json
import math
import os
from pathlib import Path
import re
import selectors
import stat
import subprocess
import sys
import time
from types import SimpleNamespace

REPO = Path(__file__).absolute().parents[2]
PREP = REPO / 'work/t17-save-five-mod-inventory-repair-preparation/preservation-bridge-regression-preparation/implementation-v1'
FIX_PREP = PREP / 'source-fix-v4'  # evidence/context version, never a new run leaf
OFFICIAL = 'ccb24dedee399e6d2810ccb62b0b1b77a937999d9f1dedffbc189b3e359f2429'
ORACLE_SHA = 'd3361786bd195f3596ea6785919e7715bc3af387c515dc90c9dd49538cb90310'
SOURCE_SHAS = {
    'python': 'd687c19c9be59ba4e241d0d6fc4d0b331cb7ec3555f2267b4fa125e56bdb5022',
    'node': 'e7100dd52b755cc7dedefa07624520dbacdd41ccf8e20428160ec2c588f2c3b1',
    'schema': '280357ab50426d73f1265cb07458d8d4f86f226ab3b02d68025d1762d7975191'}
SOURCE_FILES = {'python': 't17-save-five-mod-capture.py', 'node': 't17-save-five-mod-source-inventory-v2.cjs', 'schema': 't17-save-five-mod-analysis-schema.json'}
NODE = '/opt/homebrew/bin/node'
PYTHON = '/Library/Developer/CommandLineTools/usr/bin/python3'
OUTPUT_LEAF = 'preservation_fixture_v1'
RUN_LEAF = 'preservation-regression-v1'
SCOPE = 'SOURCE_MODEL_CONFIG_ADAPTED'
LIMIT = 64 * 1024 * 1024
FILE_LIMIT = 256
ROOTS = ('binaries/data/mods/epoch_rts', 'tools/epoch-rts/t16-harness', 'tools/epoch-rts/t17-save-harness', 'tools/epoch-rts/t17-save-allocation-witness')
UNSUPPORTED = ['implicit engine mod mount','user/rdata higher overrides','DELETED tombstones','loose/archive and archive ordering','mtime arbitration','actual runtime mount/profile inventory','map startup/trigger/native job caller closure']
OPEN = ['independent Python OS wait/reap', 'independent directional pipe bytes',
        'fullhost process tree/FD closure', 'full producer matrix', 'large/sparse ZIP64',
        'actual64MiB/8MiB boundary/RSS', 'official archive/native/GUI/save/network']


class Block(Exception):
    pass


def check(ok, code):
    if not ok:
        raise Block(code)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canon(value):
    return json.dumps(value, ensure_ascii=True, separators=(',', ':'), allow_nan=False).encode('ascii')


def same(a, b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(same(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b


def strict(raw):
    check(type(raw) is bytes and len(raw) <= 4 * 1024 * 1024, 'JSON_LIMIT')
    def pairs(items):
        result = {}
        for key, value in items:
            check(key not in result, 'JSON_DUPLICATE')
            result[key] = value
        return result
    def invalid(_):
        raise Block('JSON_NUMBER')
    value=json.loads(raw.decode('utf-8', 'strict'), object_pairs_hook=pairs, parse_constant=invalid)
    def finite(v):
        if type(v) is float:check(math.isfinite(v),'JSON_NUMBER')
        elif type(v) is dict:
            for child in v.values():finite(child)
        elif type(v) is list:
            for child in v:finite(child)
    finite(value)
    return value


def frames(raw):
    check(raw.endswith(b'\n'), 'RAW_PARTIAL_FRAME')
    rows = raw.split(b'\n')[:-1]
    check(rows and len(rows) <= 16 and all(rows), 'RAW_FRAME_COUNT')
    return [strict(row) for row in rows]


def validate_schema(value, schema):
    """Independent fail-closed evaluator for the exact frozen schema keywords."""
    def equal(a, b):
        return type(a) is type(b) and (a == b)
    def visit(v, rule):
        allowed = {'$schema','$id','$comment','$defs','$ref','allOf','oneOf','type',
                   'const','enum','required','properties','additionalProperties',
                   'items','maxItems','minLength','maxLength','minimum','maximum','pattern'}
        check(not set(rule)-allowed, 'SCHEMA_KEYWORD')
        if '$ref' in rule:
            check(rule['$ref'].startswith('#/'), 'SCHEMA_REF')
            target = schema
            for part in rule['$ref'][2:].split('/'):
                target = target[part]
            visit(v, target)
        for child in rule.get('allOf', []):
            visit(v, child)
        if 'oneOf' in rule:
            count = 0
            for child in rule['oneOf']:
                try:
                    visit(v, child)
                    count += 1
                except Block:
                    pass
            check(count == 1, 'SCHEMA_ONEOF')
        if 'type' in rule:
            names = rule['type'] if isinstance(rule['type'], list) else [rule['type']]
            actual = 'null' if v is None else 'boolean' if type(v) is bool else 'integer' if type(v) is int else 'string' if type(v) is str else 'array' if type(v) is list else 'object' if type(v) is dict else 'unsupported'
            check(actual in names, 'SCHEMA_TYPE')
        if 'const' in rule:check(equal(v, rule['const']), 'SCHEMA_CONST')
        if 'enum' in rule:check(any(equal(v, x) for x in rule['enum']), 'SCHEMA_ENUM')
        if type(v) is dict:
            check(set(rule.get('required', [])) <= set(v), 'SCHEMA_REQUIRED')
            if rule.get('additionalProperties') is False:
                check(set(v) <= set(rule.get('properties', {})), 'SCHEMA_EXTRA')
            for key, child in rule.get('properties', {}).items():
                if key in v:visit(v[key], child)
        if type(v) is list:
            check(len(v) <= rule.get('maxItems', len(v)), 'SCHEMA_ARRAY')
            for item in v:
                if 'items' in rule:visit(item, rule['items'])
        if type(v) is str:
            length = len(v.encode('utf-16-le','surrogatepass'))//2
            check(rule.get('minLength',0) <= length <= rule.get('maxLength',length), 'SCHEMA_STRING')
            if 'pattern' in rule:check(re.search(rule['pattern'],v) is not None,'SCHEMA_PATTERN')
        if type(v) is int:
            check(rule.get('minimum',v) <= v <= rule.get('maximum',v),'SCHEMA_INTEGER')
    visit(value, schema)


def parts(name):
    check(type(name) is str and name and len(name.encode('utf-8')) <= 4096, 'PATH')
    result = name.split('/')
    check(all(p not in ('', '.', '..') and '\\' not in p and '\0' not in p for p in result), 'PATH')
    return result


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_uid, s.st_gid, s.st_nlink,
            s.st_size, s.st_mtime_ns, s.st_ctime_ns]


def cleanup_owned(primary, resources):
    """Attempt every acquired close once; never replace an active primary."""
    errors=[]
    for fd, label in resources:
        if fd is None:continue
        try:os.close(fd)
        except BaseException as error:
            errors.append({'fd':fd,'owner':label,'error':repr(error),'status':'CLOSE_UNKNOWN_NO_RETRY'})
    if errors:
        owner=primary if primary is not None else Block('RESOURCE_CLOSE_UNKNOWN')
        owner.cleanupUnknown=getattr(owner,'cleanupUnknown',[])+errors
        if primary is None:raise owner


def close_once(fd, label):
    cleanup_owned(sys.exc_info()[1],[(fd,label)])


def physical(path):
    p = Path(path)
    check(p.is_absolute() and '..' not in p.parts, 'PHYSICAL_ABSOLUTE')
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for part in p.parts[1:]:
            nxt = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            old, fd = fd, nxt
            close_once(old,'physical previous ancestor')
        return fd
    except BaseException:
        close_once(fd,'physical current ancestor')
        raise


def read_at(root, name, cap=4*1024*1024):
    ps = parts(name)
    fd = os.dup(root)
    source = None
    try:
        for p in ps[:-1]:
            nxt = os.open(p, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            old, fd = fd, nxt
            close_once(old,'read_at previous directory')
        source = os.open(ps[-1], os.O_RDONLY | os.O_NOFOLLOW, dir_fd=fd)
        before = os.fstat(source)
        check(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and before.st_size <= cap, 'REGULAR_READ_LIMIT')
        chunks = []
        count = 0
        while True:
            data = os.read(source, min(65536, cap + 1 - count))
            if not data:
                break
            count += len(data)
            check(count <= cap, 'READ_OVERFLOW')
            chunks.append(data)
        check(count == before.st_size and identity(os.fstat(source)) == identity(before), 'READ_CHANGED')
        current = os.stat(ps[-1], dir_fd=fd, follow_symlinks=False)
        check(identity(current) == identity(before), 'READ_NAME_CHANGED')
        return b''.join(chunks)
    finally:
        cleanup_owned(sys.exc_info()[1],[(source,'read_at source'),(fd,'read_at directory')])


def read_absolute(path, cap=4*1024*1024):
    p = Path(path)
    fd = physical(p.parent)
    try:
        return read_at(fd, p.name, cap)
    finally:
        close_once(fd,'read_absolute parent')


class Store:
    """Supervisor-owned held directories, exclusive files; never deletes/retries."""
    def __init__(self, root, path, limit=LIMIT, file_limit=FILE_LIMIT):
        self.root = root
        self.path = Path(path)
        self.anchor = identity(os.fstat(root))[:2]
        self.dirs = {'': root}
        self.active = {}
        self.unknown = []
        self.faults = []
        self.written = 0
        self.progress = {}
        self.writeUnknown = []
        self.files = 0
        self.limit = limit
        self.file_limit = file_limit
        s = os.fstat(root)
        check(stat.S_ISDIR(s.st_mode) and s.st_uid == os.getuid() and stat.S_IMODE(s.st_mode) == 0o700, 'STORE_ROOT')

    def check(self):
        fd = physical(self.path)
        try:
            check(identity(os.fstat(fd))[:2] == self.anchor, 'STORE_ANCHOR')
        finally:
            close_once(fd,'Store.check physical anchor')

    def directory(self, ps):
        self.check()
        rel = ''
        parent = self.root
        for p in ps:
            parts(p)
            rel = rel + '/' + p if rel else p
            if rel not in self.dirs:
                os.mkdir(p, 0o700, dir_fd=parent)
                new = os.open(p, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent)
                self.dirs[rel] = new
            held = os.fstat(self.dirs[rel])
            current = os.stat(p, dir_fd=parent, follow_symlinks=False)
            check(stat.S_ISDIR(current.st_mode) and identity(current)[:2] == identity(held)[:2]
                  and held.st_uid == os.getuid() and stat.S_IMODE(held.st_mode) == 0o700, 'STORE_DIRECTORY')
            parent = self.dirs[rel]
        return parent

    def reserve(self, name):
        check(self.files < self.file_limit, 'FILE_COUNT')
        ps = parts(name)
        parent = self.directory(ps[:-1])
        fd = os.open(ps[-1], os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=parent)
        self.active[fd] = name
        self.progress[fd] = 0
        self.files += 1
        return fd

    def write(self, fd, data):
        # The complete already-read chunk is attempted before overflow is raised.
        # On write failure the file prefix and primary failure stay retained.
        view = memoryview(data)
        while view:
            try:n = os.write(fd, view)
            except BaseException as error:
                self.writeUnknown.append({'fd':fd,'file':self.active.get(fd),'knownSuccessfulBytes':self.progress[fd],'error':repr(error),'unknownWriteOutcome':True})
                raise
            check(0 < n <= len(view), 'SHORT_WRITE')
            self.written += n
            self.progress[fd] += n
            view = view[n:]
        check(self.written <= self.limit, 'EVIDENCE_OVERFLOW')

    def finish(self, fd):
        check(fd in self.active, 'FD_OWNERSHIP')
        first = None
        try:
            os.fsync(fd)
        except BaseException as error:
            first = error
        self.active.pop(fd)  # no close retry, even if close result is unknown
        try:
            os.close(fd)
        except BaseException as error:
            self.unknown.append({'fd': fd, 'error': repr(error)})
            if first is None:
                first = error
        if first is not None:
            raise first

    def put(self, name, data):
        fd = self.reserve(name)
        primary = None
        try:
            self.write(fd, data)
        except BaseException as error:
            primary = error
            self.faults.append({'file':name,'primaryWrite':repr(error)})
        try:
            self.finish(fd)
        except BaseException as error:
            self.faults.append({'file':name,'closeOrFsync':repr(error),'secondary':primary is not None})
            if primary is None:primary=error
        if primary is not None:raise primary
        check(self.read(name, len(data)) == data, 'WRITE_READBACK')

    def json(self, name, value):
        self.put(name, canon(value) + b'\n')

    def read(self, name, cap=4*1024*1024):
        self.check()
        return read_at(self.root, name, cap)

    def close(self):
        errors = []
        for fd in list(self.active):
            try:
                self.finish(fd)
            except BaseException as error:
                errors.append(repr(error))
        for name, fd in reversed(list(self.dirs.items())):
            self.dirs.pop(name)
            try:
                os.close(fd)
            except BaseException as error:
                self.unknown.append({'fd': fd, 'error': repr(error)})
                errors.append(repr(error))
        check(not errors and not self.unknown, 'CLOSE_UNKNOWN:' + repr(errors + self.unknown))


class RawSink:
    def __init__(self, store, name, cap):
        self.store, self.name, self.cap = store, name, cap
        self.fd = store.reserve(name)
        self.fdKey = self.fd
        self.count = 0
        self.observedFileBytes = None

    def append(self, data):
        before=self.store.progress[self.fd]
        try:self.store.write(self.fd, data)
        finally:self.count += self.store.progress[self.fd]-before
        check(self.count <= self.cap, 'OUTER_RAW_OVERFLOW')

    def close(self):
        fd, self.fd = self.fd, None
        if fd is not None:
            primary=None
            try:self.observedFileBytes=os.fstat(fd).st_size
            except BaseException as error:primary=error
            try:self.store.finish(fd)
            except BaseException as error:
                if primary is None:primary=error
                else:primary.cleanupUnknown=getattr(primary,'cleanupUnknown',[])+[{'fd':fd,'owner':'raw close/fsync','error':repr(error),'status':'CLOSE_OR_FSYNC_UNKNOWN'}]
            if primary is not None:raise primary


def oracle():
    raw = read_absolute(PREP / 'fixture-oracle.json')
    check(sha(raw) == ORACLE_SHA, 'ORACLE_SOURCE')
    o = strict(raw)
    check(len(o['rows']) == 13 and o['layerCounts'] == [3, 2, 2, 2, 4] and len(o['selectedVFS']) == 5, 'ORACLE_COUNTS')
    for row in o['rows']:
        body = base64.b64decode(row['bodyBase64'], validate=True)
        check(len(body) == row['bytes'] and sha(body) == row['sha256'], 'ORACLE_BODY')
    archive = base64.b64decode(o['zipBase64'], validate=True)
    check(len(archive) == o['zipBytes'] <= 65536 and sha(archive) == o['zipSHA256'], 'ORACLE_ZIP')
    check(sum(r['bytes'] for r in o['rows']) + len(archive) <= 131072, 'FIXTURE_PAYLOAD')
    return o


def adapt_node(original, archive_sha):
    check(re.fullmatch('[0-9a-f]{64}', archive_sha) is not None and archive_sha != OFFICIAL, 'ADAPT_DIGEST')
    atom = ("const ARCHIVE_SHA = '" + OFFICIAL + "';").encode('ascii')
    replacement = ("const ARCHIVE_SHA = '" + archive_sha + "';").encode('ascii')
    check(original.count(atom) == 1 and replacement not in original, 'ADAPT_OCCURRENCE')
    adapted = original.replace(atom, replacement)
    check(adapted.count(replacement) == 1 and adapted.replace(replacement, atom) == original, 'ADAPT_REVERSE')
    return adapted, {'occurrences': 1, 'beforeAtom': atom.decode(), 'afterAtom': replacement.decode(),
                     'beforeSHA256': sha(original), 'afterSHA256': sha(adapted), 'reverseByteIdentical': True}


def expected(o, base):
    """Expected paths derive only from fixed literal table/config, never actual."""
    layers, selected = [], {}
    for i, mod in enumerate(o['orderedMods']):
        root = str(base / 'synthetic-public.zip') if i == 0 else str(base / 'fixture-repo' / ROOTS[i-1])
        rows = []
        for literal in o['rows']:
            if literal['mod'] != mod:
                continue
            vfs = literal['vfs']
            display = root + ('::' if i == 0 else '/') + vfs
            row = {'vfs': vfs, 'sourceDisplay': display, 'bytes': literal['bytes'], 'sha256': literal['sha256']}
            rows.append(row)
            previous = selected.get(vfs)
            shadows = [] if previous is None else previous['shadowed'] + [{'mod': previous['mod'], 'sourceDisplay': previous['sourceDisplay'], 'sha256': previous['sha256']}]
            selected[vfs] = {'vfs': vfs, 'mod': mod, 'sha256': literal['sha256'], 'bytes': literal['bytes'],
                             'shadowed': shadows, 'sourceDisplay': display, 'archiveEntry': vfs if i == 0 else None,
                             'defaultLoaderFolder': ('globalscripts/' if vfs.startswith('globalscripts/') else 'simulation/helpers/' if vfs.startswith('simulation/helpers/') else None),
                             'realm': 'METADATA' if vfs == 'mod.json' else 'SIMULATION_CANDIDATE'}
        layers.append({'name': mod, 'rootKind': 'archive' if i == 0 else 'loose', 'rootDisplay': root, 'entries': rows})
    rows = []
    for i, name in enumerate(o['selectedVFS']):
        row = dict(selected[name])
        row.pop('sourceDisplay')
        rows.append({'index': i, **row})
    return layers, rows


def snapshot_tree(root, cap=LIMIT):
    """Bounded physical inventory; includes directories and exact inode sentinel."""
    result, total, count = {'': {'kind':'directory','identity':identity(os.fstat(root))}}, 0, 0
    def walk(fd, prefix):
        nonlocal total, count
        before = identity(os.fstat(fd))
        names = []
        with os.scandir(fd) as entries:
            for entry in entries:
                count += 1
                check(count <= FILE_LIMIT, 'TREE_COUNT')
                names.append(entry.name)
        for name in sorted(names, key=lambda n: n.encode('utf-8')):
            parts(name)
            path = prefix + '/' + name if prefix else name
            s = os.stat(name, dir_fd=fd, follow_symlinks=False)
            row = {'identity': identity(s)}
            if stat.S_ISDIR(s.st_mode):
                child = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                try:
                    check(identity(os.fstat(child))[:2] == identity(s)[:2], 'TREE_CHANGED')
                    row['kind'] = 'directory'
                    walk(child, path)
                finally:
                    close_once(child,'snapshot_tree child directory')
            else:
                check(stat.S_ISREG(s.st_mode) and s.st_nlink == 1 and s.st_uid == os.getuid(), 'TREE_TYPE')
                total += s.st_size
                check(total <= cap, 'TREE_BYTES')
                row.update(kind='file', sha256=sha(read_at(fd, name, min(cap, 16*1024*1024))))
            result[path] = row
        check(identity(os.fstat(fd)) == before, 'TREE_CHANGED')
    walk(root, '')
    return result


def verify_runtime(rows):
    """Literal chain rows supplied by external freeze, never generic realpath."""
    check(type(rows) is list and rows, 'RUNTIME_ROWS_MISSING')
    paths = set()
    for row in rows:
        p = Path(row['path'])
        check(str(p) not in paths, 'RUNTIME_DUPLICATE')
        paths.add(str(p))
        parent = physical(p.parent)
        try:
            before = os.stat(p.name, dir_fd=parent, follow_symlinks=False)
            check(identity(before) == row['identity'], 'RUNTIME_IDENTITY')
            if row['kind'] == 'symlink':
                check(stat.S_ISLNK(before.st_mode) and os.readlink(p.name, dir_fd=parent) == row['rawlink'], 'RUNTIME_LINK')
            else:
                check(row['kind'] == 'file' and sha(read_at(parent, p.name, 256*1024*1024)) == row['sha256'], 'RUNTIME_HASH')
            check(identity(os.stat(p.name, dir_fd=parent, follow_symlinks=False)) == identity(before), 'RUNTIME_CHANGED')
        finally:
            close_once(parent,'verify_runtime physical parent')
    check(NODE in paths and PYTHON in paths and
          '/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3' in paths and
          '/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9' in paths, 'RUNTIME_CHAIN_INCOMPLETE')
    for row in rows:
        if row['kind']=='symlink':
            target=os.path.normpath(os.path.join(str(Path(row['path']).parent),row['rawlink']))
            check(target in paths,'RUNTIME_LINK_TARGET_NOT_FROZEN')


def approved_bindings(frozen):
    """Join reviewed manifests to the complete deterministic current input set.

    Historical manifest files are opaque context members, not recursively
    interpreted as if their superseded source paths were still current.
    """
    source_keys={'schema','purpose','createdUTC','status','scope','currentPythonSHA256','currentPythonTestSHA256','currentNodeSHA256','currentNodeTestSHA256','rootPinnedNodeSHAReadback','priorRootReadbacks','authorTests','coverage','historicalApplicability','bindings','sourceApproval','bridgeApproval','officialCaptureApproval','native'}
    harness_keys={'schema','createdUTC','purpose','scope','bindings','retainedHelperLinks','readiness','sourceApproval','bridgeApproval','officialCaptureApproval','native'}
    joined={}
    def normalized(name):
        check(type(name) is str and str(Path(name))==name and '..' not in Path(name).parts,'APPROVED_PATH')
        return str(Path(name) if Path(name).is_absolute() else REPO/Path(name))
    def add(row):
        path=normalized(row['path'])
        check(type(row['bytes']) is int and 0<=row['bytes']<=4*1024*1024 and type(row['sha256']) is str and re.fullmatch('[0-9a-f]{64}',row['sha256']) is not None,'APPROVED_BINDING_TYPE')
        value={'path':path,'bytes':row['bytes'],'sha256':row['sha256']}
        check(path not in joined or same(joined[path],value),'APPROVED_CONFLICT')
        joined[path]=value
        return path
    for role,path,raw in frozen:
        doc=strict(raw)
        check(type(doc) is dict and set(doc)==(source_keys if role=='source' else harness_keys) and same(doc['schema'],1),'APPROVED_MANIFEST_SCHEMA')
        for flag in ['sourceApproval','bridgeApproval','officialCaptureApproval','native']:
            check(doc[flag] is False,'APPROVED_MANIFEST_FLAGS')
        check(type(doc['bindings']) is list and 1<=len(doc['bindings'])<=512,'APPROVED_BINDING_COUNT')
        members=set()
        for row in doc['bindings']:
            keys={'path','bytes','sha256','snapshot','context' if role=='source' else 'applicability'}
            check(type(row) is dict and set(row)==keys,'APPROVED_BINDING_SCHEMA')
            normalized(row['snapshot'])
            label=row['context' if role=='source' else 'applicability']
            check(type(label) is str and 0<len(label)<=1024,'APPROVED_CONTEXT_LABEL')
            current=add(row)
            check(current not in members,'APPROVED_DUPLICATE')
            members.add(current)
        required=[REPO/'tools/epoch-rts'/name for name in SOURCE_FILES.values()] if role=='source' else [Path(__file__).absolute(),FIX_PREP/'CONTRACT-v5.md',FIX_PREP/'helpertests-v5.py',PREP/'fixture-oracle.json']
        check(all(str(p) in members for p in required),'APPROVED_REQUIRED_INPUT_MISSING')
        add({'path':path,'bytes':len(raw),'sha256':sha(raw)})
    check(len(joined)<=512 and sum(row['bytes'] for row in joined.values())<=128*1024*1024,'APPROVED_BINDINGS_LIMIT')
    return sorted(joined.values(),key=lambda row:row['path'].encode('utf-8'))


def gate(capsule):
    """Consistency gate only. External root authorization remains mandatory."""
    check(type(capsule) is dict and capsule.get('scope') == SCOPE, 'EXTERNAL_GATES_MISSING')
    check(capsule.get('runParent') == str(PREP) and capsule.get('runLeaf') == RUN_LEAF, 'FIXED_NAMESPACE')
    check(capsule.get('retry') == 0 and capsule.get('seed') is False, 'FIXED_CASE_POLICY')
    check(capsule.get('sourceSHAs') == SOURCE_SHAS and capsule.get('oracleSHA256') == ORACLE_SHA, 'CURRENT_SOURCE_POLICY')
    check(capsule.get('nodeVersion') == 'v26.0.0' and capsule.get('pythonVersion') == '3.9.6' and capsule.get('acornVersion') == '8.16.0', 'FIXED_RUNTIME_POLICY')
    frozen=[]
    for role in ('source', 'harness'):
        freeze = capsule[role + 'FreezeSHA256']
        check(re.fullmatch('[0-9a-f]{64}', freeze) is not None, 'FREEZE_MISSING')
        raw=read_absolute(capsule[role+'FreezeManifest'])
        check(sha(raw)==freeze,'FREEZE_MANIFEST_CHANGED')
        frozen.append((role,capsule[role+'FreezeManifest'],raw))
        reviews = capsule[role + 'Reviews']
        check(set(reviews) == {'CODE', 'Python', 'JS'}, 'FULL_REVIEWS_MISSING')
        for name, row in reviews.items():
            raw = read_absolute(row['path'])
            check(sha(raw) == row['sha256'], 'REVIEW_CHANGED:' + name)
            report = strict(raw)
            manifests = [report.get('inputManifestSHA256'), report.get('reviewedManifest',{}).get('sha256'), report.get('freeze',{}).get('sha256')]
            manifests = [value for value in manifests if value is not None]
            check(report['verdict'] == 'APPROVE_SOURCE_ONLY' and manifests and all(value == freeze for value in manifests), 'REVIEW_NOT_APPROVED:' + name)
    reviewed=approved_bindings(frozen)
    check(same(capsule['sourceBindings'],reviewed),'APPROVED_CURRENT_BINDINGS_MISMATCH')
    for name in ('rootReadback', 'independentFreshGuard'):
        row = capsule[name]
        raw = read_absolute(row['path'])
        check(sha(raw) == row['sha256'], 'GATE_CHANGED')
        report = strict(raw)
        check(report['sourceFreezeSHA256'] == capsule['sourceFreezeSHA256'] and report['harnessFreezeSHA256'] == capsule['harnessFreezeSHA256'] and report['capsuleId'] == capsule['id'], 'GATE_FREEZE')
        check(report['status'] == 'MATCH' and report['runParent'] == str(PREP) and report['runLeaf'] == RUN_LEAF, 'GATE_SCOPE')
        check(0 <= time.time() - report['checkedUnixSeconds'] <= 60 and report['expiresUnixSeconds'] >= time.time() + 270, 'GATE_EXPIRED')
        check(270 <= report['expiresUnixSeconds']-report['checkedUnixSeconds'] <= 600,'GATE_TTL')
        check(report['sourceBindings'] == capsule['sourceBindings'], 'GATE_BINDINGS')
    check(capsule['rootReadback']['path'] != capsule['independentFreshGuard']['path'], 'INDEPENDENT_GUARD_MISSING')
    check(type(capsule['sourceBindings']) is list and 1 <= len(capsule['sourceBindings']) <= 512,'SOURCE_BINDINGS_LIMIT')
    check(len({row['path'] for row in capsule['sourceBindings']})==len(capsule['sourceBindings']),'SOURCE_BINDINGS_DUPLICATE')
    check(all(type(row['bytes']) is int and 0 <= row['bytes'] <= 4*1024*1024 for row in capsule['sourceBindings']) and sum(row['bytes'] for row in capsule['sourceBindings'])<=128*1024*1024,'SOURCE_PREFLIGHT_BYTES')
    for row in capsule['sourceBindings']:
        check(sha(read_absolute(row['path'], row['bytes'])) == row['sha256'], 'FROZEN_INPUT_CHANGED')
    bound = {r['path']: r['sha256'] for r in capsule['sourceBindings']}
    check(bound.get(str(Path(__file__).absolute())) == sha(read_absolute(Path(__file__).absolute())), 'HARNESS_NOT_BOUND')
    for role, name in SOURCE_FILES.items():
        check(bound.get(str(REPO/'tools/epoch-rts'/name)) == SOURCE_SHAS[role], 'SOURCE_NOT_BOUND')
    check(bound.get(str(PREP/'fixture-oracle.json')) == ORACLE_SHA, 'ORACLE_NOT_BOUND')
    verify_runtime(capsule['runtimeRows'])


WRAPPER = b'''# Purpose: frozen CONFIG_ADAPTED test wrapper only; no runtime/crypto hooks.
import importlib.util,json,sys,os
from pathlib import Path
from importlib.machinery import SourceFileLoader
sys.dont_write_bytecode=True
here=Path(__file__).absolute().parent
loader=SourceFileLoader('preservation_snapshot',str(here/'production-python.snapshot'))
spec=importlib.util.spec_from_loader(loader.name,loader)
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;loader.exec_module(m)
c=json.loads((here/'private-test-config.json').read_bytes())
allowed={'REPO','ARCHIVE_PATH','ARCHIVE_SHA','OUTPUT_PARENT','NODE_PATH','NODE_SOURCE_EXPECTED','SCHEMA_PATH'}
if set(c)!=allowed or len(sys.argv)!=1:raise RuntimeError('CONFIG_KEYS_OR_ARGC')
for key in allowed:
 if not hasattr(m,key):raise RuntimeError('MISSING_PRIVATE_GLOBAL')
 if key in ('ARCHIVE_SHA','NODE_SOURCE_EXPECTED'):setattr(m,key,c[key])
 else:
  p=Path(c[key])
  if not p.is_absolute() or '..' in p.parts or not str(p).startswith(str(here)+'/'):raise RuntimeError('CONFIG_ESCAPE')
  setattr(m,key,p)
if not callable(m._run):raise RuntimeError('MISSING_PRIVATE_API')
sys.exit(m._run(sys.stdin.buffer,sys.stdout.buffer))
'''


def setup(store, o):
    base = store.path
    store.put('literal-oracle.json', read_absolute(PREP/'fixture-oracle.json'))
    originals = {}
    provenance = []
    for role, name in SOURCE_FILES.items():
        raw = read_absolute(REPO/'tools/epoch-rts'/name)
        check(sha(raw) == SOURCE_SHAS[role], 'SOURCE_CURRENT')
        originals[role] = raw
        store.put('production-' + role + '.snapshot', raw)
        parent=physical(REPO/'tools/epoch-rts')
        try:
            provenance.append({'role':role,'path':str(REPO/'tools/epoch-rts'/name),'identity':identity(os.stat(name,dir_fd=parent,follow_symlinks=False)),'bytes':len(raw),'sha256':sha(raw)})
        finally:
            close_once(parent,'setup source provenance parent')
    store.json('production-provenance.json',provenance)
    store.put('synthetic-public.zip', base64.b64decode(o['zipBase64'], validate=True))
    for row in o['rows']:
        if row['mod'] == 'public':
            continue
        i = o['orderedMods'].index(row['mod']) - 1
        store.put('fixture-repo/' + ROOTS[i] + '/' + row['vfs'], base64.b64decode(row['bodyBase64'], validate=True))
    store.directory(parts('fixture-repo/work/t17-save-five-mod-inventory-repair-preparation'))
    adapted, proof = adapt_node(originals['node'], o['zipSHA256'])
    store.put(SOURCE_FILES['node'], adapted)
    store.put(SOURCE_FILES['schema'], originals['schema'])
    store.put(SOURCE_FILES['python'], WRAPPER)
    config = {'REPO': str(base/'fixture-repo'), 'ARCHIVE_PATH': str(base/'synthetic-public.zip'), 'ARCHIVE_SHA': o['zipSHA256'],
              'OUTPUT_PARENT': str(base/'fixture-repo/work/t17-save-five-mod-inventory-repair-preparation/captures'),
              'NODE_PATH': str(base/SOURCE_FILES['node']), 'NODE_SOURCE_EXPECTED': sha(adapted), 'SCHEMA_PATH': str(base/SOURCE_FILES['schema'])}
    store.json('private-test-config.json', config)
    store.json('adaptation.json', {'scope': SCOPE, 'pythonSnapshotSHA256': sha(originals['python']), 'schemaSHA256': sha(originals['schema']), 'node': proof, 'config': config, 'wrapperSHA256': sha(WRAPPER), 'seed': False})
    store.put('node-forward.diff', ''.join(difflib.unified_diff(originals['node'].decode().splitlines(True), adapted.decode().splitlines(True), fromfile='production', tofile='adapted')).encode())
    store.put('node-reverse.diff', ''.join(difflib.unified_diff(adapted.decode().splitlines(True), originals['node'].decode().splitlines(True), fromfile='adapted', tofile='production')).encode())
    return config


def check_first_launch(setup_end, overall_end, invocation=None, case_end=None):
    now=time.monotonic()
    if setup_end is not None:check(now<setup_end,'SETUP_TIMEOUT')
    check(now<overall_end,'OVERALL_TIMEOUT')
    if case_end is not None:check(now<case_end,'ACTIVE_TIMEOUT_PRELAUNCH')
    if invocation is not None:invocation['attempted']=True


def check_final_deadline(overall_end):
    if time.monotonic()>=overall_end:
        try:
            sys.stderr.write('SUPERVISOR_OVERALL_TIMEOUT_AFTER_CLOSE\n');sys.stderr.flush()
        except BaseException:pass  # Failure remains nonzero even if stderr is unavailable.
        raise Block('OVERALL_TIMEOUT_AFTER_CLOSE')


def record_spawn(invocation, pid):
    # Caller owns this state, so late logging/readback exceptions cannot erase it.
    invocation.update(attempted=True,spawned=True,pid=pid)


def classify_invocation_failures(result):
    for case,state in result['invocations'].items():
        if state['attempted'] and result[case]!='PASS_BOUNDED_SOURCE_MODEL':
            result[case]='FAIL_OR_UNKNOWN'


def finish_setup_evidence(store, setup_end, overall_end):
    store.json('setup-tree.json',snapshot_tree(store.root))
    check_first_launch(setup_end,overall_end)


def validate_collision(value):
    check(same(value,{'status':'UNKNOWN_TOOL_CAPTURE','reasonCode':'PYTHON_OUTPUT_EXISTS','sourceClosure':False,'native':False,'pythonDiskReadback':'NOT_INDEPENDENTLY_VERIFIED_BY_NODE'}),'COLLISION_DECLARATION')


def retire_stream(selector, key, ledger, retired):
    """No second unregister/close after uncertainty; raw owners still finalize."""
    token=id(key.fileobj)
    if token in retired:return False
    retired.add(token)
    okay=True
    try:descriptor=key.fileobj.fileno()
    except BaseException:descriptor=None
    for owner,operation in [('outer stream unregister',lambda:selector.unregister(key.fileobj)),('outer stream close',key.fileobj.close)]:
        try:operation()
        except KeyError as error:
            # A pipe may have been acquired before selector registration failed.
            if owner=='outer stream unregister':continue
            okay=False
            row={'owner':owner,'fd':descriptor,'stream':key.data,'error':repr(error),'status':'RESOURCE_CLOSE_UNKNOWN_NO_RETRY'}
            ledger['cleanupUnknown'].append(row);ledger['secondary'].append(row)
        except BaseException as error:
            okay=False
            row={'owner':owner,'fd':descriptor,'stream':key.data,'error':repr(error),'status':'RESOURCE_CLOSE_UNKNOWN_NO_RETRY'}
            ledger['cleanupUnknown'].append(row);ledger['secondary'].append(row)
    return okay


def observe_node(store, case, active_end, overall_end, cleanup, invocation, setup_end=None):
    """Own/reap direct Node only. No descendant wait/pipe or process-group kill."""
    sinks = {}
    env = {'PATH': '/usr/bin:/bin', 'LANG': 'C', 'LC_ALL': 'C', 'PYTHONDONTWRITEBYTECODE': '1'}
    argv = [NODE, '--expose-internals', '--max-old-space-size=512', str(store.path/SOURCE_FILES['node']), OUTPUT_LEAF]
    ledger = {'argv': argv, 'cwd': str(store.path), 'environment': env, 'scope': SCOPE, 'seed': False,
              'events': [], 'primary': None, 'secondary': [], 'cleanupUnknown': [], 'abandonedStreams': [], 'nodeReaped': False,
              'pythonWait': 'NOT_INDEPENDENTLY_OBSERVED', 'directionalPipeEquality': 'NOT_INDEPENDENTLY_VERIFIED'}
    proc, sel = None, selectors.DefaultSelector()
    active_end = min(active_end, overall_end)  # caller's original cutoff, never restarted
    stop_start = None
    killed = False
    retired=set()
    streams={}
    def event(kind, **extra):
        ledger['events'].append({'kind': kind, 'monotonic': time.monotonic(), **extra})
    def stop(code):
        nonlocal stop_start
        if ledger['primary'] is None:
            ledger['primary'] = code
            stop_start = time.monotonic()
            if cleanup['end'] is None:
                cleanup['end'] = min(stop_start+90, overall_end)
            event('STOP', reason=code)
            if proc is not None and proc.poll() is None:
                try:
                    proc.terminate()
                    event('OWNED_NODE_SIGTERM', pid=proc.pid)
                except BaseException as error:
                    ledger['secondary'].append(repr(error))
    try:
        for name in ('stdout','stderr'):
            sinks[name] = RawSink(store, case + '.' + name + '.raw', 16*1024*1024)
        check_first_launch(setup_end,overall_end,invocation,case_end=active_end)
        proc = subprocess.Popen(argv, cwd=str(store.path), env=env, stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, close_fds=True)
        record_spawn(invocation,proc.pid)
        streams={'stdout':proc.stdout,'stderr':proc.stderr}
        event('NODE_SPAWNED', pid=proc.pid)
        for name in sinks:
            stream = getattr(proc, name)
            os.set_blocking(stream.fileno(), False)
            sel.register(stream, selectors.EVENT_READ, name)
        while True:
            now = time.monotonic()
            if ledger['primary'] is None and now >= active_end:
                stop('ACTIVE_TIMEOUT')
            if stop_start is not None:
                if not killed and now >= stop_start+1 and proc.poll() is None:
                    killed = True
                    try:
                        proc.kill()
                        event('OWNED_NODE_SIGKILL', pid=proc.pid)
                    except BaseException as error:
                        ledger['secondary'].append(repr(error))
                if now >= cleanup['end']:
                    ledger['secondary'].append('CLEANUP_REAP_OR_DRAIN_UNKNOWN')
                    break
            for key, _ in sel.select(0.05):
                try:
                    chunk = os.read(key.fileobj.fileno(), 65536)
                except BlockingIOError:
                    continue
                if not chunk:
                    if retire_stream(sel,key,ledger,retired):event('OUTER_EOF', stream=key.data)
                    else:stop('OUTER_STREAM_CLOSE_UNKNOWN')
                else:
                    try:
                        sinks[key.data].append(chunk)
                    except BaseException as error:
                        stop('RAW_OR_WRITE:' + repr(error))
                        # Preserve the complete already-read chunk; stop reading
                        # future bytes after a cap/write failure, never call it drain.
                        ledger['abandonedStreams'].append(key.data)
                        retire_stream(sel,key,ledger,retired)
            code = proc.poll()
            if code is not None and not ledger['nodeReaped']:
                # Popen.poll performs waitpid on this directly owned child.
                ledger.update(nodeReaped=True, returncode=code, signal=-code if code<0 else None)
                event('DIRECT_NODE_WAITPID_OBSERVED', returncode=code)
            if code is not None and not sel.get_map():
                break
        check(ledger['nodeReaped'] and not sel.get_map(), 'NODE_REAP_DRAIN_UNKNOWN')
    except BaseException as error:
        stop('SUPERVISOR:' + repr(error))
    finally:
        # Exceptions after spawn still own cleanup. Use the same one90s budget,
        # oneTERM/oneKILL and direct-child wait, never kill an unowned PID.
        try:
            if proc is not None and (proc.poll() is None or sel.get_map()):
                stop('CLEANUP_AFTER_EXCEPTION')
                while time.monotonic() < cleanup['end']:
                    now = time.monotonic()
                    if not killed and now >= stop_start+1 and proc.poll() is None:
                        killed = True
                        try:
                            proc.kill();event('OWNED_NODE_SIGKILL',pid=proc.pid)
                        except BaseException as error:
                            ledger['secondary'].append(repr(error))
                    for key in list(sel.get_map().values()):
                        try:
                            chunk=os.read(key.fileobj.fileno(),65536)
                            if chunk:
                                sinks[key.data].append(chunk)
                            else:
                                if retire_stream(sel,key,ledger,retired):event('OUTER_EOF',stream=key.data)
                        except BlockingIOError:
                            pass
                        except BaseException as error:
                            ledger['secondary'].append('CLEANUP_RAW:'+repr(error))
                            ledger['abandonedStreams'].append(key.data)
                            retire_stream(sel,key,ledger,retired)
                    code=proc.poll()
                    if code is not None:
                        if not ledger['nodeReaped']:
                            ledger.update(nodeReaped=True,returncode=code,signal=-code if code<0 else None)
                            event('DIRECT_NODE_WAITPID_OBSERVED',returncode=code)
                        if not sel.get_map():break
                    time.sleep(0.05)
                if proc.poll() is None or sel.get_map():
                    ledger['secondary'].append('FINAL_REAP_OR_DRAIN_UNKNOWN')
        except BaseException as error:
            if ledger['primary'] is None:ledger['primary']='PROCESS_CLEANUP:'+repr(error)
            ledger['secondary'].append({'owner':'direct Node cleanup','error':repr(error),'status':'RESOURCE_CLEANUP_UNKNOWN'})
        finally:
            for name,stream in streams.items():
                retire_stream(sel,SimpleNamespace(fileobj=stream,data=name),ledger,retired)
            try:sel.close()
            except BaseException as error:
                row={'owner':'outer selector','error':repr(error),'status':'RESOURCE_CLOSE_UNKNOWN_NO_RETRY'}
                ledger['cleanupUnknown'].append(row);ledger['secondary'].append(row)
            for sink in sinks.values():
                try:
                    sink.close()
                except BaseException as error:
                    ledger['secondary'].append('RAW_CLOSE:' + repr(error))
            ledger['retainedRawBytes'] = {name: sink.observedFileBytes for name, sink in sinks.items()}
            ledger['rawWriteAccounting'] = {name:{'knownSuccessfulWriteBytes':sink.count,'observedFileBytes':sink.observedFileBytes,'unknownWriteOutcomes':[row for row in store.writeUnknown if row['fd']==sink.fdKey]} for name,sink in sinks.items()}
            ledger['outerDrainComplete'] = not ledger['abandonedStreams'] and len([e for e in ledger['events'] if e['kind']=='OUTER_EOF']) == 2
            try:store.json(case + '.lifecycle.json', ledger)
            except BaseException as error:
                error.cleanupUnknown=getattr(error,'cleanupUnknown',[])+ledger['cleanupUnknown']
                raise
    if not (ledger['primary'] is None and not ledger['secondary'] and ledger['nodeReaped'] and ledger['outerDrainComplete']):
        error=Block('NODE_LIFECYCLE_UNKNOWN')
        error.cleanupUnknown=ledger['cleanupUnknown']
        raise error
    try:return ledger, store.read(case+'.stdout.raw', 16*1024*1024), store.read(case+'.stderr.raw', 16*1024*1024)
    except BaseException as error:
        error.cleanupUnknown=getattr(error,'cleanupUnknown',[])+ledger['cleanupUnknown']
        raise


def verify_capture(store, o, config, node, outer):
    root = physical(Path(config['OUTPUT_PARENT'])/OUTPUT_LEAF)
    try:
        tree = snapshot_tree(root)
        files = {name for name, row in tree.items() if row['kind']=='file'}
        bodies = {(r['mod'], r['vfs']): base64.b64decode(r['bodyBase64']) for r in o['rows']}
        layers, selected = expected(o, store.path)
        expected_bodies = {'layer-sources/'+mod+'/'+vfs: data for (mod, vfs), data in bodies.items()}
        expected_bodies.update({'layer-metadata/'+mod+'/mod.json': bodies[(mod, 'mod.json')] for mod in o['orderedMods']})
        expected_bodies.update({'effective/'+row['vfs']: bodies[(row['mod'], row['vfs'])] for row in selected})
        artifacts = set(expected_bodies) | {'inventory.json','layer-inputs.json','writer-sites.json','capture-inputs.json','archive-auth.json'}
        allfiles = artifacts | {'manifest.json','completed.json','protocol-input.ndjson','protocol-output.ndjson','diagnostics.ndjson'}
        check(files == allfiles, 'COMPLETE_FILE_BIJECTION')
        for name, data in expected_bodies.items():
            check(read_at(root, name) == data, 'LITERAL_BODY:' + name)
        documents = {name: strict(read_at(root, name)) for name in artifacts if name.endswith('.json') and name not in expected_bodies}
        manifest = strict(read_at(root, 'manifest.json'))
        completed_raw = read_at(root, 'completed.json')
        completed = strict(completed_raw)
        check(set(manifest)=={'schema','status','captureId','artifactHashes','excludedFromWholeFileHashes','rawSeal','sourceClosure','native'} and same(manifest['schema'],1) and manifest['status']=='CAPTURE_COMPLETE_CANDIDATE_ONLY','MANIFEST_SCHEMA')
        check(set(completed)=={'v','kind','captureId','status','artifactHashes','sourceClosure','native'} and same(completed['v'],1) and completed['kind']=='COMPLETED','COMPLETED_SCHEMA')
        check(set(manifest['artifactHashes']) == artifacts, 'MANIFEST_BIJECTION')
        for name, digest in manifest['artifactHashes'].items():
            check(tree[name]['sha256'] == digest, 'MANIFEST_DIGEST')
        check(manifest['excludedFromWholeFileHashes'] == ['protocol-input.ndjson','protocol-output.ndjson','diagnostics.ndjson','manifest.json','completed.json','fault.json'] and manifest['rawSeal']=='NOT_CLAIMED', 'RAW_SEAL_BOUNDARY')
        for doc in [manifest, completed] + list(documents.values()):
            # archive-auth is a held-FD fact document without closure flags.
            if doc is not documents['archive-auth.json']:
                check(doc['sourceClosure'] is False and doc['native'] is False, 'CLOSURE')
        declared = strict(outer)
        check(declared.pop('pythonDiskReadback') == 'DECLARED_BY_PYTHON_NOT_INDEPENDENT_NODE_FS_PROOF' and same(declared,completed), 'NODE_DISK_DECLARATION')
        check(node['returncode']==0 and node['signal'] is None and completed['status']=='CAPTURE_COMPLETE_CANDIDATE_ONLY', 'SUCCESS_EXIT_STATUS')
        check(set(completed['artifactHashes']) == {'inventory.json','layer-inputs.json','writer-sites.json','manifest.json'}, 'COMPLETED_HASH_SET')
        for name, digest in completed['artifactHashes'].items():
            check(tree[name]['sha256']==digest, 'COMPLETED_HASH')
        inputs = frames(read_at(root, 'protocol-input.ndjson', 16*1024*1024))
        outputs = frames(read_at(root, 'protocol-output.ndjson', 16*1024*1024))
        check([f['kind'] for f in inputs]==['BEGIN','FINISH'] and [f['kind'] for f in outputs]==['SOURCE']*5+['CAPTURED','COMPLETED'], 'RAW_ORDER')
        check(same(inputs[0],{'v':1,'kind':'BEGIN','outputLeaf':OUTPUT_LEAF}), 'BEGIN')
        check(same(outputs[-1],completed) and read_at(root, 'protocol-output.ndjson').endswith(completed_raw), 'RAW_COMPLETED_EXACT')
        check(read_at(root, 'diagnostics.ndjson')==b'', 'DIAGNOSTICS_EXPECTED_EMPTY')
        capture=outputs[-2]
        check(set(capture)=={'v','kind','captureId','sourceCount','selectedDigest','layers','selected','archive','unsupportedRuntimeRules'} and same(capture['v'],1),'CAPTURED_SCHEMA')
        archive_facts={'expectedSHA':o['zipSHA256'],'actualSHA':o['zipSHA256'],'size':o['zipBytes'],'chunkBytes':4194304,'chunkCount':1,'authorityKind':'VERIFIED_HELD_FD_BYTES'}
        check(same(capture['archive'],archive_facts),'CAPTURED_ARCHIVE_LITERAL')
        check(same(capture['layers'],layers) and same(capture['selected'],selected) and same(capture['sourceCount'],5) and capture['unsupportedRuntimeRules']==UNSUPPORTED, 'LITERAL_METADATA')
        check(same(documents['layer-inputs.json'],{'layers':layers,'sourceClosure':False,'native':False}), 'LAYERS_DOCUMENT')
        check(same(documents['capture-inputs.json']['captured'],capture), 'CAPTURE_DOCUMENT')
        input_doc=documents['capture-inputs.json']
        check(set(input_doc)=={'captured','runtime','nodeSource','sourceClosure','native'} and input_doc['nodeSource']=={'path':config['NODE_PATH'],'expectedSHA':config['NODE_SOURCE_EXPECTED'],'actualSHA':config['NODE_SOURCE_EXPECTED']},'CAPTURE_SOURCE_DOCUMENT')
        check(input_doc['runtime']['pythonExecutable']==PYTHON and input_doc['runtime']['pythonVersion'].startswith('3.9.6') and input_doc['runtime']['authority']=='OBSERVED_RUNTIME_DEPENDENCIES_NOT_EXECUTION_ATTESTATION','RUNTIME_DECLARATION')
        digest=sha('\n'.join(r['vfs']+'\0'+r['mod']+'\0'+r['sha256']+'\0'+str(r['bytes']) for r in selected).encode())
        capture_id=sha(canon({'version':1,'archiveExpectedSHA':o['zipSHA256'],'selectedDigest':digest}))
        check(capture['selectedDigest']==digest and capture['captureId']==capture_id and completed['captureId']==capture_id and manifest['captureId']==capture_id, 'ORACLE_CAPTURE_ID')
        for frame, row in zip(outputs[:5], selected):
            data=bodies[(row['mod'],row['vfs'])]
            check(same(frame,{'v':1,'kind':'SOURCE','index':row['index'],'vfs':row['vfs'],'mod':row['mod'],'sha256':row['sha256'],'bytes':len(data),'bodyBase64':base64.b64encode(data).decode()}), 'SOURCE_RAW_LITERAL')
        finish=inputs[1]
        schema=strict(store.read(SOURCE_FILES['schema']))
        check(sha(store.read(SOURCE_FILES['schema']))==SOURCE_SHAS['schema'],'SCHEMA_IDENTITY')
        validate_schema(finish,schema)
        check(finish['kind']=='FINISH' and finish['v']==1 and finish['captureId']==capture_id and finish['tool']['nodeVersion']=='v26.0.0' and finish['tool']['acornVersion']=='8.16.0' and finish['tool']['nodeSourceSHA256']==sha(store.read(SOURCE_FILES['node'])), 'FINISH_TOOL')
        check(len(finish['analyses'])==5, 'ANALYSIS_COUNT')
        inventory=documents['inventory.json']
        check(set(inventory)=={'schema','status','tool','archive','orderedMods','unsupportedRuntimeRules','entries','counts','sourceClosure','native'} and inventory['schema']==1 and inventory['status']=='OPEN_CANDIDATE_SOURCE_INVENTORY_NOT_RUNTIME_OR_WRITER_CLOSURE' and inventory['tool']==finish['tool'] and inventory['archive']==archive_facts and inventory['unsupportedRuntimeRules']==UNSUPPORTED,'INVENTORY_SCHEMA')
        check(inventory['orderedMods']==o['orderedMods'] and same(inventory['counts'],{'effective':5,'scripts':4,'parseErrors':0}), 'INVENTORY_COUNTS')
        check(len(inventory['entries'])==5, 'INVENTORY_ENTRY_COUNT')
        for entry, row, analysis in zip(inventory['entries'],selected,finish['analyses']):
            check(same(analysis['index'],row['index']) and analysis['sha256']==row['sha256'] and same(entry,{**row,'analysis':analysis['analysis']}), 'INVENTORY_CORRELATION')
            check(analysis['analysis'] is None if row['vfs']=='mod.json' else analysis['analysis']['parseStatus']=='PARSED', 'ANALYSIS_VARIANT')
        writer={'vfs':'globalscripts/ArchiveOnly.js','mod':'public','callee':'Engine.RegisterGlobal','args':['"SyntheticPreservationArchive"','{}'],'line':1,'context':'(file)','kind':'RegisterGlobal','literalName':'SyntheticPreservationArchive','nameArgumentIndex':0,'target':'Engine'}
        check(same(documents['writer-sites.json'],{'status':'UNRESOLVED_REQUIRES_POSITIVE_PER_CALLER_SEMANTICS','sites':[writer],'sourceClosure':False,'native':False}),'WRITER_LITERAL_CONTROL')
        archive=documents['archive-auth.json']
        check(set(archive)==set(archive_facts)|{'chunkSHA256','fdMetadata','status'} and archive['status']=='VERIFIED_HELD_FD_BYTES' and all(archive[k]==v for k,v in archive_facts.items()),'ARCHIVE_SCHEMA')
        check(archive['expectedSHA']==o['zipSHA256'] and archive['actualSHA']==o['zipSHA256'] and archive['size']==o['zipBytes'] and archive['chunkSHA256']==[o['zipSHA256']], 'ARCHIVE_LITERAL')
        check(len(archive['fdMetadata'])==5 and all(type(x) is int for x in archive['fdMetadata']),'ARCHIVE_FD_METADATA_SHAPE')
        s=os.stat('synthetic-public.zip',dir_fd=store.root,follow_symlinks=False)
        check(archive['fdMetadata']==[s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns],'ARCHIVE_DECLARED_IDENTITY_READBACK')
        check(manifest['artifactHashes']['archive-auth.json']==tree['archive-auth.json']['sha256'],'ARCHIVE_AUTH_HASH')
        return tree
    finally:
        close_once(root,'verify_capture producer output root')


def run_reviewed(capsule):
    """Only an explicit later root call may invoke this, after independent gates."""
    start=time.monotonic()
    gate(capsule)  # no run leaf or subprocess before successful external readback
    parent=physical(PREP)
    fd=None
    try:
        os.mkdir(RUN_LEAF,0o700,dir_fd=parent)  # EEXIST terminal, no retry
        fd=os.open(RUN_LEAF,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=parent)
    finally:
        try:close_once(parent,'run reservation parent')
        except BaseException as error:
            cleanup_owned(error,[(fd,'run leaf before Store handoff')])
            raise
    try:
        store=Store(fd,PREP/RUN_LEAF)
    except BaseException:
        close_once(fd,'run leaf failed Store constructor')
        raise
    result={'scope':SCOPE,'case1':'NOT_RUN','case2':'NOT_RUN_DEPENDENCY_FAILED','sourceClosure':False,'native':False,'open':OPEN,'retry':0}
    result['invocations']={case:{'attempted':False,'spawned':False,'pid':None} for case in ['case1','case2']}
    cleanup={'end':None}
    primary=None
    final_faults=[]
    def retain_final_fault(owner,error):
        # Preserve the first exception object; later evidence may be incomplete.
        nonlocal primary
        detail={'owner':owner,'error':repr(error),'status':'FINALIZATION_UNKNOWN_NO_RETRY'}
        final_faults.append(detail)
        if primary is None:
            primary=error
        else:
            primary.secondaryUnknown=getattr(primary,'secondaryUnknown',[])+[detail]
        if owner=='Store.close':
            primary.cleanupUnknown=getattr(primary,'cleanupUnknown',[])+[detail]
        if error is not primary:
            primary.cleanupUnknown=getattr(primary,'cleanupUnknown',[])+getattr(error,'cleanupUnknown',[])
        result.update(status='FAIL_OR_UNKNOWN_RETAINED',error=repr(primary))
        result['secondaryUnknown']=getattr(primary,'secondaryUnknown',[])
        result['cleanupUnknown']=getattr(primary,'cleanupUnknown',[])
    try:
        store.json('external-capsule.json',capsule)
        o=oracle();config=setup(store,o)
        check(time.monotonic()<start+30,'SETUP_TIMEOUT')
        finish_setup_evidence(store,start+30,start+270)
        case1_end=time.monotonic()+120
        one,out,err=observe_node(store,'case1',case1_end,min(case1_end+90,start+270),cleanup,result['invocations']['case1'],setup_end=start+30)
        result['case1']='RUNNING'
        check(not err,'CASE1_STDERR')
        tree=verify_capture(store,o,config,one,out)
        store.json('case1-sentinel.json',tree)
        check(time.monotonic()<case1_end,'CASE1_READBACK_TIMEOUT')
        result['case1']='PASS_BOUNDED_SOURCE_MODEL'
        result['case2']='NOT_RUN_PRELAUNCH'
        case2_end=time.monotonic()+30
        two,out2,err2=observe_node(store,'case2',case2_end,min(case2_end+90,start+270),cleanup,result['invocations']['case2'])
        result['case2']='RUNNING'
        check(two['returncode']!=0 and two['signal'] is None,'COLLISION_EXIT')
        failure=strict(out2)
        validate_collision(failure)
        root=physical(Path(config['OUTPUT_PARENT'])/OUTPUT_LEAF)
        try:
            check(snapshot_tree(root)==tree,'COLLISION_SENTINEL_CHANGED')
        finally:
            close_once(root,'collision sentinel producer output root')
        store.json('case2-readback.json',{'sentinelMatch':True,'outerStderrSHA256':sha(err2),'pythonWait':'NOT_INDEPENDENTLY_OBSERVED'})
        check(time.monotonic()<case2_end,'CASE2_READBACK_TIMEOUT')
        result['case2']='PASS_BOUNDED_SOURCE_MODEL'
        result['status']='TWO_FIXED_PRESERVATION_REGRESSION_CASES_PASS'
        result['pythonChildClose']='SOURCE_COMPATIBLE_INFERENCE_FROM_FROZEN_NODE_SUCCESS_PATH'
        for role,name in SOURCE_FILES.items():
            check(sha(read_absolute(REPO/'tools/epoch-rts'/name))==SOURCE_SHAS[role],'ORIGINAL_SOURCE_CHANGED')
        store.json('post-tree.json',snapshot_tree(store.root))
        check(time.monotonic()<start+270,'OVERALL_TIMEOUT')
    except BaseException as error:
        primary=error
        result.update(status='FAIL_OR_UNKNOWN_RETAINED',error=repr(error))
        result['cleanupUnknown']=getattr(error,'cleanupUnknown',[])
        classify_invocation_failures(result)
    finally:
        try:
            result['supervisorWriteFaults']=store.faults
            store.json('result.json',result)
        except BaseException as error:
            retain_final_fault('result.json',error)
        try:
            snapshot_tree(store.root)  # independent final cap/readback attempt
        except BaseException as error:
            retain_final_fault('final snapshot',error)
        try:
            store.close()  # once, including when either evidence owner failed
        except BaseException as error:
            retain_final_fault('Store.close',error)
        if final_faults:
            try:
                sys.stderr.write('SUPERVISOR_FINALIZATION_UNKNOWN '+repr(final_faults)+'\n')
            except BaseException as error:
                retain_final_fault('stderr',error)
    if primary is not None:
        raise primary
    check_final_deadline(start+270)
    return result


if __name__=='__main__':
    # External capsule digest must be fixed by root in the separate launch call.
    # It detects drift, not authorization; no trusted:true credential is accepted.
    if len(sys.argv)==4 and sys.argv[1]=='--execute-reviewed':
        raw=read_absolute(Path(sys.argv[2]))
        check(sha(raw)==sys.argv[3],'EXTERNAL_CAPSULE_DIGEST')
        print(canon(run_reviewed(strict(raw))).decode())
    elif len(sys.argv)==1:
        print(canon({'status':'PENDING_INDEPENDENT_REVIEWS_ROOT_READBACK_FRESHGUARD_SEPARATE_EXECUTION_CALL','scope':SCOPE,'attempt':'NOT_CREATED','bridge':'NOT_RUN','open':OPEN}).decode())
    else:
        raise Block('EXACT_ARGC_REQUIRED_NO_LAUNCH')
