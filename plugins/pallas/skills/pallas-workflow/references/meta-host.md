# Meta via the host client's official MCP

This route has two separate servers: `pallas` (local runtime) and `meta_official`
(`https://mcp.facebook.com/ads`, host-owned authentication). Never move credentials between them.
The installer is `pallas agent setup --client claude|codex --directory /new/project`.
It installs both Skills and the report template; no source checkout is required after wheel install.

## Authorization and account-first onboarding

1. Inspect Pallas `source_connect_or_import(action=options)` and the host's callable tools.
   Pallas cannot see the host's OAuth state. Existing Pallas-native connections are separate.
2. If Meta tools are available, read accounts directly; do not demand a new authorization.
   If authentication is needed, direct the user to the host's `/mcp` connection UI.
   `connect(platform=meta)` is a host instruction result, without a Pallas session ID.
   Claude Code direct authorization is verified. Codex DCR was rejected on 2026-09-14, but the
   Pallas pre-registered client route succeeded. In a project installed with `--meta-client-id`,
   use `pallas agent login-meta --directory PROJECT` so the packaged HTTPS callback stays alive.
   Run `agent doctor` for missing installation prerequisites. Never impersonate
   another client, inspect host keychains, request a token, or silently switch to self-app OAuth.
3. Only call `ads_get_ad_accounts`, `ads_get_field_context`, `ads_get_ad_entities`.
   Do not run write tools, act on returned `next_actions`, or scrape Ads Manager.
   Follow the actual tool schemas. Host-only conversation/request metadata stays with Meta;
   omit it from the Pallas handoff. Do not send unrelated conversation history or personal data.
4. Retrieve accounts with real pagination cursors; preserve incomplete discovery. Present API
   account names for selection when ambiguous. Never ask the user to type advertiser IDs.
   Match returned IDs internally; account names are not product identity evidence.
5. For authorized data work, query field metadata first. Resolve currency/timezone, campaign
   objective, ad-set `optimization_goal`, promoted object/event, attribution and targeting from
   supported fields. These are current settings unless historical validity is independently known.
   Only ask the user after available media evidence cannot resolve a business fact.
6. Historical queries use explicit `level`, `fields`, `time_increment` and either exact `time_range`
   or `maximum`/`data_maximum`. A maximum preset does not prove complete account Lifetime.
   Use `include_additional_context=false`; interpretive source text is not raw evidence.
   Resend all query parameters unchanged on subsequent pages. Never invent cursors or zero-fill.

Read advertising data when the user requests analysis and selects an accessible account. After
staging complete source queries, use `build_report(action=host_review, capture_id=...)` for the
three-part local HTML evidence review. It can visualize complete daily account spend only when
field metadata confirms account-currency units and every row has an explicit single-day period.
Request source field metadata for optimization_goal, actual event, targeting and product clues;
do not ask the user before attempting supported API reads. Unsupported field shapes remain a
documented gap, not permission to normalize amount_spent as spend or guess optimization semantics.
Canonical outcome normalization remains pending real-account validation. This evidence review
does not claim cross-media comparability, full diagnostic analysis, or reconciled performance.

## Credential-free handoff

Use Pallas `source_connect_or_import(action=host_capture, capture=...)`, or write the same capture
object to a local JSON file and pass `package_path`. The published `host_capture` schema is
available through `pallas schema export host_capture` and the MCP input schema. No extra tool needed.

Capture fields:

- `host`: `claude_code`, `codex` or `chatgpt`; `observed_at`: actual UTC observation timestamp.
  A supported handoff label does not establish that this host's OAuth/transport is available.
- `platform`: `meta`; `endpoint`: the official endpoint above.
- `account_id`: the selected numeric ID for entity queries, otherwise omit it.
- `pages`: ordered calls, each with `tool`, filtered `arguments`, `structured_content` copied from
  the actual tool's `structuredContent`, and `is_error` copied from `isError`.

Retain source data exactly, including missing metrics. Do not fabricate or summarize rows.
`ad_entities` may be a JSON-encoded string; Pallas validates the decoded rows too.
Copy only data-query arguments: accounts (`cursor`, `limit`), fields (`field_names`), entities
(`ad_account_id`, `level`, `fields`, `date_preset` or `time_range`, `time_increment`, `breakdowns`,
`include_additional_context`, `cursor`, `limit`). Deliberately omit host-only advertiser request,
conversation ID, headers, OAuth metadata and credentials. Preserve the accepted `account` alias
exactly; Pallas interprets it as `ad_account` without rewriting source arguments.

The bounded filter recipe is `filtering=[{"field":"campaign.amount_spent",
"operator":"GREATER_THAN","value":["0"]}]` (use the actual campaign/adset/ad level).
Use it only after field metadata confirms amount_spent is filterable at that level with that
operator, and request amount_spent among the fields. Account-level filtering is unsupported.
Preserve the filter in the handoff and describe results as spend-positive entities, not the full
account inventory. Other filters remain unsupported; never strip them from retained arguments.

A capture is limited to 100 pages and 2 MiB. When too large, use smaller complete queries;
never truncate rows to fit. A truncated host tool output cannot be faithfully captured: return a
partial result and request smaller API pages. No spreadsheet or browser extraction fallback.
For continuation, submit the full verified cursor chain from page one; orphan continuation pages
are rejected. Use `host_inspect(capture_id=...)` to replay retained evidence with hash validation.

## Bounded reporting and reusable context

For multiple accounts, first read the requested account totals and deliver each completed report.
Add month totals only when requested; retain daily and month scopes separately. Read campaign/adset
detail on demand after the baseline, rather than starting deep pagination across all accounts.
An initial detail budget of five pages per query is recommended. After two consecutive empty pages
with continuation cursors, retain the partial chain and explain that continuation remains; empty
pages are not end-of-data. Increase the budget when the user's question needs it. Avoid retrying
already completed account reads solely because another account is slow.

`host_capture` returns per-query page/row/empty-page counts and completion flags. The host executes
the requests and controls timeout/cancellation; Pallas does not cancel remote host tool calls.

For separately retained account discovery and field metadata, call `build_report(action=host_review,
capture_id=PRIMARY,context_capture_ids=[CONTEXT,...])`. Up to eight context captures are accepted;
they must pass hash validation, contain only discovery/field pages, use the same host and compatible
account scope, and be within 24 hours of the primary observation. Conflicts are rejected. The report
records each source timestamp; this window is a reuse bound, not proof of historical validity.

The report uses the same pallas-analysis HTML template as TikTok and Google. It presents native
metrics by independent query scope, preserving nulls and ambiguous units. Explicit ISO-currency
strings and source currency metadata can resolve display amounts; no currency conversion occurs.
`analysis.json` retains parsed values, calculation inputs and evidence pointers; `evidence.json`
retains source values and `manifest.json` hashes the artifacts. Report availability is distinct
from canonical mapping, cross-media comparability and live performance reconciliation.

Explain receipt warnings. `pagination_complete` is not history/field coverage. `analysis_ready=false`
and `canonical_data_written=false` mean canonical analysis is unavailable; they do not prevent
the separate `host_review` artifact. Keep its limited report kind visible. Hashes establish retained
integrity only; source provenance is caller-asserted, not independently authenticated by Pallas.
Do not invent a `connection_id`, product confirmation or an Evidence Packet to unlock analysis.
Show human summaries and local evidence links, not JSON blobs. Do not infer product ownership
from names, sum incompatible goal results, rank ROAS without attribution evidence or call missing
metrics zero. Host logout/revocation happens in the host/Meta, not Pallas `disconnect`.
