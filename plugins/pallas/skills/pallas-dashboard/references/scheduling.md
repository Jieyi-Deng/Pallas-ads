# Opt-in daily dashboard updates

Do not enable a schedule by default. Before creating it, obtain the user's agreement to daily
updates and establish the dashboard/workspace, sources, local time and timezone. Reuse explicit
consent already in the conversation. Use the host's supported scheduler; no hidden cron or
launch agent. This reference is not authorization to create a schedule.

Default refresh is the latest seven complete account-local days, excluding today. On missed
runs, catch up from the saved watermark; initial incomplete backfill may also resume. A wider
window (up to 30 days through the existing CLI) or explicit normalized-file import can include
older adjustments. Seven days is a refresh policy, not a guarantee that all attribution is final.

For built-in live sources:

```sh
pallas dashboard update --dashboard dash_main --workspace /absolute/workspace --lookback-days 7
```

For Meta host_capture, the scheduled host must have the signed-in official MCP tools. Run the
returned exact reads, retain complete pagination and account/field context, stage the capture,
then update with capture_id. A plain shell timer cannot perform this signed-in host step.
For rich authorized-host exports, normalize the complete window using data-contract.md and
import data_path. An uploaded-only source waits for a new file; do not claim polling an old
file produces fresh data.

Suggested approved task prompt:

> Refresh dashboard dash_main in /absolute/workspace from its authorized sources. Fetch the
> latest seven complete days in each account timezone, using the configured route. For host
> capture, execute the requested reads; for normalized evidence, preserve field mappings and
> conversion definitions and validate the complete window before importing. Incrementally
> replace matching daily records, retain older history, regenerate data.json and dashboard.html.
> If a read is incomplete or authorization has expired, keep previous evidence and report the
> actionable problem. Do not change advertising accounts, expand authorization or fabricate
> missing fields. Report changed/restated windows, coverage, freshness and errors; avoid routine
> notifications when there is nothing actionable, unless the user requested daily summaries.

CLI exit codes: 0 complete, 2 partial (including explicitly synthetic evidence), 3 waiting for
host capture, 1 needs input. A failed source keeps its prior evidence; healthy sources may update.
`dashboard status` reads retained state and re-renders; it does not fetch new account data.
Browser Reload report similarly only reloads saved HTML. Alert rules evaluate the saved snapshot
inside the browser and are separate from scheduled data refresh.
