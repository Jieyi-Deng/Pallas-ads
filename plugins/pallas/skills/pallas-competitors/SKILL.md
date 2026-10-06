---
name: pallas-competitors
description: Research a product, brand, app, game or service's competitors from public sources in seven stages (scope, market context, competitor selection, evidence profiles, go-to-market and acquisition, investment and performance, synthesis) and build a cited Pallas HTML report that separates verified facts, sourced estimates, observations, inference and hypotheses. Use when the user asks who competes with them, how competitors acquire users or what competitor activity implies for their growth or marketing; not for reading the user's own ad accounts or for scraping logged-in tools.
---

# Pallas competitor research

You research; Pallas validates and renders. The runtime never browses. You collect public
evidence through the seven stages below, write a `CompetitorBrief`, and call
`build_report(action=competitor_review, competitor_brief={...})`. The runtime rejects briefs that
break the evidence rules, then writes `report.html`, `report.md`, `chat.md`, `report.json`,
`sources.csv`, `observations.csv`, `metrics.csv` and `manifest.json` under
`reports/competitors/competitor_<id>/` in the selected workspace. Brief schema: `pallas operations`
(`ReportRequest.competitor_brief`).

## Principles

1. **Evidence first.** Establish facts and evidence before interpreting them. Every claim cites
   the sources it rests on, and only pages you actually opened in this session count. Never invent
   a source, competitor, campaign, date, metric or creative.
2. **Adaptive dimensions.** Profile fields, channels, propositions and metrics follow the
   category and business model. A subscription app, a game, a retailer and a B2B service are
   compared on different things; do not force one fixed template onto all of them.
3. **Missing is not zero.** Data you could not find is `unavailable`, with a note on why. Never
   write 0, a guessed number or a placeholder for missing data, and never make an estimate look
   like verified data.
4. **Observation → Evidence → Implication → Hypothesis.** Competitor behaviour generates
   hypotheses for the user to validate, never "best practice". Do not claim that a tactic works,
   causes growth or explains a competitor's results unless a disclosed source says so.

## Stage 1 — Define the research scope

Do not start by searching. First establish why the research is being done and which decisions it
must inform. Confirm, asking only for what is missing (use a confirmed Pallas product profile when
one exists; never guess the product from account or campaign names):

- the subject (product, brand, app, game or service), its category and core function;
- target markets and geography, and the audience;
- business model: one-time purchase, subscription, in-app purchase, advertising-supported,
  marketplace, freemium or other;
- the growth or marketing objective;
- any specific questions the user actually asked; an objective alone is enough.

Record these as `subject` and `scope` (`objective`, optional `questions`, `researched_on`,
`period_note`, `method`, `queries`). Questions supplied by the user have `origin=user` and each
gets one answer. Optional researcher planning questions have `origin=research`; they are internal
working notes, not a questionnaire for the reader. Do not invent eight questions to fill the
schema. `answers` is the executive summary: retain the few findings that change a decision;
`question_id` is optional. Do not repeat planning questions or display Q/O/P/M identifiers in prose.
Set `competitor_brief.report_language` to `zh-CN` for Chinese input (including Traditional
Chinese), and `en` for every other input language. An explicit output-language request takes
precedence under this same mapping. Determine it from the user's request, not the researched
market, source pages, brand names or previous reports. Write all analyst-authored brief prose
(title, summaries, profile attributes, observations, hypotheses and gaps) in that selected
language before rendering; the runtime localizes fixed labels, not arbitrary supplied prose.
Keep original brand names, source titles, quotations, URLs, IDs and values intact. If also
passing top-level `build_report.report_language`, it must match the brief. Other locale codes
normalize to English; the renderer does not translate a third-language brief automatically.

## Stage 2 — Understand product, audience and market

Build the comparison framework before choosing competitors:

- **Product:** the problem solved, value proposition, key features and formats.
- **Audience:** who uses it, who pays, who decides, and the usage occasions.
- **Market:** segmentation, prevailing business models, pricing and monetization, channels,
  geography, seasonality and trends.

Record each sourced point as a `context` item (`dimension` product/audience/market). Seasonal
windows with sourced or inferred timing go in `seasonality`; a market-level size or growth figure
goes in `metrics` with no `profile_id`.

## Stage 3 — Discover and classify competitors

- **Direct** (`direct`): solves a similar problem for a similar audience with a similar format or
  business model.
- **Adjacent** (`adjacent`): competes for the same need, budget, time or attention in a different
  way.
- **Category benchmark** (`benchmark`): a reference point for how the category acquires and
  monetizes users, even if it does not compete head-on.

Choose for comparison value, not fame or size. Each `profile` states its `selection_reason` and
cites a source. Add the subject itself as the one `subject` profile when you have public evidence
about it, so the report compares like with like. If you cannot confirm a candidate, leave it out
and record the gap.

## Stage 4 — Build competitor evidence profiles

