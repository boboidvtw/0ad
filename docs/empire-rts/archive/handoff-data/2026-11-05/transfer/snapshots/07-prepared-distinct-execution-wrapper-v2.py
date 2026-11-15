# Purpose: one distinct reviewed controller invocation with retained outer stdout/stderr. Date:2026-11-05. Version2: fresh reports and current time immediately before exec.
import os,stat,json,hashlib,time,sys,re,math,traceback
from pathlib import Path
REPO=Path('/Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/0ad')
IMPL=REPO/'work/t17-save-five-mod-inventory-repair-preparation/required-fault-controls-implementation-v1'
PREP=IMPL/'execution-preparation-v1'
DATA=REPO/'work/t14-t18-resume-20261104-current'
RUN=IMPL.parent/'required-fault-controls-preparation-v1/execution-v1'
LAUNCHER=Path('/Library/Developer/CommandLineTools/usr/bin/python3')
CONTROLLER=REPO/'tools/epoch-rts/test-t17-save-five-mod-required-fault-controls.py'
sha=lambda raw:hashlib.sha256(raw).hexdigest()
canon=lambda obj:json.dumps(obj,ensure_ascii=True,separators=(',',':'),allow_nan=False).encode('ascii')
ident=lambda st:[getattr(st,'st_'+key) for key in ['dev','ino','mode','uid','gid','nlink','size','mtime_ns','ctime_ns']]
def cleanup(fds, primary=None):
 for fd in fds:
  try: os.close(fd)
  except BaseException as error:
   if primary is None: primary=error
   primary.cleanupUnknown=list(getattr(primary,'cleanupUnknown',[]))+[{'fd':fd,'closeAttempts':1,'status':'UNKNOWN','type':type(error).__name__,'message':str(error)}]
 return primary

def parent(p):
 p=Path(p)
 if not p.is_absolute() or '..' in p.parts: raise ValueError('PHYSICAL_ABSOLUTE_PARENT')
 current=os.open('/',os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
 try:
  for part in p.parts[1:]:
   child=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=current)
   previous,current=current,child
   failure=cleanup([previous])
   if failure is not None: raise failure
  return current
 except BaseException as primary:
  cleanup([current],primary)
  raise

def read(p,cap=33554432):
 p=Path(p);fd=parent(p.parent);f=None;primary=None;result=None
 try:
  before=os.stat(p.name,dir_fd=fd,follow_symlinks=False)
  assert stat.S_ISREG(before.st_mode) and before.st_nlink==1 and before.st_size<=cap
  f=os.open(p.name,os.O_RDONLY|os.O_NOFOLLOW,dir_fd=fd)
  assert ident(os.fstat(f))==ident(before)
  buf=[];n=0
  while True:
   chunk=os.read(f,min(65536,cap-n+1))
   if not chunk: break
   n+=len(chunk);assert n<=cap;buf.append(chunk)
  assert ident(os.fstat(f))==ident(before)==ident(os.stat(p.name,dir_fd=fd,follow_symlinks=False))
  result=b''.join(buf)
 except BaseException as error: primary=error
 primary=cleanup(([f] if f is not None else [])+[fd],primary)
 if primary is not None: raise primary
 return result

def absent(p):
 p=Path(p);fd=parent(p.parent);primary=None;missing=False
 try:
  try: os.stat(p.name,dir_fd=fd,follow_symlinks=False)
  except FileNotFoundError: missing=True
  if not missing: raise RuntimeError('FIXED_ROOT_EXISTS')
 except BaseException as error: primary=error
 primary=cleanup([fd],primary)
 if primary is not None: raise primary
 return missing

