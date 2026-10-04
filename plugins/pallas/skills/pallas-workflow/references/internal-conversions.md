# Internal conversion data with an advertising file

Use this route only after an advertising CSV/XLSX has been confirmed through
[the file workflow](file-import.md) and the user also supplies a first-party export from their own
product, CRM, analytics or back office (new users, conversions, revenue, retention by channel).
No media authorization is required. Internal data never becomes platform data.

## Accepted shape

One row per local date and acquisition channel, optionally split by media platform and campaign ID.
Required: `date` (ISO daily), `channel`, and at least one of `new_users` or `conversions`.
Optional: `platform` (for example a `utm_source`), `campaign_id`, `revenue`, `retained_users`.
Counts must be integers. Rows must be unique by date + channel + platform + campaign_id.
Auto-detected aliases include `signups`/`installs` (new users), `first_purchases`/`purchasers`
(conversions), `utm_source`/`media_source` (platform) and `d7_retained` (retained users). Supply
`column_mapping` when a header is ambiguous. Same CSV/XLSX limits as advertising files.

## Steps

1. Call `source_connect_or_import(action=internal_preview,file_path=...,internal_options=...)`.
   `internal_options` records the user's confirmed meaning: `timezone` (IANA), `currency` when
   revenue exists, `conversion_definition`, `attribution_basis` (how the business assigned a
   channel, for example last non-direct UTM), `cohort_basis` (`acquisition_date` when later
   conversions/retention are attributed back to the signup date; `event_date` otherwise),
   optional `new_user_definition`, `retention_definition` (required with retained users),
   `channel_mapping`, `platform_mapping` and `omitted_zero_rows` (below).
2. Only exact values `paid` / `organic` map automatically. Show `channel_values_unmapped` and ask
   the user to classify every channel as paid, organic, excluded (for example test/internal
   traffic) or unknown. Unknown is never forced into paid or organic. Platform values map
   automatically only for exact `google`, `meta`, `tiktok`; ask about others (for example
   `facebook` → meta). Do not infer channel type from a name; ask.
3. Present date range, row count, mapping, unmapped values, missing fields, definitions and any
   omitted-zero confirmation. After
   the user confirms that exact interpretation, call `internal_import` with unchanged inputs,
   the returned `review_hash` and `user_confirmed=true`. Never ask the user for hashes.
4. Call `build_report(action=file_review,dataset_id=...,internal_dataset_id=...)`. The standard
   three-section report gains an integrated assessment in section 二 and findings in section 三.

## Matching rules (enforced by the runtime)

- Dates: only local dates present in both files. If timezones differ, no daily match is made and
  no integrated metric is computed; ask for a re-export in one timezone.
- Platform: only paid rows mapped to this advertising file's platform are divided by its spend.
  Paid rows for other platforms, paid rows without a platform, unknown and excluded rows are
  counted and shown separately, never credited to this platform.
- Campaigns: exact `campaign_id` equality only. Names, partial text and similar IDs never match.
  Unmatched IDs on either side are listed.
- Explicit `0` is valid data, never a missing-data warning.
- Missing internal rows (a scope date without a group's rows, or a date with ad rows for a
  campaign but no internal row for that campaign ID when paid rows are split by campaign) and
  blank values: metrics are calculated from the provided observations whenever computable. Raw
  gaps stay missing in `internal_integration.coverage` and in daily values; they are never filled
  with zero. Another campaign's row, or an organic row, never covers the gap.
- Each affected metric is labelled `basis: provided_data` with factual `warnings` beside it
  (`metric_notes` for efficiency, the row itself for quality, campaign, daily and trend rows).
  The report shows "（按已提供数据计算）" and the warning next to the number. Warnings name the
  dates, campaigns or blank fields and ask whether the absence means zero or an incomplete
  export. Never say data was lost.
- `omitted_zero_rows`: only when the user confirms the export covers the full stated scope and
  intentionally omits zero-valued rows, pass `[{start, end, metrics}]`. Absent rows on those
  dates are then read as zero for the listed metrics only, without a warning; blanks in rows
  that exist are still warned. Zero conversions never imply zero new users, revenue or retention;
  list each metric the user actually confirmed. A confirmed date with no rows at all stays in the
  overlap. The confirmation is part of the reviewed options, so changing it needs a new preview.
- Ratios: a missing operand or a zero denominator makes the ratio unavailable with that reason in
  `unavailable` (a quality row's `reason`, a campaign row's `unavailable`), never a zero. Ratios use summed numerators
  and denominators. Advertising-side blank spend still withholds spend-based metrics.
- Currency: internal revenue / ad spend is computed only when currencies match.

## Metrics and when they are unavailable

Missing internal rows or blanks do not withhold a metric; they label it `provided_data` with a
warning (see above). A metric is unavailable only in these cases:

| Metric | Formula | Unavailable when |
| --- | --- | --- |
| Internal CAC | ad spend / paid new users mapped to this platform | no platform field, no mapped paid rows, no provided paid new users, a zero denominator, or blank ad spend |
| Cost per internal conversion | ad spend / paid conversions for this platform | same for conversions, or no conversions column |
| Internal revenue / spend | internal paid revenue / ad spend | no revenue, currency differs, or zero/blank spend |
| Platform ÷ internal conversions | platform-reported conversions / internal paid conversions | ad file has no complete conversions column, or zero internal conversions |
| Conversion rate, revenue per new user, retention rate | group numerator / group new users | a missing operand or zero new users in either group, or fewer than 30 new users in either group |
| Organic trend | equal halves of a continuous overlap of at least 8 days | shorter or gapped overlap |

Paid-versus-organic quality compares paid users mapped to this platform (or all paid users when
no platform field exists, which is labelled) against organic users. The 30-user floor is a display
threshold, not a significance test.

## Interpretation limits

State these when relevant; do not overwrite them with confident prose:

- Differences between paid and organic users are descriptive. They do not measure incrementality,
  cannibalization or lift; organic users can be influenced by advertising.
- Internal attribution and platform attribution differ. Never add the two conversion counts or call
  either one wrong without checking definitions, windows and deduplication.
- With `event_date` cohorts, conversion and retention rates are same-period ratios, not
  acquisition cohort quality.
- Unknown and excluded channels, unmatched campaigns and dates outside the overlap reduce coverage;
  report their counts before conclusions.
- Missing columns remove metrics instead of creating zeros or estimates. Do not recommend budget
  moves from a single period, small groups or unmatched data.