Per profile, collect Competitor → Product → Audience → Positioning → Business model →
Distribution → Marketing → Evidence → Source. Record each as a `ProfileAttribute` with a
category-appropriate `label` (for example "Entry price", "Content library", "Store rating",
"Retail footprint") and its evidence label. Establish facts and evidence first, then interpret
them: an attribute you read off a page is `verified`; your reading of positioning or audience is
`inference` with a confidence. Use the same labels across profiles where possible so the
landscape table compares them; a field you could not establish is simply omitted and shows as
"not established".

## Stage 5 — Investigate go-to-market and user acquisition

Record one `AcquisitionObservation` per distinct activity, not per source URL or country filter:

- **Where** they acquire users (`channel_type`): search, paid social, organic social, app stores,
  creators, retail, marketplaces, partnerships, affiliates, communities, content/SEO, email/CRM,
  events or other. `channel` names the specific surface.
- **What** they use to acquire them (`proposition_type`): product, feature, content, creative
  concept, value proposition, offer, user scenario, social proof or brand positioning.
  `proposition` is a short name for it; `description` says what you saw, in your own words.
- **What this proves** (`evidence_kind`): `paid_ad`, `owned_content`, `store_listing`,
  `organic_content` or `other`. Paid ads require a platform disclosure source, the actual
  `advertiser`, `region` and an `evidence_locator` (creative/library ID or page section).
  Record the advertiser shown, including agencies; do not silently replace it with the game name.
  For other observations, retain a locator where useful (version notes, dated post, offer terms).
  Use `limitation` for a material boundary such as only seeing a video's opening frame.

Adapt to the category: a game's acquisition is creatives and store pages, a retailer's is search,
marketplaces and offers, a B2B service's is content, events and partnerships. Each observation
needs a primary public source; a third-party estimate alone is not an observation. Delivery
figures (reach, impressions, rank) go in `public_metric` only when the platform's own ad library,
transparency center or creative center shows them. A funnel you can evidence goes in `journey`.

Make each observation inspectable: name the concrete hook, offer, product change or destination,
the market and relevant date/version, and link directly to the supporting item. A qualitative
observation can be valuable without a performance number. A title, generic library homepage or
unplayed video does not support a scene-by-scene creative analysis. Store availability proves
distribution; patch notes prove a product change; neither proves paid delivery, lapsed-user
targeting, a current returner entitlement or effectiveness. Keep historical and current offers
separate. Search requested channels/countries before expanding into convenient store-page evidence.

## Stage 6 — Investigate investment and performance

Which metrics matter depends on the business model (downloads and ratings for apps, subscribers or
revenue for subscriptions, active ads and creative volume for paid social, store footprint for
retail, funding or headcount for early companies). Record each as a `Metric` on the evidence
hierarchy (`tier`):

1. `disclosed` — reliable first-party or publicly disclosed data (official site, app store,
   filing, press release, news reporting a disclosure, platform disclosure surface).
2. `third_party_estimate` — an estimate from a specific, identifiable publisher; cite it and use a
   `low`–`high` range when the publisher gives one.
3. `observed_signal` — an indirect signal you counted or saw yourself (active ad count, review
   volume, posting cadence), cited to the page you observed.
4. `inferred` — your interpretation; `display` text only, never a number, plus `confidence`
   and the evidence it rests on.
5. `unavailable` — insufficient or unavailable; no value, range or display, and a `note` on why.

Investigate availability, but do not manufacture a competitor × KPI grid of unavailable rows.
Retain missing metrics only when needed to document a decision the user asked about; group the
reason once in `gaps`. Missing values remain in JSON/CSV, not repeated in the report body.

The report's metrics section is evidence-dependent:

- With usable spend/performance figures, compare only matching definitions, geography, period,
  units and population. Record `geography` and `period`; unlike scopes must not share a chart.
- With only activity proxies, use **Observable activity signals** and explain what each means
  and cannot mean. A count of active ads is not spend, reach, creative diversity or success.
- With no substantive measures, omit the metrics section. Use the already-evidenced creative,
  offer, destination and timing comparison instead; do not add a replacement section of generic
  advice. One decision boundary can explain why no budget or ROAS ranking is possible.

## Stage 7 — Synthesize patterns and opportunities

Synthesis starts with an evidence test, not a quota of opportunities. For each proposed finding,
ask whether the cited item supports this exact claim, in this market/time/channel. A reliable
publisher is not a guarantee of claim relevance. Delete a conclusion that only restates a gap or
could have been written without reading any of the evidence.

Each retained `pattern` follows Observation → Evidence → Implication → Hypothesis / potential test:

- `observation`: what competitors do, stated neutrally;
- `evidence`: a self-contained sentence naming the competitor, concrete example and boundary,
  with `observation_ids`, `metric_ids` and `source_ids` as internal traceability. “See O4–O7” is
  not evidence. Source citations appear beside the reasoning, without requiring ID decoding;