def put(p,raw,held=None):
 p=Path(p);owned=held is None;directory=parent(p.parent) if owned else held
 f=None;primary=None
 try:
  anchor=os.fstat(directory)
  assert stat.S_ISDIR(anchor.st_mode) and anchor.st_uid==os.getuid() and not (stat.S_IMODE(anchor.st_mode)&0o022)
  current=parent(p.parent);anchor_error=None
  try: assert ident(os.fstat(current))[:2]==ident(anchor)[:2]
  except BaseException as error: anchor_error=error
  anchor_error=cleanup([current],anchor_error)
  if anchor_error is not None: raise anchor_error
  assert type(raw) is bytes and len(raw)<=1048576
  f=os.open(p.name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600,dir_fd=directory)
  view=memoryview(raw)
  while view:
   count=os.write(f,view);assert 0<count<=len(view);view=view[count:]
  os.fsync(f);after=os.fstat(f)
  assert stat.S_ISREG(after.st_mode) and after.st_nlink==1 and after.st_uid==os.getuid() and stat.S_IMODE(after.st_mode)==0o600 and after.st_size==len(raw)
  assert ident(after)==ident(os.stat(p.name,dir_fd=directory,follow_symlinks=False))
 except BaseException as error: primary=error
 primary=cleanup(([f] if f is not None else [])+([directory] if owned else []),primary)
 if primary is not None: raise primary
 assert read(p,1048576)==raw
 os.fsync(directory) if not owned else None


def strict(raw):
 def pairs(items):
  out={}
  for key,value in items:
   if key in out: raise ValueError('DUPLICATE_KEY')
   out[key]=value
  return out
 return json.loads(raw.decode('ascii'),object_pairs_hook=pairs,parse_constant=lambda value:(_ for _ in ()).throw(ValueError(value)))

