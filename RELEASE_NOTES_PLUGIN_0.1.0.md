# Pallas native plugin 0.1.0

Install Pallas from one public Git source in Codex or Claude Code, then use its setup Skill to prepare a project, authorize an available media connection, and analyze account data or uploaded exports.

- Adds both plugin catalogs and host manifests, a setup Skill, runtime preparation, diagnostics, and reversible project migration.
- Reuses the Pallas workflow and analysis Skills and the existing runtime 0.2.0a1. No new npm package is required.
- Stores project data outside plugin caches; updates retain prior runtimes and reports.
- Codex setup binds an explicit project MCP entry. Run setup after plugin updates and deactivate before uninstalling. Claude Code loads the bundled MCP entry.
- Preserves existing Meta host identity and adds the Claude Meta read guard when requested. Installation does not grant media access or change platform admission requirements.

Validation: both manifest formats; Codex model/tool invocation; Claude connected MCP with ten tools and three Skills; supported-Python and managed-Python setup; migration/rollback guards; three-media file reports across twelve process restarts; package integrity and runtime checks. Claude model-dialogue acceptance was deferred at initial release. The 2026-09-22 follow-up completed the file workflow and identified an interpretation issue addressed in [plugin 0.1.1](RELEASE_NOTES_PLUGIN_0.1.1.md). Fresh real-account and unattended scheduled-run acceptance remain separate.

See [PLUGIN_INSTALL.md](PLUGIN_INSTALL.md) for installation, activation, authorization, updates and recovery. This release is distributed through the Pallas Git source; it is not an official-directory listing or a ChatGPT remote connector.
