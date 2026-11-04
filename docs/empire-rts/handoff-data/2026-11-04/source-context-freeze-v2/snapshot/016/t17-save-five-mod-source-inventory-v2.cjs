// Purpose: NEW bounded five-mod Node AST producer and one Python capture protocol.
// Created: 2026-10-25. SPDX-License-Identifier: GPL-2.0-or-later
// Python owns archive/output/readback. Node never claims independent disk/native proof.
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const cp = require('node:child_process');
const acorn = require('internal/deps/acorn/acorn/dist/acorn');
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
function strictDecode(bytes){return new TextDecoder('utf-8',{fatal:true,ignoreBOM:true}).decode(bytes);}
// Analyzer/name/default-folder producers retained; only genuine syntax errors
// permit parser fallback. Internal/stack failures propagate to NODE_ANALYSIS.
function analyze(source,vfs){
 let ast,mode='script';try{ast=acorn.parse(source,{ecmaVersion:'latest',locations:true,allowReturnOutsideFunction:true});}catch(first){if(!(first instanceof SyntaxError))throw first;try{mode='module';ast=acorn.parse(source,{ecmaVersion:'latest',sourceType:'module',locations:true});}catch(second){if(!(second instanceof SyntaxError))throw second;return{vfs,parseStatus:'BLOCK_PARSE_ERROR',error:second.message,closure:'OPEN_PARSE_ERROR'};}}
 const text=n=>n?source.slice(n.start,n.end):null;
 const functions=[],calls=[],writerSites=[],aliases=[],assignments=[],fileTopLevelDeclarations=[];
 const danger=new Set(['RegisterGlobal','RegisterComponentType','RegisterSystemComponentType','ReRegisterComponentType','RegisterInterface','RegisterMessageType','SetGlobal','SetProperty','defineProperty','defineProperties','assign','setPrototypeOf','set','deleteProperty','eval','Function','LoadScript','LoadGlobalScript','LoadComponentScript','LoadLibrary','IncludeScript','RunJobs']);
 function property(n){if(n.type==='Identifier')return n.name;if(n.type==='Literal')return String(n.value);return null;}
 function visit(n,context='(file)',top=true,parent=null){if(!n||typeof n!=='object'||!n.type)return;
  let next=context,nextTop=top;
  if(['FunctionDeclaration','FunctionExpression','ArrowFunctionExpression'].includes(n.type)){
   next=n.id?n.id.name:(parent&&parent.type==='VariableDeclarator'?text(parent.id):(parent&&parent.type==='AssignmentExpression'?text(parent.left):context+'::<anonymous@'+n.loc.start.line+'>'));nextTop=false;
   functions.push({name:next,line:n.loc.start.line,endLine:n.loc.end.line,params:n.params.map(text),start:n.start,end:n.end});
  }
  if(n.type==='VariableDeclarator'){aliases.push({name:text(n.id),value:text(n.init),line:n.loc.start.line,context});if(top)fileTopLevelDeclarations.push({kind:'variable',name:text(n.id),line:n.loc.start.line});}
  if(n.type==='FunctionDeclaration'&&top)fileTopLevelDeclarations.push({kind:'function',name:n.id.name,line:n.loc.start.line});
  if(n.type==='CallExpression'||n.type==='NewExpression'){
   const callee=text(n.callee),args=n.arguments.map(text),row={callee,args,line:n.loc.start.line,context,kind:n.type};calls.push(row);
   const key=n.callee.type==='MemberExpression'?property(n.callee.property):property(n.callee);
   if(danger.has(key)){const index=['RegisterComponentType','RegisterSystemComponentType','ReRegisterComponentType'].includes(key)?1:0;writerSites.push({...row,kind:key,literalName:n.arguments[index]&&n.arguments[index].type==='Literal'&&typeof n.arguments[index].value==='string'?n.arguments[index].value:null,nameArgumentIndex:index,target:n.callee.type==='MemberExpression'?text(n.callee.object):null});}
  }
  if(n.type==='AssignmentExpression')assignments.push({kind:n.operator,left:text(n.left),right:text(n.right),line:n.loc.start.line,context});
  if(n.type==='UpdateExpression')assignments.push({kind:n.operator,left:text(n.argument),line:n.loc.start.line,context});
  if(n.type==='UnaryExpression'&&n.operator==='delete')assignments.push({kind:'delete',left:text(n.argument),line:n.loc.start.line,context});
  for(const [key,value]of Object.entries(n)){if(['loc','start','end','type'].includes(key))continue;if(Array.isArray(value))for(const child of value)visit(child,next,nextTop,n);else if(value&&typeof value==='object')visit(value,next,nextTop,n);}
 }
 visit(ast);
 // Retain alias evidence rather than treating aliases as absent native writers.
 // This is a candidate expansion, not a proof that a lexical binding is immutable.
 for(const alias of aliases){const match=/^(Object|Reflect)\.(defineProperty|defineProperties|assign|set|deleteProperty)$/.exec(alias.value||'');if(!match)continue;for(const call of calls)if(call.callee===alias.name)writerSites.push({...call,kind:match[2],alias:alias.name,aliasSource:alias.value,aliasDeclarationLine:alias.line,literalName:null,target:call.args[0]||null});}
 return{vfs,parseStatus:'PARSED',mode,functions,calls,writerSites,aliases,assignments,fileTopLevelDeclarations,closure:'OPEN_REQUIRES_POSITIVE_SEMANTIC_CALLER_PROOF'};
}
function defaultFolder(vfs){for(const folder of ['globalscripts/','simulation/components/interfaces/','simulation/helpers/','simulation/components/'])if(vfs.startsWith(folder)&&vfs.endsWith('.js')&&!vfs.slice(folder.length).includes('/'))return folder;return null;}

