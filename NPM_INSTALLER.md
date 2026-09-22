# Pallas npm installer

A small Node.js launcher installs the existing Python Pallas runtime, local MCP configuration, `pallas-workflow` and `pallas-analysis` Skills, and synthetic samples. The analysis engine is not rewritten in JavaScript.

**macOS (Apple Silicon / Intel), Node.js 22+, internet access.** There are no npm dependencies or installation lifecycle scripts. Runtime installation happens only when you explicitly invoke `install`.

## Install

Published npm entry:

```sh
npx pallas-ads install
```

The interactive installer asks for Codex or Claude Code and a new project directory. For an agent or script:

```sh
npx pallas-ads install --client codex --directory "$HOME/pallas-codex"
```

The equivalent GitHub package entry is `npx github:Jieyi-Deng/Pallas-ads install`. Both routes are now published. For a fixed version use `npx pallas-ads@0.2.0-alpha.1 install`.

A supported local Python 3.12/3.13 is reused. Otherwise the installer downloads a pinned, SHA-256-verified uv binary from Astral's official GitHub release and uses it to provision Python 3.13 alongside the project's runtime. It does not change system Python, shell profiles or global agent configuration. Use `--managed-python` to explicitly choose this isolated Python, or `--python /absolute/python3.13` to select an existing one.

The installed project, adjacent `-runtime` and optional `-runtime-tools` directories must remain in place. Files and reports live in the project's `.pallas`. Installation targets a new/empty dedicated workspace; it does not merge into an existing coding project or install globally for every project.

After installation, open the generated folder in your agent, confirm project trust and start a new task. Ask Pallas to preview `samples/meta_campaign_daily.csv`; confirm the interpretation to generate a report. Default installation does not connect media, request API keys or change certificates. Live media access remains optional and separately verified.

## Check and update

```sh
npx pallas-ads doctor --directory "$HOME/pallas-codex"
npx pallas-ads@latest update --directory "$HOME/pallas-codex"
```

Updating uses the runtime bundled with the installer version you selected. The first release wraps Python runtime 0.2.0a1; it does not silently fetch a newer Python package. Saved data and MCP configuration remain in place; Skills updates keep a backup. Back up the project before upgrading. Update manages projects installed by this launcher, not unrelated installations.

Interrupted installs preserve partial state and report the affected step. Do not delete existing projects to retry. Diagnose the partial environment or choose a fresh project name. Re-running install on a successfully installed project checks it without overwriting files.

Only a publisher needs an npm account; users can install public packages without logging in. The full development repository is private; the distributed wheel includes readable runtime code under Apache-2.0. This is a local Alpha, not an unattended cloud service.

See https://github.com/Jieyi-Deng/Pallas-ads for file formats, media limitations and feedback instructions.
