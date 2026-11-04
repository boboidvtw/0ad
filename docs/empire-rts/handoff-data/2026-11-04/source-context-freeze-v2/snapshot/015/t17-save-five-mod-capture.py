# Purpose: NEW held-FD authenticated five-mod capture; candidate evidence only.
# Created: 2026-10-25. SPDX-License-Identifier: GPL-2.0-or-later
"""Stdlib-only. No official capture until complete independent source reviews.
No engine, retry, deletion, caller authority override, or semantic closure proof.
"""
import base64
import hashlib
import io
import json
import math
import os
from pathlib import Path
import re
import select
import stat
import sys
import time
import zipfile

CHUNK=4194304
ARCHIVE_MAX=8589934592
FILE_MAX=8388608
TOTAL_MAX=67108864
CENTRAL_MAX=67108864 # independent ZIP read bound; never the selected-byte budget
METADATA_MAX=8388608
CANDIDATE_MAX=4096
LAYER_ENTRY_MAX=16384
LOOSE_ENUM_MAX=16384 # separate PER-root full-tree traversal admission budget
STREAM_CHUNK=65536 # bounded phase-A payload/readback buffer; never whole-file assembly
ZIP_ENTRY_MAX=250000
FRAME_MAX=33554432
RAW_MAX=268435456
DEPTH_MAX=128
REPO=Path(__file__).resolve().parents[2]
ARCHIVE_PATH=Path('/Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/runtime/0 A.D..app/Contents/Resources/data/mods/public/public.zip')
ARCHIVE_SHA='ccb24dedee399e6d2810ccb62b0b1b77a937999d9f1dedffbc189b3e359f2429'
ROOTS=(('epoch_rts','binaries/data/mods/epoch_rts'),('epoch_t16_harness','tools/epoch-rts/t16-harness'),('epoch_t17_save_harness','tools/epoch-rts/t17-save-harness'),('epoch_t17_save_allocation_witness','tools/epoch-rts/t17-save-allocation-witness'))
FOLDERS=('globalscripts/','simulation/components/interfaces/','simulation/helpers/','simulation/components/')
FIXED=('maps/random/epoch_t17_save_six.js','maps/random/epoch_t17_save_six.json','mod.json')
OUTPUT_PARENT=REPO/'work/t17-save-five-mod-inventory-repair-preparation/captures'
SCHEMA_PATH=Path(__file__).with_name('t17-save-five-mod-analysis-schema.json')
# Replaced below once, from the exact independently approved normative bytes.
SCHEMA_SHA='280357ab50426d73f1265cb07458d8d4f86f226ab3b02d68025d1762d7975191'

class CaptureError(Exception):
    def __init__(self,code):super().__init__(code);self.code=code;self.secondary=[];self.unknown_fds=[]

def fail(code):raise CaptureError(code)
def sha(data):return hashlib.sha256(data).hexdigest()
def canon(value):return json.dumps(value,ensure_ascii=True,separators=(',',':'),allow_nan=False).encode('ascii')
def equal(a,b):return type(a) is type(b) and (list(a)==list(b) and all(equal(a[k],b[k]) for k in a) if type(a) is dict else len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b)) if type(a) is list else a==b)
def exact(value,keys):
    if type(value) is not dict or set(value)!=set(keys):fail('PROTOCOL_SCHEMA')

def strict_json(raw):
    if type(raw) is not bytes or len(raw)>FRAME_MAX:fail('PROTOCOL_LIMIT')
    try:text=raw.decode('utf-8','strict')
    except UnicodeError:fail('PROTOCOL_UTF8')
    depth=0;quoted=False;escaped=False
    for c in text:
        if quoted:
            if escaped:escaped=False
            elif c=='\\':escaped=True
            elif c=='"':quoted=False
        elif c=='"':quoted=True
        elif c in '[{':
            depth+=1
            if depth>DEPTH_MAX:fail('PROTOCOL_LIMIT')
        elif c in ']}':depth-=1
    def pairs(items):
        d={}
        for k,v in items:
            if k in d:fail('PROTOCOL_JSON_DUPLICATE')
            d[k]=v
        return d
    try:value=json.loads(text,object_pairs_hook=pairs,parse_constant=lambda _:fail('PROTOCOL_SCHEMA'))
    except CaptureError:raise
    except Exception:fail('PROTOCOL_SCHEMA')
    def numbers(v):
        if type(v) in (int,float) and (not math.isfinite(v) or abs(v)>2**53-1):fail('PROTOCOL_LIMIT')
        if type(v) is dict:
            for x in v.values():numbers(x)
        elif type(v) is list:
            for x in v:numbers(x)
    numbers(value);return value

class Deadline:
    def __init__(self):self.start=time.monotonic_ns();self.last=self.start;self.end=self.start+600*10**9;self.failed=False
    def check(self):
        if self.failed:fail('TIMEOUT')
        try:n=time.monotonic_ns()
        except Exception:self.failed=True;fail('TIMEOUT')
        if type(n) is not int or n<self.last or n>=self.end:self.failed=True;fail('TIMEOUT')
        self.last=n
    def io(self,fn,*args,**kwargs):
        self.check()
        try:value=fn(*args,**kwargs)
        except FileExistsError:raise
        except OSError:fail('OUTPUT_WRITE_OR_FSYNC' if fn in (os.write,os.fsync) else 'SOURCE_TYPE')
        try:self.check()
        except BaseException as error:
            if fn is os.open:cleanup_close(value,error)
            raise
        return value

