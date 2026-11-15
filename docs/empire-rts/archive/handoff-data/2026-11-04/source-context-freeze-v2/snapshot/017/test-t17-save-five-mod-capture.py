# Purpose: retained synthetic host-file controls for NEW capture; no official archive/native run.
# Created: 2026-10-25. SPDX-License-Identifier: GPL-2.0-or-later
import unittest,importlib.util,sys,os,hashlib,time,io,zipfile,json
from pathlib import Path
from unittest import mock
ROOT=Path(__file__).resolve().parents[2]
PREP=ROOT/'work/t17-save-five-mod-inventory-repair-preparation/joint-source-fix-v1/python'
RUN=PREP/('cases-'+str(time.time_ns()));RUN.mkdir(mode=0o700)
spec=importlib.util.spec_from_file_location('five_capture',Path(__file__).with_name('t17-save-five-mod-capture.py'))
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m
try:spec.loader.exec_module(m)
except FileNotFoundError:m=None
class Tests(unittest.TestCase):
 def setUp(self):
  self.root=RUN/self._testMethodName;self.root.mkdir(mode=0o700);self.fds=[]
 def tearDown(self):
  for fd in self.fds:os.close(fd)
 def file(self,data,name='source.bin'):
  p=self.root/name
  fd=os.open(p,os.O_CREAT|os.O_EXCL|os.O_RDWR,0o600);self.fds.append(fd);os.write(fd,data);return p,fd
 def reader(self,data):
  p,fd=self.file(data);return p,fd,m.AuthenticatedReader(fd,hashlib.sha256(data).hexdigest(),m.Deadline())
 def test_archive_held_fd_replacement(self):
  self.assertIsNotNone(m);data=b'A'*(m.CHUNK+31);p,fd,r=self.reader(data)
  other=self.root/'replacement';other.write_bytes(b'B'*len(data));p.rename(self.root/'original');other.rename(p)
  self.assertEqual(r.read(20),b'A'*20)
 def test_archive_uncached_inplace_rejects(self):
  p,fd,r=self.reader(b'A'*(m.CHUNK+31));os.pwrite(fd,b'B',m.CHUNK)
  r.seek(m.CHUNK)
  with self.assertRaises(m.CaptureError):r.read(1)
 def test_crosschunk_and_partial(self):
  data=b'a'*(m.CHUNK-3)+b'XYZ123';p,fd,r=self.reader(data);r.seek(m.CHUNK-3);self.assertEqual(r.read(6),b'XYZ123')
 def test_cache_is_immutable_authority(self):
  p,fd,r=self.reader(b'A'*50);self.assertEqual(r.read(1),b'A');os.pwrite(fd,b'B',1);self.assertEqual(r.read(1),b'A')
 def test_seek_whence_eof_and_size_limit(self):
  p,fd,r=self.reader(b'abcdef');self.assertEqual(r.seek(-2,2),4);self.assertEqual(r.read(),b'ef');self.assertEqual(r.read(),b'')
  for offset,whence in ((-1,0),(7,0),(0,99)):
   with self.assertRaises(m.CaptureError):r.seek(offset,whence)
 def test_wrongsha_shortpread_and_exception(self):
  p,fd=self.file(b'abc')
  with self.assertRaises(m.CaptureError):m.AuthenticatedReader(fd,'0'*64,m.Deadline())
  with mock.patch.object(m.os,'pread',return_value=b'a'):
   with self.assertRaises(m.CaptureError):m.AuthenticatedReader(fd,hashlib.sha256(b'abc').hexdigest(),m.Deadline())
 def test_zip64_small_and_unsafe_names(self):
  b=io.BytesIO()
  with zipfile.ZipFile(b,'w',compression=zipfile.ZIP_DEFLATED,allowZip64=True) as z:
   with z.open('mod.json','w',force_zip64=True) as f:f.write(b'{}')
  p,fd,r=self.reader(b.getvalue())
  with m.open_zip(r) as z:self.assertEqual(z.read('mod.json'),b'{}');m.validate_zip(z)
  for name in ('../x','/x','a//b','a\\b','C:x','a\0b'):
   with self.assertRaises(m.CaptureError):m.safe_vfs(name)
 def test_output_exclusive_and_symlink_parent(self):
  o=m.Output(self.root,'one',m.Deadline());o.write('inventory.json',b'prior')
  with self.assertRaises(m.CaptureError):o.write('inventory.json',b'changed')
  self.assertEqual((self.root/'one/inventory.json').read_bytes(),b'prior');o.close()
  with self.assertRaises(m.CaptureError):m.Output(self.root,'one',m.Deadline())
  (self.root/'link').symlink_to(self.root/'one',target_is_directory=True)
  with self.assertRaises(m.CaptureError):m.Output(self.root/'link','two',m.Deadline())
 def test_json_duplicate_depth_bool_and_schema(self):
  with self.assertRaises(m.CaptureError):m.strict_json(b'{"v":1,"v":1}')
  with self.assertRaises(m.CaptureError):m.strict_json(b'['*129+b']'*129)
  with self.assertRaises(m.CaptureError):m.validate_schema({'v':True,'kind':'FINISH','captureId':'a'*64,'analyses':[],'tool':{'nodeVersion':'v1','acornVersion':'1','nodeSourceSHA256':'b'*64}})
 def test_deadline_backward_and_after_io(self):
  with mock.patch.object(m.time,'monotonic_ns',side_effect=[100,99]):
   d=m.Deadline()
   with self.assertRaises(m.CaptureError):d.check()
 def test_terminal_begin_original_bytes_once(self):
  raw=b'{ "outputLeaf" : "one", "kind":"BEGIN", "v":1 }\n'
  protocol=m.Protocol(io.BytesIO(raw),io.BytesIO(),m.Deadline());value=protocol.receive()
  output=m.Output(self.root,'one',protocol.d);protocol.attach(output)
  self.assertEqual((self.root/'one/protocol-input.ndjson').read_bytes(),raw)
  self.assertEqual(protocol.rawtotal,len(raw));output.close()
 def test_terminal_fixed_launcher_chain(self):
  record=m.runtime_context(m.Deadline())
  self.assertEqual(record['launcher']['targetSHA256'],'6e7ae61f68a3838094fc56590f84c52069a97d7816f6bb79e0e85995b340e464')
  self.assertEqual(len(record['launcher']['hops']),2)
  self.assertEqual(record['authority'],'OBSERVED_RUNTIME_DEPENDENCIES_NOT_EXECUTION_ATTESTATION')
 def test_terminal_primary_and_final_close_unknown(self):
  node=self.root/'node.cjs';node.write_bytes(b'controlled node source')
  stdout=io.BytesIO();stderr=io.StringIO();realclose=m.Output.close;calls=[]
  def closing(output):
   realclose(output);calls.append(1)
   error=m.CaptureError('RESOURCE_CLOSE_UNKNOWN');error.unknown_fds=[123];raise error
  with mock.patch.object(m,'OUTPUT_PARENT',self.root/'captures'),mock.patch.object(m,'NODE_PATH',node),mock.patch.object(m,'NODE_SOURCE_EXPECTED',m.sha(node.read_bytes())),mock.patch.object(m,'runtime_context',side_effect=m.CaptureError('SOURCE_CHANGED')),mock.patch.object(m.Output,'close',closing),mock.patch.object(m.sys,'stderr',stderr):
   result=m._run(io.BytesIO(b'{"v":1,"kind":"BEGIN","outputLeaf":"one"}\n'),stdout)
  frames=[json.loads(line) for line in stdout.getvalue().splitlines()]
  self.assertEqual(result,1);self.assertEqual(calls,[1]);self.assertEqual(frames[-1]['code'],'SOURCE_CHANGED')
  self.assertIs(frames[-1]['durableFault'],False)
  self.assertIn('RESOURCE_CLOSE_UNKNOWN',stderr.getvalue())
  snapshot=json.loads((self.root/'captures/one/fault.json').read_bytes())
  self.assertIs(snapshot['outputCleanupComplete'],False)
  self.assertFalse((self.root/'captures/one/completed.json').exists())
 def finish_value(self,body=b'',vfs='mod.json',analysis=None):
  row={'index':0,'vfs':vfs,'sha256':m.sha(body)}
  finish={'v':1,'kind':'FINISH','captureId':'a'*64,'analyses':[{'index':0,'sha256':row['sha256'],'analysis':analysis}],'tool':{'nodeVersion':'v26.0.0','acornVersion':'8.16.0','nodeSourceSHA256':'b'*64}}
  return finish,[row],[body]
 def test_protocol_finish_exact_null_correlations(self):
  f,rows,bodies=self.finish_value();m.validate_finish(f,'a'*64,rows,bodies)
  import copy
  for mutate in (lambda v:v.update(captureId='c'*64),lambda v:v['analyses'][0].update(index=1),lambda v:v['analyses'][0].update(sha256='c'*64),lambda v:v.update(outputLeaf='injected'),lambda v:v['tool'].update(nodeVersion=True),lambda v:v.update(analyses=[])):
   bad=copy.deepcopy(f);mutate(bad)
   with self.assertRaises(m.CaptureError):m.validate_finish(bad,'a'*64,rows,bodies)
 def test_protocol_finish_utf8_and_variant_exactness(self):
  a={'vfs':'x.js','parseStatus':'BLOCK_UTF8_ERROR','closure':'OPEN_INVALID_SOURCE_ENCODING'}
  f,rows,bodies=self.finish_value(b'\xff','x.js',a);m.validate_finish(f,'a'*64,rows,bodies)
  for body in (b'valid',b'\xef\xbb\xbfvalid'):
   with self.assertRaises(m.CaptureError):m.validate_finish(f,'a'*64,rows,[body])
  f['analyses'][0]['analysis']['error']='must not be optional'
  with self.assertRaises(m.CaptureError):m.validate_finish(f,'a'*64,rows,bodies)
 def test_protocol_finish_utf16_boundaries_and_name_shapes(self):
  import copy
  text='function f(){/*😀*/}\r\n';body=text.encode();end=m.u16(text)-2
  analysis={'vfs':'x.js','parseStatus':'PARSED','mode':'script','functions':[{'name':'f','line':1,'endLine':1,'params':[],'start':0,'end':end}],'calls':[],'writerSites':[],'aliases':[],'assignments':[],'fileTopLevelDeclarations':[{'kind':'function','name':'f','line':1}],'closure':'OPEN_REQUIRES_POSITIVE_SEMANTIC_CALLER_PROOF'}
  f,rows,bodies=self.finish_value(body,'x.js',analysis);m.validate_finish(f,'a'*64,rows,bodies)
  for field,value in (('start',m.u16('function f(){/*')+1),('end',m.u16(text)-1),('endLine',2),('end',0)):
   bad=copy.deepcopy(f);bad['analyses'][0]['analysis']['functions'][0][field]=value
   with self.assertRaises(m.CaptureError):m.validate_finish(bad,'a'*64,rows,bodies)
 def test_protocol_real_zip_nul_and_duplicate(self):
  b=io.BytesIO()
  with zipfile.ZipFile(b,'w') as z:z.writestr('axb',b'{}')
  p,fd,r=self.reader(b.getvalue().replace(b'axb',b'a\0b'))
  with m.open_zip(r) as z:
   self.assertNotEqual(z.infolist()[0].orig_filename,z.infolist()[0].filename)
   with self.assertRaises(m.CaptureError):m.validate_zip(z)
  duplicate=io.BytesIO()
  with zipfile.ZipFile(duplicate,'w') as z:z.writestr('mod.json',b'{}');z.writestr('mod.json',b'{}')
  p,fd=self.file(duplicate.getvalue(),'duplicate.zip');r=m.AuthenticatedReader(fd,m.sha(duplicate.getvalue()),m.Deadline())
  with m.open_zip(r) as z:
   with self.assertRaises(m.CaptureError):m.validate_zip(z)
 def test_protocol_output_shortwrite_and_fsync_partials(self):
  for label in ('short','fsync'):
   output=m.Output(self.root,label,m.Deadline());real=m.os.write
   def short(fd,data):return real(fd,data[:1])
   patch=mock.patch.object(m.os,'write',side_effect=short) if label=='short' else mock.patch.object(m.os,'fsync',side_effect=OSError('controlled fsync fault'))
   with patch:
    with self.assertRaises(m.CaptureError):output.write('inventory.json',b'partial retained')
   self.assertTrue((self.root/label/'inventory.json').exists());self.assertFalse((self.root/label/'completed.json').exists());output.close()
 def test_protocol_raw_sent_fault_exact_after_close_unknown(self):
  node=self.root/'node.cjs';node.write_bytes(b'controlled node source');stdout=io.BytesIO();realclose=m.Output.close
  def closing(output):realclose(output);raise m.CaptureError('RESOURCE_CLOSE_UNKNOWN')
  with mock.patch.object(m,'OUTPUT_PARENT',self.root/'captures'),mock.patch.object(m,'NODE_PATH',node),mock.patch.object(m,'NODE_SOURCE_EXPECTED',m.sha(node.read_bytes())),mock.patch.object(m,'runtime_context',side_effect=m.CaptureError('SOURCE_CHANGED')),mock.patch.object(m.Output,'close',closing),mock.patch.object(m.sys,'stderr',io.StringIO()):
   self.assertEqual(m._run(io.BytesIO(b'{ "outputLeaf":"one", "v":1,"kind":"BEGIN" }\n'),stdout),1)
  self.assertEqual((self.root/'captures/one/protocol-output.ndjson').read_bytes(),stdout.getvalue())
  self.assertEqual(json.loads(stdout.getvalue())['durableFault'],False)
 def test_protocol_depth_utf8_and_no_output_override(self):
  for raw in (b'{"x":"\xff"}',b'{"x":NaN}',b'{"x":Infinity}',b'{"x":1,"x":2}',b'['*129+b']'*129):
   with self.assertRaises(m.CaptureError):m.strict_json(raw)
  stdout=io.BytesIO()
  with mock.patch.object(m.sys,'stderr',io.StringIO()):
   self.assertEqual(m._run(io.BytesIO(b'{"v":1,"kind":"BEGIN","outputLeaf":"one","expectedSHA":"fake"}\n'),stdout),1)
  self.assertIs(json.loads(stdout.getvalue())['durableFault'],False)
 def test_ledger_archive_partial_actual_fault_artifact(self):
  node=self.root/'node.cjs';node.write_bytes(b'controlled node');archive=self.root/'small.bin';archive.write_bytes(b'not official archive')
  stdout=io.BytesIO()
  with mock.patch.object(m,'OUTPUT_PARENT',self.root/'captures'),mock.patch.object(m,'NODE_PATH',node),mock.patch.object(m,'NODE_SOURCE_EXPECTED',m.sha(node.read_bytes())),mock.patch.object(m,'ARCHIVE_PATH',archive),mock.patch.object(m,'runtime_context',return_value={'synthetic':True}),mock.patch.object(m.sys,'stderr',io.StringIO()):
   self.assertEqual(m._run(io.BytesIO(b'{"v":1,"kind":"BEGIN","outputLeaf":"one"}\n'),stdout),1)
  artifact=json.loads((self.root/'captures/one/archive-auth.json').read_bytes())
  self.assertEqual(artifact['status'],'PARTIAL');self.assertEqual(artifact['actualSHA'],m.sha(archive.read_bytes()))
  self.assertEqual(artifact['bytesScanned'],len(archive.read_bytes()))
  self.assertFalse((self.root/'captures/one/completed.json').exists())
 def test_ledger_source_read_failure_closes_owned_fd(self):
  root=self.root/'loose';root.mkdir();(root/'mod.json').write_bytes(b'{}');capture=m.Capture(m.Deadline());opened=[];real=m.os.open
  def op(name,*args,**kwargs):
   fd=real(name,*args,**kwargs)
   if name=='mod.json':opened.append(fd)
   return fd
  output=m.Output(self.root,'owned-read-fault',m.Deadline())
  try:
   with mock.patch.object(m.os,'open',side_effect=op):capture.loose_layer('model',root)
   with mock.patch.object(m.os,'pread',side_effect=m.CaptureError('SOURCE_CHANGED')):
    with self.assertRaises(m.CaptureError):capture.capture_candidate(output,'model',{'vfs':'mod.json','bytes':2})
  finally:output.close()
  capture.close();self.assertEqual(len(opened),1)
  with self.assertRaises(OSError):os.fstat(opened[0])
 def test_ledger_capture_close_unknown_all_once(self):
  capture=m.Capture(m.Deadline());fds=[]
  for n in range(2):
   p=self.root/('fd-'+str(n));fd=os.open(p,os.O_CREAT|os.O_EXCL|os.O_RDWR,0o600);fds.append(fd);capture.loose.append((fd,None,None,None,None))
  actual=m.os.close;calls=[]
  def close(fd):calls.append(fd);actual(fd);raise OSError('uncertain close after actual close')
  with mock.patch.object(m.os,'close',side_effect=close):
   with self.assertRaises(m.CaptureError) as caught:capture.close()
   capture.close()
  self.assertEqual(calls,fds);self.assertEqual(caught.exception.unknown_fds,fds)
 def test_protocol_extra_buffer_and_eof(self):
  protocol=m.Protocol(io.BytesIO(b'{"v":1}\n{"v":2}\n'),io.BytesIO(),m.Deadline());protocol.receive()
  with self.assertRaises(m.CaptureError):protocol.ensure_no_extra()
  for raw in (b'',b'{"v":1}'):
   with self.assertRaises(m.CaptureError):m.Protocol(io.BytesIO(raw),io.BytesIO(),m.Deadline()).receive()
 def test_protocol_runtime_link_unknown_not_followed(self):
  original=m.os.readlink
  def altered(path,*args,**kwargs):
   value=original(path,*args,**kwargs)
   return 'unapproved-target' if path=='python3' else value
  with mock.patch.object(m.os,'readlink',side_effect=altered):
   with self.assertRaises(m.CaptureError):m.fixed_launcher(m.Deadline())

