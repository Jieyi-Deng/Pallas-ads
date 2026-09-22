# Pallas installer reference

For the native Codex / Claude Code plugin, start with [PLUGIN_INSTALL.md](PLUGIN_INSTALL.md). This page covers the npm project installation; use one entry per project.

The npm launcher prepares the Pallas runtime, local MCP configuration, and the `pallas-workflow` and `pallas-analysis` Skills. Start with [INSTALL.md](INSTALL.md) for the complete install, activation, and first-use flow.

## Install

Requires macOS on Apple Silicon or Intel, Node.js 22+, and internet access.

```sh
npx pallas-ads install
```

The installer asks for Codex or Claude Code and a new project directory. For non-interactive use:

```sh
npx pallas-ads install --client codex --directory "$HOME/pallas-codex"
```

Use `--client claude` for Claude Code. An alternative package source is `npx github:Jieyi-Deng/Pallas-ads install`.

A supported Python 3.12 or 3.13 is reused. If none is available, the installer downloads a pinned, SHA-256-verified uv binary and prepares Python 3.13 alongside the runtime. Choose `--managed-python` to explicitly use a dedicated Python, or `--python /absolute/path/to/python3.13` to select an existing interpreter. These options are mutually exclusive.

Installation runs only when `install` is invoked; the package has no npm installation lifecycle hooks. It does not change shell profiles or global agent settings.

## Project files

Keep the project and the adjacent `-runtime` and optional `-runtime-tools` directories in place. Imported data and reports are stored in the project's `.pallas` directory. Each installation uses a new or empty dedicated project; it does not merge arbitrary existing projects.

Open the generated folder in your agent, confirm trust, and start a new task. Follow [AUTHORIZATION.md](AUTHORIZATION.md) to connect a media account, then analyze its data or provide your own export as described in [FILE_IMPORT.md](FILE_IMPORT.md). File-only analysis can skip authorization. After a successful analysis, use the [recurring-check workflow](README.md#5-set-up-recurring-checks) if your agent supports scheduling.

## Diagnose

```sh
npx pallas-ads doctor --directory "$HOME/pallas-codex"
```

The check covers local installation and reports media setup separately. Confirm tool loading in an actual agent task and verify media access by listing authorized accounts.

## Update

Back up your project, then run:

```sh
npx pallas-ads@latest update --directory "$HOME/pallas-codex"
```

The update uses the runtime bundled with the selected installer. It retains project data and MCP configuration and backs up Skills before refreshing them. Review any custom Skills changes against that backup, then restart your agent task. Consult [Releases](https://github.com/Jieyi-Deng/Pallas-ads/releases) for version details.

## Recover an interrupted installation

Preserve the error message and partial directories. Do not delete or overwrite a populated project to retry. If a completed installation receipt exists, run `doctor`. Otherwise, ask your agent to inspect the failed step or contact [support@pallas-ads.com](mailto:support@pallas-ads.com). Re-running `install` on a completed installation checks it without replacing files.

## Remove an installation

Back up reports and imported data first. Remove only the project and adjacent runtime directories created for that installation, once they are no longer needed. Removing `.pallas` deletes its local analysis data. Revoke connected media access separately in the agent and the media platform; deleting local files does not revoke consent.
