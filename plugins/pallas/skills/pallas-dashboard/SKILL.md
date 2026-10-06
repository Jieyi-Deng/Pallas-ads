---
name: pallas-dashboard
description: Create and update a local Google, Meta and TikTok advertising dashboard from authorized accounts or user-uploaded history, using a validated daily data template and deterministic calculations. Use for cross-platform dashboards and user-approved daily refreshes.
---

# Pallas advertising dashboard

Use the approved `assets/dashboard.html`, `dashboard.css` and `dashboard.js`. Keep its layout;
fill it through the data contract, not by editing HTML totals or asking a model to invent
insights. The flow is **raw evidence → normalized daily template → code calculations → dashboard**.
The agent selects permitted sources, maps documented fields and explains limitations; code
validates, deduplicates, calculates metrics, applies insight rules and renders the page.

## 1. Before first generation

Set `report_language` from the user's request: Chinese -> `zh-CN`; all other languages ->
`en`. An explicit requested output language takes precedence with the same mapping. Pass it
at the top level of `build_report`/`pallas_command`, or in `dashboard.report_language` when
using the direct dashboard helper. Never infer it from account names, input files or the OS.
The saved language covers headings, filters, charts, insights, dialogs and accessibility text.
Explicit user-requested updates pass the current request's language. Unattended/scheduled
updates omit the field and retain the saved language; new dashboards default to English.
Keep user-supplied names/titles and evidence values unchanged. Generate new descriptive titles
in the selected report language. Do not translate or replace the finished HTML manually.

Choose the route from the user's request and existing authorization; ask only for missing
account/file selection or ambiguous metric definitions. Do not ask again for an already
confirmed title or source. A file-only request needs no advertising-account authorization.

- **Authorized accounts (default when the user requests account data):** use pallas-workflow
  to discover/select existing authorized accounts. Google/TikTok use `live_api` and a workspace
  `connection_id`; Meta uses `host_capture` through the signed-in official MCP, or an already
  operator-configured live API. Never request credentials in chat.
- **Uploaded history:** inspect the CSV/XLSX/JSON's date grain, IDs, units, currency, timezone,
  conversion definition and available hierarchy. Map the original fields to
  [the data contract](references/data-contract.md); retain the original file and its hash.
  Do not substitute sample data for missing uploaded fields.
- Keep one source per platform/account, up to 12. Do not mix synthetic and real evidence.

First account generation fetches **the last 90 complete days**, ending yesterday in each
account's timezone. `history_start` may explicitly override this. Newest-first reads are
bounded to 31 days each, with `max_windows` default 12 per source; finish/resume all windows
and pagination before calling the requested history complete. Persist the first history floor;
subsequent updates retain older data. Uploaded history uses its actual confirmed coverage,
which may be shorter or longer than 90 days. Never stretch monthly totals into daily data,
fill missing dates with zero, or claim an incomplete export is a complete window.

Retrieve documented campaign/day spend, impressions and clicks, account currency/timezone,
IDs/names/status/objective; request conversion, ad-group/ad-set, creative, OS and video fields
only when the selected account tools actually support them. Current built-in live/capture
adapters retain campaign/day traffic; richer evidence can enter through the normalized file
contract. Do not claim automatic live creative/conversion fetching has been implemented.
Unavailable dimensions remain empty, without allocating campaign totals to invented children.

## 2. Build the normalized data

For flat CSV/XLSX/JSON exports, use the bundled [dashboard helper](scripts/dashboard.py):

```sh
python /absolute/skill/scripts/dashboard.py normalize --raw /absolute/export.csv --mapping /absolute/mapping.json --output-dir /absolute/WS/dashboards/dash_main/inputs
```

Run with the installed Pallas runtime's Python. The script delegates to versioned runtime code;
no per-run processing script is needed. Start with `assets/file-mapping.json` and its schema.
The agent maps literal column names, declares account/window/grain and documented units; the
code parses values, converts micros, derives campaign totals from complete creative leaves,
validates hierarchy/duplicates and writes content-addressed raw, mapping and normalized files.
Inspect returned totals against source totals, then ingest the returned data_path. Reuse the
saved mapping on subsequent exports of the same shape; update only the explicit window and
review any field/unit/meaning changes. No expressions, arbitrary code, silent row skipping,
ratio averaging, currency guessing or parent-to-child allocation are supported.
See [data-contract.md](references/data-contract.md) for supported formats and rejection rules.
Unsupported nested/ambiguous exports need a reviewed reusable adapter; explain the missing
support instead of writing an untested one-off transformation and claiming equivalence.


