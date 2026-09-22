import {spawnSync} from 'node:child_process';
import {resolve} from 'node:path';
import assert from 'node:assert/strict';
const project=resolve(process.argv[2]);
const frames=[
  {jsonrpc:'2.0',id:1,method:'initialize',params:{protocolVersion:'2025-11-25',capabilities:{},clientInfo:{name:'pallas-plugin-ci',version:'1'}}},
  {jsonrpc:'2.0',method:'notifications/initialized'},
  {jsonrpc:'2.0',id:2,method:'tools/list'},
  {jsonrpc:'2.0',id:3,method:'tools/call',params:{name:'profile_get_context',arguments:{}}}
];
const result=spawnSync(process.execPath,[resolve('plugins/pallas/scripts/pallas.mjs'),'serve','--project',project],{input:frames.map(JSON.stringify).join('\n')+'\n',encoding:'utf8',timeout:20000});
assert.equal(result.status,0,result.stderr);
assert.equal(result.stderr,'');
const responses=result.stdout.trim().split('\n').map(JSON.parse);
assert.equal(responses.find(x=>x.id===2).result.tools.length,10);
assert.equal(responses.find(x=>x.id===3).result.structuredContent.status,'needs_input');
console.log('Plugin stdio handshake, ten tools and empty-project invocation passed.');