# Purpose: amendment-v2 RED-first controls, physical tiny fixtures unless labelled model.
# Added: 2026-10-26. No child process, official archive, or engine execution.
class Preservation(unittest.TestCase):
 def setUp(self):
  self.root=RUN/self._testMethodName;self.root.mkdir(mode=0o700);self.cap=None;self.out=None;self.stack=__import__('contextlib').ExitStack();self.layerdata=None
 def tearDown(self):
  if self.cap:self.cap.close()
  if self.out:self.out.close()
  self.stack.close()
 def fixture(self,public=None,overrides=None):
  public={'mod.json':b'public'} if public is None else public
  overrides=[{'mod.json':('mod'+str(i)).encode()} for i in range(4)] if overrides is None else overrides
  archive=self.root/'tiny.zip'
  with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
   for name,body in public.items():z.writestr(name,body)
  roots=[]
  for i,items in enumerate(overrides):
   root=self.root/('root'+str(i));root.mkdir();roots.append(('mod'+str(i),str(root)))
   for name,body in items.items():
    p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(body)
  for key,value in (('ARCHIVE_PATH',archive),('ARCHIVE_SHA',m.sha(archive.read_bytes())),('ROOTS',tuple(roots))):self.stack.enter_context(mock.patch.object(m,key,value))
  self.layerdata=[public]+overrides;return roots
 def build(self):
  self.out=m.Output(self.root,'case',m.Deadline());self.cap=m.Capture(self.out.d)
  return self.cap.build(self.out)
 def verify(self,captured,bodies):self.cap.verify_preservation(self.out,captured,bodies)
 def test_P01_all_layers_roundtrip(self):
  v='simulation/helpers/same.js';self.fixture({'mod.json':b'public',v:b'lower'},[{'mod.json':str(i).encode(),v:('upper'+str(i)).encode()} for i in range(4)])
  captured,bodies=self.build();self.verify(captured,bodies)
  self.assertEqual(len(captured['layers']),5)
  for layer,items in zip(captured['layers'],self.layerdata):
   for name,body in items.items():self.assertEqual((self.root/'case/layer-sources'/layer['name']/name).read_bytes(),body)
  self.assertEqual(bodies[[r['vfs'] for r in captured['selected']].index(v)],b'upper3')
  self.assertEqual(len(captured['selected'][1]['shadowed']),4)
 def test_P02_archive_aggregate_selected_only_model(self):
  # Explicit scaled limit model: 67 bytes -> 64-byte override; real physical tiny ZIP.
  v='simulation/helpers/a.js';self.fixture({'mod.json':b'',v:b'a'*67},[{'mod.json':b'',v:b'b'*64}]+[{'mod.json':b''}]*3)
  self.stack.enter_context(mock.patch.object(m,'TOTAL_MAX',64));c,b=self.build();self.assertEqual(sum(map(len,b)),64);self.verify(c,b)
 def test_P03_selected_file_metadata_edges_model(self):
  # Independent scaled constants; no claim measured actual64MiB/8MiB boundary.
  for label,length,limit in (('edge',8,8),('over',9,8)):
   with self.subTest(label=label):
    root=self.root/label;root.mkdir();o=m.Output(root,'case',m.Deadline());c=m.Capture(o.d)
    try:
     with mock.patch.object(m,'FILE_MAX',limit):
      p=root/'body';p.write_bytes(b'x'*length);fd=os.open(p,os.O_RDONLY)
      try:
       if label=='edge':self.assertEqual(len(m.read_source_fd(fd,os.fstat(fd),o.d)),8)
       else:
        with self.assertRaises(m.CaptureError):m.read_source_fd(fd,os.fstat(fd),o.d)
      finally:os.close(fd)
    finally:c.close();o.close()
  self.fixture({'mod.json':b''},[{'mod.json':b'aa'}]*4)
  self.stack.enter_context(mock.patch.object(m,'FILE_MAX',8));self.stack.enter_context(mock.patch.object(m,'METADATA_MAX',8));self.stack.enter_context(mock.patch.object(m,'TOTAL_MAX',8))
  c,b=self.build();self.verify(c,b);self.assertEqual(sum(r['bytes'] for l in c['layers'] for r in l['entries'] if r['vfs']=='mod.json'),8)
 def test_P04_lower_layers_no_aggregate_model(self):
  v='simulation/helpers/a.js';self.fixture({'mod.json':b'',v:b'a'*63},[{'mod.json':b'',v:b'b'*63}]*3+[{'mod.json':b'',v:b'c'}])
  self.stack.enter_context(mock.patch.object(m,'TOTAL_MAX',64));c,b=self.build();self.verify(c,b)
  self.assertGreater(sum(r['bytes'] for l in c['layers'] for r in l['entries']),64)
 def test_P05_corruption_relation_controls(self):
  import copy
  self.fixture();c,b=self.build();self.verify(c,b)
  for mutation in ('missing','duplicate','wrongmod','size','sha','selected','shadowed'):
   bad=copy.deepcopy(c)
   if mutation=='missing':bad['layers'][0]['entries']=[]
   elif mutation=='duplicate':bad['layers'][0]['entries']*=2
   elif mutation=='wrongmod':bad['layers'][0]['name']='wrong'
   elif mutation in ('size','sha'):bad['layers'][0]['entries'][0]['bytes' if mutation=='size' else 'sha256']=123 if mutation=='size' else 'f'*64
   elif mutation=='selected':bad['selected'][0]['sha256']='f'*64
   else:bad['selected'][0]['shadowed'][0]['sha256']='f'*64
   with self.subTest(mutation=mutation),self.assertRaises(m.CaptureError):self.verify(bad,b)
  path=self.root/'case/layer-sources/public/mod.json';path.write_bytes(b'broken')
  with self.assertRaises(m.CaptureError):self.verify(c,b)
 def test_P06_original_mutation_never_substitutes(self):
  roots=self.fixture();c,b=self.build();before=b[0];Path(roots[-1][1],'mod.json').write_bytes(b'mutated')
  self.assertEqual(b[0],before);self.assertEqual((self.root/'case/layer-sources/mod3/mod.json').read_bytes(),before)
  with self.assertRaises(m.CaptureError):self.cap.recheck()
 def test_P07_live_body_retention_and_requests(self):
  # Changed streaming dependency: full internal frame tracing replaces the
  # historical returned-wrapper-only observation (5b1242 preimage retained).
  SourceFix.test_FIX_phaseA_internal_allocations(self)
 def test_P08_layer_collision_and_write_faults(self):
  self.fixture();self.out=m.Output(self.root,'case',m.Deadline());self.cap=m.Capture(self.out.d)
  self.out.write('layer-sources/public/mod.json',b'preserved collision')
  with self.assertRaises(m.CaptureError):self.cap.build(self.out)
  self.assertEqual((self.root/'case/layer-sources/public/mod.json').read_bytes(),b'preserved collision')
  self.assertFalse((self.root/'case/completed.json').exists())
 def test_P09_post_FINISH_terminal_source_change(self):
  roots=self.fixture();node=self.root/'node.cjs';node.write_bytes(b'controlled node');stdout=io.BytesIO();realreceive=m.Protocol.receive
  def receive(protocol):
   if not stdout.getvalue():return realreceive(protocol)
   captured=[json.loads(x) for x in stdout.getvalue().splitlines() if json.loads(x)['kind']=='CAPTURED'][0]
   Path(roots[-1][1],'mod.json').write_bytes(b'changed during analysis')
   return {'v':1,'kind':'FINISH','captureId':captured['captureId'],'analyses':[{'index':r['index'],'sha256':r['sha256'],'analysis':None} for r in captured['selected']],'tool':{'nodeVersion':'v26.0.0','acornVersion':'8.16.0','nodeSourceSHA256':m.sha(node.read_bytes())}}
  with mock.patch.object(m,'OUTPUT_PARENT',self.root/'captures'),mock.patch.object(m,'NODE_PATH',node),mock.patch.object(m,'NODE_SOURCE_EXPECTED',m.sha(node.read_bytes())),mock.patch.object(m,'runtime_context',return_value={'model':True}),mock.patch.object(m.Protocol,'receive',receive),mock.patch.object(m.sys,'stderr',io.StringIO()):
   self.assertEqual(m._run(io.BytesIO(b'{"v":1,"kind":"BEGIN","outputLeaf":"one"}\n'),stdout),1)
  self.assertEqual(json.loads(stdout.getvalue().splitlines()[-1])['code'],'SOURCE_CHANGED');self.assertFalse((self.root/'captures/one/completed.json').exists())


