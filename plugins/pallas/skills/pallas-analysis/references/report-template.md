# Human-facing report contract

Read this before delivering a new Pallas HTML analysis report. The default template is
[`../assets/report.html`](../assets/report.html). The runtime and the exported Skill use this same
file; do not maintain a second independent layout. Change the format only when the user explicitly
requests another format. Retained legacy reports stay immutable; their original format is not a
reason to deliver a new account report outside this template.

## Required HTML structure

```html
<header><!-- Report title, one-sentence purpose, section navigation --></header>
<section id="overview">
  <h2>一、账户与期间总结</h2>
  <!-- Account, verified products, actual current goals/events, dates, coverage, KPI cards -->
</section>
<section id="changes">
  <h2>二、变化与原因拆解</h2>
  <!-- Each finding: where, what changed, quantified contribution, why/uncertainty, chart -->
  <!-- Time trend; before/after comparison; campaign mix; relevant delivered audience -->
</section>
<section id="recommendations">
  <h2>三、主要发现与建议</h2>
  <!-- Summarize supported findings, prioritized actions, validation measures -->
  <footer><!-- Links to local evidence and precise data; display methodology --></footer>
</section>
```

The runtime fills `$title`, `$subtitle`, `$overview`, `$changes`, `$recommendations`, and
`$evidence_links` in the asset. Source strings must be escaped. Place no JSON, Python dictionary
representation, raw API field inventory, `<pre>`, or large raw-data block in the HTML body,
including collapsed details. Small curated tables have reader-facing labels, explicit units and
only the columns needed to understand a finding.

Keep full-precision data and raw source evidence in separate local files. Link the actual files
from the corresponding finding and footer. Default files: `report.json`, `evidence/daily.csv`,
`evidence/campaigns.csv`, `evidence/audience.csv`, `evidence/context.json`,
`evidence/diagnostics.json`, `evidence/notes.md`, and `manifest.json`. Do not link fake paths or
provider record URIs that the user cannot open. Preserve failures and scope limits in the sidecars;
put their material implications in the body, in human language.

## Numeric presentation

All displayed quantitative measurements use two digits after the decimal (omit the decimal part when the rounded value is an integer): money, impressions,
clicks, conversion counts, percentages, relative changes, percentage-point changes, contributions,
thresholds and chart annotations. Convert ratio to percent before rounding; distinguish percent
change from percentage-point change. Formatting is a presentation operation, not a transformation
of retained data or intermediate arithmetic. Null/zero-denominator values read “未提供”. Do not
round dates, identifiers, version strings, or categorical age labels as though they were measures.
Use section names or Chinese ordinals rather than decimalized section numbering.

## Interpretation and visualization

- Start with the question a business reader needs answered. The overview sets account/product,
  goal/event, actual scope and comparison context before presenting performance judgments.
- For a change, say where it appears, the before/after magnitude, the measurable contributors,
  what they imply for this product and optimization goal, and what still needs verification.
  Observed differences are not automatically anomalies. A same-period audience contrast is not
  evidence of audience composition changing over time.
- An arithmetic decomposition explains contribution; it does not establish auction competition,
  creative fatigue or another business cause. Label such causes as hypotheses and specify the
  evidence or controlled test required. If supporting data is missing, state that plainly.
- Use actual-date line charts for trends and break lines over missing dates. Never equate absent
  rows with zeros. Use sorted horizontal bars for categories and zero-centered bars for signed
  contributions. Category bars start at zero. Do not connect unrelated categorical groups.
- Prefer direct labels, units and short explanatory captions. Use muted context and a small
  number of emphasis colors; color direction consistently (cost increase vs decrease). Avoid
  decoration, crowded legends, unexplained abbreviations and large technical tables.
- Chart and table values come from the same retained arithmetic. Explicitly disclose any displayed
  subset; do not silently drop the rest of a time series. Link full data for truncated category lists.
- The closing recommendations must follow the findings. State action, rationale, success measure,
  needed evidence and key constraints. Do not invent budget or business success thresholds.

## Reference basis

Cole Nussbaumer Knaflic, *Storytelling with Data* (Wiley, 2015): context (chapter 1), choosing visuals
(chapter 2), reducing clutter (chapter 3), directing attention (chapter 4), and narrative structure
(chapter 7). Consulted the user's local English PDF, particularly printed pages 21, 45, 73, 103 and
168 (PDF pages 37, 61, 89, 119 and 184). These principles are paraphrased; no book graphics or long
excerpts are copied into the template. The two-decimal/integer convention is the user's explicit product
requirement, not a recommendation attributed to the book.

Presentation details: left-align text columns and right-align numeric columns, including their headers. Place units visibly inside every chart (axis/header or value labels), not only in tooltips or captions. Label intermediate dates at readable intervals based on the time span; retain endpoints, avoid crowding, and show a single tick for a single-day range. These numeric rules also apply to chat/Markdown summaries.