const ARCHIVE_SHA = 'ccb24dedee399e6d2810ccb62b0b1b77a937999d9f1dedffbc189b3e359f2429';
const SCHEMA_SHA = '280357ab50426d73f1265cb07458d8d4f86f226ab3b02d68025d1762d7975191';
const PYTHON = '/Library/Developer/CommandLineTools/usr/bin/python3';
const MODS = ['public','epoch_rts','epoch_t16_harness','epoch_t17_save_harness','epoch_t17_save_allocation_witness'];
const LIMIT = Object.freeze({frame:33554432,raw:268435456,source:8388608,totalSource:67108864,
  analysis:134217728,diagnostics:1048576,candidates:4096,layerEntries:16384,path:1024,
  depth:128,archive:8589934592,chunk:4194304,wall:600000});
const HASH_FILES = ['inventory.json','layer-inputs.json','writer-sites.json','manifest.json'];
function fail(code) { const error = new Error(code); error.code = code; throw error; }
function check(condition, code='PROTOCOL_SCHEMA') { if (!condition) fail(code); }
function exact(value, names) {
  check(value !== null && typeof value === 'object' && !Array.isArray(value));
  const keys=Object.keys(value);
  check(keys.length===names.length && keys.every(k=>names.includes(k)));
}
function integer(value, max, min=0) { check(Number.isSafeInteger(value) && value>=min && value<=max); }
function string(value, max=LIMIT.source, allowEmpty=false) {
  check(typeof value==='string' && (allowEmpty || value.length>0));
  check(value.length<=max,'PROTOCOL_LIMIT');
}
function hash(value) { check(typeof value==='string' && /^[0-9a-f]{64}$/.test(value)); }
function array(value, max) { check(Array.isArray(value)); check(value.length<=max,'PROTOCOL_LIMIT'); }
function vfsPath(value) {
  string(value,LIMIT.path);
  check(Buffer.byteLength(value,'utf8')<=LIMIT.path,'PROTOCOL_LIMIT');
  check(!/[\\:\x00-\x1f]/.test(value) && !value.startsWith('/') &&
    value.split('/').every(p=>p!=='' && p!=='.' && p!=='..'));
}

