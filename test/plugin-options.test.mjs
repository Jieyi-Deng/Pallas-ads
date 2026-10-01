import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync, mkdirSync, copyFileSync, writeFileSync, rmSync, existsSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join, resolve, dirname} from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
const here=dirname(fileURLToPath(import.meta.url));
const root=mkdtempSync(join(tmpdir(),'pallas-plugin-unit-'));
mkdirSync(join(root,'scripts')); mkdirSync(join(root,'.codex-plugin'));
copyFileSync(resolve(here,'../plugins/pallas/scripts/pallas.mjs'),join(root,'scripts/pallas.mjs'));
copyFileSync(resolve(here,'../lib/installer.mjs'),join(root,'scripts/installer.mjs'));
writeFileSync(join(root,'.codex-plugin/plugin.json'),JSON.stringify({version:'0.1.0'}));
const {options,lock}=await import(pathToFileURL(join(root,'scripts/pallas.mjs')));
test.after(()=>rmSync(root,{recursive:true,force:true}));
test('native setup requires explicit client and project, never defaults to a saved customer',()=>{
  assert.throws(()=>options(['setup']),/requires/);
  assert.throws(()=>options(['setup','--project','/tmp/a']),/requires/);
  assert.deepEqual(options(['setup','--project',"/tmp/account 'one'",'--client','claude','--migrate']),{command:'setup',project:"/tmp/account 'one'",client:'claude',migrate:true});
  assert.equal(options(['setup','--project','/tmp/project','--client','claude','--install-command']).installCommand,true);
});
test('native commands reject unknown, repeated and out-of-scope options',()=>{
  for(const args of [['setup','--client','bad'],['serve','--migrate'],['serve','--install-command'],['setup','--install-command','--install-command'],['setup','--project','a','--project','b'],['setup','--project'],['serve','--trust-local-certificate']]) assert.throws(()=>options(args));
});
test('workspace lock prevents concurrent servers and releases idempotently',()=>{
  const path=join(root,'workspace.lock'); const release=lock(path);
  assert.ok(existsSync(join(path,'owner.json')));
  assert.throws(()=>lock(path),/already active/);
  release();release();const releaseAgain=lock(path); releaseAgain();
});