class Required(unittest.TestCase):
 setUp=Preservation.setUp
 tearDown=Preservation.tearDown
 fixture=Preservation.fixture
 build=Preservation.build
 verify=Preservation.verify
 def test_P03_selected_one_over_and_metadata_over_model(self):
  v='simulation/helpers/a.js';self.fixture({'mod.json':b'',v:b'x'*9},[{'mod.json':b''}]*4)
  with mock.patch.object(m,'TOTAL_MAX',8):
   with self.assertRaises(m.CaptureError):self.build()
  self.assertTrue((self.root/'case/layer-sources/public'/v).exists());self.assertFalse((self.root/'case/completed.json').exists())
 def test_P03_metadata_one_over_before_capture_model(self):
  self.fixture({'mod.json':b'a'},[{'mod.json':b'aa'}]*4)
  with mock.patch.object(m,'METADATA_MAX',8):
   with self.assertRaises(m.CaptureError):self.build()
  self.assertFalse((self.root/'case/layer-sources').exists())
 def test_P05_physical_missing_extra_size_sha_nlink(self):
  self.fixture();c,b=self.build();self.verify(c,b)
  path=self.root/'case/layer-sources/public/mod.json'
  original=path.read_bytes();held=self.root/'held';path.rename(held)
  with self.assertRaises(m.CaptureError):self.verify(c,b)
  held.rename(path);self.verify(c,b)
  extra=path.parent/'extra.js';extra.write_bytes(b'unrecorded')
  with self.assertRaises(m.CaptureError):self.verify(c,b)
  extra.rename(self.root/'extra-retained')
  os.link(path,self.root/'second-link')
  with self.assertRaises(m.CaptureError):self.verify(c,b)
  self.assertEqual(path.read_bytes(),original)
 def test_P08_short_fsync_close_enospc_and_final_readback(self):
  for label in ('short','fsync','close','enospc'):
   with self.subTest(label=label):
    parent=self.root/label;parent.mkdir();output=m.Output(parent,'case',m.Deadline());realwrite=m.os.write;realclose=m.os.close
    name='layer-sources/public/mod.json';patch=None
    if label=='short':patch=mock.patch.object(m.os,'write',side_effect=lambda fd,data:realwrite(fd,data[:1]))
    elif label=='fsync':patch=mock.patch.object(m.os,'fsync',side_effect=OSError('fsync model'))
    elif label=='enospc':
     import errno
     patch=mock.patch.object(m.os,'write',side_effect=OSError(errno.ENOSPC,'ENOSPC model'))
    else:
     def uncertain(fd):
      regular=__import__('stat').S_ISREG(os.fstat(fd).st_mode);realclose(fd)
      if regular:raise OSError('uncertain close after actual close')
     patch=mock.patch.object(m.os,'close',side_effect=uncertain)
    try:
     with patch:
      with self.assertRaises(m.CaptureError):output.write(name,b'preserved partial')
     self.assertTrue((parent/'case'/name).exists());self.assertNotIn(name,output.hashes);self.assertFalse((parent/'case/completed.json').exists())
    finally:output.close()
  self.fixture();c,b=self.build();target=self.root/'case/layer-sources/public/mod.json';raw=target.read_bytes();target.write_bytes(raw[:-1])
  with self.assertRaises(m.CaptureError):self.verify(c,b)
 def test_R02_concurrent_root_and_every_artifact_exclusive(self):
  import concurrent.futures
  def reserve(_):
   try:
    o=m.Output(self.root,'race',m.Deadline());o.close();return 'won'
   except m.CaptureError as error:return error.code
  with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(reserve,range(2)))
  self.assertEqual(sorted(results),['OUTPUT_EXISTS','won'])
  o=m.Output(self.root,'files',m.Deadline())
  try:
   names=['effective/mod.json','layer-metadata/public/mod.json','layer-sources/public/mod.json','archive-auth.json','capture-inputs.json','protocol-input.ndjson','protocol-output.ndjson','diagnostics.ndjson','inventory.json','layer-inputs.json','writer-sites.json','manifest.json','completed.json','fault.json']
   for name in names:
    o.write(name,b'sentinel')
    with self.assertRaises(m.CaptureError):o.write(name,b'overwrite')
    self.assertEqual((self.root/'files'/name).read_bytes(),b'sentinel')
  finally:o.close()
 def test_R03_ABA_forged_metadata_and_restore(self):
  p=self.root/'archive';data=b'a'*(m.CHUNK+9);p.write_bytes(data);fd=os.open(p,os.O_RDWR)
  try:
   r=m.AuthenticatedReader(fd,m.sha(data),m.Deadline());other=self.root/'B';other.write_bytes(b'B'*len(data));a=self.root/'A';p.rename(a);other.rename(p);p.rename(other);a.rename(p)
   self.assertEqual(r.read(3),b'aaa');before=os.fstat(fd);os.pwrite(fd,b'B',m.CHUNK);r.seek(m.CHUNK)
   with mock.patch.object(m.os,'fstat',return_value=before):
    with self.assertRaises(m.CaptureError):r.read(1)
   os.pwrite(fd,b'a',m.CHUNK);self.assertEqual(r.read(1),b'a')
  finally:os.close(fd)
 def test_R04_truncate_interrupt_and_no_path_bypass(self):
  data=b'a'*(m.CHUNK+17);path=self.root/'archive';path.write_bytes(data);fd=os.open(path,os.O_RDWR)
  try:
   with mock.patch.object(m.os,'pread',side_effect=InterruptedError('controlled')):
    with self.assertRaises(m.CaptureError):m.AuthenticatedReader(fd,m.sha(data),m.Deadline())
   r=m.AuthenticatedReader(fd,m.sha(data),m.Deadline());os.ftruncate(fd,m.CHUNK+1);r.seek(m.CHUNK)
   with self.assertRaises(m.CaptureError):r.read(1)
  finally:os.close(fd)
  path2=self.root/'during';path2.write_bytes(data);fd=os.open(path2,os.O_RDWR);realpread=m.os.pread;calls=[]
  def read(source,size,offset):
   calls.append((source,size,offset));raw=realpread(source,size,offset)
   if offset==0:os.ftruncate(source,1)
   return raw
  try:
   with mock.patch.object(m.os,'pread',side_effect=read):
    with self.assertRaises(m.CaptureError):m.AuthenticatedReader(fd,m.sha(data),m.Deadline())
   self.assertTrue(all(source==fd and size<=m.CHUNK for source,size,_ in calls))
  finally:os.close(fd)
 def test_R05_real_stored_deflated_crc_and_entry_gates(self):
  for method in (zipfile.ZIP_STORED,zipfile.ZIP_DEFLATED):
   raw=io.BytesIO()
   with zipfile.ZipFile(raw,'w',compression=method) as z:z.writestr('mod.json',b'body')
   p=self.root/str(method);p.write_bytes(raw.getvalue());fd=os.open(p,os.O_RDONLY)
   try:
    r=m.AuthenticatedReader(fd,m.sha(raw.getvalue()),m.Deadline())
    with m.open_zip(r) as z:m.validate_zip(z);self.assertEqual(z.read('mod.json'),b'body')
   finally:os.close(fd)
  for kind in ('symlink','device','method','size','count'):
   info=zipfile.ZipInfo('mod.json');info.external_attr=(__import__('stat').S_IFLNK if kind=='symlink' else __import__('stat').S_IFCHR if kind=='device' else __import__('stat').S_IFREG)<<16
   info.file_size=m.FILE_MAX+1 if kind=='size' else 1;info.compress_type=99 if kind=='method' else 0
   z=mock.Mock();z.infolist.return_value=[info]
   with mock.patch.object(m,'ZIP_ENTRY_MAX',0 if kind=='count' else 250000):
    with self.assertRaises(m.CaptureError):m.validate_zip(z)
 def test_R05_crc_corrupt_body_and_central_read_cap_model(self):
  self.fixture({'mod.json':b'known stored body'})
  # Rewrite this synthetic archive once before authority SHA is fixed; CRC stays original.
  archive=m.ARCHIVE_PATH;raw=io.BytesIO()
  with zipfile.ZipFile(raw,'w',compression=zipfile.ZIP_STORED) as z:z.writestr('mod.json',b'known stored body')
  damaged=raw.getvalue().replace(b'known stored body',b'wrong stored body');archive.write_bytes(damaged)
  self.stack.enter_context(mock.patch.object(m,'ARCHIVE_SHA',m.sha(damaged)))
  with self.assertRaises(m.CaptureError):self.build()
  self.assertFalse((self.root/'case/completed.json').exists())
  fd=os.open(archive,os.O_RDONLY)
  try:
   r=m.AuthenticatedReader(fd,m.sha(damaged),m.Deadline())
   with mock.patch.object(m,'CENTRAL_MAX',1):
    with self.assertRaises(m.CaptureError):m.open_zip(r)
  finally:os.close(fd)
 def test_R06_symlinks_enum_and_root_replacement(self):
  roots=self.fixture();c,b=self.build();self.cap.recheck();root=Path(roots[-1][1]);root.rename(self.root/'retained-root');root.mkdir();(root/'mod.json').write_bytes(b'replacement')
  with self.assertRaises(m.CaptureError):self.cap.recheck()
  loose=self.root/'symlink';loose.mkdir();(loose/'mod.json').symlink_to(root/'mod.json');cap=m.Capture(m.Deadline())
  try:
   with self.assertRaises(m.CaptureError):cap.loose_layer('model',loose)
  finally:cap.close()
  (self.root/'ancestor').symlink_to(loose,target_is_directory=True)
  with self.assertRaises(m.CaptureError):m.physical(self.root/'ancestor',m.Deadline())
 def terminal(self,mutate=None,stdout=None):
  self.fixture();node=self.root/'node';node.write_bytes(b'node model');stdout=io.BytesIO() if stdout is None else stdout;receive=m.Protocol.receive
  def finish(protocol):
   if not stdout.getvalue():return receive(protocol)
   c=[json.loads(x) for x in stdout.getvalue().splitlines() if json.loads(x)['kind']=='CAPTURED'][0]
   frame={'v':1,'kind':'FINISH','captureId':c['captureId'],'analyses':[{'index':r['index'],'sha256':r['sha256'],'analysis':None} for r in c['selected']],'tool':{'nodeVersion':'v26.0.0','acornVersion':'8.16.0','nodeSourceSHA256':m.sha(node.read_bytes())}}
   if mutate:mutate(frame)
   return frame
  with mock.patch.object(m,'OUTPUT_PARENT',self.root/'captures'),mock.patch.object(m,'NODE_PATH',node),mock.patch.object(m,'NODE_SOURCE_EXPECTED',m.sha(node.read_bytes())),mock.patch.object(m,'runtime_context',return_value={'model':True}),mock.patch.object(m.Protocol,'receive',finish),mock.patch.object(m.sys,'stderr',io.StringIO()):result=m._run(io.BytesIO(b'{"v":1,"kind":"BEGIN","outputLeaf":"one"}\n'),stdout)
  return result,stdout
 def test_R07_local_import_finish_and_manifest(self):
  result,out=self.terminal();self.assertEqual(result,0);case=self.root/'captures/one';manifest=json.loads((case/'manifest.json').read_bytes());complete=json.loads((case/'completed.json').read_bytes())
  self.assertEqual(len([name for name in manifest['artifactHashes'] if name.startswith('layer-sources/')]),5)
  for name,digest in manifest['artifactHashes'].items():self.assertEqual(m.sha((case/name).read_bytes()),digest)
  self.assertEqual(complete['artifactHashes']['manifest.json'],m.sha((case/'manifest.json').read_bytes()));self.assertFalse(complete['sourceClosure']);self.assertFalse(complete['native'])
 def test_R09_stdout_after_completed_disk_caller_unknown(self):
  class Broken(io.BytesIO):
   def write(self,raw):
    if json.loads(raw)['kind']=='COMPLETED':raise OSError('controlled stdout terminal failure')
    return super().write(raw)
  result,out=self.terminal(stdout=Broken());self.assertEqual(result,1);self.assertTrue((self.root/'captures/one/completed.json').exists());self.assertFalse((self.root/'captures/one/fault.json').exists());self.assertNotIn(b'"kind":"COMPLETED"',out.getvalue())
 def test_R09_invalid_finish_no_healthy_completion(self):
  result,out=self.terminal(lambda f:f.update(captureId='f'*64));self.assertEqual(result,1);self.assertFalse((self.root/'captures/one/completed.json').exists());self.assertEqual(json.loads(out.getvalue().splitlines()[-1])['code'],'PROTOCOL_DIGEST')
 def test_R10_count_and_layer_edges_model(self):
  self.fixture()
  with mock.patch.object(m,'CANDIDATE_MAX',1),mock.patch.object(m,'LAYER_ENTRY_MAX',5):c,b=self.build();self.verify(c,b)
 def test_R10_count_oneover_before_body_model(self):
  self.fixture({'mod.json':b'', 'simulation/helpers/a.js':b'x'})
  with mock.patch.object(m,'CANDIDATE_MAX',1),mock.patch.object(m.Capture,'capture_candidate',side_effect=AssertionError('body read before union gate')):
   with self.assertRaises(m.CaptureError):self.build()
 def test_R10_layer_oneover_before_body_model(self):
  self.fixture()
  with mock.patch.object(m,'LAYER_ENTRY_MAX',4),mock.patch.object(m.Capture,'capture_candidate',side_effect=AssertionError('body read before layer gate')):
   with self.assertRaises(m.CaptureError):self.build()


 def test_P08_partial_layer_fault_retains_prior_and_raw(self):
  real=m.Output.capture
  def injected(output,name,size,read):
   if name=='layer-sources/mod0/mod.json':raise m.CaptureError('OUTPUT_WRITE_OR_FSYNC')
   return real(output,name,size,read)
  with mock.patch.object(m.Output,'capture',injected):result,out=self.terminal()
  case=self.root/'captures/one';self.assertEqual(result,1);self.assertTrue((case/'layer-sources/public/mod.json').exists());self.assertFalse((case/'completed.json').exists());self.assertEqual((case/'protocol-output.ndjson').read_bytes(),out.getvalue());self.assertIs(json.loads(out.getvalue())['durableFault'],False)
 def test_R06_directory_changed_during_enumeration(self):
  loose=self.root/'loose';loose.mkdir();(loose/'mod.json').write_bytes(b'{}');cap=m.Capture(m.Deadline());real=m.os.scandir
  def listed(fd):
   iterator=real(fd);(loose/'added-after-enum').write_bytes(b'evidence');return iterator
  try:
   with mock.patch.object(m.os,'scandir',side_effect=listed):
    with self.assertRaises(m.CaptureError):cap.loose_layer('model',loose)
  finally:cap.close()
 def test_R10_path_raw_deadline_edges_models(self):
  self.assertEqual(m.safe_vfs('a'*1024),'a'*1024)
  with self.assertRaises(m.CaptureError):m.safe_vfs('a'*1025)
  protocol=m.Protocol(io.BytesIO(),io.BytesIO(),m.Deadline())
  with mock.patch.object(m,'RAW_MAX',2):
   protocol.raw('protocol-input.ndjson',b'aa')
   with self.assertRaises(m.CaptureError):protocol.raw('protocol-input.ndjson',b'b')
  with mock.patch.object(m.time,'monotonic_ns',side_effect=[0,600*10**9-1,600*10**9]):
   d=m.Deadline();d.check()
   with self.assertRaises(m.CaptureError):d.check()
 def test_P08_final_readback_partial_IO(self):
  self.fixture();c,b=self.build()
  with mock.patch.object(m.os,'pread',return_value=b''):
   with self.assertRaises(m.CaptureError):self.verify(c,b)