Read [data-contract.md](references/data-contract.md) when mapping a file or a host export.
Use `assets/data-template.json` as the shape and `assets/data-template.schema.json` as the
machine contract. Replace every example value with evidence; it is not a real-account fixture.
One input file represents one account and a complete explicit date window. It contains:

- source metadata and raw evidence reference/hash/field mapping;
- campaign metadata and daily additive metrics, with optional documented conversion definition;
- optional complete creative/day[/OS] rows plus campaign → group → creative relationships;
- explicit campaign target CPA and preview assets only when provided.

Persist normalized inputs locally and validate with:

```sh
python -m pallas_ads.dashboard_data /absolute/path/account-window.json
```

Use the Pallas runtime's Python environment. Do not calculate/store CTR, CPC, CVR, CPA, ROAS,
percentage deltas or prose insights in the input. Missing is `null`; zero is an observed zero.
The validator rejects duplicate keys, broken relationships, invalid values, out-of-window rows,
undocumented conversions and unreconciled parent/child totals. It does not independently prove
that an agent's mapping matches the original: inspect samples and reconcile aggregate totals
against the raw source before importing. Never mark a mapping verified solely because it parses.

## 3. Generate using the fixed template

All runtime work uses `build_report(action=dashboard, dashboard={...})`:

```json
{"action":"dashboard","dashboard":{"op":"create","dashboard_id":"dash_main","title":"Advertising Performance","sources":[{"platform":"google","route":"live_api","account_id":"123","connection_id":"connection_example"}]}}
```

For normalized uploaded or authorized-account export evidence, use `file_import` and ingest the
validated window (automatic fetching is not enabled for this route):

```json
{"action":"dashboard","dashboard":{"op":"create","dashboard_id":"dash_main","title":"Advertising Performance","sources":[{"platform":"meta","route":"file_import","account_id":"123"}],"ingest":[{"source_key":"meta:123","data_path":"/absolute/path/account-window.json"}]}}
```

Existing confirmed CSV/XLSX `dataset_id` imports and Meta `capture_id` imports remain supported.
A `dataset_id` import adds observed rows only: its first/last dates do not establish complete
coverage, dates without rows stay unknown (not zero), and the result is `partial_result` with
`coverage_not_established`; comparisons and Key Insights are withheld for those dates. Only a
`data_path` window with `complete: true` (or a complete API/capture read) establishes coverage.
`status.json` `sources.<key>.coverage` separates `complete_windows`, `observed_only` and
`unknown_within_observed_span`; report these instead of a data-through date for observed-only
sources. A `coverage_repaired` issue means older state claimed file coverage that no retained
complete window supports; rows were kept and those dates are now observed-only.
For Meta `host_capture`, run exactly the runtime's `requested_reads` plus account/field context,
stage via `source_connect_or_import(action=host_capture)`, then update with the capture ID.
Day boundaries use the account `timezone_name` from that retained evidence. A read with
`purpose: account_timezone` is a prerequisite until it is captured; never supply the computer's
timezone, infer one from currency, or assume UTC. Until then (`source_timezone_required` or
`source_timezone_invalid`), reads end at the last date that has ended in every timezone. Days
not yet ended in the account timezone at `observed_at` are reported as `excluded_unfinished`
and never become rows or coverage; re-read them after they end. Older capture state is checked
once against retained captures; a `coverage_repaired` issue there means days read before they
ended, or with no retained capture, are now observed-only until a complete capture re-reads them.

`dashboards/<id>/data.json` is the saved view data and the **exact data embedded in the HTML**.
All routes converge on this file through the same code. `state.json` is the deduplicated update
store, not an agent editing surface. Keep `evidence/`, `rows.csv`, `status.json`, `manifest.json`
for local provenance and integrity. Normalized inputs are archived by content hash on import.

### Data composition and calculations by section

Calculations are implemented in `pallas_ads.dashboard_data` and the bundled `dashboard.js`.
Global date/account/media/currency filters apply before aggregation; sum currencies separately.
Use summed numerators/denominators, never averages of row ratios.

