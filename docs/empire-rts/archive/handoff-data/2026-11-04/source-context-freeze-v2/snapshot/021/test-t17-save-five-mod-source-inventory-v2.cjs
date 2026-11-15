// Purpose: NEW bounded Node v2 producer/protocol controls; no official capture.
// Created: 2026-10-25. SPDX-License-Identifier: GPL-2.0-or-later
'use strict';
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const {EventEmitter} = require('node:events');
const api = require('./t17-save-five-mod-source-inventory-v2.cjs');
const sha = b => crypto.createHash('sha256').update(b).digest('hex');
let groups = 0;
// New repair controls can run alone for preserved RED evidence.
const repairCase = process.argv.find(x => x.startsWith('--repair-case='))?.slice(14);
const enabled = name => !repairCase || name.startsWith('repair '+repairCase+':');
function test(name, fn) { if (!enabled(name)) return; fn(); groups++; process.stdout.write(`PASS ${name}\n`); }

test('eight actual Acorn escaped/astral producer branches', () => {
  const astral = String.fromCodePoint(0x10400);
  const cases = [
    [String.raw`function \u0066() {}`, ['f'], ['f']],
    [String.raw`const \u0066 = () => {};`, [String.raw`\u0066`], [String.raw`\u0066`]],
    [String.raw`const \u0066 = function \u0067() {};`, [String.raw`\u0066`], ['g']],
    [String.raw`o.\u0066 = function() {};`, [], [String.raw`o.\u0066`]],
    [String.raw`function \u0066(){ use(() => {}); }`, ['f'], ['f', 'f::<anonymous@1>']],
    [String.raw`function \u{10400}() {}`, [astral], [astral]],
    [`function ${astral}() {}`, [astral], [astral]],
    [String.raw`const {x: \u0066} = o;`, [String.raw`{x: \u0066}`], []]
  ];
  for (const [source, names, functions] of cases) {
    const row = api.analyze(source, 'simulation/helpers/Example.js');
    assert.equal(row.parseStatus, 'PARSED');
    assert.deepEqual(row.fileTopLevelDeclarations.map(r => r.name), names);
    assert.deepEqual(row.functions.map(r => r.name), functions);
  }
});

test('source UTF8/BOM and exact failure variants', () => {
  assert.equal(api.strictDecode(Buffer.from('\ufeffx()')), '\ufeffx()');
  assert.throws(() => api.strictDecode(Buffer.from([0xc3, 0x28])));
  assert.deepEqual(Object.keys(api.analyze('function {', 'x.js')).sort(),
    ['closure', 'error', 'parseStatus', 'vfs']);
  assert.equal(api.analyze('export const x=1;', 'x.js').mode, 'module');
  assert.throws(() => api.analyze('export default function(){}', 'x.js'));
});

test('nested row shapes, decoded literal value and mutation omission', () => {
  const row = api.analyze(String.raw`let missing;let n=0;n++;delete o[k];n+=1;const assign=Object.assign;assign(o,n);Engine.RegisterGlobal("",n);Engine.RegisterGlobal("\ud800",n);`, 'x.js');
  assert.equal(row.aliases.find(a => a.name === 'missing').value, null);
  assert.equal('right' in row.assignments.find(a => a.kind === '++'), false);
  assert.equal('right' in row.assignments.find(a => a.kind === 'delete'), false);
  assert.equal(row.assignments.find(a => a.kind === '+=').right, '1');
  const alias = row.writerSites.find(a => a.alias === 'assign');
  assert.equal('nameArgumentIndex' in alias, false);
  const direct = row.writerSites.filter(a => a.kind === 'RegisterGlobal');
  assert.equal(direct[0].literalName, '');
  assert.equal(direct[1].literalName.charCodeAt(0), 0xd800);
});

test('protocol decoder duplicate keys, UTF8, JSON and depth', () => {
  assert.deepEqual(api.decodeFrame(Buffer.from('{"v":1,"x":"\\u0066"}')), {v:1,x:'f'});
  for (const frame of ['{"a":1,"\\u0061":2}', '{"x":{"a":1,"a":2}}',
    '{"n":NaN}', '[1,]', '{} garbage', '['.repeat(129) + ']'.repeat(129)])
    assert.throws(() => api.decodeFrame(Buffer.from(frame)));
  assert.throws(() => api.decodeFrame(Buffer.from([0xff])));
  assert.doesNotThrow(() => api.decodeFrame(Buffer.from('['.repeat(128)+'0'+']'.repeat(128))));
});