// JSON.parse alone loses duplicate keys. This bounded grammar walk checks every
// decoded object key before constructing the frame with the standard parser.
function decodeFrame(bytes) {
  check(Buffer.isBuffer(bytes)); check(bytes.length<=LIMIT.frame,'PROTOCOL_LIMIT');
  let source;
  try { source=strictDecode(bytes); } catch (_) { fail('PROTOCOL_UTF8'); }
  let i=0;
  function ws() { while (i<source.length && /[\x20\t\r\n]/.test(source[i])) i++; }
  function readString() {
    check(source[i]==='"','PROTOCOL_JSON'); const start=i++;
    while (i<source.length) {
      const ch=source[i++];
      if (ch==='"') {
        try { return JSON.parse(source.slice(start,i)); } catch (_) { fail('PROTOCOL_JSON'); }
      }
      if (ch==='\\') { check(i<source.length,'PROTOCOL_JSON'); i++; }
      else check(ch.charCodeAt(0)>=32,'PROTOCOL_JSON');
    }
    fail('PROTOCOL_JSON');
  }
  function value(depth) {
    ws();
    const ch=source[i];
    if(ch==='{' || ch==='[')check(depth<=LIMIT.depth,'PROTOCOL_LIMIT');
    if (ch==='"') { readString(); return; }
    if (ch==='{') {
      i++; ws(); const keys=new Set(); if (source[i]==='}') { i++; return; }
      for (;;) {
        ws(); const key=readString(); check(!keys.has(key),'PROTOCOL_JSON_DUPLICATE'); keys.add(key);
        ws(); check(source[i++]===':','PROTOCOL_JSON'); value(depth+1); ws();
        const next=source[i++]; if (next==='}') return; check(next===',','PROTOCOL_JSON');
      }
    }
    if (ch==='[') {
      i++; ws(); if (source[i]===']') { i++; return; }
      for (;;) { value(depth+1); ws(); const next=source[i++]; if(next===']')return; check(next===',','PROTOCOL_JSON'); }
    }
    for (const token of ['true','false','null']) if (source.startsWith(token,i)) { i+=token.length; return; }
    const number=/^-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?/.exec(source.slice(i));
    check(number,'PROTOCOL_JSON');
    check(Number.isFinite(Number(number[0])),'PROTOCOL_JSON'); i+=number[0].length;
  }
  value(1); ws(); check(i===source.length,'PROTOCOL_JSON');
  try { return JSON.parse(source); } catch (_) { fail('PROTOCOL_JSON'); }
}

function analysisFor(bytes,vfs) {
  let text;
  try { text=strictDecode(bytes); }
  catch (_) { return {vfs,parseStatus:'BLOCK_UTF8_ERROR',closure:'OPEN_INVALID_SOURCE_ENCODING'}; }
  let result;
  try { result=analyze(text,vfs); } catch (_) { fail('NODE_ANALYSIS'); }
  if (result.parseStatus==='PARSED') {
    const vectors=['functions','calls','writerSites','aliases','assignments','fileTopLevelDeclarations'];
    let count=0;
    for (const name of vectors) {
      check(result[name].length<=65536,'NODE_LIMIT'); count+=result[name].length;
      for(const row of result[name]) for(const field of ['args','params'])
        if(row[field])check(row[field].length<=4096,'NODE_LIMIT');
    }
    check(count<=262144,'NODE_LIMIT');
  }
  return result;
}

