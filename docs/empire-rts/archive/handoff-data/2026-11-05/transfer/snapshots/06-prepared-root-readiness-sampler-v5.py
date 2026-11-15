# Purpose: prewritten independently reviewed root preparation sampler, no controller import. Date:2026-11-05. Version5: case-insensitive Python and reject unknown exact-target argv.
import json,sys,traceback

def main():
 # Purpose: prewritten root read-only sampler to avoid model drafting during the60s gate. Date:2026-11-05. Version5: case-insensitive Python and reject unknown exact-target argv. Version4: scoped owner parsing, once-only cleanup, full guard parity, held-parent writes.
 # coding: utf-8
 import os,stat,json,hashlib,base64,time,subprocess,re,shlex,resource,sys,math
 from pathlib import Path
 r=Path.cwd();i=r/'work/t17-save-five-mod-inventory-repair-preparation/required-fault-controls-implementation-v1';prep=i/'execution-preparation-v1';v1=i.parent/'required-fault-controls-preparation-v1';run=v1/'execution-v1';d=r/'work/t14-t18-resume-20261104-current';started=time.time();sha=lambda b:hashlib.sha256(b).hexdigest();canon=lambda v:json.dumps(v,ensure_ascii=True,separators=(',',':'),allow_nan=False).encode('ascii');ident=lambda s:[getattr(s,'st_'+k) for k in ['dev','ino','mode','uid','gid','nlink','size','mtime_ns','ctime_ns']]
 os.umask(0o077)
 if not __debug__ or not sys.dont_write_bytecode: raise RuntimeError("ROOT_SAMPLER_MODE")
 if len(sys.argv)!=2 or re.fullmatch("[0-9a-f]{64}",sys.argv[1]) is None: raise ValueError("EXPECTED_GUARD_SHA256_REQUIRED")
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

 def pairs(items):
  out={}
  for k,v in items:assert k not in out;out[k]=v
  return out
 def strict(raw):return json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
 def ab(p):
  p=Path(p);return p if p.is_absolute() else r/p
 def checked(p,size,h):
  b=read(ab(p));assert len(b)==size and sha(b)==h,str(p);return b
 core_raw=read(prep/'capsule-core-v1.json');assert sha(core_raw)=='b75b8b33dad3223a396844e2b53db0a6b0faeffe4ca5ab19b11f8e9233011dd7';core=strict(core_raw);assert canon(core)==core_raw;mp=Path(core['sourceFreeze']['path']);mb=read(mp);assert sha(mb)==core['sourceFreeze']['sha256']=='d69d3456754b19f0592682824c4772c72d62169799fc9c02f0466d8291f951d4';m=strict(mb);physical=[];logical=[]
 for b in m['bindings']:
  p=ab(b['path']);snap=ab(b['snapshot']);effective=p if b['requireCurrentMatchForDesignApproval'] else snap;raw=checked(effective,b['bytes'],b['sha256']);assert raw==checked(snap,b['bytes'],b['sha256']);physical.append(dict(path=str(effective),bytes=len(raw),sha256=sha(raw)))
  if str(p)!=m['historyContainer']['path']:logical.append(dict(path=str(p),bytes=len(raw),sha256=sha(raw)))
 hc=m['historyContainer'];hb=checked(hc['path'],hc['bytes'],hc['sha256']);h=strict(hb);assert canon(h)==hb and len(h['entries'])==53;inv=strict(checked(hc['inventory']['path'],hc['inventory']['bytes'],hc['inventory']['sha256']));checked(hc['schema']['path'],hc['schema']['bytes'],hc['schema']['sha256'])
 for idx,(row,expected) in enumerate(zip(h['entries'],inv['fixedEntries'])):
  assert expected['entryIndex']==idx and expected['historyOnly'] is True and (row['path'],row['bytes'],row['sha256'])==(expected['path'],expected['bytes'],expected['sha256']);assert type(row['bytes']) is int and row['bytes']<=262144;decoded=base64.b64decode(row['bodyBase64'],validate=True);assert base64.b64encode(decoded).decode()==row['bodyBase64'];assert decoded==checked(row['path'],row['bytes'],row['sha256']);logical.append(dict(path=row['path'],bytes=len(decoded),sha256=sha(decoded)))
 physical.sort(key=lambda x:x['path']);logical.sort(key=lambda x:x['path']);assert physical==core['sourceBindings'] and sha(canon(physical))==m['reviewedBindingsSHA256'];assert len(physical)==113 and len(logical)==len(set(x['path'] for x in logical))==165 and sha(canon(logical))==hc['expandedLogicalBindingsSHA256'];assert sum(x['bytes'] for x in physical)==5728239
 ctx=i.parent/'required-fault-controls-context-amendment-v1';cr=read(ctx/'manifest.json');assert sha(cr)=='20e7e2e53967afdce38b7b594c8cedab0e83cbd9aec61fb7af09e5a24a6b914e';cm=strict(cr);assert len(cm['bindings'])==94;total=0
 for b in cm['bindings']:
  checked(ab(b['snapshot']),b['bytes'],b['sha256']);total+=b['bytes']
  if b['requireCurrentMatchForDesignApproval'] and b['path']!='tools/epoch-rts/test-t17-save-five-mod-required-fault-controls.py':checked(ab(b['path']),b['bytes'],b['sha256'])
 assert total==3409262
 for desc in core['sourceReviews']:
  raw=read(desc['path']);assert sha(raw)==desc['sha256'];j=strict(raw);assert j['reviewerRole']==desc['role'] and j['verdict']=='APPROVE_SOURCE_ONLY' and j['inputManifestSHA256']==core['sourceFreeze']['sha256'] and j['reviewedBindingsSHA256']==sha(canon(physical)) and all(j[k]==v for k,v in m['historyContext'].items())
 runtime=[]
 for name,link in [('/Library/Developer/CommandLineTools/usr/bin/python3','../../Library/Frameworks/Python3.framework/Versions/3.9/bin/python3'),('/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3','python3.9')]:
  p=Path(name);fd=parent(p.parent)
  try:
   s=os.stat(p.name,dir_fd=fd,follow_symlinks=False);assert stat.S_ISLNK(s.st_mode) and os.readlink(p.name,dir_fd=fd)==link;assert ident(s)==ident(os.stat(p.name,dir_fd=fd,follow_symlinks=False));runtime.append(dict(path=name,identity=ident(s),rawlink=link))
  except BaseException as primary:
   cleanup([fd],primary)
   raise
  failure=cleanup([fd])
  if failure is not None: raise failure
 p=Path('/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9');b=read(p);assert sha(b)=='6e7ae61f68a3838094fc56590f84c52069a97d7816f6bb79e0e85995b340e464';runtime.append(dict(path=str(p),identity=ident(p.lstat()),bytes=len(b),sha256=sha(b)));assert runtime==core['runtimeRows'];assert absent(run)
 vm=subprocess.run(['/usr/bin/vm_stat'],check=True,stdout=subprocess.PIPE,text=True).stdout;page=int(re.search(r'page size of (\d+) bytes',vm).group(1));counts={k:int(re.search(r'^'+re.escape(k)+r':\s+(\d+)\.',vm,re.M).group(1)) for k in ['Pages free','Pages inactive','Pages speculative']};mem=int(subprocess.run(['/usr/sbin/sysctl','-n','hw.memsize'],check=True,stdout=subprocess.PIPE,text=True).stdout.strip());fs=os.statvfs(v1);resources=dict(availableDiskMin=fs.f_bavail*fs.f_frsize,physicalRAMMin=mem,reclaimableEstimateMin=sum(counts.values())*page,softFDMin=resource.getrlimit(resource.RLIMIT_NOFILE)[0]);assert all(type(resources[k]) is int and resources[k]>=v for k,v in core['resourcePolicy'].items())
 ps=subprocess.run(['/bin/ps','-ww','-axo','pid=,ppid=,command='],check=True,stdout=subprocess.PIPE,text=True).stdout
 owners=[];controller=str(r/'tools/epoch-rts/test-t17-save-five-mod-required-fault-controls.py')
 def relevant(text):
  return 'test-t17-save-five-mod-required-fault-controls' in text or str(run) in text
 simple_flags={'-b','-bb','-B','-d','-E','-h','--help','--help-env','--help-xoptions','--help-all','-i','-I','-O','-OO','-q','-R','-s','-S','-u','-v','-V','--version','-x'}
 def script_argument(argv):
  exe=Path(argv[0]).name.lower()
  if argv[0].endswith('.py'): return argv[0]
  if not re.fullmatch(r'pythonw?(?:\d+(?:\.\d+)*)?',exe):
   # Inspect complete argv tokens only, never substring-grep shell/heredoc code.
   for token in argv[1:]:
    if len(token.encode('utf-8'))<=1024 and (str(ab(token))==controller or Path(token).name==Path(controller).name or str(ab(token)).startswith(str(run)+'/')):
     raise RuntimeError('OWNER_UNKNOWN_INTERPRETER_EXACT_TARGET_ARGV')
   return None
  cursor=1
  while cursor<len(argv):
   token=argv[cursor]
   if token=='--':
    return argv[cursor+1] if cursor+1<len(argv) else None
   if token in ('-W','-X'):
    if cursor+1>=len(argv):
     if relevant(' '.join(argv)): raise RuntimeError('OWNER_OPTION_OPERAND_UNKNOWN')
     return None
    cursor+=2;continue
   if token.startswith('-W') or token.startswith('-X') or token in simple_flags:
    cursor+=1;continue
   if token in ('-c','-m','-'):
    if relevant(' '.join(argv[cursor+1:])): raise RuntimeError('OWNER_INDIRECT_OR_STDIN_SCOPE_UNKNOWN')
    return None
   if token.startswith('-'):
    if relevant(' '.join(argv)): raise RuntimeError('OWNER_UNRECOGNIZED_OPTION_UNKNOWN')
    return None
   return token
  return None
 for line in ps.splitlines():
  match=re.match(r'^\s*(\d+)\s+(\d+)\s+(.+)$',line)
  if not match: continue
  try: argv=shlex.split(match[3])
  except ValueError:
   if relevant(match[3]): raise RuntimeError('OWNER_RELEVANT_ARGV_PARSE_UNKNOWN')
   continue
  if not argv: continue
  script=script_argument(argv)
  if script and (str(ab(script))==controller or Path(script).name==Path(controller).name or str(ab(script)).startswith(str(run)+'/')):
   owners.append(dict(pid=int(match[1]),ppid=int(match[2]),script=script))
 assert owners==[];assert absent(run)
 gp=prep/'freshguard-v1.json';gb=read(gp)
 assert len(sys.argv)==2 and re.fullmatch('[0-9a-f]{64}',sys.argv[1]) and sha(gb)==sys.argv[1]
 guard=strict(gb);now=time.time()
 assert guard['capsuleId']==core['capsuleId'] and type(guard['capsuleId']) is str
 assert guard['runRoot']==str(run) and type(guard['runRoot']) is str
 assert guard['status']=='MATCH' and guard['fixedRootAbsent'] is True and guard['scopedOwnerAbsent'] is True
 assert guard['capsuleCoreSHA256']==sha(core_raw)
 assert canon(guard['sourceBindings'])==canon(physical) and canon(guard['runtimeRows'])==canon(runtime)
 assert canon(guard['resourcePolicy'])==canon(core['resourcePolicy'])
 assert guard['sourceBindingsSHA256']==sha(canon(physical))
 assert guard['sourceFreezeSHA256']==guard['reviewedSourceFreezeSHA256']==core['sourceFreeze']['sha256']
 assert all(type(guard[k]) is type(value) and guard[k]==value for k,value in m['historyContext'].items())
 assert type(guard['resources']) is dict
 assert all(type(guard['resources'][k]) is int and guard['resources'][k]>=value for k,value in core['resourcePolicy'].items())
 checked_time,expires_time=guard['checkedUnixSeconds'],guard['expiresUnixSeconds']
 assert type(checked_time) in (int,float) and type(expires_time) in (int,float) and math.isfinite(checked_time) and math.isfinite(expires_time)
 assert 0<=now-checked_time<=60 and now+120<=expires_time and 120<=expires_time-checked_time<=600
 report=dict(capsuleId=core['capsuleId'],capsuleCoreSHA256=sha(core_raw),sourceBindings=physical,sourceBindingsSHA256=sha(canon(physical)),runtimeRows=runtime,resourcePolicy=core['resourcePolicy'],**m['historyContext'],checkedUnixSeconds=started,expiresUnixSeconds=started+300,runRoot=str(run),sourceFreezeSHA256=core['sourceFreeze']['sha256'],reviewedSourceFreezeSHA256=core['sourceFreeze']['sha256'],status='MATCH',fixedRootAbsent=True,scopedOwnerAbsent=True,resources=resources,sampler=dict(role='ROOT_ACTUAL_INDEPENDENT_SAMPLER',pid=os.getpid(),sourceMethod='held O_DIRECTORY NOFOLLOW parents, regular nlink1 held+named9fieldidentity before/after whole bytes',sourceEffectiveAndSnapshot=113,historyDecodedAndOriginal=53,contextSnapshot94=True,contextUnchangedCurrentExceptSupersededController=True,resourceCommands=['/usr/bin/vm_stat','/usr/sbin/sysctl -n hw.memsize'],reclaimableFormula='pageSize*(free+inactive+speculative), estimate not reservation; purgeable excluded',pageSize=page,pageCounts=counts,ownerMethod='ps -ww argv actual Python/direct script position; consume -W/-X operands; relevant indirect/unknown argv rejects readiness; fullhost scope remains open',psCaptureSHA256=sha(ps.encode()),ownerMatches=owners));assert time.time()-started<=60
 rp=prep/'root-readback-v1.json';prep_fd=parent(prep);primary=None
 try:
  put(rp,canon(report)+b'\n',prep_fd)
  cap=dict(core,rootReadback=dict(path=str(rp),sha256=sha(read(rp))),independentFreshGuard=dict(path=str(gp),sha256=sha(gb)))
  cb=canon(cap);cp=prep/'capsule-v1.json';put(cp,cb,prep_fd)
  assert sha(canon({k:v for k,v in cap.items() if k not in ('rootReadback','independentFreshGuard')}))==sha(core_raw)
 except BaseException as error: primary=error
 primary=cleanup([prep_fd],primary)
 if primary is not None: raise primary
 receipt=dict(schema=1,purpose='Actual current two-sampler capsule gate admission; distinct later execution required',createdUnixSeconds=time.time(),capsulePath=str(cp),capsuleSHA256=sha(cb),capsuleCoreSHA256=sha(core_raw),rootReportSHA256=sha(read(rp)),guardSHA256=sha(gb),guardAgeSeconds=time.time()-guard['checkedUnixSeconds'],rootAgeSeconds=time.time()-started,allThreeSourceApproved=True,source113History53Context94MATCH=True,runtimeMATCH=True,actualResources=resources,actualOwnerMatches=owners,fixedRunRootAbsent=True,distinctLaterExecutionAuthorized=True,caseIds=core['caseIds'],retry=0,scope=core['scope'],formalCases='THREE_NOT_RUN',attempt='NOT_CREATED',boundary='Only three fixed negative source models; no native/official/realOSpermission/fullhost approval')
 q=d/'stage-c-two-sampler-admission-v1.json';put(q,canon(receipt)+b'\n')
 print(json.dumps(receipt,indent=2))

if __name__=='__main__':
 try:
  main()
 except BaseException as error:
  evidence={'status':'ROOT_READINESS_STOP','type':type(error).__name__,'message':str(error),'cleanupUnknown':getattr(error,'cleanupUnknown',[]),'stageCAdmitted':False,'formalControllerInvocation':'NOT_RUN','durability':'NOT_ATTESTED_IF_DIAGNOSTIC_CHANNEL_FAILS'}
  message=json.dumps(evidence,ensure_ascii=True,allow_nan=False,separators=(',',':'))+'\n'
  if len(message.encode('ascii'))>1048576: message='{"status":"ROOT_READINESS_STOP_DIAGNOSTIC_BOUND_UNKNOWN"}\n'
  sys.stderr.write(message);sys.stderr.flush()
  traceback.print_exc()
  raise SystemExit(1)