function sourceFrame(index, vfs, text) {
  const body = Buffer.isBuffer(text) ? text : Buffer.from(text);
  return {v:1,kind:'SOURCE',index,vfs,mod:'epoch_t17_save_allocation_witness',
    sha256:sha(body),bytes:body.length,bodyBase64:body.toString('base64')};
}
function captured(frames) {
  const mods = ['public','epoch_rts','epoch_t16_harness','epoch_t17_save_harness','epoch_t17_save_allocation_witness'];
  const selected = frames.map(f => ({index:f.index,vfs:f.vfs,mod:f.mod,sha256:f.sha256,
    bytes:f.bytes,shadowed:[],archiveEntry:null,defaultLoaderFolder:api.defaultFolder(f.vfs),
    realm:f.vfs.endsWith('mod.json')?'METADATA':'SIMULATION_CANDIDATE'}));
  const selectedDigest = sha(selected.map(r => `${r.vfs}\0${r.mod}\0${r.sha256}\0${r.bytes}`).join('\n'));
  const captureId = sha(JSON.stringify({version:1,archiveExpectedSHA:api.ARCHIVE_SHA,selectedDigest}));
  return {v:1,kind:'CAPTURED',captureId,sourceCount:frames.length,selectedDigest,
    layers:mods.map((name,i) => ({name,rootKind:i?'loose':'archive',rootDisplay:name,entries:[]})),
    selected,archive:{expectedSHA:api.ARCHIVE_SHA,actualSHA:api.ARCHIVE_SHA,size:1,
      chunkBytes:4194304,chunkCount:1,authorityKind:'VERIFIED_HELD_FD_BYTES'},
    unsupportedRuntimeRules:[]};
}

test('whole source pack binds index/hash/vfs and exact FINISH variants', () => {
  const frames = [sourceFrame(0,'mod.json','{}'),sourceFrame(1,'x.js',Buffer.from([0xff]))];
  const session = new api.ProtocolSession();
  for (const f of frames) assert.equal(session.accept(f), null);
  const finish = session.accept(captured(frames));
  assert.equal(finish.kind, 'FINISH');
  assert.equal(finish.analyses[0].analysis, null);
  assert.deepEqual(finish.analyses[1].analysis,
    {vfs:'x.js',parseStatus:'BLOCK_UTF8_ERROR',closure:'OPEN_INVALID_SOURCE_ENCODING'});
  assert.equal(session.analysisBlocks, 1);
});

test('protocol wrong order/hash/keys/base64 and metadata correlation fail', () => {
  const frame = sourceFrame(0,'x.js','x()');
  for (const f of [{...frame,index:1},{...frame,extra:1},{...frame,sha256:'0'.repeat(64)},
    {...frame,bodyBase64:frame.bodyBase64+'='},{...frame,vfs:'../x.js'}])
    assert.throws(() => new api.ProtocolSession().accept(f));
  for (const mutation of [c => c.selected[0].vfs='wrong.js', c => c.captureId='0'.repeat(64),
    c => c.archive.expectedSHA='0'.repeat(64), c => c.selected[0].extra=1]) {
    const session = new api.ProtocolSession(); session.accept(frame);
    const c = captured([frame]); mutation(c); assert.throws(() => session.accept(c));
  }
  assert.throws(() => new api.ProtocolSession().accept({v:1,kind:'COMPLETED'}));
});

test('COMPLETED is Python readback declaration, exact hashes/status then no extra frames', () => {
  const frame=sourceFrame(0,'x.js','x()'), session=new api.ProtocolSession();
  session.accept(frame); const finish=session.accept(captured([frame]));
  const hashes=Object.fromEntries(['inventory.json','layer-inputs.json','writer-sites.json','manifest.json'].map(n=>[n,'0'.repeat(64)]));
  session.accept({v:1,kind:'COMPLETED',captureId:finish.captureId,
    status:'CAPTURE_COMPLETE_CANDIDATE_ONLY',artifactHashes:hashes,sourceClosure:false,native:false});
  assert.equal(session.state,'COMPLETED');
  assert.throws(()=>session.accept(frame));
});

