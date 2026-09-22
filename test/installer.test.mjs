import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync, mkdirSync, writeFileSync, readFileSync, symlinkSync, rmSync, existsSync} from 'node:fs';
import {tmpdir, homedir} from 'node:os';
import {join} from 'node:path';
import {parseArgs, canonicalDirectory, validateFresh, findPython, verifiedResources, sha256, downloadPinned} from '../lib/installer.mjs';

function temporary(t) { const p = mkdtempSync(join(tmpdir(), 'pallas-npm-unit-')); t.after(() => rmSync(p, {recursive:true, force:true})); return p; }
test('explicit client/directory and managed Python parse without shell interpolation', () => {
  assert.deepEqual(parseArgs(['install','--client','claude','--directory',"/tmp/a 'quote' $(never)",'--managed-python']), {command:'install', client:'claude', directory:"/tmp/a 'quote' $(never)",managedPython:true});
  assert.equal(parseArgs(['--help']).command,'help');
});
test('refuse ambiguous and unknown installer arguments', () => {
  for (const args of [['install','--client','unknown'],['install','--directory'],['install','--trust-local-certificate'],['install','--python','x','--managed-python'],['doctor','--client','codex'],['install','--directory','a','--directory','b']]) assert.throws(()=>parseArgs(args));
});
test('existing project and adjacent runtime remain unchanged', t => {
  const root = temporary(t), project = join(root,'project'); mkdirSync(project);
  validateFresh(project);
  writeFileSync(join(project,'notes.md'),'keep');
  assert.throws(()=>validateFresh(project),/Existing project files/);
  assert.equal(readFileSync(join(project,'notes.md'),'utf8'),'keep');
  for(const suffix of ['-runtime','-runtime-tools']) {
    const candidate = join(root,'new'+suffix); mkdirSync(candidate);
    assert.throws(()=>validateFresh(join(root,'new')),/already exists/); rmSync(candidate,{recursive:true});
  }
});
test('canonicalize macOS temporary aliases but reject dangerous root destinations', t => {
  const root = temporary(t);
  assert.equal(canonicalDirectory(join(root,'future')),join(canonicalDirectory(root),'future'));
  assert.throws(()=>canonicalDirectory(homedir()),/dedicated/);
  assert.throws(()=>canonicalDirectory('/'),/dedicated/);
  symlinkSync(join(root,'missing'),join(root,'broken'));
  assert.throws(()=>canonicalDirectory(join(root,'broken','child')),/Broken symlink/);
});
test('runtime selection reuses supported Python and rejects bad explicit interpreter', () => {
  const calls=[];
  const candidate=name=>{calls.push(name);return name==='python3.12'?'/safe/python3.12':null;};
  assert.equal(findPython(undefined,candidate),'/safe/python3.12');
  assert.deepEqual(calls,['python3.13','python3.12']);
  assert.throws(()=>findPython('bad',()=>null),/3.12 or 3.13/);
  assert.equal(findPython(undefined,()=>null),null);
});
test('verify all executable resources and reject modified installer', t => {
  const root=temporary(t), resources=join(root,'resources'); mkdirSync(resources);
  const wheel='pallas_ads-0.2.0a1-py3-none-any.whl',files={};
  for(const name of [wheel,'install_macos.py','release-manifest.json']){ writeFileSync(join(resources,name),'synthetic'); files[name]=sha256('synthetic'); }
  writeFileSync(join(resources,'npm-runtime.json'),JSON.stringify({wheel,files}));
  assert.equal(verifiedResources(root).manifest.wheel,wheel);
  writeFileSync(join(resources,'install_macos.py'),'tampered');
  assert.throws(()=>verifiedResources(root),/checksum mismatch/);
});
test('bootstrap checksum failure never writes an executable or archive', async t => {
  const root=temporary(t), old=globalThis.fetch;
  t.after(()=>{globalThis.fetch=old;});
  globalThis.fetch=async()=>({ok:true,url:'https://release-assets.githubusercontent.com/example',body:(async function*(){yield Buffer.from('corrupted');})()});
  const path=join(root,'uv.tar.gz');
  await assert.rejects(downloadPinned('https://github.com/astral-sh/uv/releases/download/0.10.8/uv.tar.gz','0'.repeat(64),path),/checksum mismatch/);
  assert.ok(!existsSync(path));
  await assert.rejects(downloadPinned('http://example.com/run','x',path),/Unapproved/);
});
