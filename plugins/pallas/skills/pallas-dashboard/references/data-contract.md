# Dashboard data contract 1.0

Use `assets/data-template.json` as an editable example; validate against
`assets/data-template.schema.json` / `pallas_ads.dashboard_data.DashboardData`.
The input is one account's complete daily evidence window, distinct from generated `data.json`
which combines retained windows and sources for the browser. Both are versioned 1.0.

## Mapping raw evidence

Record `source` (platform, account_id as string, account_name, ISO currency, IANA timezone),
`evidence` (kind `uploaded_file` or `authorized_account`, retained reference, SHA-256 of the raw
file/capture, canonical-field → original-column/path mapping), `period.start/end` and
`complete: true`. This last flag is permitted only when all relevant rows/pages in the stated
window were obtained. Incomplete exports must be completed or split into provably complete
windows before ingestion. A date span inferred from the first/last row alone is not proof.

Map amounts into the account currency; e.g. documented Google costMicros ÷1,000,000, not a
currency conversion. Do not guess unknown units/timezones/ambiguous click or conversion fields.
Native mapping examples are field paths, not permission to call an unsupported API:
Google `campaign.id`, `segments.date`, `metrics.costMicros/impressions/clicks`;
Meta `campaign_id`, `date_start`, documented `spend` or `amount_spent`, `impressions`, `clicks`;
TikTok `dimensions.campaign_id/stat_time_day`, `metrics.spend/impressions/clicks`.
Upload mappings use the actual provided headers and declared units. Separate roll-up/total rows
from detail rows; do not count both or sum different reporting breakdowns into one fact.

`rows` has one record per campaign/date, with campaign_id, date (YYYY-MM-DD), spend,
impressions and clicks; optional conversions and conversion_value. Counts are nonnegative
integers; conversions can be fractional where the documented attribution system supplies them.
Money may be a decimal string. No percent/rate/delta fields are accepted. Null is unavailable;
zero requires evidence. Do not derive missing conversion count from CPA or clicks.

`campaigns` supplies unique id/name and optional status/ad_type/target_cpa. CPA targets must
be explicitly provided by the source or user. Never infer target CPA from observed CPA.

If conversions/value exist, supply `conversion_definition`: event, attribution_window,
counting_method, value_currency and evidence_reference. Normalize terms only where documented
semantics actually match. Two different definitions cannot be appended to one retained source.
Cross-source aggregation uses equality of the four semantic fields (reference may differ).
Revenue is the supplied attributed conversion value, not necessarily booked revenue or profit.

## Hierarchy and optional media

`details` may be null for campaign-only evidence. Otherwise provide ad_groups (id, campaign_id,
name, optional os), creatives (id, ad_group_id, name, format, optional preview_data/original_url)
and rows (creative_id, date, optional os, raw metrics, optional video counts).

The leaf key is creative_id/date/os. Every supplied campaign/day must have a complete leaf
partition; all five additive metrics must reconcile exactly. Nulls must reconcile as null,
not as zero. If a raw export is creative-level only, sum its complete leaves by campaign/day to
create parent rows; never allocate parent values down. If granular evidence is partial, omit
`details` and explain the limitation. Parent and leaf rows are separate aggregation paths.

Use os on rows for device-segmented evidence. Only set ad_group.os if it is genuinely fixed for
that group. Missing OS stays unknown, not Others. Do not submit an unsegmented creative/day
alongside its OS partitions. Format is Image, Video, Carousel or Other. Video views and
completions require Video; completions cannot exceed views. Document the platform's view-count
threshold in evidence.field_mapping. View rate = views/impressions, completion = completions/views;
these names do not imply video definitions are identical across platforms.

Offline image previews accept embedded PNG/JPEG/WebP data URLs; otherwise leave them null.
An original HTTPS URL opens only when the user selects it. A video entry without media is a
placeholder, not a playable video. Do not fetch/upload assets merely to fill a preview.

## Ingestion, retention and update

Validate with `python -m pallas_ads.dashboard_data /absolute/account-window.json`.
Use source route `file_import`, then `ingest` with source_key and data_path. The source route
means the runtime consumes normalized local evidence, even if the agent originally obtained
that evidence through an authorized host tool. It does not become an automatic live adapter.

The runtime archives the validated input under `evidence/template_<hash>.json`, then merges its
complete window. Duplicate imports do not add counts. Restated optional conversion fields also
increment row revision. Updated detail rows replace the window while historical rows remain.
Incomplete or invalid input cannot advance coverage. Existing IDs must keep their hierarchy,
format and fixed OS; changed identity needs distinct source IDs. Previously retained detail
outside the replaced window must remain in metadata.

Built-in live/capture and legacy dataset routes still work for campaign/day traffic. Their
readers normalize into the same retained store; `data.json` projects sanitized metadata, all
retained campaign rows, validated detail, coverage and conversion definitions. The renderer
embeds this file's exact object and performs filter-dependent calculations in the bundled JS.
Never edit generated data.json directly: it will be replaced by the next update.

Daily scheduling, with user consent, normally reads the last seven complete days. A file-only
source cannot fetch missing data: wait for a new complete export, then normalize/import that
window. An authorized host may run the same mapping under an approved schedule if its tools
remain available. Do not create a second unauthorized account route to make scheduling work.

## Fixed file mapping entrypoint

`../scripts/dashboard.py normalize` calls `pallas_ads.dashboard_import`, not generated agent code.
`../assets/file-mapping.json` is an example, not evidence; its companion JSON Schema matches
FileMapping. The mapping is persisted with each normalized output, including the actual raw
SHA-256. Raw bytes are copied locally, not fetched or uploaded. Missing column fields are
rejected. Empty metric cells map to null; the literal 0 remains zero.

Supported: UTF-8 CSV with a single header; XLSX with an explicitly selected sheet and a single
header; flat JSON arrays of row objects. Use ISO dates or native midnight XLSX dates, plain
numbers without currency symbols or thousands separators, exact text IDs (especially long
Excel IDs), and explicit spend/value units `currency` or `micros`. Formulas in metric cells,
ambiguous date formats, duplicate keys, mismatched account/currency, conflicting metadata,
non-integer counts and incomplete leaf partitions fail. Every row must be valid; subtotal,
summary, blank or mixed-grain rows are not silently removed. Files are bounded to 20 MiB and
200,000 rows. A header-only complete CSV window is allowed for authoritative empty windows;
confirm that the export truly represents the entire stated window before importing.

`campaign_day` preserves campaign/day rows and has no creative detail. `creative_day` retains
creative/day[/OS] rows and sums complete leaves to campaign/day, propagating nulls. It does
not distribute parent totals. The helper supports names, status/objective, conversion metrics
and video counts. Other shapes/fields (e.g. nested host payloads, separate metadata joins,
preview asset embedding, CPA targets) still need existing native adapters or a reviewed
reusable adapter; do not claim the generic flat mapper supports them. Names may contain up
to 2,000 characters; IDs stay bounded to 200 characters.

A reused mapping makes mechanics reproducible, but does not prove the export is complete or
that a column called Conversions means purchases. Confirm semantics from source documentation
and sample/aggregate reconciliation. Mapping is a configuration decision, not an LLM arithmetic
step. Semantic mistakes require a corrected mapping and explicit reimport window.