| Section | Evidence and code computation |
| --- | --- |
| Header | Selected complete dates, account/currency and media; latest successful source update formatted as `Last updated` / `MM/DD/YYYY`. Failed/stale source details go in chat. |
| Account Overview | Campaign/day sums for spend, impressions, clicks, conversions and value. CTR = clicks/impressions ×100; CPC = spend/clicks; CPM = spend/impressions ×1000; CVR = conversions/clicks ×100; CPA = spend/conversions; ROAS = conversion value/spend. Platform/ad-type totals use campaign rows; OS rows use reconciled creative evidence. |
| Comparisons | Previous adjacent interval has the same number of days; previous-year shifts calendar dates, clamping leap day. Delta = (current/prior −1) ×100 after recomputing each metric. Missing/incomplete coverage or zero baseline yields `—`, not infinity or inferred growth. Costs down are favorable; spend direction is neutral. |
| Performance Change | Same platform and Total aggregates and comparison formula for Spend/CTR/CVR/CPA/CPM; Total bold. No independent calculation path. |
| Daily Trends | Fixed last 90 complete dates, Spend and Conversions panels, default last 28 days highlighted. Daily sums per media; shared hover includes media and Total Spend/Conv/CPA/CTR. Legend totals cover the 90-day canvas. Focus fills to baseline, not cumulative stacking; unread dates are gaps. |
| Campaign Performance | Group campaign/day rows; expand reconciled groups/ad sets. Search and independent media chips; filters: all, active, CPA above explicit target, a group with observed zero conversions, spend up >20%, CTR below the selected platform aggregate. Include ROAS. Group selection narrows creatives below. |
| Creative Performance / preview / compare | Sum selected creative/day[/OS] rows. Reuse the same traffic/conversion formulas. Video view rate = views/impressions ×100; completion = completions/views ×100. Non-video or unavailable video evidence is `—`. Context and assets come from metadata; absent media gets an honest placeholder. Compare up to four creatives. |
| Key Insights | Deterministic rule candidates, thresholds and priorities below; preserve numeric delta/absolute evidence, regular text weight. No model prose in the saved dashboard. |
| Message Center | User-saved spend-above, CTR-below or CPC-above rules on selected campaign aggregates, configured currency and minimum impressions. High when above 2× threshold (CTR below half); otherwise Medium. Summary shows up to three, prioritizing severity. Resolve/reopen state and rules live in browser storage; no background monitoring. Real reports start without demo rules. |

Missing additive inputs propagate to a missing aggregate for that metric; zero denominators
produce `—`. Cross-source conversion totals/share/CPA/CVR/ROAS require matching documented
**event, attribution window, counting method and value currency**. A single platform's native
conversion definition is not automatically comparable to another's; agent normalization must
not invent equivalence. Spend/impressions/clicks remain available when conversions cannot combine.

### Table layout contract

- Account Overview omits the Currency column; the global currency selector still scopes amounts.
- Campaign Performance has a separate leading selection column, then Platform and Campaign / Ad
  group. Freeze all three while horizontally scrolling. Parent and child checkboxes share the same
  column; child platform cells are blank. Group names use a tree connector and a consistent inset
  below campaign names, with creative count beneath; Status identifies Ad Group / Ad Set.
- Creative Performance begins with selection, then the standalone Preview thumbnail column,
  Creative ID and Platform. Freeze these four columns together. Display only the creative ID
  in the identifier cell; show the full creative name in Preview details. The thumbnail opens
  that dialog. Do not add a trailing Details/Preview action column.
- Frozen header/body offsets use shared fixed column widths. Preserve opaque backgrounds, child
  shading, hover states and header stacking so scrolling values cannot bleed through. Long campaign/group names
  use a one-line ellipsis with the full name in a title tooltip; keyboard-focusable group/context
  labels reveal the complete text on focus. Campaign disclosure retains its full accessible name.
  Preview details wrap complete names; IDs remain complete and wrap if necessary. Narrow screens use compact frozen widths and internal scrolling.

### Key Insights rule contract (version 1)

These are descriptive screening rules, not statistical significance or causal conclusions.
Apply the selected filters and complete comparison coverage first. Emit at most one observation
per rule, in this order; skip ineligible rules rather than filling five cards with weak claims.

1. **Spend change:** current and prior each ≥1,000 impressions, prior spend >0, absolute spend
   delta ≥20%. Choose largest absolute percentage change. Without a qualifying change, a neutral
   largest-spend observation may show the current amount without claiming abnormality.
