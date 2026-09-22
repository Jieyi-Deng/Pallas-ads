# Install the Pallas plugin

Pallas brings its workflow and analysis Skills, project setup, and local advertising-analysis runtime to Codex and Claude Code. Use macOS, Node.js 22 or newer, and a current version of your agent with plugin support. Python is prepared automatically when needed.

This guide installs from Pallas's public Git repository. It does not require access to the private development repository, an OpenAI API key, or an npm publisher account. Adding this source does not mean Pallas is listed in your agent's default public directory.

## 1. Install

### Codex

Run in your terminal:

```sh
codex plugin marketplace add Jieyi-Deng/Pallas-ads
codex plugin add pallas@pallas-ads
```

Start a new task in the project where you want to keep advertising data. You can also ask your agent:

> Install the Pallas plugin from https://github.com/Jieyi-Deng/Pallas-ads using PLUGIN_INSTALL.md, then use its setup Skill to prepare this project for Codex.

### Claude Code

In Claude Code, run:

```text
/plugin marketplace add Jieyi-Deng/Pallas-ads
/plugin install pallas@pallas-ads
```

Or use the terminal:

```sh
claude plugin marketplace add Jieyi-Deng/Pallas-ads
claude plugin install pallas@pallas-ads
```

Then use `/pallas:pallas-setup` in your intended project.

Choose either the native plugin or the [npm installation](INSTALL.md) for a project. Existing npm users should use the migration instructions below.

## 2. Prepare and activate your project

Tell your agent:

> Use the Pallas setup Skill to prepare this project. Verify the installed tools and Skills. Then help me authorize the media account I want to analyze.

The agent resolves the installed plugin path and runs its setup helper for your selected project. Setup may download Python and runtime dependencies. It stores analysis data in the project's `.pallas` directory, separately from the plugin cache. Confirm host project trust and requested permissions, then start a new task or reload the plugin.

Codex setup creates one project MCP entry with an explicit launcher and workspace path; the native plugin provides its Skills and setup helper. Claude Code uses the plugin's bundled MCP entry and the current project binding. Use separate project folders for separate clients or customers. Open the prepared project root when starting your agent.

The expected inventory is **three Skills** (`pallas-setup`, `pallas-workflow`, `pallas-analysis`) and **ten Pallas tools**. The helper's `doctor` command checks the binding and runtime; your agent must also verify that the tools load. A connected local Pallas server does not imply that a media account is authorized.

## 3. Authorize

> Connect my Meta / Google Ads / TikTok Ads account to Pallas. Check the required connection setup, guide me through browser authorization, list accessible accounts, and let me select one before reading performance data.

Complete the platform's login and consent screens. Your agent uses the [authorization guide](AUTHORIZATION.md) and preserves existing connections.

For Meta in Claude Code, the setup Skill can add the project `meta_official` server and its read-tool guard. Reload and trust the project MCP and hook, then authenticate through `/mcp`. Meta remains a host-managed connection; the plugin does not copy tokens or change client identities. Existing Codex Meta connections are retained. New Codex Meta access needs the supported preregistered configuration; Google live access needs operator application setup. Contact [support@pallas-ads.com](mailto:support@pallas-ads.com) when that setup is missing. TikTok follows the Pallas connection flow.

For uploaded CSV/XLSX analysis, skip media authorization.

## 4. Analyze

For an authorized account:

> Use Pallas to analyze the last seven complete days for the account I selected. Confirm the reporting scope and data coverage, explain performance changes, and generate an HTML report with evidence and recommended next steps.

For an uploaded export:

> Preview this advertising export in Pallas. Show the account, dates, field mapping, currency, timezone, and missing data. After I confirm, import it and generate an HTML report.

Both paths use the same `pallas-analysis` report template. See [FILE_IMPORT.md](FILE_IMPORT.md) for file preparation. Imported evidence and reports remain in your local project; do not put them in the plugin repository.

## 5. Repeat or schedule

After a successful analysis, ask your host agent to schedule checks if it supports scheduling. Confirm timezone, account, date window and notification preferences. Each run must open the same prepared project, load Pallas, retrieve fresh data, and report expired authorization or retrieval failures. File-based checks require updated exports. Pallas itself does not run a scheduler, and installation creates no scheduled jobs.

## Existing npm projects

Close active Pallas tasks first. Ask the setup Skill to migrate the selected project. The helper initially stops when it detects an old project entry or copied Skills; `setup --migrate` backs up the configuration and Skills, then switches the entry while keeping `.pallas` data and unrelated MCP settings.

Customized MCP configurations need review before migration. OAuth credentials are not copied. Backups are under `.pallas/plugin-backups`; rollback restores the last configuration change and refuses to overwrite later edits. The old npm runtime can remain for recovery. Do not run the npm updater on a migrated project, because it recreates the old project Skills.

## Update

Codex:

```sh
codex plugin marketplace upgrade pallas-ads
codex plugin add pallas@pallas-ads
```

Claude Code:

```sh
claude plugin marketplace update pallas-ads
claude plugin update pallas@pallas-ads
```

Close existing Pallas tasks, update through your host, and ask the setup Skill to prepare each project again before starting a new task. This refreshes the project entry and selects the runtime shipped with the plugin. Previous runtimes and analysis data remain available for recovery. Use the same installation scope when updating a project-scoped Claude plugin.

## Diagnose, deactivate, or recover

Ask the setup Skill to run the appropriate helper operation. The agent resolves `PLUGIN_ROOT` from the installed Skill; it is a placeholder below, not a path to copy literally:

```sh
node PLUGIN_ROOT/scripts/pallas.mjs doctor --project /path/to/project
node PLUGIN_ROOT/scripts/pallas.mjs rollback --project /path/to/project
node PLUGIN_ROOT/scripts/pallas.mjs deactivate --project /path/to/project
```

Before disabling or uninstalling in Codex, **deactivate each prepared project** to remove its generated MCP entry. Then disable/uninstall in the host and reload. Claude Code removes the bundled Pallas MCP entry when its plugin is disabled. Uninstalling Pallas does not delete imported data, reports or managed runtimes, and does not revoke media consent. Disconnect media separately in the host/platform when desired.

A busy result means another operation holds the project lock. Let it finish. If the previous process crashed, inspect `.pallas/plugin.lock/owner.json` and confirm that its PID is no longer running before removing that lock directory. Startup and tool discovery can coexist across sessions; data operations are serialized. Run scheduled jobs in the prepared project without concurrent setup or migration.

For other needs, contact [support@pallas-ads.com](mailto:support@pallas-ads.com). Share errors and client versions, never passwords, access tokens, API keys or advertising data you did not intend to disclose.