class ProtocolSession {
  constructor() { this.state='SOURCES'; this.sources=[]; this.totalSource=0; this.analysisBlocks=0; this.captureId=null; }
  accept(frame) {
    check(this.state!=='COMPLETED' && this.state!=='FAULT','PROTOCOL_ORDER');
    check(frame && frame.v===1 && typeof frame.kind==='string');
    if (frame.kind==='FAULT') {
      exact(frame,['v','kind','phase','code','durableFault']); string(frame.phase,128); string(frame.code,128);
      check(typeof frame.durableFault==='boolean'); this.state='FAULT'; fail('PYTHON_'+frame.code);
    }
    if(frame.kind==='SOURCE')return this.source(frame);
    if(frame.kind==='CAPTURED')return this.captured(frame);
    if(frame.kind==='COMPLETED')return this.completed(frame);
    fail('PROTOCOL_ORDER');
  }
  source(frame) {
    check(this.state==='SOURCES','PROTOCOL_ORDER');
    exact(frame,['v','kind','index','vfs','mod','sha256','bytes','bodyBase64']);
    integer(frame.index,LIMIT.candidates-1); check(frame.index===this.sources.length,'PROTOCOL_ORDER');
    vfsPath(frame.vfs); check(MODS.includes(frame.mod)); hash(frame.sha256); integer(frame.bytes,LIMIT.source);
    string(frame.bodyBase64,LIMIT.frame,true);
    // Verify encoded length before allocating the decoded source buffer.
    check(frame.bodyBase64.length===4*Math.ceil(frame.bytes/3),'PROTOCOL_DIGEST');
    this.totalSource+=frame.bytes; check(this.totalSource<=LIMIT.totalSource,'PROTOCOL_LIMIT');
    const bytes=Buffer.from(frame.bodyBase64,'base64');
    check(bytes.length===frame.bytes && bytes.toString('base64')===frame.bodyBase64 && sha(bytes)===frame.sha256,'PROTOCOL_DIGEST');
    this.sources.push({index:frame.index,vfs:frame.vfs,mod:frame.mod,sha256:frame.sha256,bytes});
    return null;
  }
  captured(frame) {
    check(this.state==='SOURCES','PROTOCOL_ORDER');
    exact(frame,['v','kind','captureId','sourceCount','selectedDigest','layers','selected','archive','unsupportedRuntimeRules']);
    hash(frame.captureId); hash(frame.selectedDigest); integer(frame.sourceCount,LIMIT.candidates);
    check(frame.sourceCount===this.sources.length,'PROTOCOL_DIGEST');
    array(frame.layers,5); check(frame.layers.length===5);
    let candidateLayerEntries=0;
    for (let i=0;i<5;i++) {
      const layer=frame.layers[i]; exact(layer,['name','rootKind','rootDisplay','entries']);
      check(layer.name===MODS[i] && layer.rootKind===(i?'loose':'archive')); string(layer.rootDisplay);
      array(layer.entries,LIMIT.layerEntries);
      candidateLayerEntries+=layer.entries.length;
      check(candidateLayerEntries<=LIMIT.layerEntries,'PROTOCOL_LIMIT');
      for(const entry of layer.entries) {
        exact(entry,['vfs','sourceDisplay','sha256','bytes']); vfsPath(entry.vfs); string(entry.sourceDisplay);
        hash(entry.sha256); integer(entry.bytes,LIMIT.source);
      }
    }
    array(frame.selected,LIMIT.candidates); check(frame.selected.length===this.sources.length,'PROTOCOL_DIGEST');
    for(let i=0;i<frame.selected.length;i++) {
      const row=frame.selected[i],source=this.sources[i];
      exact(row,['index','vfs','mod','sha256','bytes','shadowed','archiveEntry','defaultLoaderFolder','realm']);
      check(row.index===i && row.vfs===source.vfs && row.mod===source.mod &&
        row.sha256===source.sha256 && row.bytes===source.bytes.length,'PROTOCOL_DIGEST');
      if(i)check(Buffer.compare(Buffer.from(frame.selected[i-1].vfs),Buffer.from(row.vfs))<0,'PROTOCOL_ORDER');
      array(row.shadowed,4);
      for(const shadow of row.shadowed) {
        exact(shadow,['mod','sourceDisplay','sha256']); check(MODS.includes(shadow.mod)); string(shadow.sourceDisplay); hash(shadow.sha256);
      }
      if(row.archiveEntry!==null) { vfsPath(row.archiveEntry); check(row.archiveEntry===row.vfs && row.mod==='public'); }
      check(row.defaultLoaderFolder===defaultFolder(row.vfs));
      check(row.realm===(row.vfs.startsWith('maps/')?'MAP_GENERATOR_REQUIRES_NATIVE_REALM_BINDING':
        row.vfs==='mod.json'?'METADATA':'SIMULATION_CANDIDATE'));
    }
    exact(frame.archive,['expectedSHA','actualSHA','size','chunkBytes','chunkCount','authorityKind']);
    const a=frame.archive;
    check(a.expectedSHA===ARCHIVE_SHA && a.actualSHA===ARCHIVE_SHA,'PROTOCOL_DIGEST');
    integer(a.size,LIMIT.archive,1); integer(a.chunkCount,2048,1);
    check(a.chunkBytes===LIMIT.chunk && a.chunkCount===Math.ceil(a.size/LIMIT.chunk) && a.authorityKind==='VERIFIED_HELD_FD_BYTES');
    array(frame.unsupportedRuntimeRules,64); for(const rule of frame.unsupportedRuntimeRules)string(rule,4096);
    const digest=sha(frame.selected.map(row=>`${row.vfs}\0${row.mod}\0${row.sha256}\0${row.bytes}`).join('\n'));
    check(digest===frame.selectedDigest,'PROTOCOL_DIGEST');
    const id=sha(JSON.stringify({version:1,archiveExpectedSHA:ARCHIVE_SHA,selectedDigest:digest}));
    check(id===frame.captureId,'PROTOCOL_DIGEST'); this.captureId=id;
    // This state permits one ABORT if producer analysis fails before FINISH.
    this.state='ANALYZING';
    const analyses=this.sources.map(source=> {
      const analysis=source.vfs.endsWith('.js')?analysisFor(source.bytes,source.vfs):null;
      if(analysis && analysis.parseStatus!=='PARSED')this.analysisBlocks++;
      return {index:source.index,sha256:source.sha256,analysis};
    });
    this.state='FINISH_READY';
    return {v:1,kind:'FINISH',captureId:id,analyses,tool:{nodeVersion:process.version,acornVersion:acorn.version,
      nodeSourceSHA256:sha(fs.readFileSync(__filename))}};
  }
  completed(frame) {
    check(this.state==='FINISH_READY','PROTOCOL_ORDER');
    exact(frame,['v','kind','captureId','status','artifactHashes','sourceClosure','native']);
    check(frame.captureId===this.captureId,'PROTOCOL_DIGEST');
    check(frame.sourceClosure===false && frame.native===false);
    check(frame.status===(this.analysisBlocks?'CAPTURE_COMPLETE_WITH_ANALYSIS_BLOCKS':'CAPTURE_COMPLETE_CANDIDATE_ONLY'));
    exact(frame.artifactHashes,HASH_FILES); for(const file of HASH_FILES)hash(frame.artifactHashes[file]);
    this.state='COMPLETED'; this.completion=frame; return null;
  }
}