def ident(s):return (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
def once_close(fd):
    try:os.close(fd)
    except Exception:
        error=CaptureError('RESOURCE_CLOSE_UNKNOWN');error.unknown_fds.append(fd);raise error

def cleanup_close(fd,primary):
    try:once_close(fd)
    except CaptureError as secondary:
        if primary is None:raise
        if not hasattr(primary,'secondary'):primary.secondary=[];primary.unknown_fds=[]
        primary.secondary.append(secondary.code);primary.unknown_fds.extend(secondary.unknown_fds)


def physical(path,d):
    """Open a physical absolute directory chain; no path symlink follow."""
    path=Path(path)
    if not path.is_absolute() or '..' in path.parts:fail('SOURCE_TYPE')
    fd=d.io(os.open,'/',os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:
        for part in path.parts[1:]:
            new=d.io(os.open,part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd)
            old=fd;fd=new;once_close(old)
        return fd
    except BaseException as error:
        cleanup_close(fd,error);raise

def open_source(path,d):
    parent=physical(Path(path).parent,d)
    fd=None
    try:
        fd=d.io(os.open,Path(path).name,os.O_RDONLY|os.O_NOFOLLOW,dir_fd=parent)
    finally:
        try:once_close(parent)
        except BaseException as error:
            if fd is not None:cleanup_close(fd,error)
            raise
    try:
        s=d.io(os.fstat,fd)
        if not stat.S_ISREG(s.st_mode):fail('SOURCE_TYPE')
        return fd,s
    except BaseException as error:cleanup_close(fd,error);raise

class AuthenticatedReader(io.RawIOBase):
    """Every returned range is sliced from whole authenticated immutable chunks."""
    def __init__(self,fd,expected,d):
        super().__init__();self.fd=fd;self.d=d;self.position=0;self.cache_index=None;self.cache=None
        self.expected=expected;self.chunks=[];self.scanned=0;self.actual=None;self.size=None;self.before=None
        try:
            self.before=d.io(os.fstat,fd);self.size=self.before.st_size
            if not stat.S_ISREG(self.before.st_mode) or self.size<=0 or self.size>ARCHIVE_MAX:fail('ARCHIVE_TOO_LARGE')
            digest=hashlib.sha256();self.chunks=[];self.scanned=0
            for offset in range(0,self.size,CHUNK):
                count=min(CHUNK,self.size-offset);data=d.io(os.pread,fd,count,offset)
                if len(data)!=count:fail('ARCHIVE_SHORT_READ')
                digest.update(data);self.chunks.append(sha(data));self.scanned+=len(data);d.check()
            self.actual=digest.hexdigest()
            if ident(d.io(os.fstat,fd))!=ident(self.before):fail('ARCHIVE_METADATA_CHANGED')
            if self.actual!=expected:fail('ARCHIVE_SHA_MISMATCH')
        except BaseException as error:
            error.archive_partial={'status':'PARTIAL','expectedSHA':expected,'actualSHA':self.actual,'size':self.size,'bytesScanned':self.scanned,'chunkBytes':CHUNK,'chunkSHA256':self.chunks[:],'fdMetadata':list(ident(self.before)) if self.before is not None else None}
            raise
    def readable(self):return True
    def seekable(self):return True
    def tell(self):self.d.check();return self.position
    def seek(self,offset,whence=0):
        self.d.check()
        if type(offset) is not int or whence not in (0,1,2):fail('ARCHIVE_READ_LIMIT')
        result=offset+(0 if whence==0 else self.position if whence==1 else self.size)
        if not 0<=result<=self.size:fail('ARCHIVE_READ_LIMIT')
        self.position=result;return result
    def read(self,size=-1):
        self.d.check()
        if type(size) is not int or size < -1:fail('ARCHIVE_READ_LIMIT')
        size=self.size-self.position if size==-1 else min(size,self.size-self.position)
        if size>CENTRAL_MAX:fail('ARCHIVE_READ_LIMIT')
        pieces=[];pos=self.position;end=pos+size
        while pos<end:
            index=pos//CHUNK
            if self.cache_index!=index:
                offset=index*CHUNK;count=min(CHUNK,self.size-offset)
                data=self.d.io(os.pread,self.fd,count,offset)
                if len(data)!=count:fail('ARCHIVE_SHORT_READ')
                if sha(data)!=self.chunks[index]:fail('ARCHIVE_CHUNK_MISMATCH')
                self.cache_index=index;self.cache=data
            stop=min(end,(index+1)*CHUNK);pieces.append(self.cache[pos%CHUNK:pos%CHUNK+stop-pos]);pos=stop
        result=b''.join(pieces);self.d.check();self.position=pos;return result
    def facts(self):return {'expectedSHA':self.expected,'actualSHA':self.actual,'size':self.size,'chunkBytes':CHUNK,'chunkCount':len(self.chunks),'authorityKind':'VERIFIED_HELD_FD_BYTES'}

def safe_vfs(name):
    if type(name) is not str or not name or len(name.encode('utf-8','strict'))>1024 or '\\' in name or ':' in name or '\0' in name or name.startswith('/') or any(p in ('','.','..') for p in name.split('/')):fail('ZIP_ENTRY_UNSAFE')
    return name

def default_folder(name):
    return next((f for f in FOLDERS if name.startswith(f) and name.endswith('.js') and '/' not in name[len(f):]),None)
def candidate(name):return default_folder(name) is not None or name in FIXED

def open_zip(reader):
    try:return zipfile.ZipFile(reader,'r',allowZip64=True)
    except CaptureError:raise
    except Exception:fail('ZIP_FORMAT_OR_CRC')

def validate_zip(z):
    if len(z.infolist())>ZIP_ENTRY_MAX:fail('SOURCE_LIMIT')
    seen=set()
    for info in z.infolist():
        name=info.orig_filename
        isdir=info.is_dir();safe_vfs(name[:-1] if isdir and name.endswith('/') else name)
        if name in seen:fail('ZIP_ENTRY_DUPLICATE')
        seen.add(name);mode=info.external_attr>>16;kind=stat.S_IFMT(mode)
        if kind not in (0,stat.S_IFDIR if isdir else stat.S_IFREG):fail('ZIP_ENTRY_UNSAFE')
        if info.compress_type not in (0,8):fail('ZIP_METHOD_UNSUPPORTED')
        if not isdir and candidate(name) and info.file_size>FILE_MAX:fail('SOURCE_LIMIT')

class Output:
    def __init__(self,parent,leaf,d):
        if type(leaf) is not str or not re.fullmatch('[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}',leaf):fail('PROTOCOL_SCHEMA')
        self.parent=Path(parent);self.leaf=leaf;self.d=d;self.fds=[];self.hashes={};self.root=None
        self.dirs={};self.unknown_fds=[];self.sizes={}
        self.parentfd=physical(self.parent,d)
        try:
            self.parentid=ident(d.io(os.fstat,self.parentfd))[:2]
            try:d.io(os.mkdir,leaf,0o700,dir_fd=self.parentfd)
            except FileExistsError:fail('OUTPUT_EXISTS')
            self.root=d.io(os.open,leaf,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=self.parentfd)
            s=d.io(os.fstat,self.root)
            if stat.S_IMODE(s.st_mode)!=0o700 or s.st_uid!=os.getuid():fail('OUTPUT_ANCHOR_CHANGED')
            self.rootid=ident(s)[:2];self.dirs={'':self.root};self.check()
        except BaseException as error:
            if self.root is not None:cleanup_close(self.root,error)
            cleanup_close(self.parentfd,error);raise
    def check(self):
        self.d.check();fd=physical(self.parent,self.d)
        primary = None
        try:
            if ident(self.d.io(os.fstat,fd))[:2]!=self.parentid:fail('OUTPUT_ANCHOR_CHANGED')
            s=self.d.io(os.stat,self.leaf,dir_fd=fd,follow_symlinks=False)
            if not stat.S_ISDIR(s.st_mode) or ident(s)[:2]!=self.rootid:fail('OUTPUT_ANCHOR_CHANGED')
        except BaseException as error:
            primary = error
            raise
        finally:
            cleanup_close(fd,primary)
    def directory(self,parts):
        rel='';fd=self.root
        for part in parts:
            rel=rel+'/'+part if rel else part
            if rel not in self.dirs:
                self.d.io(os.mkdir,part,0o700,dir_fd=fd)
                new=self.d.io(os.open,part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);self.dirs[rel]=new
            current=self.d.io(os.stat,part,dir_fd=fd,follow_symlinks=False)
            held=self.d.io(os.fstat,self.dirs[rel])
            if not stat.S_ISDIR(current.st_mode) or ident(current)[:2]!=ident(held)[:2] or stat.S_IMODE(held.st_mode)!=0o700 or held.st_uid!=os.getuid():fail('OUTPUT_ANCHOR_CHANGED')
            fd=self.dirs[rel]
        return fd
    def reserve(self,name):
        self.check();safe_vfs(name);parts=name.split('/');fd=self.directory(parts[:-1])
        try:out=self.d.io(os.open,parts[-1],os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600,dir_fd=fd)
        except FileExistsError:fail('OUTPUT_FILE_EXISTS')
        self.fds.append(out);return out
    def put(self,fd,data):
        count=self.d.io(os.write,fd,data)
        if count!=len(data):fail('OUTPUT_WRITE_OR_FSYNC')
    def finish_fd(self,fd):
        self.d.io(os.fsync,fd)
        try:once_close(fd)
        except CaptureError as error:self.unknown_fds.extend(error.unknown_fds);raise
        finally:self.fds.remove(fd) # remove active ownership; unknown ledger retains uncertain fd, never retry
        self.d.check()
    def write(self,name,data):
        fd=self.reserve(name)
        try:self.put(fd,data);self.finish_fd(fd)
        except BaseException as error:
            if fd in self.fds:
                cleanup_close(fd,error);self.fds.remove(fd)
            raise
        # Chunked hash readback never keeps a second whole input body live.
        self.readback(name,len(data),sha(data))
        parent=self.dirs['/'.join(name.split('/')[:-1])]
        self.d.io(os.fsync,parent);self.hashes[name]=sha(data);self.sizes[name]=len(data);return self.hashes[name]
    def capture(self,name,size,read):
        """Stream one source into its exclusive artifact, then bounded readback.
        read(n) is an internal held-FD/held-ZIP reader, never caller authority.
        No whole-file parts, bytearray accumulation or final join in phase A.
        """
        fd=self.reserve(name);digest=hashlib.sha256();count=0
        try:
            while True:
                self.d.check();data=read(min(STREAM_CHUNK,size+1-count));self.d.check()
                if not data:break
                if len(data)>STREAM_CHUNK or count+len(data)>size:fail('SOURCE_CHANGED')
                self.put(fd,data);digest.update(data);count+=len(data)
                del data
            if count!=size:fail('SOURCE_CHANGED')
            self.finish_fd(fd)
        except BaseException as error:
            if fd in self.fds:cleanup_close(fd,error);self.fds.remove(fd)
            raise
        actual=digest.hexdigest();self.readback(name,size,actual)
        parent=self.dirs['/'.join(name.split('/')[:-1])];self.d.io(os.fsync,parent)
        self.hashes[name]=actual;self.sizes[name]=size;return actual
    def copy_snapshot(self,name,source,size,digest):
        self.check();parts=source.split('/');parent=self.directory(parts[:-1])
        fd=self.d.io(os.open,parts[-1],os.O_RDONLY|os.O_NOFOLLOW,dir_fd=parent);primary=None;offset=0
        try:
            before=self.d.io(os.fstat,fd)
            if not stat.S_ISREG(before.st_mode) or before.st_nlink!=1 or before.st_size!=size:fail('OUTPUT_ANCHOR_CHANGED')
            def read(count):
                nonlocal offset
                data=self.d.io(os.pread,fd,count,offset);offset+=len(data);return data
            actual=self.capture(name,size,read)
            after=self.d.io(os.fstat,fd);named=self.d.io(os.stat,parts[-1],dir_fd=parent,follow_symlinks=False)
            if actual!=digest or ident(after)!=ident(before) or ident(named)!=ident(before) or after.st_nlink!=1:fail('OUTPUT_ANCHOR_CHANGED')
        except BaseException as error:primary=error;raise
        finally:cleanup_close(fd,primary)
    def readback(self,name,size,digest,retain=False):
        """Only held physical directory FDs; bound each read, verify full bytes.
        retain is used only for one candidate or final selected bodies, never
        an all-layer body pack. Hash records are checked separately from disk.
        """
        self.check();safe_vfs(name);parts=name.split('/');parent=self.directory(parts[:-1])
        fd=self.d.io(os.open,parts[-1],os.O_RDONLY|os.O_NOFOLLOW,dir_fd=parent)
        primary=None
        try:
            before=self.d.io(os.fstat,fd)
            if not stat.S_ISREG(before.st_mode) or before.st_nlink!=1 or before.st_size!=size:fail('OUTPUT_ANCHOR_CHANGED')
            actual=hashlib.sha256();parts_read=[] if retain else None;offset=0
            while offset<size:
                data=self.d.io(os.pread,fd,min(STREAM_CHUNK,size-offset),offset)
                if not data:fail('OUTPUT_WRITE_OR_FSYNC')
                actual.update(data);offset+=len(data)
                if retain:parts_read.append(data)
            if self.d.io(os.pread,fd,1,offset) or actual.hexdigest()!=digest:fail('OUTPUT_WRITE_OR_FSYNC')
            after=self.d.io(os.fstat,fd);named=self.d.io(os.stat,parts[-1],dir_fd=parent,follow_symlinks=False)
            if ident(after)!=ident(before) or ident(named)!=ident(before) or after.st_nlink!=1:fail('OUTPUT_ANCHOR_CHANGED')
            return b''.join(parts_read) if retain else None
        except BaseException as error:
            primary=error;raise
        finally:cleanup_close(fd,primary)
    def verify_files(self):
        # Revalidate every successfully closed artifact before manifest binds
        # it, including effective copies and metadata copies, not raw log FDs.
        if set(self.hashes)!=set(self.sizes):fail('OUTPUT_ANCHOR_CHANGED')
        for name,digest in self.hashes.items():self.readback(name,self.sizes[name],digest)
    def snapshot_names(self):
        """Physical namespace enumeration catches unrecorded layer files too."""
        found=set()
        if 'layer-sources' not in self.dirs:fail('OUTPUT_ANCHOR_CHANGED')
        def walk(parts):
            parent=self.directory(parts)
            for name in self.d.io(os.listdir,parent):
                safe_vfs(name);rel='/'.join(parts+[name]);st=self.d.io(os.stat,name,dir_fd=parent,follow_symlinks=False)
                if stat.S_ISDIR(st.st_mode):
                    if rel not in self.dirs:fail('OUTPUT_ANCHOR_CHANGED')
                    walk(parts+[name])
                elif stat.S_ISREG(st.st_mode):found.add(rel)
                else:fail('OUTPUT_ANCHOR_CHANGED')
        walk(['layer-sources']);return found
    def close(self):
        error=CaptureError('RESOURCE_CLOSE_UNKNOWN')
        fds=self.fds+list(reversed(list(self.dirs.values())))+([self.parentfd] if self.parentfd is not None else [])
        self.fds=[];self.dirs={};self.parentfd=None
        for fd in fds:
            try:once_close(fd)
            except CaptureError as secondary:error.unknown_fds.extend(secondary.unknown_fds)
        self.unknown_fds.extend(error.unknown_fds)
        if error.unknown_fds:raise error

_SCHEMA=None
def schema():
    global _SCHEMA
    if _SCHEMA is None:
        raw=SCHEMA_PATH.read_bytes()
        if sha(raw)!=SCHEMA_SHA:fail('AUTHORITY_UNAVAILABLE')
        _SCHEMA=strict_json(raw)
    return _SCHEMA

def validate_schema(value):
    root=schema()
    def check(v,s):
        if '$ref' in s:return check(v,root['$defs'][s['$ref'].split('/')[-1]])
        if 'allOf' in s:
            for child in s['allOf']:check(v,child)
        if 'oneOf' in s:
            matches=0
            for child in s['oneOf']:
                try:check(v,child);matches+=1
                except CaptureError:pass
            if matches!=1:fail('PROTOCOL_SCHEMA')
        if 'const' in s and not equal(v,s['const']):fail('PROTOCOL_SCHEMA')
        if 'enum' in s and not any(equal(v,x) for x in s['enum']):fail('PROTOCOL_SCHEMA')
        t=s.get('type')
        if t and type(v) is not {'object':dict,'array':list,'integer':int,'string':str,'null':type(None)}[t]:fail('PROTOCOL_SCHEMA')
        if t=='object':
            if set(v)!=set(s['required']):fail('PROTOCOL_SCHEMA')
            for k,x in v.items():check(x,s['properties'][k])
        if t=='array':
            if len(v)>s['maxItems']:fail('PROTOCOL_LIMIT')
            for x in v:check(x,s['items'])
        if t=='string':
            if not s.get('minLength',0)<=len(v)<=s.get('maxLength',2**53):fail('PROTOCOL_LIMIT')
            if 'pattern' in s and not re.fullmatch(s['pattern'],v):fail('PROTOCOL_SCHEMA')
        if t=='integer' and not s['minimum']<=v<=s['maximum']:fail('PROTOCOL_LIMIT')
    check(value,root)

def u16(s):return len(s.encode('utf-16-le','surrogatepass'))//2

def source_positions(text):
    # UTF16 boundaries; forbid both CRLF midpoints and surrogate-pair splits.
    positions={0:1};pos=0;line=1;i=0
    while i<len(text):
        c=text[i];pos+=2 if ord(c)>65535 else 1
        if c=='\r' and i+1<len(text) and text[i+1]=='\n':
            pos+=1;i+=1;line+=1
        elif c in '\r\n\u2028\u2029':line+=1
        positions[pos]=line;i+=1
    return positions,pos,line

def validate_finish(finish,capture_id,selected,bodies):
    validate_schema(finish)
    if finish['captureId']!=capture_id or len(finish['analyses'])!=len(selected):fail('PROTOCOL_DIGEST')
    object_count=0
    for i,(envelope,row,body) in enumerate(zip(finish['analyses'],selected,bodies)):
        if envelope['index']!=i or envelope['sha256']!=row['sha256']:fail('PROTOCOL_DIGEST')
        a=envelope['analysis']
        if not row['vfs'].endswith('.js'):
            if a is not None:fail('PROTOCOL_SCHEMA')
            continue
        if a is None or a['vfs']!=row['vfs']:fail('PROTOCOL_DIGEST')
        try:text=body.decode('utf-8','strict')
        except UnicodeError:
            if a['parseStatus']!='BLOCK_UTF8_ERROR':fail('PROTOCOL_SCHEMA')
            continue
        if a['parseStatus']=='BLOCK_UTF8_ERROR':fail('PROTOCOL_SCHEMA')
        if a['parseStatus']!='PARSED':continue
        positions,units,lines=source_positions(text)
        def label(value,synthetic=False,empty=False):
            if type(value) is not str or (not empty and not value) or u16(value)>units+(4096 if synthetic else 0):fail('PROTOCOL_LIMIT')
        def expression(value):
            label(value)
            if value not in text:fail('PROTOCOL_SCHEMA')
        def rowline(v):
            if not 1<=v<=lines:fail('PROTOCOL_SCHEMA')
        vectors=('functions','calls','writerSites','aliases','assignments','fileTopLevelDeclarations')
        object_count=sum(len(a[k]) for k in vectors)
        if object_count>262144:fail('PROTOCOL_LIMIT')
        for r in a['functions']:
            label(r['name'],True)
            if r['start'] not in positions or r['end'] not in positions or not r['start']<r['end'] or r['line']!=positions[r['start']] or r['endLine']!=positions[r['end']]:fail('PROTOCOL_SCHEMA')
            for value in r['params']:expression(value)
        for key in vectors[1:]:
            for r in a[key]:
                rowline(r['line'])
                if 'context' in r:label(r['context'],True)
                if key in ('calls','writerSites'):
                    expression(r['callee'])
                    for value in r['args']:expression(value)
                elif key=='aliases':
                    expression(r['name'])
                    if r['value'] is not None:expression(r['value'])
                elif key=='assignments':
                    expression(r['left'])
                    if 'right' in r:expression(r['right'])
                else:
                    if r['kind']=='variable':expression(r['name'])
                    else:label(r['name'])
        # Exact writer/call multiplicity remains retained, not deduplicated.
        calls={(r['callee'],tuple(r['args']),r['line'],r['context']) for r in a['calls']}
        aliases={(r['name'],r['value'],r['line']) for r in a['aliases']}
        for r in a['writerSites']:
            if (r['callee'],tuple(r['args']),r['line'],r['context']) not in calls:fail('PROTOCOL_SCHEMA')
            if r['target'] is not None:expression(r['target'])
            if 'alias' in r:
                expression(r['alias']);rowline(r['aliasDeclarationLine'])
                if r['alias']!=r['callee'] or r['aliasSource'].split('.')[1]!=r['kind'] or (r['alias'],r['aliasSource'],r['aliasDeclarationLine']) not in aliases or r['target']!=(r['args'][0] if r['args'] else None):fail('PROTOCOL_SCHEMA')
            else:
                expected=1 if r['kind'] in ('RegisterComponentType','RegisterSystemComponentType','ReRegisterComponentType') else 0
                if r['nameArgumentIndex']!=expected:fail('PROTOCOL_SCHEMA')
                if r['literalName'] is not None:label(r['literalName'],empty=True)

UNSUPPORTED=['implicit engine mod mount','user/rdata higher overrides','DELETED tombstones','loose/archive and archive ordering','mtime arbitration','actual runtime mount/profile inventory','map startup/trigger/native job caller closure']

def read_source_fd(fd,before,d):
    if before.st_size>FILE_MAX:fail('SOURCE_LIMIT')
    data=d.io(os.pread,fd,before.st_size+1,0)
    if len(data)!=before.st_size or ident(d.io(os.fstat,fd))!=ident(before):fail('SOURCE_CHANGED')
    return data

class Capture:
    def __init__(self,d):
        self.d=d;self.loose=[];self.directories=[];self.archivefd=None;self.z=None
        self.sources={};self.rootanchors=[];self.candidate_count=0
    def enumerate_names(self,fd,prefix,counter):
        self.d.check();iterator=None;primary=None;names=[]
        try:
            # Do not pass this resource-producing call to Deadline.io: its
            # generic postcheck cannot own/close an iterator which just returned.
            try:iterator=os.scandir(fd)
            except OSError:fail('SOURCE_TYPE')
            self.d.check()
            while True:
                self.d.check()
                try:entry=next(iterator)
                except StopIteration:break
                except OSError:fail('SOURCE_TYPE')
                self.d.check();counter[0]+=1
                if counter[0]>LOOSE_ENUM_MAX:fail('SOURCE_LIMIT')
                name=entry.name;safe_vfs(prefix+'/'+name if prefix else name)
                self.d.check();names.append(name)
            self.d.check();return sorted(names,key=lambda v:v.encode('utf-8','strict'))
        except BaseException as error:primary=error;raise
        finally:
            if iterator is not None:
                try:iterator.close()
                except Exception:
                    if primary is None:fail('RESOURCE_CLOSE_UNKNOWN')
                    if not hasattr(primary,'secondary'):primary.secondary=[];primary.unknown_fds=[]
                    primary.secondary.append('RESOURCE_CLOSE_UNKNOWN')
                else:
                    if primary is None:self.d.check()
    def register_candidate(self):
        self.candidate_count+=1
        if self.candidate_count>LAYER_ENTRY_MAX:fail('SOURCE_LIMIT')
    def loose_layer(self,name,path):
        # Enumerate and retain descriptors first, before any body allocation.
        # A terminal recheck also binds each root pathname to its original FD.
        path=Path(path);root=physical(path,self.d)
        self.directories.append((root,None));self.directories[-1]=(root,ident(self.d.io(os.fstat,root)))
        self.rootanchors.append((path,ident(self.d.io(os.fstat,root))[:2]))
        rows=[];counter=[0]
        def walk(fd,prefix):
            before=ident(self.d.io(os.fstat,fd));names=self.enumerate_names(fd,prefix,counter)
            for entry in names:
                vfs=(prefix+'/'+entry if prefix else entry);safe_vfs(vfs)
                st=self.d.io(os.stat,entry,dir_fd=fd,follow_symlinks=False)
                if stat.S_ISLNK(st.st_mode):fail('SOURCE_SYMLINK')
                if stat.S_ISDIR(st.st_mode):
                    child=self.d.io(os.open,entry,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd)
                    self.directories.append((child,None));self.directories[-1]=(child,ident(self.d.io(os.fstat,child)))
                    walk(child,vfs)
                elif not stat.S_ISREG(st.st_mode):fail('SOURCE_TYPE')
                elif candidate(vfs):
                    self.register_candidate()
                    if st.st_size>FILE_MAX:fail('SOURCE_LIMIT')
                    source=self.d.io(os.open,entry,os.O_RDONLY|os.O_NOFOLLOW,dir_fd=fd)
                    self.loose.append((source,None,None,fd,entry));actual=self.d.io(os.fstat,source)
                    if not stat.S_ISREG(actual.st_mode) or ident(st)!=ident(actual):fail('SOURCE_CHANGED')
                    index=len(self.loose)-1;self.loose[index]=(source,actual,None,fd,entry)
                    self.sources[(name,vfs)]=('loose',index)
                    rows.append({'vfs':vfs,'sourceDisplay':str(path)+'/'+vfs,'bytes':actual.st_size})
            if before!=ident(self.d.io(os.fstat,fd)):fail('SOURCE_CHANGED')
        walk(root,'')
        return {'name':name,'rootKind':'loose','rootDisplay':str(path),'entries':sorted(rows,key=lambda r:r['vfs'].encode('utf-8'))}
    def capture_candidate(self,output,mod,row):
        kind,source=self.sources[(mod,row['vfs'])];name='layer-sources/'+mod+'/'+row['vfs']
        if kind=='loose':
            fd,before,_,parent,leaf=self.loose[source];offset=0
            def read(count):
                nonlocal offset
                data=self.d.io(os.pread,fd,count,offset);offset+=len(data);return data
            digest=output.capture(name,row['bytes'],read)
            if ident(self.d.io(os.fstat,fd))!=ident(before):fail('SOURCE_CHANGED')
            self.loose[source]=(fd,before,digest,parent,leaf);return digest
        stream=None;primary=None
        try:
            stream=self.z.open(source,'r');self.d.check()
            return output.capture(name,row['bytes'],stream.read)
        except BaseException as error:
            primary=error
            if isinstance(error,CaptureError):raise
            wrapped=CaptureError('ZIP_FORMAT_OR_CRC');wrapped.secondary.extend(getattr(error,'secondary',[]));wrapped.unknown_fds.extend(getattr(error,'unknown_fds',[]));primary=wrapped;raise wrapped
        finally:
            if stream is not None:
                try:stream.close()
                except Exception:
                    if primary is not None:primary.secondary.append('RESOURCE_CLOSE_UNKNOWN')
                    else:fail('RESOURCE_CLOSE_UNKNOWN')
    def build(self,output):
        self.archivefd,st=open_source(ARCHIVE_PATH,self.d)
        self.reader=AuthenticatedReader(self.archivefd,ARCHIVE_SHA,self.d);self.z=open_zip(self.reader);validate_zip(self.z)
        rows=[]
        for info in self.z.infolist():
            if info.is_dir() or not candidate(info.filename):continue
            self.register_candidate()
            self.sources[('public',info.filename)]=('archive',info)
            rows.append({'vfs':info.filename,'sourceDisplay':str(ARCHIVE_PATH)+'::'+info.filename,'bytes':info.file_size})
        layers=[{'name':'public','rootKind':'archive','rootDisplay':str(ARCHIVE_PATH),'entries':sorted(rows,key=lambda r:r['vfs'].encode('utf-8'))}]
        for name,path in ROOTS:layers.append(self.loose_layer(name,REPO/path))
        allrows=[row for layer in layers for row in layer['entries']]
        if len(allrows)>LAYER_ENTRY_MAX or len({row['vfs'] for row in allrows})>CANDIDATE_MAX or sum(row['bytes'] for row in allrows if row['vfs']=='mod.json')>METADATA_MAX:fail('SOURCE_LIMIT')
        # Phase A: snapshot one authenticated candidate, independently copy each
        # mod.json, release its bytes before the next candidate read. No layer
        # aggregate byte gate: only the final selected set has a 64MiB limit.
        for layer in layers:
            for row in layer['entries']:
                row['sha256']=self.capture_candidate(output,layer['name'],row)
                if row['vfs']=='mod.json':output.copy_snapshot('layer-metadata/'+layer['name']+'/mod.json','layer-sources/'+layer['name']+'/mod.json',row['bytes'],row['sha256'])
        picked={}
        for layer in layers:
            for row in layer['entries']:
                old=picked.get(row['vfs']);shadow=[] if old is None else old['shadowed']+[{'mod':old['mod'],'sourceDisplay':old['sourceDisplay'],'sha256':old['sha256']}]
                picked[row['vfs']]={'vfs':row['vfs'],'mod':layer['name'],'sha256':row['sha256'],'bytes':row['bytes'],'shadowed':shadow,'sourceDisplay':row['sourceDisplay'],'archiveEntry':row['vfs'] if layer['name']=='public' else None,'defaultLoaderFolder':default_folder(row['vfs']),'realm':'MAP_GENERATOR_REQUIRES_NATIVE_REALM_BINDING' if row['vfs'].startswith('maps/') else 'METADATA' if row['vfs']=='mod.json' else 'SIMULATION_CANDIDATE'}
        if sum(row['bytes'] for row in picked.values())>TOTAL_MAX:fail('SOURCE_LIMIT')
        # Phase B: selected bytes come exclusively from owned snapshots, never
        # re-open or reread the original pathname/ZIP to produce a second capture.
        selected=[];bodies=[]
        for i,vfs in enumerate(sorted(picked,key=lambda v:v.encode('utf-8'))):
            row=dict(picked[vfs]);del row['sourceDisplay'];selected.append({'index':i,**row})
            bodies.append(output.readback('layer-sources/'+row['mod']+'/'+vfs,row['bytes'],row['sha256'],retain=True))
        digest=sha('\n'.join(r['vfs']+'\0'+r['mod']+'\0'+r['sha256']+'\0'+str(r['bytes']) for r in selected).encode('utf-8'))
        capture_id=sha(canon({'version':1,'archiveExpectedSHA':ARCHIVE_SHA,'selectedDigest':digest}))
        captured={'v':1,'kind':'CAPTURED','captureId':capture_id,'sourceCount':len(selected),'selectedDigest':digest,'layers':layers,'selected':selected,'archive':self.reader.facts(),'unsupportedRuntimeRules':UNSUPPORTED}
        self.verify_preservation(output,captured,bodies)
        return captured,bodies
    def verify_preservation(self,output,captured,bodies):
        expected={};by_vfs={};mods=['public']+[name for name,_ in ROOTS]
        if [layer['name'] for layer in captured['layers']]!=mods:fail('PROTOCOL_DIGEST')
        for layer in captured['layers']:
            for row in layer['entries']:
                key=(layer['name'],safe_vfs(row['vfs']));name='layer-sources/'+key[0]+'/'+key[1]
                if key in expected:fail('PROTOCOL_DIGEST')
                expected[key]=row;by_vfs.setdefault(row['vfs'],[]).append((layer['name'],row))
                if output.hashes.get(name)!=row['sha256'] or output.sizes.get(name)!=row['bytes']:fail('PROTOCOL_DIGEST')
                output.readback(name,row['bytes'],row['sha256'])
                if row['vfs']=='mod.json':
                    copy='layer-metadata/'+layer['name']+'/mod.json'
                    if output.hashes.get(copy)!=row['sha256'] or output.sizes.get(copy)!=row['bytes']:fail('PROTOCOL_DIGEST')
        names={'layer-sources/'+mod+'/'+vfs for mod,vfs in expected}
        if names!={n for n in output.hashes if n.startswith('layer-sources/')} or names!=output.snapshot_names():fail('PROTOCOL_DIGEST')
        if len(bodies)!=len(captured['selected']) or len(by_vfs)!=len(bodies) or captured['sourceCount']!=len(bodies):fail('PROTOCOL_DIGEST')
        for i,(row,body,vfs) in enumerate(zip(captured['selected'],bodies,sorted(by_vfs,key=lambda v:v.encode('utf-8')))):
            history=by_vfs[vfs];mod,original=history[-1]
            shadow=[{'mod':name,'sourceDisplay':r['sourceDisplay'],'sha256':r['sha256']} for name,r in history[:-1]]
            if row['index']!=i or row['vfs']!=vfs or row['mod']!=mod or row['bytes']!=original['bytes'] or row['sha256']!=original['sha256'] or not equal(row['shadowed'],shadow) or len(body)!=row['bytes'] or sha(body)!=row['sha256']:fail('PROTOCOL_DIGEST')
        output.verify_files()

    def recheck(self):
        for fd,before,digest,parent,name in self.loose:
            data=read_source_fd(fd,before,self.d)
            if sha(data)!=digest or ident(self.d.io(os.stat,name,dir_fd=parent,follow_symlinks=False))!=ident(before):fail('SOURCE_CHANGED')
        for fd,before in self.directories:
            if ident(self.d.io(os.fstat,fd))!=before:fail('SOURCE_CHANGED')
        for path,expected in self.rootanchors:
            fd=physical(path,self.d);primary=None
            try:
                if ident(self.d.io(os.fstat,fd))[:2]!=expected:fail('SOURCE_CHANGED')
            except BaseException as error:primary=error;raise
            finally:cleanup_close(fd,primary)
    def close(self):
        errors=[]
        if self.z is not None:
            try:self.z.close()
            except Exception:errors.append(CaptureError('RESOURCE_CLOSE_UNKNOWN'))
            self.z=None
        fds=[r[0] for r in self.loose]+[r[0] for r in reversed(self.directories)]+([self.archivefd] if self.archivefd is not None else [])
        # Active ownership transferred to one close attempt. Unknown descriptors
        # remain in the returned error ledger, never re-enter active ownership.
        self.loose=[];self.directories=[];self.archivefd=None
        for fd in fds:
            try:once_close(fd)
            except CaptureError as error:errors.append(error)
        if errors:
            first=errors[0]
            for error in errors[1:]:first.secondary.append(error.code);first.unknown_fds.extend(error.unknown_fds)
            raise first

NODE_PATH=REPO/'tools/epoch-rts/t17-save-five-mod-source-inventory-v2.cjs'
NODE_SOURCE_EXPECTED='e7100dd52b755cc7dedefa07624520dbacdd41ccf8e20428160ec2c588f2c3b1'
THREE=('inventory.json','layer-inputs.json','writer-sites.json')

LAUNCHER_ROWS=({'path': '/Library/Developer/CommandLineTools/usr/bin/python3', 'dev': 16777234, 'ino': 46451073, 'mode': 41453, 'uid': 0, 'gid': 0, 'size': 67, 'mtime_ns': 1789303430844563422, 'ctime_ns': 1789303480687160753, 'rawlink': '../../Library/Frameworks/Python3.framework/Versions/3.9/bin/python3'}, {'path': '/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3', 'dev': 16777234, 'ino': 46448185, 'mode': 41453, 'uid': 0, 'gid': 0, 'size': 9, 'mtime_ns': 1789303428276361629, 'ctime_ns': 1789303483027023952, 'rawlink': 'python3.9'}, {'path': '/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9', 'dev': 16777234, 'ino': 46448186, 'mode': 33261, 'uid': 0, 'gid': 0, 'size': 53200, 'mtime_ns': 1787720187000000000, 'ctime_ns': 1789303483027858471, 'sha256': '6e7ae61f68a3838094fc56590f84c52069a97d7816f6bb79e0e85995b340e464'})

def runtime_stat(s):
    return {k:getattr(s,'st_'+k) for k in ('dev','ino','mode','uid','gid','size','mtime_ns','ctime_ns')}

def fixed_launcher(d):
    # Exactly these two literal hops are observed dependencies; never resolve an
    # arbitrary symlink or relax physical opening for archive/source/output.
    parents=[];target=None;primary=None
    try:
        for row in LAUNCHER_ROWS:
            path=Path(row['path']);parent=physical(path.parent,d);parents.append((parent,path.name,row))
            before=d.io(os.stat,path.name,dir_fd=parent,follow_symlinks=False)
            if runtime_stat(before)!={k:row[k] for k in runtime_stat(before)}:fail('AUTHORITY_UNAVAILABLE')
            if 'rawlink' in row:
                if not stat.S_ISLNK(before.st_mode) or d.io(os.readlink,path.name,dir_fd=parent)!=row['rawlink']:fail('AUTHORITY_UNAVAILABLE')
            else:
                target=d.io(os.open,path.name,os.O_RDONLY|os.O_NOFOLLOW,dir_fd=parent)
                actual=d.io(os.fstat,target)
                if not stat.S_ISREG(actual.st_mode) or runtime_stat(actual)!=runtime_stat(before):fail('AUTHORITY_UNAVAILABLE')
                data=d.io(os.pread,target,actual.st_size+1,0)
                if len(data)!=actual.st_size or sha(data)!=row['sha256'] or runtime_stat(d.io(os.fstat,target))!=runtime_stat(actual):fail('AUTHORITY_UNAVAILABLE')
        for parent,name,row in parents:
            after=d.io(os.stat,name,dir_fd=parent,follow_symlinks=False)
            if runtime_stat(after)!={k:row[k] for k in runtime_stat(after)}:fail('AUTHORITY_UNAVAILABLE')
            if 'rawlink' in row and d.io(os.readlink,name,dir_fd=parent)!=row['rawlink']:fail('AUTHORITY_UNAVAILABLE')
        return {'hops':[dict(r) for r in LAUNCHER_ROWS[:-1]],'physicalTarget':LAUNCHER_ROWS[-1]['path'],'targetSHA256':LAUNCHER_ROWS[-1]['sha256']}
    except BaseException as error:primary=error;raise
    finally:
        errors=[]
        for fd in ([target] if target is not None else [])+[r[0] for r in reversed(parents)]:
            try:once_close(fd)
            except CaptureError as error:errors.append(error)
        if errors:
            owner=primary or errors[0]
            for error in errors:
                if error is not owner:owner.secondary.append(error.code);owner.unknown_fds.extend(error.unknown_fds)
            if primary is None:raise owner

def runtime_context(d):
    import _hashlib,zlib,_io
    rows=[]
    launcher=fixed_launcher(d)
    paths=[Path(launcher['physicalTarget'])]
    for module in (zipfile,hashlib,io,json,os,_hashlib,zlib,_io):
        p=getattr(module,'__file__',None)
        if p and p not in ('built-in','frozen'):paths.append(Path(p))
    for path in paths:
        fd,s=open_source(path,d)
        primary = None
        try:
            h=hashlib.sha256()
            for offset in range(0,s.st_size,CHUNK):
                raw=d.io(os.pread,fd,min(CHUNK,s.st_size-offset),offset)
                if len(raw)!=min(CHUNK,s.st_size-offset):fail('SOURCE_CHANGED')
                h.update(raw)
            if ident(d.io(os.fstat,fd))!=ident(s):fail('SOURCE_CHANGED')
            rows.append({'path':str(path),'bytes':s.st_size,'sha256':h.hexdigest()})
        except BaseException as error:
            primary = error
            raise
        finally:
            cleanup_close(fd,primary)
    return {'pythonExecutable':sys.executable,'pythonVersion':sys.version,'launcher':launcher,'dependencies':rows,'authority':'OBSERVED_RUNTIME_DEPENDENCIES_NOT_EXECUTION_ATTESTATION'}

class Protocol:
    def __init__(self,stdin,stdout,d):self.stdin=stdin;self.stdout=stdout;self.d=d;self.output=None;self.logs={};self.rawtotal=0;self.diagnosticbytes=0;self.pending=[];self.buffer=bytearray()
    def attach(self,output):
        self.output=output
        for name in ('protocol-input.ndjson','protocol-output.ndjson','diagnostics.ndjson'):self.logs[name]=output.reserve(name)
        for name,data in self.pending:output.put(self.logs[name],data)
        self.pending=[]
    def raw(self,name,data):
        if self.rawtotal+len(data)>RAW_MAX:fail('PROTOCOL_LIMIT')
        self.rawtotal+=len(data)
        if name in self.logs:self.output.put(self.logs[name],data)
        elif self.output is None:self.pending.append((name,data))
        else:fail('OUTPUT_WRITE_OR_FSYNC')
    def _input_chunk(self):
        self.d.check()
        try:fd=self.stdin.fileno()
        except (AttributeError,io.UnsupportedOperation):return self.stdin.read(65536)
        return self.d.io(os.read,fd,65536)
    def receive(self):
        self.d.check()
        while b'\n' not in self.buffer:
            chunk=self._input_chunk()
            if not chunk:
                if self.buffer:self.raw('protocol-input.ndjson',bytes(self.buffer));self.buffer.clear()
                fail('CHILD_EOF')
            self.buffer.extend(chunk)
            if len(self.buffer)>FRAME_MAX and b'\n' not in self.buffer:
                self.raw('protocol-input.ndjson',bytes(self.buffer));self.buffer.clear();fail('PROTOCOL_LIMIT')
        stop=self.buffer.index(10)+1;raw=bytes(self.buffer[:stop]);del self.buffer[:stop]
        self.raw('protocol-input.ndjson',raw)
        if len(raw)>FRAME_MAX:fail('PROTOCOL_LIMIT')
        return strict_json(raw)
    def ensure_no_extra(self):
        # Reject bytes already received/buffered after FINISH; cannot attest
        # arbitrary future writes by another process after this observation.
        extra=bytes(self.buffer);self.buffer.clear()
        if not extra:
            try:fd=self.stdin.fileno()
            except (AttributeError,io.UnsupportedOperation):extra=self.stdin.read(FRAME_MAX+1)
            else:
                self.d.check()
                if select.select([fd],[],[],0)[0]:extra=self.d.io(os.read,fd,FRAME_MAX+1)
        if extra:self.raw('protocol-input.ndjson',extra);fail('PROTOCOL_ORDER')
        self.d.check()
    def frame(self,value):
        raw=canon(value)+b'\n'
        if len(raw)>FRAME_MAX:fail('PROTOCOL_LIMIT')
        self.raw('protocol-output.ndjson',raw);return raw
    def send_raw(self,raw):
        self.d.check();count=self.stdout.write(raw)
        if count!=len(raw):fail('OUTPUT_WRITE_OR_FSYNC')
        self.stdout.flush();self.d.check()
    def emit(self,value):self.send_raw(self.frame(value))
    def finish_logs(self):
        errors=[]
        for name,fd in list(self.logs.items()):
            try:self.output.finish_fd(fd)
            except Exception as error:errors.append(error)
            del self.logs[name]
        if errors:
            first=errors[0]
            if not hasattr(first,'secondary'):first.secondary=[];first.unknown_fds=[]
            for error in errors[1:]:first.secondary.append(str(error));first.unknown_fds.extend(getattr(error,'unknown_fds',[]))
            raise first

def synthesize(captured,bodies,finish):
    analyses=finish['analyses'];blocks=sum(1 for r in analyses if r['analysis'] is not None and r['analysis']['parseStatus']!='PARSED')
    inventory={'schema':1,'status':'OPEN_CANDIDATE_SOURCE_INVENTORY_NOT_RUNTIME_OR_WRITER_CLOSURE','tool':finish['tool'],'archive':captured['archive'],'orderedMods':[r['name'] for r in captured['layers']],'unsupportedRuntimeRules':UNSUPPORTED,'entries':[{**row,'analysis':a['analysis']} for row,a in zip(captured['selected'],analyses)],'counts':{'effective':len(bodies),'scripts':sum(r['analysis'] is not None for r in analyses),'parseErrors':blocks},'sourceClosure':False,'native':False}
    writers=[]
    for row,analysis in zip(captured['selected'],analyses):
        a=analysis['analysis']
        if a is not None and a['parseStatus']=='PARSED':
            for site in a['writerSites']:writers.append({'vfs':row['vfs'],'mod':row['mod'],**site})
    result={'inventory.json':inventory,'layer-inputs.json':{'layers':captured['layers'],'sourceClosure':False,'native':False},'writer-sites.json':{'status':'UNRESOLVED_REQUIRES_POSITIVE_PER_CALLER_SEMANTICS','sites':writers,'sourceClosure':False,'native':False}}
    return result,'CAPTURE_COMPLETE_WITH_ANALYSIS_BLOCKS' if blocks else 'CAPTURE_COMPLETE_CANDIDATE_ONLY'

def _run(stdin,stdout):
    d=Deadline();protocol=Protocol(stdin,stdout,d);output=None;capture=Capture(d);diskcomplete=False;phase='BEGIN';primary=None
    try:
        begin=protocol.receive();exact(begin,('v','kind','outputLeaf'))
        if type(begin['v']) is not int or begin['v']!=1 or begin['kind']!='BEGIN':fail('PROTOCOL_SCHEMA')
        if sys.version_info[:3]!=(3,9,6) or Path(sys.executable)!=Path('/Library/Developer/CommandLineTools/usr/bin/python3'):fail('AUTHORITY_UNAVAILABLE')
        # Only the fixed parent may be created, one level relative to an already
        # opened physical directory. Never mkdir parents recursively.
        parentfd=physical(OUTPUT_PARENT.parent,d)
        primary = None
        try:
            try:d.io(os.mkdir,OUTPUT_PARENT.name,0o700,dir_fd=parentfd)
            except FileExistsError:pass
        except BaseException as error:
            primary = error
            raise
        finally:
            cleanup_close(parentfd,primary)
        output=Output(OUTPUT_PARENT,begin['outputLeaf'],d);protocol.attach(output)
        phase='TOOLING'
        nodefd,nodestat=open_source(NODE_PATH,d)
        primary = None
        try:nodebytes=read_source_fd(nodefd,nodestat,d);nodeactual=sha(nodebytes)
        except BaseException as error:
            primary = error
            raise
        finally:
            cleanup_close(nodefd,primary)
        if nodeactual!=NODE_SOURCE_EXPECTED:fail('AUTHORITY_UNAVAILABLE')
        context=runtime_context(d)
        phase='ARCHIVE_AND_SOURCES';captured,bodies=capture.build(output)
        for row,body in zip(captured['selected'],bodies):
            output.write('effective/'+row['vfs'],body)
            protocol.emit({'v':1,'kind':'SOURCE','index':row['index'],'vfs':row['vfs'],'mod':row['mod'],'sha256':row['sha256'],'bytes':len(body),'bodyBase64':base64.b64encode(body).decode('ascii')})
        output.write('archive-auth.json',canon({**captured['archive'],'chunkSHA256':capture.reader.chunks,'fdMetadata':list(ident(capture.reader.before)),'status':'VERIFIED_HELD_FD_BYTES'})+b'\n')
        output.write('capture-inputs.json',canon({'captured':captured,'runtime':context,'nodeSource':{'path':str(NODE_PATH),'expectedSHA':NODE_SOURCE_EXPECTED,'actualSHA':nodeactual},'sourceClosure':False,'native':False})+b'\n')
        protocol.emit(captured);phase='FINISH';finish=protocol.receive()
        if type(finish) is dict and finish.get('kind')=='ABORT':
            exact(finish,('v','kind','code'))
            if type(finish['v']) is not int or finish['v']!=1 or finish['code'] not in ('NODE_PROTOCOL','NODE_ANALYSIS','NODE_LIMIT'):fail('PROTOCOL_SCHEMA')
            fail('ABORT_'+finish['code'])
        protocol.ensure_no_extra()
        validate_finish(finish,captured['captureId'],captured['selected'],bodies)
        if finish['tool']['nodeSourceSHA256']!=nodeactual:fail('PROTOCOL_DIGEST')
        capture.recheck();capture.close();phase='OUTPUT';output.check()
        capture.verify_preservation(output,captured,bodies)
        documents,status=synthesize(captured,bodies,finish)
        for name in THREE:output.write(name,canon(documents[name])+b'\n')
        output.verify_files()
        manifest={'schema':1,'status':status,'captureId':captured['captureId'],'artifactHashes':dict(output.hashes),'excludedFromWholeFileHashes':['protocol-input.ndjson','protocol-output.ndjson','diagnostics.ndjson','manifest.json','completed.json','fault.json'],'rawSeal':'NOT_CLAIMED','sourceClosure':False,'native':False}
        output.write('manifest.json',canon(manifest)+b'\n')
        complete={'v':1,'kind':'COMPLETED','captureId':captured['captureId'],'status':status,'artifactHashes':{name:output.hashes[name] for name in THREE+('manifest.json',)},'sourceClosure':False,'native':False}
        output.check();output.write('completed.json',canon(complete)+b'\n');diskcomplete=True
        terminal=protocol.frame(complete);protocol.finish_logs();output.close();output=None
        # Disk completion can exist even if stdout fails; caller then UNKNOWN.
        protocol.send_raw(terminal);return 0
    except BaseException as error:
        primary=error;code=error.code if isinstance(error,CaptureError) else 'PROTOCOL_SCHEMA'
        # Bytes already read from the OS but not yet framed remain evidence.
        if protocol.buffer:
            try:protocol.raw('protocol-input.ndjson',bytes(protocol.buffer));protocol.buffer.clear()
            except Exception:pass
        secondary=[];capture_unknown=[]
        try:capture.close()
        except Exception as close_error:secondary.append(str(close_error));secondary.extend(getattr(close_error,'secondary',[]));capture_unknown.extend(getattr(close_error,'unknown_fds',[]))
        secondary.extend(getattr(error,'secondary',[]))
        unknown=list(getattr(error,'unknown_fds',[]))+capture_unknown;terminal=None
        if output is not None and not diskcomplete and hasattr(error,'archive_partial'):
            try:output.write('archive-auth.json',canon(error.archive_partial)+b'\n')
            except Exception as archive_log_error:secondary.append(str(archive_log_error))
        if output is not None and not diskcomplete:
            try:
                output.write('fault.json',canon({'phase':phase,'code':code,'secondary':secondary,'unknownCloseDescriptors':unknown,'outputCleanupComplete':False,'sourceClosure':False,'native':False})+b'\n')
            except Exception as fault_error:secondary.append(str(fault_error))
        if not diskcomplete:
            try:
                # Exact same bytes are recorded before closing raw FDs and sent
                # afterward. Always false: final cleanup is not yet observed.
                terminal=protocol.frame({'v':1,'kind':'FAULT','phase':phase,'code':code,'durableFault':False})
            except Exception:terminal=None
        if output is not None:
            try:protocol.finish_logs()
            except Exception as close_error:secondary.append(str(close_error));unknown.extend(getattr(close_error,'unknown_fds',[]))
            try:output.close()
            except Exception as close_error:secondary.append(str(close_error));unknown.extend(getattr(close_error,'unknown_fds',[]))
        if terminal is not None:
            try:protocol.send_raw(terminal)
            except Exception:secondary.append('OUTPUT_WRITE_OR_FSYNC')
        # No uncertain fd retry, rewritten healthy completion, or claim that an
        # earlier fault snapshot includes the final cleanup. Fixed stderr codes.
        try:
            sys.stderr.write('CAPTURE_FAULT '+phase+' '+code+'\n')
            if 'RESOURCE_CLOSE_UNKNOWN' in secondary or unknown:sys.stderr.write('CAPTURE_FAULT CLEANUP RESOURCE_CLOSE_UNKNOWN\n')
            sys.stderr.flush()
        except Exception:pass
        return 1

if __name__=='__main__':
    if len(sys.argv)!=1:
        sys.stderr.write('CAPTURE_FAULT BEGIN PROTOCOL_SCHEMA\n');sys.exit(1)
    sys.exit(_run(sys.stdin.buffer,sys.stdout.buffer))
