---
name: pallas-setup
description: Set up, activate, diagnose, update, migrate, or roll back the native Pallas advertising analysis plugin in Codex or Claude Code. Use before analysis when Pallas tools are unavailable or a project needs its first connection.
---

# Prepare Pallas

Resolve this Skill's installed plugin root from its file path (two parents above this Skill directory). The executable is [scripts/pallas.mjs](../../scripts/pallas.mjs). Run it with Node.js 22+ on macOS; use an absolute path and shell-quote paths. Never use a path guessed from another user's machine. The plugin is a local runtime, not a cloud service.

1. Determine the current host and the user's intended project. Use an explicit absolute project path. Do not bind the plugin cache, home directory, or a different customer's workspace. Different hosts should use separate projects.
2. Run `node PLUGIN_ROOT/scripts/pallas.mjs setup --client codex|claude --project PROJECT`, selecting the actual host. Setup prepares or reuses Python and the bundled runtime, writes a project binding, and leaves media authorization separate. For Codex it also registers exactly one project MCP entry with an absolute launcher and workspace path; Claude Code loads its bundled MCP declaration. It may need network access to install dependencies. Existing files and host trust prompts must be respected.
3. If it reports existing project Pallas configuration or Skills, explain that migration backs them up and disables the old project entry while retaining data and unrelated configuration. For the user's requested migration, rerun setup with `--migrate`. Custom server configuration may require manual review. Do not bypass the guard by deleting files. A rollback restores the last configuration change: `node PLUGIN_ROOT/scripts/pallas.mjs rollback --project PROJECT`. It refuses to overwrite files edited after that change.
4. Reload plugins or start a new host task in PROJECT. Verify that the ten Pallas tools and both pallas-workflow and pallas-analysis Skills load. The local server can be unavailable until setup is complete; running setup is the recovery path, not reinstalling the entire agent.
5. `doctor --project PROJECT` reports the binding/runtime. It does not prove host tool loading or media consent. A lock means a Pallas process is active or a prior process crashed: inspect its recorded PID and close the relevant session. Only remove a stale lock after confirming that its process is gone. Idle discovery connections may coexist. Data operations use the project lock and return a busy result if another operation is in progress. Finish the other operation before retrying.

## Authorization and first use

After activation, ask which media account the user wants to connect, unless already stated. Follow the installed pallas-workflow authorization rules. For Claude Code Meta setup, run `connect-meta --project PROJECT` only when the user requests Meta. This adds the official host-managed server and its read-tool guard, preserving existing configuration. Reload/trust the server and hook, then guide the user through `/mcp` -> `meta_official` -> Authenticate. Do not execute reads before the guard is loaded. The consent page's scopes may be broader than the allowed analysis tools; let the user review actual consent.

Meta remains a project server named meta_official, rather than a plugin-namespaced server: keep its existing host credentials and guard names stable. Do not copy tokens, read credential stores, rename the server to bypass access failures, or create a substitute Meta OAuth client. Codex Meta requires supported preregistered setup; Google live access requires operator application configuration. If unavailable, explain the exact missing step and direct setup questions to support@pallas-ads.com. TikTok uses the existing Pallas connection flow. Never ask the advertising user to paste developer secrets into chat.

Let the user select an accessible account and reporting period, then retrieve and analyze data using the common pallas-analysis template. File-only users can skip authorization: preview the supplied CSV/XLSX, confirm its interpretation, import, and report. Internal samples are not a substitute for the user's data.

## Update and recurring use

After updating the plugin through the host, close old Pallas sessions and run setup again for each bound project. It selects the runtime shipped with the installed plugin, retaining old runtime versions and project data for recovery. Do not run the old npm update command on a migrated native-plugin project: it would recreate project Skills. The legacy npm runtime can remain on disk for rollback or other projects.

Before disabling or uninstalling, run `deactivate --project PROJECT` for each Codex project to remove its verified generated MCP entry; stop the active sessions first. Then uninstall in the host. This prevents a dangling launcher after cache removal. Uninstalling the plugin does not delete the project's .pallas data or revoke media authorization. A migrated project can restore its last setup backup; disable the native plugin before using the restored project MCP. Preserve backups for user review.

Only arrange scheduled checks when requested and supported by the host. Confirm timezone, account, reporting period and notification preferences. The scheduled job must run in the same prepared project with the plugin and authorized connection available, retrieve fresh data and report failed/expired authorization. For files, an updated export is necessary. Pallas itself does not run a scheduler. Do not create a schedule during installation.
