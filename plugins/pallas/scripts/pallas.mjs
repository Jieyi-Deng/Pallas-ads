#!/usr/bin/env node
import {spawn} from 'node:child_process';
import {existsSync, mkdirSync, readFileSync, writeFileSync, realpathSync, lstatSync, rmSync} from 'node:fs';
import {dirname, join, resolve, relative, isAbsolute} from 'node:path';
import {homedir} from 'node:os';
import {fileURLToPath} from 'node:url';
import {canonicalDirectory, findPython, managedPython, verifiedResources} from './installer.mjs';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const RECEIPT = '.pallas/plugin-install.json';
const VERSION = JSON.parse(readFileSync(join(ROOT, '.codex-plugin/plugin.json'))).version;
export function options(args) {
  const result = {command: args.shift() || 'help'};
  if (['--help','-h'].includes(result.command)) result.command = 'help';
  if (!['setup','serve','doctor','rollback','deactivate','connect-meta','help'].includes(result.command)) throw Error('Use setup, serve, doctor, rollback, deactivate or connect-meta.');
  while (args.length) {
    const key = args.shift();
    if (key === '--migrate') { result.migrate = true; continue; }
    if (!['--project','--client','--python'].includes(key) || !args.length || args[0].startsWith('--') || result[key.slice(2)]) throw Error('Unknown, repeated or incomplete argument.');
    result[key.slice(2)] = args.shift();
  }
  if (result.client && !['codex','claude'].includes(result.client)) throw Error('Client must be codex or claude.');
  if (result.command === 'setup' && (!result.project || !result.client)) throw Error('Setup requires --project /absolute/path and --client codex|claude.');
  if (result.command !== 'setup' && (result.client || result.python || result.migrate)) throw Error('Client, Python and migrate options apply only to setup.');
  return result;
}
function regular(path) {
  if (!existsSync(path) || !lstatSync(path).isFile() || lstatSync(path).isSymbolicLink()) throw Error('Missing or unsafe Pallas installation file. Run the plugin setup Skill.');
}
function projectPath(value) {
  const project = canonicalDirectory(value || process.env.PALLAS_PROJECT || process.env.CLAUDE_PROJECT_DIR || process.cwd());
  const location = relative(ROOT, project);
  if (!location || (!location.startsWith('..') && !isAbsolute(location))) throw Error('Choose a project outside the installed plugin directory.');
  // Never infer a parent project or fall back to another customer's saved workspace.
  for (const part of ['.pallas', '.pallas/plugin-install.json', '.pallas/plugin.lock']) {
    const path = join(project,part);
    try { if (lstatSync(path).isSymbolicLink()) throw Error('Pallas state must not be a symlink.'); }
    catch (e) { if (e.code !== 'ENOENT') throw e; }
  }
  return project;
}
export function lock(path) {
  try { mkdirSync(path, {mode:0o700}); }
  catch (e) { if (e.code === 'EEXIST') throw Error(`Pallas is already active or a previous run stopped unexpectedly. Close its sessions and inspect ${path}/owner.json before removing a stale lock.`); throw e; }
  try { writeFileSync(join(path,'owner.json'), JSON.stringify({pid:process.pid,started:new Date().toISOString()}),{flag:'wx',mode:0o600}); }
  catch (e) { rmSync(path,{recursive:true,force:true}); throw e; }
  let released = false;
  return () => { if (!released) { released=true; rmSync(path,{recursive:true,force:true}); } };
}
async function run(command,args,{protocol=false,cwd}={}) {
  return new Promise((done,fail)=>{
    const child=spawn(command,args,{cwd,shell:false,stdio:protocol ? 'inherit' : ['ignore','inherit','inherit']});
    const signals=['SIGINT','SIGTERM','SIGHUP'];
    const handlers=signals.map(signal=>{ const handler=()=>child.kill(signal); process.on(signal,handler); return [signal,handler]; });
    const cleanup=()=>handlers.forEach(([signal,handler])=>process.off(signal,handler));
    child.once('error',()=>{cleanup();fail(Error(`Cannot start ${command}. Run plugin setup to repair the runtime.`));});
    child.once('exit',(code,signal)=>{cleanup();code===0?done():fail(Error(`Pallas exited ${signal || code}. See the preceding diagnostic.`));});
  });
}
function cacheRoot() {
  return canonicalDirectory(process.env.PALLAS_DATA_HOME || join(homedir(),'.local/share/pallas'));
}
async function prepareRuntime(resources,manifest,explicitPython) {
  const base=join(cacheRoot(),'runtimes'); mkdirSync(base,{recursive:true,mode:0o700});
  const runtime=join(base,manifest.files[manifest.wheel]);
  if (existsSync(runtime) && lstatSync(runtime).isSymbolicLink()) throw Error('Runtime must not be a symlink.');
  const ready=join(runtime,'pallas-runtime.json'), python=join(runtime,'bin/python');
  if (existsSync(ready)) {
    const record=JSON.parse(readFileSync(ready));
    if (record.wheelSha256!==manifest.files[manifest.wheel] || !existsSync(python)) throw Error('Runtime receipt mismatch. Preserve the directory and repair the installation.');
    return runtime;
  }
  const release=lock(runtime+'.lock');
  try {
    if (!existsSync(python)) {
      const interpreter=findPython(explicitPython) || await managedPython(runtime);
      await run(interpreter,['-I','-c','import sys,venv; venv.EnvBuilder(with_pip=True,symlinks=True).create(sys.argv[1])',runtime]);
    }
    await run(python,['-m','pip','install',join(resources,manifest.wheel)]);
    await run(python,['-I','-c',"from importlib.metadata import version; print('Pallas ' + version('pallas-ads'))"]);
    writeFileSync(ready,JSON.stringify({wheelSha256:manifest.files[manifest.wheel],runtimeVersion:manifest.runtimeVersion}),{mode:0o600});
    return runtime;
  } finally { release(); }
}
function receipt(project) {
  const path=join(project,RECEIPT); regular(path);
  const binding=JSON.parse(readFileSync(path));
  if (binding.project!==project || !['codex','claude'].includes(binding.client) || !/^[a-f0-9]{64}$/.test(binding.wheelSha256)) throw Error('Project binding is invalid or the project moved. Run setup for this exact project.');
  // Only use our managed runtime path, not an arbitrary executable in a project file.
  const runtime=join(cacheRoot(),'runtimes',binding.wheelSha256);
  regular(join(runtime,'pallas-runtime.json'));
  const record=JSON.parse(readFileSync(join(runtime,'pallas-runtime.json')));
  if (record.wheelSha256!==binding.wheelSha256) throw Error('Runtime checksum identity mismatch.');
  return {...binding,runtime};
}
export async function main(args=process.argv.slice(2)) {
  const opts=options([...args]);
  if(opts.command==='help') {
    console.log('Pallas native plugin\nsetup --client codex|claude --project PATH [--python EXECUTABLE] [--migrate]\nserve [--project PATH]\ndoctor --project PATH\nrollback --project PATH\ndeactivate --project PATH\nconnect-meta --project PATH (Claude Code only)\nSetup prepares a runtime and binds this project. It does not authorize media.'); return;
  }
  if(Number(process.versions.node.split('.')[0])<22) throw Error('Pallas requires Node.js 22 or newer.');
  if(process.platform!=='darwin') throw Error('Pallas setup and runtime support macOS.');
  const project=projectPath(opts.project);
  if(opts.command==='setup') {
    mkdirSync(join(project,'.pallas'),{recursive:true,mode:0o700});
    const release=lock(join(project,'.pallas/plugin.lock'));
    try {
      const {directory,manifest}=verifiedResources(ROOT);
      const runtime=await prepareRuntime(directory,manifest,opts.python);
      await run(join(runtime,'bin/python'),[join(ROOT,'scripts/project.py'),'setup',project,opts.client,runtime,VERSION,manifest.files[manifest.wheel],process.execPath,...(opts.migrate?['--migrate']:[])]);
      console.log('Pallas is prepared. Reload plugins or start a new agent session in this project. Then authorize a media account or provide an advertising export.');
    } finally {release();}
    return;
  }
  const binding=receipt(project);
  if(opts.command==='doctor') {
    console.log(JSON.stringify({project,client:binding.client,pluginVersion:binding.pluginVersion,runtime:binding.runtime,workspace:join(project,'.pallas'),mediaAuthorization:'Verify in the host; setup does not grant access.'}));
    await run(join(binding.runtime,'bin/python'),['-I','-c',"from importlib.metadata import version; print('Pallas ' + version('pallas-ads'))"]); return;
  }
  if(opts.command==='serve') {
    const {manifest}=verifiedResources(ROOT);
    if(binding.wheelSha256!==manifest.files[manifest.wheel]) throw Error('Plugin runtime changed. Run setup once to update this project, then reload.');
    await run(join(binding.runtime,'bin/python'),[join(ROOT,'scripts/serve.py'),join(project,'.pallas')],{protocol:true,cwd:project});
    return;
  }
  const release=lock(join(project,'.pallas/plugin.lock'));
  try {
    await run(join(binding.runtime,'bin/python'),[join(ROOT,'scripts/project.py'),opts.command,project]);
  } finally {release();}
}
if(process.argv[1] && realpathSync(process.argv[1])===fileURLToPath(import.meta.url)) main().catch(error=>{console.error(`Pallas: ${error.message}`);process.exitCode=1;});