- `implication`: what it may mean for the subject;
- `hypothesis`: what the user could test, plus optional `test`, `success_measure` and a `lever`
  the user controls (creative, messaging, format, audience_targeting, bidding,
  budget_allocation, landing_page, offer, pricing, product_packaging, channel_mix, test_design);
- `confidence` (low/medium), optional `impact` and `effort` as working metadata, and
  the internal `question_ids` it answers.

Set `kind` to match the support:

- `cross_competitor`: the same specific behaviour evidenced for at least two competitors.
  Reference their observation/usable metric records. Multiple countries, formats or pages for
  one advertiser do not create multiple competitors. Mention common ownership when relevant.
- `single_example`: one concrete example or a context source suggests a bounded test; do not
  call it a market pattern. No minimum count forces weak recommendations into the report.
- `measurement_proposal`: the analyst's measurement design, visibly separate from competitor
  findings. Missing spend or ROAS can motivate measurement, but cannot establish a winning tactic.

Keep only decision-relevant tests. State the variable, comparison and meaningful outcome; use
owned baselines for sample size, budget and timing. Do not invent media splits, uplift, fixed
video lengths or a release calendar and imply they came from competitor evidence. If a test
depends on unavailable eligibility or platform capabilities, state that dependency first.

Do not recommend changing competitor behaviour, platform policy or the market. Optional
`position` points (strength/weakness/opportunity/threat) summarize the subject's position.

## Evidence labels

Claims carry `basis`:

- `verified`: directly visible in a cited medium/high-reliability source. No confidence.
- `estimate`: a sourced third-party figure; the report names its publisher. No confidence.
- `observed`: something you saw on a primary public source (an ad, a listing, a post). No
  confidence.
- `inference`: your interpretation; cite the evidence and state `low` or `medium` confidence.

Patterns are always hypotheses. Low-reliability sources (community, third-party estimates,
other) cannot verify or observe a claim. Absence in a sample is not absence in the market: say
"not observed in this sample".

## Writing the report

- Keep it concise and scannable: short summaries, comparison tables, charts only where the data
  supports them, qualitative frameworks where data is missing, short opportunity statements.
- Lead with a small set of decision-relevant findings, not eight equally weighted answers.
  Each `answer` has a clear `headline`, a short explanation, basis and sources. Use `partial`
  or `insufficient_evidence` honestly; a lack of performance data does not negate a sourced
  qualitative fact. Include the user's actual question only if needed to understand the answer.
- Give each section a distinct job: summary = decision; observations = concrete evidence;
  opportunities = bounded inference/test; gaps = unresolved decision and needed input.
  Reuse the source citation where necessary, but do not repeat whole paragraphs or use IDs as
  substitutes for reasoning. Do not turn every source into an observation and every observation
  into a recommendation. Omit generic SWOT, arbitrary priority scores and empty sections.
- Keep verified facts, sourced estimates, observations, inference and hypotheses visibly apart
  through the labels above, not through wording alone.
- **Do not recommend other analytics, market-intelligence or dashboard tools.** When public data
  cannot settle a point, describe the data that would help and say the user can provide it to
  Pallas. Each `gap` states the blocked decision in `topic`/`reason`; `user_data` names only
  the specific useful input, without repeating “provide to Pallas” (the renderer supplies it).
  Owned campaign data can validate the user's economics; it cannot reveal competitor spend.
  Do not repeat every scope exclusion as a separate data request.
- The final reference list displays **publisher/author, title, full linked URL only**.
  Source IDs remain anchors. Access/publication dates, type, reliability, queries, method and
  export/manifest metadata stay in the research files, not the references display.
- Keep the fixed template. It uses readable evidence records rather than eight-column prose
  tables or four-column long-text cards. Verify real English/Chinese content at desktop and
  narrow widths; examine wrapping, nearby citations and print flow, not just file validity.

## Research rules

Follow [research sources](references/research-sources.md). Use public pages you can open without
signing in. Do not log in, bypass consent walls, use the user's ad accounts or the Pallas
connections to read competitors, or scrape Ads Manager. Describe creative in your own words; do
not copy media or long ad text. Reliability is derived from `source_type`; you cannot set it.

## Delivery

Before rendering, audit the strongest summary claims and every proposed test against their
actual sources: exact supporting fact, scope match, alternative explanation, and decision value.
Downgrade or remove unsupported claims. Count independent examples, not links. The runtime
checks structure and some evidence rules; it does not verify a page's contents or entailment.

Share `report.html` as the human-facing report (self-contained; it opens in a browser and prints
to PDF) and use `chat.md` as the factual summary in chat. State the research date, how many
sources, observations and metrics back the report, how many metrics are unavailable, and the main
gaps with the data the user could provide to Pallas. `status=partial_result` with
`competitor_evidence_insufficient` means the evidence cannot support a competitive picture; say so
rather than padding the report. Use `evidence_mode=public_research` for real research;
`synthetic_fixture` is only for invented demonstrations with `example.com` URLs, and the runtime
rejects placeholder domains in research and real domains in fixtures.
