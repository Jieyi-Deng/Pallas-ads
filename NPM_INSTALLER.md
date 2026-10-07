# Pallas installer reference

For the native Codex / Claude Code plugin, start with [PLUGIN_INSTALL.md](PLUGIN_INSTALL.md). This is the complete guide for npm project installation, activation, updates and recovery. Use one installation method per project; do not run the npm updater on a project migrated to the native plugin.

This installer includes the unified Pallas command and dashboard Skills. Check the [npm package](https://www.npmjs.com/package/pallas-ads) for registry availability and `latest`; [release.json](release.json) records the component versions in this GitHub checkout. Channels may update at different times. To pin an installer, use `pallas-ads@<version>` with a published npm version.

The npm launcher prepares the Pallas runtime, local MCP configuration, and five Skills: `pallas`, `pallas-workflow`, `pallas-analysis`, `pallas-dashboard`, and `pallas-competitors`. Follow the activation steps below after installation. File analysis needs no media authorization or separate OpenAI runtime API key.

## Install

Requires macOS on Apple Silicon or Intel, Node.js 22+, and internet access.

```sh
npx pallas-ads install
```

The installer asks for Codex or Claude Code and a new project directory. For non-interactive use:

```sh
npx pallas-ads install --client codex --directory "$HOME/pallas-codex"
```

Use `--client claude` for Claude Code. The alternative GitHub source is `npx github:Jieyi-Deng/Pallas-ads install`; consult its release manifest before choosing a channel.

A supported Python 3.12 or 3.13 is reused. If none is available, the installer downloads a pinned, SHA-256-verified uv binary and prepares Python 3.13 alongside the runtime. Choose `--managed-python` to explicitly use a dedicated Python, or `--python /absolute/path/to/python3.13` to select an existing interpreter. These options are mutually exclusive.

Installation runs only when `install` is invoked; the package has no npm installation lifecycle hooks. It does not change shell profiles or global agent settings.

## Project files

Keep the project and the adjacent `-runtime` and optional `-runtime-tools` directories in place. Imported data and reports are stored in the project's `.pallas` directory. Each installation uses a new or empty dedicated project; it does not merge arbitrary existing projects.

## Activate and create a first report

1. Open the generated project folder in the selected agent. Use separate projects for Codex and Claude Code.
2. Confirm project trust and the requested local MCP permissions, then start a new task.
3. Ask the agent to verify eleven Pallas tools and the five portable Skills. A successful installation diagnostic does not prove the agent has loaded its tools. No separate MCP terminal needs to stay open.
4. Provide a CSV/XLSX export or its local path and ask:

> Preview this advertising export with Pallas. Show the account, dates, field mappings, currency, timezone and missing data. After I confirm the interpretation, import it and generate an HTML report. Explain the findings and link the report.

See [FILE_IMPORT.md](FILE_IMPORT.md) for export preparation and [PALLAS_COMMAND.md](PALLAS_COMMAND.md) for command invocation. File-only analysis skips account authorization. For a live connection, first check the platform's supported route and limitations in [AUTHORIZATION.md](AUTHORIZATION.md). Pallas-owned Meta login does not yet enable account discovery or reports.

After a successful analysis, use the [recurring-check workflow](README.md#5-set-up-recurring-checks) if your agent supports scheduling. Scheduled runs need access to this project, runtime and connection; file-based checks require a fresh export. Installation creates no schedule.

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

## Historical ZIP installations

Only the historical [runtime 0.2.0a1 release](https://github.com/Jieyi-Deng/Pallas-ads/releases/tag/v0.2.0a1) provides the installation ZIP and its SHA-256 checksum. It lacks later command, dashboard and browser-authorization updates. New installations should use the native plugin or the npm instructions above.

For recovery of that specific old installation, follow the instructions attached to its release and verify its checksum. Current GitHub Releases provide the reviewed npm tgz and `release.json`; GitHub's automatically generated source archives are not installation bundles. npm maintenance commands require an npm-managed project; they do not manage a manually installed archive.