2. **Declining conversion efficiency:** current/prior each ≥20 conversions and ≥100 clicks,
   CPA increase ≥20% and CVR decline ≥10%. Choose largest CPA increase; show CPA/CVR/spend deltas.
3. **Conversion contribution:** with comparable definitions and positive total conversions,
   choose the platform with most conversions; show conversion share, spend share and CPA.
   This is descriptive, not an alert.
4. **High creative CTR:** ≥5,000 impressions and ≥100 clicks; CTR ≥1.5× its same-period ad-group
   average. Choose highest ratio, show both CTRs and sample count.
5. **High spend / weak conversion:** top spend quartile of creatives in scope, ≥20 conversions
   and ≥100 clicks, CPA ≥1.3× same-platform aggregate. Choose highest ratio; show amount, CPA
   ratio and CVRs. A 2% difference does not qualify.

Thresholds live in `INSIGHT_RULES` in the bundled JavaScript; change code and tests together,
not ad hoc agent judgments. Missing baseline or incomparable conversion definitions suppresses
conversion-based rules. Discuss additional contextual hypotheses separately in chat.

## 4. Update and scheduling

Before create/update, read [the persistence workflow](references/persistence.md). Resolve the
user-selected project binding and reuse its absolute workspace root. Discover retained dashboards:

```sh
python /absolute/skill/scripts/dashboard.py list --workspace /absolute/WS
```

Reuse a unique matching dashboard by title and source accounts. If multiple match, ask which
one; do not silently create a new ID, switch workspaces, or load another client's state. The
same workspace + dashboard ID survives a new conversation/process. A copied HTML is a view,
not an incremental update store.


On demand: `pallas dashboard update --dashboard dash_main --workspace WS`.
Default refresh re-reads **the latest seven complete days**, upserts by source/campaign/date,
recomputes data.json and renders the same template. Missed runs catch up from the watermark;
unfinished initial backfill may also resume. Keep older rows. Successful complete windows
replace that window including authoritative removals; failed/incomplete windows keep prior
rows/coverage. A later correction outside seven days needs an explicitly wider refresh/import.
For normalized files, supply a new `ingest` `data_path` for that complete window; never add
new totals onto existing same-key values. An unchanged file reimport is idempotent.

**Daily scheduling is opt-in.** Offering a refresh or creating a dashboard does not authorize a
timer. Obtain user agreement to enable it and establish time, timezone, workspace/dashboard and
source route before using the host scheduler. This skill update itself does not enable one.
Read [scheduling.md](references/scheduling.md) only when setting up/troubleshooting a schedule.
Uploaded-only sources require a newly supplied file; do not schedule reprocessing a static file
and describe it as fresh account data. Browser `Reload report` only reloads saved HTML.

## Delivery consistency

The runtime renders through the bundled HTML/CSS/JS; agents must not rewrite these assets or
create a substitute dashboard for individual runs. Use build_report and open its returned HTML.
After generation run the helper's read-only integrity check:

```sh
python /absolute/skill/scripts/dashboard.py verify --workspace /absolute/WS --dashboard dash_main
```

It checks manifest asset hashes against the installed runtime, state/artifact generation hashes,
and exact embedded data equality. Read returned data_status separately: integrity is not account
completeness or freshness. Check manifest.json's renderer and template_assets_sha256 (HTML/CSS/JS). If this manifest field is absent, the installed runtime predates this
layout verification contract; explain the version mismatch and use the user's approved update
path before claiming this template was used. Do not fabricate the manifest or patch an older
output to pretend it came from the current renderer.

Repository edits do not update an already installed plugin/runtime. Distribution must bundle
this skill and the matching runtime assets, then pass installed-package end-to-end acceptance.
A fixed renderer provides repeatable structure/calculation for valid inputs; actual section
population still depends on complete supported source data. Missing groups/creatives/conversion
metrics must keep their empty states and be explained in chat. Neither skill prose alone nor
synthetic tests guarantee every future agent run or real-account payload.

## 5. Handoff

Open the generated HTML. In chat, state routes, actual coverage, data-through date, last success,
errors/pending captures, missing dimensions and conversion comparability limits. Keep operational
status, unavailable-metric lists and update logs out of dashboard sections and Message Center.
Retain compact synthetic badge, date/currency, update date and contextual empty states.
Synthetic validation is not real-account or installed-plugin acceptance.