def main():
 if not __debug__ or not sys.dont_write_bytecode or sys.version_info[:3]!=(3,9,6) or Path(sys.executable)!=LAUNCHER: raise RuntimeError('FIXED_RUNTIME_MODE')
 if len(sys.argv)!=2 or re.fullmatch('[0-9a-f]{64}',sys.argv[1]) is None: raise ValueError('EXPECTED_CAPSULE_SHA256_REQUIRED')
 cp=PREP/'capsule-v1.json';raw=read(cp,1048576)
 if sha(raw)!=sys.argv[1]: raise ValueError('CAPSULE_SHA256')
 cap=strict(raw);core={key:value for key,value in cap.items() if key not in ('rootReadback','independentFreshGuard')}
 if sha(canon(core))!='b75b8b33dad3223a396844e2b53db0a6b0faeffe4ca5ab19b11f8e9233011dd7': raise ValueError('CORE_SHA256')
 if cap['runRoot']!=str(RUN) or cap['retry']!=0 or cap['seed'] is not False: raise ValueError('FIXED_RUN_IDENTITY')
 if sha(read(CONTROLLER))!='fd1948d65cdd57cb851f651128639499f958a59f003707889bfb32e9f6f24e9b': raise ValueError('CURRENT_CONTROLLER_SHA256')
 manifest=REPO/'work/t17-save-five-mod-inventory-repair-preparation/required-fault-controls-implementation-v1/source-context-freeze-v2/manifest.json'
 if sha(read(manifest))!='d69d3456754b19f0592682824c4772c72d62169799fc9c02f0466d8291f951d4': raise ValueError('CURRENT_SOURCE_MANIFEST')
 m=strict(read(manifest));now=time.time()
 for key,name in [('rootReadback','root-readback-v1.json'),('independentFreshGuard','freshguard-v1.json')]:
  desc=cap[key]
  if desc['path']!=str(PREP/name): raise ValueError('REPORT_PATH')
  report_raw=read(desc['path'],1048576)
  if sha(report_raw)!=desc['sha256']: raise ValueError('REPORT_SHA256')
  report=strict(report_raw)
  if report['capsuleId']!=cap['capsuleId'] or report['runRoot']!=str(RUN) or report['status']!='MATCH' or report['fixedRootAbsent'] is not True or report['scopedOwnerAbsent'] is not True: raise ValueError('REPORT_IDENTITY')
  if report['capsuleCoreSHA256']!=sha(canon(core)) or canon(report['sourceBindings'])!=canon(cap['sourceBindings']) or report['sourceBindingsSHA256']!=sha(canon(cap['sourceBindings'])) or canon(report['runtimeRows'])!=canon(cap['runtimeRows']) or canon(report['resourcePolicy'])!=canon(cap['resourcePolicy']): raise ValueError('REPORT_JOINS')
  if report['sourceFreezeSHA256']!=cap['sourceFreeze']['sha256'] or report['reviewedSourceFreezeSHA256']!=cap['sourceFreeze']['sha256'] or not all(type(report[field]) is type(value) and report[field]==value for field,value in m['historyContext'].items()): raise ValueError('REPORT_HISTORY')
  checked,expires=report['checkedUnixSeconds'],report['expiresUnixSeconds']
  if type(checked) not in (int,float) or type(expires) not in (int,float) or not math.isfinite(checked) or not math.isfinite(expires) or not (0<=now-checked<=60 and now+120<=expires and 120<=expires-checked<=600): raise ValueError('REPORT_FRESHNESS')
  if not all(type(report['resources'][field]) is int and report['resources'][field]>=value for field,value in cap['resourcePolicy'].items()): raise ValueError('REPORT_RESOURCES')
 absent(RUN)
 os.umask(0o077);log=DATA/'formal-case-execution-v1';os.mkdir(log,0o700)
 # Only outer evidence; the reviewed controller alone creates original RUN/cases.
 start=dict(schema=1,scope=cap['scope'],capsuleSHA256=sha(raw),startedUnixSeconds=time.time(),startedMonotonic=time.monotonic(),controllerSHA256=sha(read(CONTROLLER)),command=[str(LAUNCHER),'-B',str(CONTROLLER),'--execute-reviewed',str(cp),sha(raw)],retry=0,caseIds=cap['caseIds'],rootSourceNotChanged=True)
 put(log/'outer-start-v1.json',canon(start)+b'\n')
 parent_fd=parent(log);fds=[];primary=None
 try:
  out=os.open('stdout.raw',os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600,dir_fd=parent_fd);fds.append(out)
  err=os.open('stderr.raw',os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600,dir_fd=parent_fd);fds.append(err)
  sys.stdout.flush();sys.stderr.flush();os.dup2(out,1);os.dup2(err,2)
 except BaseException as error: primary=error
 primary=cleanup(fds+[parent_fd],primary)
 if primary is not None: raise primary
 # Re-read both exact reports after every log/stream/fsync/close operation.
 final_reports=[]
 for key in ('rootReadback','independentFreshGuard'):
  desc=cap[key];fresh_raw=read(desc['path'],1048576)
  if sha(fresh_raw)!=desc['sha256']: raise ValueError('FINAL_REPORT_CHANGED')
  final_reports.append(strict(fresh_raw))
 absent(RUN)
 final_now=time.time()
 for report in final_reports:
  checked,expires=report['checkedUnixSeconds'],report['expiresUnixSeconds']
  if type(checked) not in (int,float) or type(expires) not in (int,float) or not math.isfinite(checked) or not math.isfinite(expires) or not (0<=final_now-checked<=60 and final_now+120<=expires and 120<=expires-checked<=600): raise ValueError('FINAL_PRE_EXEC_FRESHNESS_STOP')
 # No more file/probe/diagnostic operations between final clock check and exec.
 # Replace this same process; no Popen/Node/extra case or second controller.
 os.execv(str(LAUNCHER),start['command'])

if __name__=='__main__':
 try: main()
 except BaseException as error:
  record={'status':'OUTER_EXECUTION_PREFLIGHT_OR_EXEC_UNKNOWN_STOP','type':type(error).__name__,'message':str(error),'cleanupUnknown':getattr(error,'cleanupUnknown',[]),'retry':0,'durability':'NOT_ATTESTED_IF_CHANNEL_FAILS'}
  message=json.dumps(record,ensure_ascii=True,allow_nan=False,separators=(',',':'))+'\n'
  if len(message.encode('ascii'))>1048576: message='{"status":"OUTER_DIAGNOSTIC_BOUND_UNKNOWN"}\n'
  sys.stderr.write(message);sys.stderr.flush();traceback.print_exc();raise SystemExit(1)
