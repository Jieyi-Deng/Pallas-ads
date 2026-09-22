# Install and activate Pallas

Pallas runs inside a dedicated project in Codex or Claude Code. You can follow these steps yourself or give this page to your agent.

## Requirements

- macOS on Apple Silicon or Intel.
- Node.js 22 or later, including npm/npx.
- Codex or Claude Code, and internet access for installation.
- A new or empty project folder.

The installer reuses supported Python or prepares it automatically. You do not need an npm account or a separate OpenAI runtime API key for local analysis.

## Install

Run the interactive installer:

```sh
npx pallas-ads install
```

Choose your agent and project folder. For an agent running without an interactive terminal, specify both explicitly.

Codex:

```sh
npx pallas-ads install --client codex --directory "$HOME/pallas-codex"
```

Claude Code:

```sh
npx pallas-ads install --client claude --directory "$HOME/pallas-claude"
```

Use separate projects for the two clients. The installer creates a project, an adjacent runtime, MCP settings, and the `pallas-workflow` and `pallas-analysis` Skills. Keep the project and its adjacent runtime directories in place.

## Activate

1. Open the generated project folder in the selected agent.
2. Confirm project trust and the requested local MCP permissions.
3. Start a new task to load the project configuration and Skills.
4. Ask: “Check that Pallas tools and both Pallas Skills are available, then help me analyze my advertising data.”

The agent should verify actual tool availability. An installation diagnostic alone does not establish that the client has loaded the MCP server. No separate MCP terminal needs to remain open.

If tools are missing, confirm that the correct project is open, reload the task, and run:

```sh
npx pallas-ads doctor --directory "$HOME/pallas-codex"
```

Substitute your actual project path. For help, contact [support@pallas-ads.com](mailto:support@pallas-ads.com).

## Use Pallas

Provide the path to your advertising CSV or XLSX export and ask:

> Analyze this file with Pallas. Preview its account, date range, fields, currency, timezone, and missing values. After I confirm the interpretation, import it and create a report with performance, changes, and recommended next steps.

See [FILE_IMPORT.md](FILE_IMPORT.md) for export preparation. To connect a live account, follow [AUTHORIZATION.md](AUTHORIZATION.md); installing or activating Pallas does not grant media access.

## Maintain an installation

See [NPM_INSTALLER.md](NPM_INSTALLER.md) for updates and recovery. Do not overwrite a populated project to reinstall. Back up the project before upgrading, and retain its `.pallas` data and any Skills backups.

## Install from a release archive

For an archive-based installation, choose the Pallas installation ZIP and its SHA-256 checksum from [Releases](https://github.com/Jieyi-Deng/Pallas-ads/releases). Use the attached installation bundle, not GitHub's automatically generated source archive. Verify the checksum before extracting, and follow that bundle's installer instructions using Python 3.12 or 3.13 on macOS. Exact artifact names and versions are recorded in the release notes.

For a standard local setup, run from the extracted bundle:

```sh
python3.13 install_macos.py --directory "$HOME/pallas-codex" --client codex
```

Then follow the activation steps above. The npm `doctor` and `update` commands manage npm-created installations; for an archive installation use the installed runtime's CLI and its release instructions.
