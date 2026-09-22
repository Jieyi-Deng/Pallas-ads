# Install Pallas / 安装 Pallas

## Recommended npm-format launcher

Requires macOS and Node.js 22+. Python is provisioned automatically when needed. No npm login is needed to install public packages.

```sh
npx github:Jieyi-Deng/Pallas-ads#npm-v0.2.0-alpha.1 install
```

For non-interactive agent use:

```sh
npx github:Jieyi-Deng/Pallas-ads#npm-v0.2.0-alpha.1 install --client codex --directory "$HOME/pallas-codex"
```

Use `--client claude` for Claude Code. Choose a new/empty project. Follow the completion message: open that folder in the agent, confirm trust and start a new task. See [NPM_INSTALLER.md](NPM_INSTALLER.md) for runtime handling, diagnostics and updates. npm registry publication is pending publisher security verification; use this GitHub command until the README confirms the short registry command is available.

## Alternative original ZIP route

# Install Pallas 0.2.0a1 / 安装 Pallas

This is the version-pinned installation entry for Codex and Claude Code. The agent performs the technical steps; the user confirms permissions requested by their host. 本页可直接交给 Agent 执行，不要求广告用户手工编写命令或配置。

## Agent procedure / Agent 执行步骤

1. Confirm the current client (Codex or Claude Code) and check macOS plus Python 3.12/3.13. If Python is missing, explain that prerequisite and follow the user's normal software installation policy. Do not silently select an unsupported version. The package does not include an agent subscription or Python itself.
2. Use a new temporary download directory. Download both fixed release assets:
   - [pallas-0.2.0a1-local-alpha.zip](https://github.com/Jieyi-Deng/Pallas-ads/releases/download/v0.2.0a1/pallas-0.2.0a1-local-alpha.zip)
   - [SHA-256 checksum](https://github.com/Jieyi-Deng/Pallas-ads/releases/download/v0.2.0a1/pallas-0.2.0a1-local-alpha.zip.sha256)
3. Verify the ZIP's SHA-256 before extracting. Stop on mismatch. The checksum establishes release consistency, not an independent cryptographic publisher identity. The installer also checks the embedded wheel hash.
4. Extract the bundle, read its NEW_MACHINE_TESTING.md, and select a new/empty project directory (for example ~/pallas-test). Do not overwrite any existing runtime or project. Run from the extracted bundle, using an available supported interpreter:

```sh
python3.13 install_macos.py --directory "$HOME/pallas-test" --client codex
```

For Claude Code replace `codex` with `claude`. The default is core/local mode: do not add live Meta flags, certificate trust or Google requirements unless the user separately requests that route. Do not request OpenAI runtime keys, tokens or developer secrets for file analysis.

5. The installer creates the adjacent `pallas-test-runtime` environment, installs dependencies, initializes `.pallas`, and copies client MCP settings, both Skills and synthetic samples. Review its `agent doctor` output; optional media gaps are not local-analysis blockers. The MCP config uses an absolute executable path, so retain the runtime folder.
6. Tell the user to open the generated project in their selected agent, trust the project and start a new task. Respect host approval prompts; never bypass them. In the new task confirm the Pallas tools and Skills are available. Installation checks alone do not prove host loading.
7. Follow START_HERE.md and preview `samples/meta_campaign_daily.csv`. Show the interpretation in ordinary language, import after confirmation, generate the report and link its local HTML. The sample is synthetic, not live media evidence.

安装结束并不等于媒体授权。文件分析可以立即试用；媒体连接按 [测试指南](NEW_MACHINE_TESTING.md) 的可选矩阵另行操作。账户登录、同意、MFA 和系统信任确认由用户完成。

## Existing installation / 已有安装

Do not rerun the fresh installer over existing projects. Back up the project, upgrade the wheel using the runtime's Python, run `pallas agent refresh-skills --directory PROJECT`, retain its backup and restart the agent task. Keep `.pallas` and the user's own credentials; never copy somebody else's workspace or tokens.

This release is a local Alpha, not a cloud service or a marketplace one-click installation. There is no verified PyPI publication. No build from the private source repository is required.