class SchemaVariants(unittest.TestCase):
 def setUp(self):self.results=[]
 def tearDown(self):
  (RUN/(self._testMethodName+'-cases.json')).write_text(json.dumps(self.results,indent=2)+'\n')
 def corpus(self):
  # Hand-authored schema/source-shape model. These are not actual Acorn output.
  text='function f(x){a(x);Object.assign(x);x=x;x++;delete x;} const a=Object.assign;'
  body=text.encode();analysis={'vfs':'x.js','parseStatus':'PARSED','mode':'script','functions':[{'name':'f','line':1,'endLine':1,'params':['x'],'start':0,'end':len(text)}],'calls':[{'callee':'a','args':['x'],'line':1,'context':'f','kind':'CallExpression'},{'callee':'Object.assign','args':['x'],'line':1,'context':'f','kind':'NewExpression'}],'writerSites':[{'callee':'Object.assign','args':['x'],'line':1,'context':'f','kind':'assign','literalName':'','nameArgumentIndex':0,'target':'Object'},{'callee':'a','args':['x'],'line':1,'context':'f','kind':'assign','alias':'a','aliasSource':'Object.assign','aliasDeclarationLine':1,'literalName':None,'target':'x'}],'aliases':[{'name':'a','value':'Object.assign','line':1,'context':'(file)'},{'name':'x','value':None,'line':1,'context':'f'}],'assignments':[{'kind':'=','left':'x','right':'x','line':1,'context':'f'},{'kind':'++','left':'x','line':1,'context':'f'},{'kind':'delete','left':'x','line':1,'context':'f'}],'fileTopLevelDeclarations':[{'kind':'function','name':'f','line':1},{'kind':'variable','name':'a','line':1}],'closure':'OPEN_REQUIRES_POSITIVE_SEMANTIC_CALLER_PROOF'}
  row={'index':0,'vfs':'x.js','sha256':m.sha(body)}
  frame={'v':1,'kind':'FINISH','captureId':'a'*64,'analyses':[{'index':0,'sha256':row['sha256'],'analysis':analysis}],'tool':{'nodeVersion':'v26.0.0','acornVersion':'8.16.0','nodeSourceSHA256':'b'*64}}
  return frame,[row],[body]
 def reject(self,label,frame,rows,bodies):
  with self.subTest(label=label),self.assertRaises(m.CaptureError):m.validate_finish(frame,'a'*64,rows,bodies)
  self.results.append({'case':label,'result':'PASS_REJECTED','model':'HAND_AUTHORED_SCHEMA_NOT_ACTUAL_ACORN'})
 def test_schema_every_nested_key_extra_and_wrongshape(self):
  import copy
  frame,rows,bodies=self.corpus();m.validate_finish(frame,'a'*64,rows,bodies)
  objects=[]
  def walk(value,path):
   if isinstance(value,dict):
    objects.append((path,value))
    for key,child in value.items():walk(child,path+[key])
   elif isinstance(value,list):
    for i,child in enumerate(value):walk(child,path+[i])
  walk(frame,[])
  def get(root,path):
   for part in path:root=root[part]
   return root
  for path,value in objects:
   for key in value:
    for mutation in ('missing','wrongshape'):
     bad=copy.deepcopy(frame);target=get(bad,path)
     if mutation=='missing':del target[key]
     else:target[key]={}
     self.reject(str(path)+'.'+key+'.'+mutation,bad,rows,bodies)
   bad=copy.deepcopy(frame);get(bad,path)['unexpected']=0;self.reject(str(path)+'.extra',bad,rows,bodies)
 def test_schema_every_tag_and_source_correlation(self):
  import copy
  frame,rows,bodies=self.corpus();analysis=frame['analyses'][0]['analysis'];schema=m.schema()['$defs']
  for kind in schema['assignmentRow']['properties']['kind']['enum']:
   good=copy.deepcopy(frame);good['analyses'][0]['analysis']['assignments'][0]['kind']=kind;m.validate_finish(good,'a'*64,rows,bodies);self.results.append({'case':'assignment '+kind,'result':'PASS_SHAPE_MODEL'})
  for kind in schema['directWriterRow']['properties']['kind']['enum']:
   good=copy.deepcopy(frame);writer=good['analyses'][0]['analysis']['writerSites'][0];writer['kind']=kind;writer['nameArgumentIndex']=1 if kind in ('RegisterComponentType','RegisterSystemComponentType','ReRegisterComponentType') else 0;writer['literalName']='\ud800';m.validate_finish(good,'a'*64,rows,bodies);self.results.append({'case':'direct '+kind,'result':'PASS_SHAPE_MODEL'})
  for source in schema['aliasWriterRow']['properties']['aliasSource']['enum']:
   good=copy.deepcopy(frame);a=good['analyses'][0]['analysis'];writer=a['writerSites'][1];writer['aliasSource']=source;writer['kind']=source.split('.')[1];a['aliases'][0]['value']=source
   # Shape positive only: source expression may not contain this alternative.
   m.validate_schema(good);self.results.append({'case':'alias '+source,'result':'PASS_SCHEMA_ONLY_MODEL'})
  mutations={
   'direct wrong index':lambda a:a['writerSites'][0].update(nameArgumentIndex=1),
   'alias wrong suffix':lambda a:a['writerSites'][1].update(kind='set'),
   'alias wrong callee':lambda a:a['writerSites'][1].update(alias='x'),
   'alias wrong target':lambda a:a['writerSites'][1].update(target='a'),
   'missing alias':lambda a:a.update(aliases=[]),
   'missing call':lambda a:a.update(calls=[]),
   'alias right forbidden':lambda a:a['assignments'][1].update(right=None),
   'delete right forbidden':lambda a:a['assignments'][2].update(right='x'),
   'top wrong kind':lambda a:a['fileTopLevelDeclarations'][0].update(kind='class'),
   'wrong vfs':lambda a:a.update(vfs='wrong.js'),
   'outofline':lambda a:a['calls'][0].update(line=2),
   'source slice absent':lambda a:a['aliases'][0].update(name='not_in_source'),
   'boolean integer':lambda a:a['calls'][0].update(line=True),
   'empty literal extra':lambda a:a['writerSites'][1].update(literalName=''),
  }
  for label,mutate in mutations.items():
   bad=copy.deepcopy(frame);mutate(bad['analyses'][0]['analysis']);self.reject(label,bad,rows,bodies)
  for mode in ('script','module'):
   good=copy.deepcopy(frame);good['analyses'][0]['analysis']['mode']=mode;m.validate_finish(good,'a'*64,rows,bodies)
 def test_schema_parse_utf8_metadata_variants(self):
  import copy
  for body,analysis in ((b'bad js',{'vfs':'x.js','parseStatus':'BLOCK_PARSE_ERROR','error':'controlled parser error','closure':'OPEN_PARSE_ERROR'}),(b'\xff',{'vfs':'x.js','parseStatus':'BLOCK_UTF8_ERROR','closure':'OPEN_INVALID_SOURCE_ENCODING'})):
   frame,rows,_=self.corpus();rows[0]['sha256']=m.sha(body);frame['analyses'][0].update(sha256=m.sha(body),analysis=analysis);m.validate_finish(frame,'a'*64,rows,[body])
   for key in analysis:
    bad=copy.deepcopy(frame);del bad['analyses'][0]['analysis'][key];self.reject(analysis['parseStatus']+' missing '+key,bad,rows,[body])
   bad=copy.deepcopy(frame);bad['analyses'][0]['analysis']['unexpected']='x';self.reject(analysis['parseStatus']+' extra',bad,rows,[body])
  frame,rows,bodies=self.corpus();frame['analyses'][0]['analysis']=None;self.reject('JSnull',frame,rows,bodies)
  frame,rows,bodies=self.corpus();rows[0]['vfs']='mod.json';self.reject('nonJSnonnull',frame,rows,bodies)
 def test_schema_scaled_array_string_frame_limits_and_utf16(self):
  import copy
  frame,rows,bodies=self.corpus();changed=copy.deepcopy(m.schema());changed['$defs']['parsed']['properties']['calls']['maxItems']=2
  with mock.patch.object(m,'_SCHEMA',changed):
   m.validate_finish(frame,'a'*64,rows,bodies)
   bad=copy.deepcopy(frame);bad['analyses'][0]['analysis']['calls'].append(copy.deepcopy(bad['analyses'][0]['analysis']['calls'][0]));self.reject('calls exact2 plus1 model',bad,rows,bodies)
  changed=copy.deepcopy(m.schema());changed['$defs']['functionRow']['properties']['params']['maxItems']=1
  with mock.patch.object(m,'_SCHEMA',changed):
   m.validate_finish(frame,'a'*64,rows,bodies);bad=copy.deepcopy(frame);bad['analyses'][0]['analysis']['functions'][0]['params']=['x','x'];self.reject('params exact1 plus1 model',bad,rows,bodies)
  changed=copy.deepcopy(m.schema());changed['$defs']['callRow']['properties']['args']['maxItems']=1
  with mock.patch.object(m,'_SCHEMA',changed):
   m.validate_finish(frame,'a'*64,rows,bodies);bad=copy.deepcopy(frame);bad['analyses'][0]['analysis']['calls'][0]['args']=['x','x'];self.reject('args exact1 plus1 model',bad,rows,bodies)
  with mock.patch.object(m,'FRAME_MAX',2):
   self.assertEqual(m.strict_json(b'{}'),{})
   with self.assertRaises(m.CaptureError):m.strict_json(b'{} ')
  for text in ('\ufeff😀\r\nx\ry\nz\u2028a\u2029b',):
   positions,units,lines=m.source_positions(text);self.assertEqual(units,m.u16(text));self.assertEqual(lines,6);self.assertNotIn(2,positions);self.assertNotIn(4,positions)