test('actual Unicode offsets/BOM and line-break producers use UTF16', () => {
  const source='\ufeff\r\nfunction '+String.fromCodePoint(0x10400)+'(){\r\n// x\u2028\u2029}';
  const row=api.analyze(source,'x.js').functions[0];
  assert.equal(row.start,source.indexOf('function'));
  assert.equal(row.end,source.length);
  assert.equal(row.line,2); assert.equal(row.endLine,5);
});

// Actual current Node source in a VM, with explicit synthetic child/clock/schema
// location fixtures. No real Python/archive/output operation occurs here.
function lifecycleFixture(mode, overrides={}) {
  const filename=path.join(__dirname,'t17-save-five-mod-source-inventory-v2.cjs');
  const source=fs.readFileSync(filename,'utf8');
  const schema=fs.readFileSync(path.join(__dirname,'../../work/t17-save-five-mod-inventory-repair-preparation/design-fix-v2/ANALYSIS-SCHEMA.json'));
  const calls={spawn:[],writes:[],kills:[],reads:[],timers:new Set()};
  const child=new EventEmitter(); child.stdout=new EventEmitter(); child.stderr=new EventEmitter(); child.stdin=new EventEmitter();
  const frame=sourceFrame(0,'x.js',mode==='producer_fail'?'export default function(){}':mode==='parser_range'?'('.repeat(4096)+'0'+')'.repeat(4096)+';':'x()');
  const capture=captured([frame]);
  const emit=(...frames)=>child.stdout.emit('data',Buffer.from(frames.map(f=>JSON.stringify(f)+'\n').join('')));
  function fire(ms) { const timer=[...calls.timers].find(t=>t.ms===ms); assert.ok(timer); timer.fn(); }
  child.kill=signal=> {
    calls.kills.push(signal);
    if(mode==='reap_unknown') {
      if(signal==='SIGTERM')queueMicrotask(()=>{fire(1000);fire(2000);});
    } else queueMicrotask(()=>child.emit('close',null,signal));
    return true;
  };
  child.stdin.end=()=>{};
  child.stdin.write=(bytes,callback)=> {
    const command=JSON.parse(bytes.toString()); calls.writes.push(command);
    if(mode==='stdin_error') { queueMicrotask(()=>callback(new Error('fixture write failure'))); return false; }
    callback(null);
    if(command.kind==='BEGIN')queueMicrotask(()=> {
      if(mode==='timeout' || mode==='reap_unknown') { fire(600000); return; }
      if(mode==='bad_utf8') { child.stdout.emit('data',Buffer.from([0xff,10])); return; }
      if(mode==='stderr_limit') { child.stderr.emit('data',Buffer.alloc(1048577)); return; }
      if(mode==='truncated') { child.stdout.emit('data',Buffer.from(JSON.stringify(frame))); child.emit('close',0,null); return; }
      emit(frame,capture);
    });
    if(command.kind==='FINISH')queueMicrotask(()=> {
      if(mode==='missing_complete') { child.emit('close',0,null); return; }
      if(mode==='repeat_capture') { emit(capture); return; }
      const done={v:1,kind:'COMPLETED',captureId:capture.captureId,status:'CAPTURE_COMPLETE_CANDIDATE_ONLY',
        artifactHashes:Object.fromEntries(['inventory.json','layer-inputs.json','writer-sites.json','manifest.json'].map(n=>[n,'0'.repeat(64)])),sourceClosure:false,native:false};
      emit(done);
      if(mode==='extra')emit(frame);
      child.emit('close',mode==='nonzero'?1:0,null);
    });
    return true;
  };
  const fakeFs={readFileSync(file) {
    calls.reads.push(file);
    if(file===filename)return Buffer.from(source);
    if(file===path.join(__dirname,'t17-save-five-mod-analysis-schema.json'))return overrides.badSchema?Buffer.from('{}'):schema;
    throw Error('FORBIDDEN_NODE_FILE_READ');
  }};
  const module={exports:{}};
  function localRequire(name) {
    if(name==='node:fs')return fakeFs;
    if(name==='internal/deps/acorn/acorn/dist/acorn' && overrides.acorn)return overrides.acorn;
    if(name==='node:child_process')return {spawn(...args) {
      calls.spawn.push(args); if(mode==='spawn_error')throw Error('fixture spawn failure'); return child;
    }};
    return require(name);
  }
  vm.runInNewContext(source,{require:localRequire,module,exports:module.exports,__dirname,__filename:filename,
    Buffer,TextDecoder,SyntaxError,process:{version:overrides.nodeVersion || process.version},
    setTimeout(fn,ms){const t={fn,ms};calls.timers.add(t);return t;},clearTimeout(t){calls.timers.delete(t);}},
    {filename});
  return {api:module.exports,calls};
}

