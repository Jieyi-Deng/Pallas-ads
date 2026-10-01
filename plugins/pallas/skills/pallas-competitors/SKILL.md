---
name: pallas-competitors
description: Research competing advertisers from reliable public sources and build a cited, consulting-style Pallas HTML report on their ad creative with recommendations the advertiser controls. Use when the user asks who competes with their advertised product and what ads competitors run; not for reading the user's own ad accounts or for scraping logged-in tools.
---

# Pallas competitor advertising report

You research; Pallas validates and renders. The runtime never browses. You collect public
evidence, write a `CompetitorBrief`, and call
`build_report(action=competitor_review, competitor_brief={...})`. The runtime rejects briefs whose
claims are not tied to cited sources, then writes `report.html`, `report.md`, `chat.md`,
`sources.csv`, `observations.csv`, `report.json` and `manifest.json` under
`reports/competitors/competitor_<id>/` in the selected workspace.

## Inputs to confirm first

Product and what it does, category, target regions, target audiences and the ad platforms that
matter (Google, Meta, TikTok, other). Use a confirmed Pallas product profile when one exists;
otherwise ask only for what is missing. Do not guess the product from account or campaign names.

## Research rules

Follow [research sources](references/research-sources.md). In short:

- Prefer platform disclosure surfaces (Meta Ad Library, Google Ads Transparency Center, TikTok
  Creative Center / Commercial Content Library), then official sites, app stores, and the
  company's own press releases. Reliability is derived from `source_type`; you cannot set it.
- Only use pages you actually opened in this session. Record the exact URL, title, publisher and
  access date. Never invent a source, competitor, campaign, date, metric or creative.
- Do not log in, bypass consent walls, use the user's ad accounts, or scrape Ads Manager.
  Describe creative in your own words; do not copy media or long ad text.
- A competitor needs a stated basis (same category, region and audience overlap) and a source.
  If you cannot confirm a candidate, leave it out and record the gap.
- Delivery figures (reach, impressions, "top ad" ranks) may only come from the platform's own
  disclosure surface (`public_metric`). Third-party spend estimates are low-reliability context
  that can support an inference, never a verified finding or a creative observation.

## Evidence layers

- `verified`: directly visible in cited medium/high-reliability sources. No confidence field.
- `inference`: your reading of the pattern; cite observations or sources and state `low` or
  `medium` confidence. Say why it could be wrong.
- `gaps`: what you could not see (for example, spend and conversion data, unsupported regions,
  or platforms whose libraries do not show the ad type) and how the user could close each one.

Absence in a sample is not absence in the market: say "not observed in this sample".

## Recommendations

Only levers the advertiser controls: `creative`, `messaging`, `format`, `audience_targeting`,
`bidding`, `budget_allocation`, `landing_page`, `offer`, `test_design`, `platform_mix`. Each one
references findings, is specific enough to execute (what, where, how many, for how long), and has
a success measure from the user's own data. Do not recommend changing competitor behaviour,
platform policy, auction dynamics or the market. Treat competitor activity as a hypothesis to test,
not as proof that a tactic works.

## Delivery

Share `report.html` as the human-facing report and use `chat.md` as the factual summary in chat.
State the research date, how many sources and observations back the report, and the main gaps.
`status=partial_result` with `competitor_evidence_insufficient` means the evidence cannot support
a competitive picture; say so rather than padding the report. Brief schema: `pallas operations`
(`ReportRequest.competitor_brief`). Use `evidence_mode=public_research` for real research;
`synthetic_fixture` is only for invented demonstrations with `example.com` URLs, and the runtime
rejects placeholder domains in research and real domains in fixtures.