# Purpose: new source-fixed regressions; historical reviewer countercases untouched.
class SourceFix(unittest.TestCase):
 setUp=Preservation.setUp
 tearDown=Preservation.tearDown
 fixture=Preservation.fixture
 build=Preservation.build
 verify=Preservation.verify
 def test_FIX_phaseA_internal_allocations(self):
  # Trace real pipeline frame locals, not just returned-wrapper objects; tiny physical body.
  v='simulation/helpers/stream.js';body=b'x'*(256*1024);self.fixture({'mod.json':b'{}',v:body},[{'mod.json':b'{}',v:body}]*4)
  observations=[];source=str(Path(m.__file__).resolve());tracked_files={source,str(Path(zipfile.__file__).resolve())}
  def tracing(frame,event,arg):
   if event=='line' and frame.f_code.co_filename in tracked_files:
    chain=[];parent=frame
    while parent:
     if parent.f_code.co_filename in tracked_files:chain.append(parent)
     parent=parent.f_back
    builds=[f for f in chain if f.f_code.co_name=='build']
    if builds and 'bodies' not in builds[0].f_locals:
     seen={}
     def inspect(value):
      if type(value) in (bytes,bytearray,memoryview):seen[id(value)]=len(value)
      elif type(value) in (list,tuple):
       for item in value:
        if type(item) in (bytes,bytearray,memoryview):seen[id(item)]=len(item)
     for f in chain:
      for value in f.f_locals.values():inspect(value)
     observations.append({'function':frame.f_code.co_name,'largest':max(seen.values(),default=0),'wholeBodies':sum(n>=len(body) for n in seen.values()),'payloadBytes':sum(seen.values())})
   return tracing
  sys.settrace(tracing)
  try:c,b=self.build()
  finally:sys.settrace(None)
  self.verify(c,b);self.assertTrue(observations)
  (self.root/'allocation-observations.json').write_text(json.dumps(observations,indent=2)+'\n')
  self.assertEqual(max(x['wholeBodies'] for x in observations),0)
  self.assertLessEqual(max(x['largest'] for x in observations),m.STREAM_CHUNK)
  self.assertEqual(b[[r['vfs'] for r in c['selected']].index(v)],body)
 def test_FIX_constructor_initial_fstat_fault_owned(self):
  realphysical=m.physical;opened=[];closed=[];realclose=m.os.close
  def physical(path,d):
   fd=realphysical(path,d);opened.append(fd);closed.clear();return fd
  class Fault(m.Deadline):
   def io(self,fn,*args,**kwargs):
    if fn is os.fstat and opened and args[0]==opened[0]:raise m.CaptureError('SOURCE_CHANGED')
    return super().io(fn,*args,**kwargs)
  def close(fd):closed.append(fd);return realclose(fd)
  with mock.patch.object(m,'physical',physical),mock.patch.object(m.os,'close',close):
   with self.assertRaises(m.CaptureError) as caught:m.Output(self.root,'case',Fault())
  # RED leak cleanup belongs only to this new test fixture, never retry uncertain FDs.
  alive=False
  try:os.fstat(opened[0]);alive=True
  except OSError:pass
  if alive:realclose(opened[0])
  self.assertFalse(alive);self.assertEqual(closed.count(opened[0]),1);self.assertEqual(caught.exception.code,'SOURCE_CHANGED')
 def test_FIX_constructor_initial_deadline_and_unknown_close(self):
  realphysical=m.physical;opened=[];realclose=m.os.close;calls=[]
  def physical(path,d):
   fd=realphysical(path,d);opened.append(fd);calls.clear();return fd
  class Fault(m.Deadline):
   def io(self,fn,*args,**kwargs):
    if fn is os.fstat and opened and args[0]==opened[0]:raise m.CaptureError('TIMEOUT')
    return super().io(fn,*args,**kwargs)
  def close(fd):
   calls.append(fd);realclose(fd)
   if opened and fd==opened[0]:raise OSError('unknown after physical close')
  with mock.patch.object(m,'physical',physical),mock.patch.object(m.os,'close',close):
   with self.assertRaises(m.CaptureError) as caught:m.Output(self.root,'case',Fault())
  if not calls or calls[-1]!=opened[0]:realclose(opened[0])
  self.assertEqual(calls.count(opened[0]),1);self.assertEqual(caught.exception.code,'TIMEOUT');self.assertIn('RESOURCE_CLOSE_UNKNOWN',caught.exception.secondary);self.assertIn(opened[0],caught.exception.unknown_fds)
 def test_FIX_independent_candidate_traversal_budget(self):
  loose=self.root/'loose';loose.mkdir()
  for name in ('mod.json','other-a','other-b'):(loose/name).write_bytes(b'{}')
  cap=m.Capture(m.Deadline())
  try:
   with mock.patch.object(m,'LAYER_ENTRY_MAX',2),mock.patch.object(m,'LOOSE_ENUM_MAX',3),mock.patch.object(m.os,'listdir',side_effect=AssertionError('unbounded listdir forbidden')):
    layer=cap.loose_layer('model',loose);self.assertEqual([r['vfs'] for r in layer['entries']],['mod.json'])
  finally:cap.close()
 def test_FIX_nested_traversal_edge_and_one_over(self):
  loose=self.root/'loose';(loose/'nested').mkdir(parents=True);(loose/'nested/mod.json').write_bytes(b'not a candidate');(loose/'mod.json').write_bytes(b'{}')
  for limit in (3,2):
   cap=m.Capture(m.Deadline())
   try:
    with mock.patch.object(m,'LOOSE_ENUM_MAX',limit):
     if limit==3:self.assertEqual(len(cap.loose_layer('model',loose)['entries']),1)
     else:
      with self.assertRaises(m.CaptureError):cap.loose_layer('model',loose)
   finally:cap.close()
 def iterator_case(self,variant):
  from types import SimpleNamespace
  fd=os.open(self.root,os.O_RDONLY|os.O_DIRECTORY);cap=m.Capture(m.Deadline());calls=[];created=[]
  class Iter:
   def __init__(self):self.i=0;created.append(self)
   def __next__(self):
    self.i+=1;calls.append('next')
    if variant in ('nextfault','nextclosefault'):raise OSError('next fault')
    if variant=='nexttimeout':raise m.CaptureError('TIMEOUT')
    if variant=='overflow':return SimpleNamespace(name='name'+str(self.i))
    raise StopIteration
   def close(self):
    calls.append('close')
    if variant in ('closefault','nextclosefault'):raise OSError('uncertain iterator close')
  def create(source):
   self.assertEqual(source,fd)
   if variant=='createfault':raise OSError('create fault')
   return Iter()
  try:
   with mock.patch.object(m.os,'scandir',side_effect=create),mock.patch.object(m,'LOOSE_ENUM_MAX',2):
    if variant in ('ok',):self.assertEqual(cap.enumerate_names(fd,'',[0]),[])
    else:
     with self.assertRaises(m.CaptureError) as caught:cap.enumerate_names(fd,'',[0])
     if variant=='closefault':self.assertEqual(caught.exception.code,'RESOURCE_CLOSE_UNKNOWN')
     if variant=='nextclosefault':self.assertIn('RESOURCE_CLOSE_UNKNOWN',caught.exception.secondary)
   self.assertEqual(calls.count('close'),0 if variant=='createfault' else 1);self.assertEqual(os.fstat(fd).st_ino,self.root.stat().st_ino)
   if variant=='overflow':self.assertEqual(calls.count('next'),3)
  finally:cap.close();os.close(fd)
 def test_FIX_iterator_constructor_next_close_timeout(self):
  for variant in ('ok','createfault','nextfault','nexttimeout','closefault','nextclosefault','overflow'):
   with self.subTest(variant=variant):self.iterator_case(variant)
 def test_FIX_iterator_post_constructor_deadline_owned(self):
  from types import SimpleNamespace
  fd=os.open(self.root,os.O_RDONLY|os.O_DIRECTORY);calls=[];created=[False]
  class Clock(m.Deadline):
   def check(self):
    if created[0]:raise m.CaptureError('TIMEOUT')
    return super().check()
  class Iterator:
   def close(self):calls.append('close')
  def create(_):created[0]=True;return Iterator()
  cap=m.Capture(Clock())
  try:
   with mock.patch.object(m.os,'scandir',side_effect=create):
    with self.assertRaises(m.CaptureError):cap.enumerate_names(fd,'',[0])
   self.assertEqual(calls,['close']);self.assertTrue(os.fstat(fd))
  finally:cap.close();os.close(fd)
 def test_FIX_actual_concurrent_existing_inventory_sentinel(self):
  import concurrent.futures,threading
  output=m.Output(self.root,'sentinel',m.Deadline());output.write('inventory.json',b'existing sentinel');barrier=threading.Barrier(2)
  def writer(_):
   barrier.wait(timeout=5)
   try:output.write('inventory.json',b'concurrent overwrite');return 'WRONG_SUCCESS'
   except m.CaptureError as error:return error.code
  try:
   with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(writer,range(2)))
   self.assertEqual(results,['OUTPUT_FILE_EXISTS']*2);self.assertEqual((self.root/'sentinel/inventory.json').read_bytes(),b'existing sentinel')
  finally:output.close()


 def test_FIX_global_candidate_vs_union_archive_noncandidates(self):
  public={'mod.json':b'{}'}
  for i in range(12):public['unrelated-'+str(i)]=b'x'
  self.fixture(public)
  with mock.patch.object(m,'LOOSE_ENUM_MAX',1),mock.patch.object(m,'LAYER_ENTRY_MAX',5),mock.patch.object(m,'CANDIDATE_MAX',1):
   c,b=self.build();self.verify(c,b);self.assertEqual(self.cap.candidate_count,5);self.assertEqual(len(c['selected']),1)
  output=m.Output(self.root,'global-over',m.Deadline());cap=m.Capture(output.d)
  try:
   with mock.patch.object(m,'LOOSE_ENUM_MAX',1),mock.patch.object(m,'LAYER_ENTRY_MAX',4):
    with self.assertRaises(m.CaptureError):cap.build(output)
   self.assertFalse((self.root/'global-over/layer-sources').exists())
  finally:cap.close();output.close()
 def test_FIX_iterator_path_overflow_and_special_type(self):
  from types import SimpleNamespace
  fd=os.open(self.root,os.O_RDONLY|os.O_DIRECTORY);calls=[]
  class Names:
   def __next__(self):return SimpleNamespace(name='a'*1025)
   def close(self):calls.append('close')
  cap=m.Capture(m.Deadline())
  try:
   with mock.patch.object(m.os,'scandir',return_value=Names()):
    with self.assertRaises(m.CaptureError):cap.enumerate_names(fd,'',[0])
   self.assertEqual(calls,['close']);self.assertTrue(os.fstat(fd))
  finally:cap.close();os.close(fd)
  loose=self.root/'fifo';loose.mkdir();os.mkfifo(loose/'not-regular');cap=m.Capture(m.Deadline())
  try:
   with self.assertRaises(m.CaptureError):cap.loose_layer('model',loose)
  finally:cap.close()

if __name__=='__main__':unittest.main(verbosity=2)




