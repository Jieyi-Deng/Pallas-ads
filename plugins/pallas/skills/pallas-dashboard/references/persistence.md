# Workspace, retained state and incremental updates

Native plugin setup binds each selected project to `<project>/.pallas`. CLI `--workspace`
overrides the root; otherwise PALLAS_DATA_DIR, then the current directory's `.pallas` is used.
Always resolve and pass the same absolute workspace explicitly for later runs or schedules.
Never infer history from the conversation or use the plugin installation/cache directory.

```text
<workspace>/dashboards/<dashboard_id>/
  state.json         # format_version 1.0: authoritative incremental store
  inputs/            # helper-preserved raw exports, mapping configs, normalized windows
  evidence/          # runtime-archived normalized windows by SHA-256
  data.json          # regenerated presentation projection, exact object embedded in HTML
  dashboard.html     # fixed offline template + embedded view data
  rows.csv           # campaign traffic audit export, not the full state backup
  status.json        # coverage, pending reads, freshness, missing metrics, source failures
  manifest.json      # renderer/template/state/output hashes
  .lock              # advisory per-dashboard process lock
```

`state.json` stores source/account identity, fixed initial history floor, currency/timezone,
watermark/backfill cursor, covered intervals, campaign/day rows and revisions, names, retained
groups/creatives/day/OS evidence and conversion definitions. Money uses decimal strings; counts
are validated integers before persistence. Main row key: platform/account/campaign/date;
leaf key within each source: creative/date/OS. Keep older rows indefinitely unless a separate
retention feature is approved. Restatement log retains the last 500 changes, run log the last
50 runs; they are not an unlimited audit ledger. Raw API reads and host captures are retained
by their existing source evidence stores elsewhere in the same workspace.

## Subsequent run

1. Use the helper `list --workspace WS` to inspect IDs/titles/source accounts without fetching
   data. Select the user's existing dashboard. Different customers/projects stay isolated.
2. Runtime loads state under the dashboard lock; validates format and fixed source context.
3. Authorized-account updates re-read the latest seven complete account-local days by default.
   Watermark gaps catch up and unfinished initial 90-day backfill resumes, in bounded windows.
   File imports require a new explicit complete window and reuse the saved mapping. No new file
   means no new file data; a scheduled reread of old bytes is not fresh advertising evidence.
4. Validate a window before merging it. Replace same-key values; never add a new snapshot's
   totals to old totals. Complete authoritative windows remove absent rows within that window.
   Preserve rows outside it. Invalid/failed windows preserve previous values and coverage;
   successful other windows may still be committed, with partial status reported.
5. Save state via atomic file replacement, then regenerate data.json, HTML, CSV, status and
   manifest. Individual files are atomic; the entire output set is not one filesystem
   transaction. `verify` detects a state/output mismatch after interruption. Once the original
   cause is repaired, `op=status` re-renders from retained state without account reads; run
   `verify` again. Never repair an output by editing state/HTML manually.
6. Deliver the verified HTML link and explain pending/partial/stale data in chat. Do not state
   that artifact integrity proves raw-file semantics, coverage or real-account reconciliation.

Older dashboard manifests without state/asset hashes need regeneration by the matching current
runtime. Unsupported state versions stop; there is no automatic destructive migration.
The raw export and mapping are preserved by the helper under inputs; the runtime archives the
normalized JSON under evidence. Direct normalized imports must retain their original evidence
separately; the runtime does not fetch or verify an arbitrary evidence reference on their behalf.

## Recovery and portability

Back up the whole workspace while updates are stopped, including inputs/evidence and source
stores. Copying dashboard.html or data.json alone cannot resume updates. A moved workspace
needs its project/runtime binding and any account connections re-established; credentials are
not embedded in HTML or data.json. Daily schedules must point to the absolute retained workspace
and existing dashboard ID and require user consent. The report's Reload button only reloads HTML.
