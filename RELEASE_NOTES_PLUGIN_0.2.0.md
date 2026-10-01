# Pallas native plugin 0.2.0

Released: October 1, 2026. Engineering Alpha.

This update delivers the unified Pallas command, persistent advertising dashboards, competitor-report Skills, and internal-conversion analysis in the public Git distribution.

| Component | Version |
| --- | --- |
| Native plugin | 0.2.0 |
| Bundled Python runtime | 0.2.0a2 |
| npm / GitHub installer | 0.2.0-alpha.2 |
| Analysis renderer | 2.3.0 |
| Dashboard renderer | 2.0.0 |
| Competitor renderer | 1.0.0 |

npm follow-up, October 1, 2026: `pallas-ads@0.2.0-alpha.2` is also published to the npm registry and selected by `latest`. Both channels ship the same reviewed runtime. These component versions are independent.

## Commands and reports

- `analysis` generates a verified HTML report from a selected connection, retained evidence, or a file preview that the user confirms.
- `dashboard` creates or updates a selected persistent dashboard. Updates preserve history and report missing or stale sources. New dashboards require an explicit creation request; ambiguous accounts or dashboards require selection.
- `help` and `status` inspect capabilities and saved state without media reads or scheduling.
- Six native Skills and eleven MCP tools ship together, including `pallas` and `pallas_command`. Project installations contain the five portable Skills; native plugins add setup.
- Dashboards include a fixed offline template, filters, trends, campaign and creative views, local rules, and a validated import mapper. Missing dimensions and noncomparable conversions remain unavailable.
- Competitor research and internal-conversion evidence use their companion Skills. They are not additional `/pallas` subcommands in this release.

Claude Code plugin commands are `/pallas:pallas analysis` and `/pallas:pallas dashboard`. Setup can add a project alias for `/pallas analysis` and `/pallas dashboard` with `--install-command`, without replacing a user-owned command. In Codex, select the installed `pallas` Skill or use `$pallas analysis` / `$pallas dashboard` where supported. See the [command guide](PALLAS_COMMAND.md).

## Update

Close active Pallas tasks, update the plugin through your host, rerun its setup Skill in each prepared project, then start a new task. Follow [PLUGIN_INSTALL.md](PLUGIN_INSTALL.md#update). Source changes do not update an existing installation automatically.

For an existing npm project:

```sh
npx pallas-ads@latest update --directory /absolute/path/to/project
```

For a new project:

```sh
npx pallas-ads install --client codex --directory /absolute/path/to/new-project
```

Use `--client claude` for Claude Code. Preserve the project, runtime, and backups. Do not use the npm updater on a project already migrated to a native plugin.

## Validation and limits

- Local release validation: 65 relevant Python regressions, Ruff and ty, 13 public Node checks, distribution inventories, wheel/Skill byte identity, and private-file exclusion checks passed.
- A fresh wheel installed outside the source checkout passed command/MCP acceptance for both project bindings. Synthetic Google, Meta, and TikTok data produced six dashboard rows, remained at six on repeat import, and reached seven after a new-process update while preserving history and reporting stale sources.
- Local macOS native setup, doctor, eleven-tool MCP discovery, and upgrade checks passed. The native upgrade preserved 14 retained evidence/report files. The npm upgrade preserved 15 data/report/configuration files and backed up the old Skills.
- Claude Code 2.1.284 and Codex CLI 0.159.2 model sessions invoked the installed command Skill and MCP tool and returned verified analysis/dashboard HTML links from synthetic retained evidence. Codex dashboard updates preserved all seven rows and reported stale sources as partial. These are CLI model sessions, not desktop slash-menu or real-account acceptance.
- Product PRs now run one Linux distribution job. Root documentation-only changes skip Actions; macOS setup is local-first with an explicit manual hosted check available.

No new live-account reconciliation or returned external-user feedback is claimed. Google real-data validation and complete Meta reconciliation remain outstanding. Installation does not authorize media, configure schedules, or change advertising campaigns. Public-directory review is separate from installation through this Git source.

Both the root installer and native plugin ship the same core wheel, without operator Google configuration. SHA-256 for `pallas_ads-0.2.0a2-py3-none-any.whl`:

```text
42553a0f6c37be742195de7ab0790945e32c21fea8a47c9d9d371f7ce8a918e8
```