async function RunCapture(outputLeaf) {
  check(typeof outputLeaf==='string' && /^[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}$/.test(outputLeaf),'BAD_OUTPUT_LEAF');
  check(process.version==='v26.0.0' && acorn.version==='8.16.0','TOOL_RUNTIME_MISMATCH');
  const helper=path.join(__dirname,'t17-save-five-mod-capture.py');
  const schema=path.join(__dirname,'t17-save-five-mod-analysis-schema.json');
  check(sha(fs.readFileSync(schema))===SCHEMA_SHA,'TOOL_SCHEMA_MISMATCH');
  // One process only. There is no caller-selected executable, path, hash or retry.
  return new Promise(resolve=> {
    const session=new ProtocolSession();
    let child, pending=Buffer.alloc(0), rawBytes=0, diagnosticsBytes=0;
    let failure=null, settled=false, closed=false, abortSent=false, terminating=false;
    let killTimer=null, reapTimer=null;
    const deadline=setTimeout(()=>stop('TIMEOUT'),LIMIT.wall);
    function finish(result) {
      if(settled)return; settled=true;
      clearTimeout(deadline); if(killTimer)clearTimeout(killTimer); if(reapTimer)clearTimeout(reapTimer);
      resolve(result);
    }
    function result(reason) {
      return {status:'UNKNOWN_TOOL_CAPTURE',reasonCode:reason,sourceClosure:false,native:false,
        pythonDiskReadback:'NOT_INDEPENDENTLY_VERIFIED_BY_NODE'};
    }
    function send(frame) {
      const bytes=Buffer.from(JSON.stringify(frame)+'\n');
      check(bytes.length-1<=LIMIT.frame,'PROTOCOL_LIMIT');
      rawBytes+=bytes.length; check(rawBytes<=LIMIT.raw,'PROTOCOL_LIMIT');
      child.stdin.write(bytes,error=> { if(error)stop('CHILD_STDIN'); });
    }
    function stop(code) {
      if(settled || failure)return;
      failure=code;
      // ABORT is allowed once after CAPTURED, including producer failure before
      // FINISH. It cannot make an earlier partial capture acceptable.
      if(child && !closed && !abortSent && ['ANALYZING','FINISH_READY'].includes(session.state)) {
        abortSent=true;
        try {
          const reason=code==='NODE_ANALYSIS'?'NODE_ANALYSIS':code.includes('LIMIT')?'NODE_LIMIT':'NODE_PROTOCOL';
          send({v:1,kind:'ABORT',code:reason});
        } catch (_) { /* The terminal failure remains; no second ABORT/retry. */ }
      }
      if(!child || closed) { finish(result(code)); return; }
      try { child.stdin.end(); } catch (_) { /* retain unknown cleanup */ }
      if(!terminating) {
        terminating=true;
        try { child.kill('SIGTERM'); } catch (_) { /* wait for close or bounded reap */ }
        // These are cleanup escalation/reap bounds after the fixed stop time,
        // not additional capture time or a second attempt.
        killTimer=setTimeout(()=> {
          if(!closed) { try { child.kill('SIGKILL'); } catch (_) { /* unknown */ } }
        },1000);
        reapTimer=setTimeout(()=> { if(!closed)finish(result('RESOURCE_CLOSE_UNKNOWN')); },2000);
      }
    }
    function receive(chunk) {
      if(settled || failure)return;
      try {
        check(Buffer.isBuffer(chunk),'PROTOCOL_UTF8');
        rawBytes+=chunk.length; check(rawBytes<=LIMIT.raw,'PROTOCOL_LIMIT');
        let offset=0;
        while(offset<chunk.length) {
          const newline=chunk.indexOf(10,offset);
          const end=newline===-1?chunk.length:newline;
          check(pending.length+end-offset<=LIMIT.frame,'PROTOCOL_LIMIT');
          pending=Buffer.concat([pending,chunk.subarray(offset,end)]);
          if(newline===-1)break;
          check(pending.length>0,'PROTOCOL_JSON');
          const frame=decodeFrame(pending); pending=Buffer.alloc(0);
          const reply=session.accept(frame);
          if(reply)send(reply);
          if(session.state==='COMPLETED')child.stdin.end();
          offset=newline+1;
        }
      } catch(error) { stop(error.code || 'NODE_ANALYSIS'); }
    }
    try {
      child=cp.spawn(PYTHON,['-u',helper],{shell:false,stdio:['pipe','pipe','pipe']});
      child.on('error',()=>stop('CHILD_SPAWN'));
      child.stdin.on('error',()=>stop('CHILD_STDIN'));
      child.stdout.on('data',receive);
      child.stdout.on('error',()=>stop('CHILD_STDOUT'));
      child.stderr.on('data',chunk=> {
        if(settled || failure)return;
        diagnosticsBytes+=chunk.length; if(diagnosticsBytes>LIMIT.diagnostics)stop('PROTOCOL_LIMIT');
      });
      child.stderr.on('error',()=>stop('CHILD_STDERR'));
      child.on('close',(code,signal)=> {
        closed=true;
        if(failure) { finish(result(failure)); return; }
        if(pending.length || session.state!=='COMPLETED' || code!==0 || signal) {
          finish(result('CHILD_EOF_OR_TERMINAL_MISMATCH')); return;
        }
        // The helper owns actual disk readback; Node only checks its exact
        // terminal declaration and drained process exit, never opens outputs.
        finish({...session.completion,pythonDiskReadback:'DECLARED_BY_PYTHON_NOT_INDEPENDENT_NODE_FS_PROOF'});
      });
      send({v:1,kind:'BEGIN',outputLeaf});
    } catch(error) { stop(error.code || 'CHILD_SPAWN'); }
  });
}

module.exports={analyze,strictDecode,defaultFolder,decodeFrame,ProtocolSession,RunCapture,ARCHIVE_SHA};
if(require.main===module) {
  if(process.argv.length!==3) {
    process.stderr.write('Exactly one fresh output leaf is required.\n'); process.exitCode=1;
  } else {
    RunCapture(process.argv[2]).then(result=> {
      process.stdout.write(JSON.stringify(result)+'\n');
      if(result.status.startsWith('UNKNOWN'))process.exitCode=1;
    }).catch(error=> {
      process.stderr.write(JSON.stringify({status:'UNKNOWN_TOOL_CAPTURE',reasonCode:error.code || 'NODE_FAILURE',
        sourceClosure:false,native:false})+'\n'); process.exitCode=1;
    });
  }
}
