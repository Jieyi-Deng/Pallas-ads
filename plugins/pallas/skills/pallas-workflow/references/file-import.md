# User advertising CSV/XLSX

Use this route when the user supplies an export. No media authorization, product profile or
OpenAI API key is required. First release accepts one platform/account/currency, campaign-day
rows with unique campaign_id + date. Do not combine account totals, campaign rows, ad rows or
breakdowns. Do not rewrite raw files to make invalid input pass.

1. Call `source_connect_or_import(action=file_preview,file_path=...,import_options=...)`.
   `import_options.platform` is meta/google/tiktok. Currency, timezone and account identity can
   come from columns or explicit user confirmation. Identify unresolved facts together, not a
   long setup questionnaire. A missing identifier in an export can use a user-confirmed local
   account label; clearly retain that it is not a verified API account identity.
2. Auto matching is conservative. For ambiguous columns supply `column_mapping` from Pallas
   field names to exact source headers. Prefer export instructions or user confirmation over
   guessing Clicks vs Clicks (all), decimal conventions, date ranges or spend units.
3. Present returned account/platform, dates, row/campaign counts, mappings, ignored columns,
   missing values, currency/timezone and conversion semantics. Obtain confirmation of the exact
   interpretation (reuse an already explicit matching confirmation). Never ask for hashes.
4. Call `file_import` with the unchanged file/options, returned `review_hash` and
   `user_confirmed=true`. Changed inputs require a fresh preview. Copy no credentials.
5. Call `build_report(action=file_review,dataset_id=...)`, then follow pallas-analysis.
   Report partial_result is expected: file coverage and business semantics remain unverified.
   Link the HTML and chat/JSON artifacts, explain results and next checks, not only paths.

CSV is UTF-8; choose delimiter comma (default), semicolon or Tab explicitly. XLSX must be
values-only, unencrypted and without formulas/errors. Choose one sheet when multiple exist.
`header_row` is 1–20. ISO daily dates, amount in account currency major units, text IDs.
No .xls, 8 MiB/50,000 rows/100 columns maximum. Full supported format: bundled FILE_IMPORT.md
in the test package. Required columns: date, campaign_id, spend, impressions, clicks.
Optional: campaign_name, date_end (same day), currency, timezone, account_id, conversions,
conversion_value. Required monetary/context metadata must be resolved before confirming.

Nulls are not zero; duplicates or mixed accounts/currencies are errors. Ratios are derived from
summed components. Arbitrary dates, micros, localized decimal commas and currency symbols must
not be silently converted. Preserved conversions are native facts, not verified purchases/ROI.
Do not average reported CTR, multiply averaged CPA or infer unreported revenue.

File datasets are independent immutable snapshots. Reimport is idempotent, not an append.
Files overlapping an API read or another file must NOT be added together. Multi-file merging,
automatic account binding and live scheduling are separate future capabilities. A stored file
is not a live media connection. For new data, preview/import a new file and report its scope.

After generating the factual report, ask only business questions that affect the user's actual
decision (product/optimization event/target/attribution) and label additional ideas as hypotheses.
No invented product profile, budget recommendation or causal claim to fill missing evidence.
