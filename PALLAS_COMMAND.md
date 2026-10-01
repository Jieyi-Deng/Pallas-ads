# Pallas command entrypoint

The unified command is included in plugin 0.2.0 and runtime 0.2.0a2. Existing installations
must update the `pallas` Skill and `pallas_command` MCP tool together, then rerun project setup.
Updating source files alone does not update a user's installed plugin.

## In the agent

```text
/pallas analysis 分析这份广告导出，说明表现变化并生成报告
/pallas dashboard 更新这个项目的广告看板
/pallas status
```

These bare slash forms are supported by a **Claude project Skill**. The native Claude plugin
normally exposes `/pallas:pallas analysis` and `/pallas:pallas dashboard`. For a bare project
entrypoint, its setup helper accepts `--install-command` alongside the existing `--client` and
`--project` arguments. It installs a small forwarding Skill, journals it for rollback and
refuses to overwrite a user command, Skill or edited managed alias. Ordinary plugin setup
does not add that alias. Legacy project-local installs include the full `pallas` Skill.

In Codex, select the installed `pallas` Skill or use `$pallas analysis` / `$pallas dashboard`
where the host supports that syntax. The exact slash-menu presentation needs host-version
acceptance. Claude plugin namespacing follows [Claude Skills](https://code.claude.com/docs/en/skills).
Codex packages portable Skills rather than importing Claude command registration, as described
in [OpenAI's migration guide](https://developers.openai.com/plugins/guides/submit-claude-plugin).

The entrypoint reads only the relevant companion Skill. Explicit subcommands determine the
route; natural language supplies the question and scope. It never guesses between accounts
or dashboards. Help/status do not authorize media, initialize a workspace, fetch account data,
or create a schedule. `analyze` remains an alias of `analysis`; `update` means dashboard update.
Competitor research and scheduling are not added as commands in this iteration.

## Shared request and result

The MCP tool is `pallas_command`. Its schema is published by `pallas operations` and
`pallas schema export command_request`. CLI, MCP and the Skill use the same dispatcher.

```json
{
  "intent": "analysis",
  "workspace": "/absolute/project/.pallas",
  "analysis": {"dataset_id": "file_<64 lowercase hex characters>"},
  "expected_artifacts": ["html"]
}
```

IDs in examples are placeholders. `workspace`, when present, asserts the bound workspace;
it never redirects a running MCP server to another project. An analysis accepts exactly one
retained dataset, host capture, selected connection or canonical packet. Optional fields must
belong to that route. Source setup continues through the existing workflow and tools.

For a new export, replace `analysis` with:

```json
{"file": {"file_path": "/absolute/export.csv", "import_options": {"platform": "meta"}}}
```

The first call previews the existing file-import interpretation and returns
`pending_user_action`. After the user confirms it, repeat the same file/options with the
returned `review_hash` and `user_confirmed: true`. Changed bytes or options invalidate the hash.
The command then imports and generates HTML using the same analysis template and calculations.

For a dashboard, send `intent=dashboard` and optional `dashboard` options. `op=auto` (default)
updates exactly one existing match by ID or exact `source_scope`, otherwise returning choices.
New dashboards require explicit `op=create`, an ID, title and selected sources. Ingest accepts
the existing retained dataset/capture or fixed-mapper normalized data paths. Creation defaults
to 90 complete account-local days; updates re-read 7 days and keep earlier history. No new file
means no new file evidence. Top-level `status` is read-only; `dashboard.op=status` deliberately
regenerates derived artifacts from saved state without account reads.

Results retain the operation status, issues and missing inputs. `result.details` preserves
the backend's coverage, diagnostics, requested reads and limitations. Only verified HTML is
advertised in `result.artifacts.html`; `result.validation` records the integrity check. Analysis
checks the HTML, file hashes and installed template; dashboards additionally check saved-state
and template asset hashes and exact embedded view data. Partial/stale evidence remains partial
even when the HTML is valid. The host must deliver the returned clickable HTML link.

## CLI

Save the full command request as `request.json`, then use the configured Pallas executable:

```sh
pallas command --workspace /absolute/project/.pallas --input request.json
pallas analysis --workspace /absolute/project/.pallas --input analysis-request.json
pallas dashboard --workspace /absolute/project/.pallas --input dashboard-request.json
pallas status --workspace /absolute/project/.pallas
pallas help
```

The new convenience commands default only to the current directory's `.pallas`; they ignore
global `PALLAS_DATA_DIR`. Full JSON requests may also use the existing
`pallas call pallas_command --workspace ... --input ...` transport. For that legacy transport,
specify the workspace explicitly (its old environment fallback remains compatible).
Exit codes remain 0 complete, 1 needs input/failure, 2 partial result, 3 pending user action.
Existing report, source, and dashboard create/update/status commands remain available.

## Acceptance boundaries

Automated tests cover source routing, file confirmation, exact dashboard scope, persistence
across a new MCP process, repeat imports, failed-window preservation, artifact damage and
command alias collisions/rollback. Local package checks exercise a built wheel and plugin.
These checks do not establish that a real host model selects the Skill or returns the link.
Clean Codex/Claude model sessions and real-account/external-user acceptance remain separate.

Release 0.2.0 validation also exercised Claude Code 2.1.284 and Codex CLI 0.159.2 model sessions against synthetic retained evidence: command Skill routing, MCP invocation, and final clickable analysis/dashboard HTML links passed. These CLI sessions do not establish desktop slash-menu behavior, real-account reconciliation, or returned external-user acceptance.
