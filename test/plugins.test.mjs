import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,readdirSync,lstatSync} from 'node:fs';
import {join,resolve} from 'node:path';
import {createHash} from 'node:crypto';
const root=resolve(process.env.PALLAS_PLUGIN_DISTRIBUTION || '.');
const plugin=join(root,'plugins/pallas');
const json=path=>JSON.parse(readFileSync(path,'utf8'));
const hash=data=>createHash('sha256').update(data).digest('hex');
function walk(dir,prefix='') {
  return readdirSync(dir).sort().flatMap(name=>{
    const path=join(dir,name),relative=prefix+name;
    assert.ok(!lstatSync(path).isSymbolicLink(),`No distribution symlinks: ${relative}`);
    return lstatSync(path).isDirectory()?walk(path,relative+'/'):[relative];
  });
}
test('every plugin file is covered by the immutable distribution inventory',()=>{
  const manifest=json(join(plugin,'distribution-manifest.json')).files;
  assert.deepEqual(walk(plugin).filter(x=>x!=='distribution-manifest.json').sort(),Object.keys(manifest).sort());
  for(const [name,digest] of Object.entries(manifest)) {
    assert.ok(!name.startsWith('/') && !name.split('/').includes('..'));
    assert.equal(hash(readFileSync(join(plugin,name))),digest,name);
    assert.ok(!/(^|\/)(\.env|\.pallas|__pycache__|google-desktop\.json)(\/|$)|\.(pem|key)$/.test(name),name);
  }
});
test('both native catalogs resolve one self-contained plugin and the same Skills',()=>{
  for(const path of ['.agents/plugins/marketplace.json','.claude-plugin/marketplace.json']) {
    const m=json(join(root,path));assert.equal(m.name,'pallas-ads');assert.equal(m.plugins.length,1);
    assert.equal(m.plugins[0].name,'pallas');
    assert.equal(typeof m.plugins[0].source==='string'?m.plugins[0].source:m.plugins[0].source.path,'./plugins/pallas');
  }
  const codex=json(join(plugin,'.codex-plugin/plugin.json')),claude=json(join(plugin,'.claude-plugin/plugin.json'));
  assert.equal(codex.name,'pallas');assert.equal(claude.version,codex.version);
  assert.deepEqual(json(join(plugin,codex.mcpServers)).mcpServers,{});
  assert.equal(json(join(plugin,claude.mcpServers)).mcpServers.pallas.args[0],'${CLAUDE_PLUGIN_ROOT}/scripts/pallas.mjs');
  for(const name of ['pallas-setup','pallas-workflow','pallas-analysis']) assert.match(readFileSync(join(plugin,'skills',name,'SKILL.md'),'utf8'),/^---/);
  for(const name of ['scripts/pallas.mjs','scripts/project.py','scripts/serve.py','assets/pallas-logo.png','skills/pallas-analysis/assets/report.html']) assert.ok(readFileSync(join(plugin,name)).length>0);
});
test('bundled runtime checksums match and no operator Google configuration is embedded',()=>{
  const resources=join(plugin,'resources'),manifest=json(join(resources,'npm-runtime.json'));
  for(const [name,digest] of Object.entries(manifest.files)) assert.equal(hash(readFileSync(join(resources,name))),digest,name);
  assert.equal(json(join(resources,'release-manifest.json')).google_application_embedded,false);
});