async function asyncTest(name, fn) { if (!enabled(name)) return; await fn(); groups++; process.stdout.write(`PASS ${name}\n`); }

// Actual pinned Acorn failure plus explicit metadata/VM models. These are not
// filesystem, Python-child, bridge, native or full resource-boundary evidence.
test('repair parser: actual Acorn recursion remains fatal through analysisFor', () => {
  assert.equal(process.version,'v26.0.0');
  const acorn=require('internal/deps/acorn/acorn/dist/acorn');
  assert.equal(acorn.version,'8.16.0');
  const source='('.repeat(4096)+'0'+')'.repeat(4096)+';';
  assert.equal(Buffer.byteLength(source),8194);
  assert.throws(()=>acorn.parse(source,{ecmaVersion:'latest'}),RangeError);
  assert.throws(()=>api.analyze(source,'x.js'),RangeError);
  const frame=sourceFrame(0,'x.js',source), session=new api.ProtocolSession();
  session.accept(frame);
  assert.throws(()=>session.accept(captured([frame])),{code:'NODE_ANALYSIS'});
  assert.equal(session.state,'ANALYZING'); assert.equal(session.analysisBlocks,0);
});

test('repair classification: genuine syntax fallback and internal errors in either parse', () => {
  assert.equal(api.analyze('const x=1;','x.js').mode,'script');
  assert.equal(api.analyze('export const x=1;','x.js').mode,'module');
  const blocked=api.analyze('function {','x.js');
  assert.equal(blocked.parseStatus,'BLOCK_PARSE_ERROR');
  assert.deepEqual(Object.keys(blocked).sort(),['closure','error','parseStatus','vfs']);
  for(const fatal of [new RangeError('internal'),new Error('internal'),{name:'SyntaxError',message:'not genuine'},null]) {
    for(const phase of ['script','module']) {
      const calls=[];
      const fixture=lifecycleFixture('success',{acorn:{version:'8.16.0',parse(source,options){
        const mode=options.sourceType || 'script'; calls.push(mode);
        if(phase==='module' && mode==='script')throw new SyntaxError('script syntax');
        throw fatal;
      }}});
      let caught=false;
      try{fixture.api.analyze('x()','x.js');}catch(error){caught=true;assert.equal(error,fatal);}
      assert.equal(caught,true);
      assert.deepEqual(calls,phase==='script'?['script']:['script','module']);
    }
  }
});

test('repair counts: global actual candidate rows edge and one-over metadata model', () => {
  // Actual 16384 row threshold, synthetic repeated rows across five layers;
  // no filesystem uniqueness/completeness or actual capture is claimed.
  const row={vfs:'mod.json',sourceDisplay:'synthetic',sha256:sha('{}'),bytes:2};
  for(const count of [16384,16385]) {
    const session=new api.ProtocolSession(), frame=captured([]);
    const counts=[4096,4096,4096,4096,count-16384];
    frame.layers.forEach((layer,i)=>{layer.entries=Array.from({length:counts[i]},()=>({...row}));});
    assert.ok(frame.layers.every(layer=>layer.entries.length<=16384));
    if(count===16384)assert.equal(session.accept(frame).kind,'FINISH');
    else assert.throws(()=>session.accept(frame),{code:'PROTOCOL_LIMIT'});
  }
  const over=captured([]); over.layers[0].entries=Array(16385).fill(row);
  assert.throws(()=>new api.ProtocolSession().accept(over),{code:'PROTOCOL_LIMIT'});
});

