import {createHash} from 'node:crypto';
import {spawn, spawnSync} from 'node:child_process';
import {existsSync, lstatSync, mkdirSync, readFileSync, readdirSync, realpathSync, writeFileSync, chmodSync, rmSync} from 'node:fs';
import {dirname, join, resolve, basename, parse} from 'node:path';
import {homedir} from 'node:os';
import {fileURLToPath} from 'node:url';
import {createInterface} from 'node:readline/promises';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const RECEIPT = '.pallas/npm-install.json';
export const UV = {
  version: '0.10.8',
  arm64: {target: 'aarch64-apple-darwin', sha256: 'c3a6fff5b6b4abddff863117878194e35dbc6b0267d61ad259ab9896f9b8dcbb'},
  x64: {target: 'x86_64-apple-darwin', sha256: 'e0a1b22b039f8155765f5bc8c13df03a5f994a901901179791572e8e5f053281'},
};
export function sha256(data) { return createHash('sha256').update(data).digest('hex'); }
export function parseArgs(args) {
  const result = {command: args[0] ?? 'help'};
  if (['--help', '-h'].includes(result.command)) result.command = 'help';
  if (result.command === '--version') result.command = 'version';
  if (!['install', 'doctor', 'update', 'help', 'version'].includes(result.command)) throw Error('Use install, doctor, update, --help or --version.');
  const names = {'--client': 'client', '--directory': 'directory', '--python': 'python'};
  for (let i = 1; i < args.length; i++) {
    const option = args[i];
    if (option === '--managed-python') { result.managedPython = true; continue; }
    if (!names[option] || !args[i + 1] || args[i + 1].startsWith('--')) throw Error(`Unknown or incomplete option: ${option}`);
    if (result[names[option]] !== undefined) throw Error(`Repeated option: ${option}`);
    result[names[option]] = args[++i];
  }
  if (result.client && !['codex', 'claude'].includes(result.client)) throw Error('--client must be codex or claude.');
  if (result.python && result.managedPython) throw Error('Choose --python or --managed-python, not both.');
  if (result.command !== 'install' && (result.python || result.managedPython || result.client)) throw Error('Client/Python options apply only to install.');
  return result;
}
export function canonicalDirectory(input) {
  const expanded = input === '~' ? homedir() : input.startsWith('~/') ? join(homedir(), input.slice(2)) : input;
  let current = resolve(expanded);
  const missing = [];
  // Canonicalize existing parents, including macOS's /tmp alias, before storing paths.
  while (!existsSync(current)) {
    if (lstatSafe(current)?.isSymbolicLink()) throw Error('Broken symlink in destination.');
    missing.unshift(basename(current)); current = dirname(current);
  }
  const path = join(realpathSync(current), ...missing);
  if ([parse(path).root, realpathSync(homedir())].includes(path)) throw Error('Choose a dedicated project directory, not your home or filesystem root.');
  return path;
}
function lstatSafe(path) { try { return lstatSync(path); } catch (error) { if (error.code === 'ENOENT') return null; throw error; } }
export function validateFresh(directory) {
  const state = lstatSafe(directory);
  if (state && (!state.isDirectory() || state.isSymbolicLink() || readdirSync(directory).length)) throw Error('Choose a new or empty project directory. Existing project files are never replaced.');
  for (const suffix of ['-runtime', '-runtime-tools']) {
    if (lstatSafe(directory + suffix)) throw Error(`The adjacent ${suffix} directory already exists. Use doctor for an existing install; preserve partial state and choose a new name to retry.`);
  }
}
export function verifiedResources(root = ROOT) {
  const directory = join(root, 'resources');
  const manifest = JSON.parse(readFileSync(join(directory, 'npm-runtime.json'), 'utf8'));
  if (!/^pallas_ads-[a-zA-Z0-9.]+-py3-none-any\.whl$/.test(manifest.wheel)) throw Error('Invalid bundled wheel filename.');
  for (const name of [manifest.wheel, 'install_macos.py', 'release-manifest.json']) {
    const file = join(directory, name);
    if (lstatSync(file).isSymbolicLink() || sha256(readFileSync(file)) !== manifest.files[name]) throw Error('Bundled runtime checksum mismatch; obtain a fresh package.');
  }
  return {directory, manifest};
}
function pythonCandidate(command) {
  const run = spawnSync(command, ['-I', '-c', 'import sys,json; print(json.dumps({"version":list(sys.version_info[:2]),"executable":sys.executable}))'], {encoding: 'utf8', timeout: 15000});
  if (run.status !== 0) return null;
  try {
    const result = JSON.parse(run.stdout.trim());
    return result.version[0] === 3 && [12, 13].includes(result.version[1]) ? result.executable : null;
  } catch { return null; }
}
export function findPython(explicit, candidate = pythonCandidate) {
  if (explicit) {
    const found = candidate(explicit);
    if (!found) throw Error('--python must point to Python 3.12 or 3.13.');
    return found;
  }
  for (const name of ['python3.13', 'python3.12', 'python3']) { const found = candidate(name); if (found) return found; }
  return null;
}
async function run(command, args, options = {}) {
  return new Promise((done, fail) => {
    const child = spawn(command, args, {stdio: 'inherit', shell: false, ...options});
    child.on('error', () => fail(Error(`Could not start ${basename(command)}.`)));
    child.on('exit', code => code === 0 ? done() : fail(Error(`${basename(command)} exited with status ${code}. Existing files were preserved; inspect the displayed error before retrying.`)));
  });
}
export async function downloadPinned(url, digest, destination) {
  if (!url.startsWith('https://github.com/astral-sh/uv/releases/download/')) throw Error('Unapproved bootstrap download URL.');
  const response = await fetch(url, {signal: AbortSignal.timeout(120000)});
  if (!response.ok || !response.url.startsWith('https://') || !response.body) throw Error('Could not download the pinned Python bootstrap.');
  const chunks = []; let bytes = 0;
  for await (const chunk of response.body) {
    bytes += chunk.length;
    if (bytes > 40 * 1024 * 1024) throw Error('Bootstrap download exceeds its size limit.');
    chunks.push(chunk);
  }
  const data = Buffer.concat(chunks);
  if (sha256(data) !== digest) throw Error('Bootstrap checksum mismatch; no downloaded code was executed.');
  writeFileSync(destination, data, {flag: 'wx', mode: 0o600});
}
export async function managedPython(directory) {
  const platform = UV[process.arch];
  if (!platform) throw Error('Managed Python supports Apple Silicon and Intel Macs.');
  const tools = directory + '-runtime-tools';
  mkdirSync(tools, {recursive: false, mode: 0o700});
  console.log('Preparing a Pallas-local Python 3.13. No system Python or shell profile will be changed.');
  const archive = join(tools, 'uv.tar.gz');
  await downloadPinned(`https://github.com/astral-sh/uv/releases/download/${UV.version}/uv-${platform.target}.tar.gz`, platform.sha256, archive);
  await run('/usr/bin/tar', ['-xzf', archive, '-C', tools]);
  const uv = join(tools, `uv-${platform.target}`, 'uv');
  chmodSync(uv, 0o700);
  const pythonDir = join(tools, 'python');
  const env = {...process.env, UV_PYTHON_INSTALL_DIR: pythonDir, UV_CACHE_DIR: join(tools, 'cache')};
  await run(uv, ['python', 'install', '3.13', '--no-bin', '--no-config'], {env});
  const found = spawnSync(uv, ['python', 'find', '3.13', '--managed-python', '--no-config'], {env, encoding: 'utf8', timeout: 15000});
  const executable = found.stdout?.trim();
  if (found.status !== 0 || !executable?.startsWith(pythonDir + '/') || !pythonCandidate(executable)) throw Error('Managed Python is incomplete. Preserve the runtime-tools directory and inspect the download error.');
  rmSync(archive);
  return executable;
}
function receiptFor(directory) {
  const path = join(directory, RECEIPT);
  if (!existsSync(path) || lstatSync(path).isSymbolicLink()) throw Error('No npm-managed Pallas installation here. Supply --directory for the installed project.');
  const receipt = JSON.parse(readFileSync(path, 'utf8'));
  if (receipt.project !== directory || receipt.runtime !== directory + '-runtime' || !['codex', 'claude'].includes(receipt.client)) throw Error('Installation receipt does not match this directory.');
  return receipt;
}
async function doctor(directory) {
  const receipt = receiptFor(directory);
  await run(join(receipt.runtime, 'bin/pallas'), ['agent', 'doctor', '--directory', directory]);
  return receipt;
}
async function selectInstall(options) {
  if (options.client && options.directory) return options;
  if (!process.stdin.isTTY) throw Error('Non-interactive install requires --client codex|claude and --directory PATH.');
  const prompt = createInterface({input: process.stdin, output: process.stdout});
  try {
    if (!options.client) {
      const answer = (await prompt.question('Agent / 客户端: 1) Codex  2) Claude Code [1]: ')).trim();
      if (!['', '1', '2', 'codex', 'claude'].includes(answer)) throw Error('Choose 1 (Codex) or 2 (Claude Code).');
      options.client = ['2', 'claude'].includes(answer) ? 'claude' : 'codex';
    }
    if (!options.directory) options.directory = (await prompt.question(`New project / 新项目目录 [~/pallas-${options.client}]: `)).trim() || `~/pallas-${options.client}`;
    return options;
  } finally { prompt.close(); }
}
export async function main(args = process.argv.slice(2)) {
  const options = parseArgs(args);
  const pkg = JSON.parse(readFileSync(join(ROOT, 'package.json'), 'utf8'));
  if (options.command === 'version') { console.log(pkg.version); return; }
  if (options.command === 'help') {
    console.log(`Pallas ${pkg.version} — local analysis installer (macOS, Node.js 22+)\n\nCommands: install | doctor | update\n  install [--client codex|claude] [--directory PATH]\n          [--python EXECUTABLE | --managed-python]\n  doctor --directory PATH\n  update --directory PATH\n\nInstall prompts for client and a new project. Existing projects/global settings are not overwritten.\nA missing supported Python is provisioned locally; downloads require internet.\nDefault setup does not authorize media, install certificates or request API keys.\nReload your agent in the generated project and confirm host trust after installation.`);
    return;
  }
  if (process.platform !== 'darwin' || !UV[process.arch]) throw Error('This Alpha installer supports macOS on Apple Silicon or Intel.');
  if (options.command === 'doctor') { await doctor(canonicalDirectory(options.directory || process.cwd())); return; }
  const {directory: resources, manifest} = verifiedResources();
  if (options.command === 'update') {
    const directory = canonicalDirectory(options.directory || process.cwd());
    const receipt = await doctor(directory);
    if (receipt.installerVersion === pkg.version && receipt.wheelSha256 === manifest.files[manifest.wheel]) {
      console.log('This project already has the runtime and Skills supplied by this installer version.'); return;
    }
    console.log('Updating the runtime; saved data and MCP configuration remain in place.');
    await run(join(receipt.runtime, 'bin/python'), ['-m', 'pip', 'install', join(resources, manifest.wheel)]);
    await run(join(receipt.runtime, 'bin/pallas'), ['agent', 'refresh-skills', '--directory', directory]);
    await doctor(directory);
    writeReceipt(directory, {...receipt, installerVersion: pkg.version, runtimeVersion: manifest.runtimeVersion, wheelSha256: manifest.files[manifest.wheel]});
    console.log('Update complete. Review the Skills backup and restart your agent task.'); return;
  }
  await selectInstall(options);
  const directory = canonicalDirectory(options.directory);
  if (existsSync(join(directory, RECEIPT))) {
    const receipt = await doctor(directory);
    if (receipt.client !== options.client) throw Error('This project belongs to a different client. Choose a separate new project.');
    console.log('Pallas is already installed here. Use update to change versions.'); return;
  }
  validateFresh(directory);
  mkdirSync(dirname(directory), {recursive: true});
  let python = options.managedPython ? null : findPython(options.python);
  console.log(`Installing Pallas ${manifest.runtimeVersion} for ${options.client} in ${directory}`);
  if (!python) python = await managedPython(directory);
  await run(python, [join(resources, 'install_macos.py'), '--directory', directory, '--client', options.client]);
  writeReceipt(directory, {project: directory, runtime: directory + '-runtime', client: options.client,
    installerVersion: pkg.version, runtimeVersion: manifest.runtimeVersion, wheelSha256: manifest.files[manifest.wheel]});
  console.log(`\nReady / 安装完成: ${directory}\nOpen this project, confirm host trust and start a new task.\nTry / 试用: 请用 Pallas 预览 samples/meta_campaign_daily.csv，确认后生成分析报告。`);
}
function writeReceipt(directory, receipt) { writeFileSync(join(directory, RECEIPT), JSON.stringify(receipt, null, 2) + '\n', {mode: 0o600}); }