async function main() {
  await asyncTest('repair abort: actual Acorn RangeError emits exactly one NODE_ANALYSIS ABORT in VM child',async()=> {
    const f=lifecycleFixture('parser_range'); const result=await f.api.RunCapture('fresh_fixture');
    assert.equal(result.status,'UNKNOWN_TOOL_CAPTURE'); assert.equal(result.reasonCode,'NODE_ANALYSIS');
    assert.deepEqual(f.calls.writes.map(x=>x.kind),['BEGIN','ABORT']);
    assert.equal(f.calls.writes[1].code,'NODE_ANALYSIS'); assert.equal(f.calls.spawn.length,1);
    assert.equal(f.calls.timers.size,0);
  });
  await asyncTest('exact one fixed child and no Node output/archive reads or writes',async()=> {
    const f=lifecycleFixture('success'); const result=await f.api.RunCapture('fresh_fixture');
    assert.equal(result.status,'CAPTURE_COMPLETE_CANDIDATE_ONLY');
    assert.equal(result.pythonDiskReadback,'DECLARED_BY_PYTHON_NOT_INDEPENDENT_NODE_FS_PROOF');
    assert.equal(f.calls.spawn.length,1);
    const [executable,args,options]=f.calls.spawn[0];
    assert.equal(executable,'/Library/Developer/CommandLineTools/usr/bin/python3');
    assert.equal(args[0],'-u'); assert.equal(args[1],path.join(__dirname,'t17-save-five-mod-capture.py'));
    assert.equal(options.shell,false);
    assert.deepEqual(f.calls.writes.map(x=>x.kind),['BEGIN','FINISH']);
    assert.equal(f.calls.kills.length,0); assert.equal(f.calls.timers.size,0);
    assert.ok(f.calls.reads.every(x=>x.endsWith('t17-save-five-mod-analysis-schema.json') || x.endsWith('t17-save-five-mod-source-inventory-v2.cjs')));
  });
  await asyncTest('exit/frame/encoding/diagnostic faults never become healthy completion',async()=> {
    for(const mode of ['missing_complete','nonzero','extra','truncated','bad_utf8','stderr_limit','spawn_error','stdin_error']) {
      const f=lifecycleFixture(mode); const result=await f.api.RunCapture('fresh_fixture');
      assert.equal(result.status,'UNKNOWN_TOOL_CAPTURE',mode);
      assert.equal(f.calls.spawn.length,1); assert.equal(f.calls.timers.size,0);
    }
  });
  await asyncTest('producer failure and repeated CAPTURED send exactly one allowed ABORT',async()=> {
    for(const mode of ['producer_fail','repeat_capture']) {
      const f=lifecycleFixture(mode); const result=await f.api.RunCapture('fresh_fixture');
      assert.equal(result.status,'UNKNOWN_TOOL_CAPTURE');
      const abort=f.calls.writes.filter(x=>x.kind==='ABORT'); assert.equal(abort.length,1);
      assert.equal(abort[0].code,mode==='producer_fail'?'NODE_ANALYSIS':'NODE_PROTOCOL');
    }
  });
  await asyncTest('fixed stop deadline, cleanup escalation and unknown reap have no respawn',async()=> {
    const timeout=lifecycleFixture('timeout'); assert.equal((await timeout.api.RunCapture('fresh_fixture')).reasonCode,'TIMEOUT');
    const unknown=lifecycleFixture('reap_unknown'); assert.equal((await unknown.api.RunCapture('fresh_fixture')).reasonCode,'RESOURCE_CLOSE_UNKNOWN');
    assert.deepEqual(unknown.calls.kills,['SIGTERM','SIGKILL']);
    assert.equal(unknown.calls.spawn.length,1); assert.equal(unknown.calls.timers.size,0);
  });
  await asyncTest('invalid leaf/runtime/schema blocks before child without overrides',async()=> {
    for(const [leaf,options] of [['../outside',{}],['fresh',{nodeVersion:'v25.0.0'}],['fresh',{badSchema:true}]]) {
      const f=lifecycleFixture('success',options); await assert.rejects(f.api.RunCapture(leaf));
      assert.equal(f.calls.spawn.length,0);
    }
  });
  process.stdout.write(JSON.stringify({groups,scope:'NEW_NODE_SOURCE_MODEL_ONLY',
    child:'EXPLICIT_VM_FIXTURE_NOT_REAL_PYTHON',officialArchive:false,engine:false})+'\n');
}
main().catch(error=>{process.stderr.write(error.stack+'\n');process.exitCode=1;});
