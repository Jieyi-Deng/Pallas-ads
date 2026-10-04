# Competitor research sources

Use public pages you can open without signing in. Record each one as a `Source` with the URL you
actually visited, its publisher and the access date (on or before `researched_on`). Every listed
source must support a claim, profile or metric. `source_type` sets reliability:

| source_type | Reliability | Typical use |
| --- | --- | --- |
| `official_site` | high | Product claims, pricing, offers, landing-page messaging |
| `app_store` | high | App category, positioning, screenshots, ratings and review counts at access time |
| `marketplace_listing` | high | Retail or marketplace listings: price, assortment, ratings, badges |
| `social_profile` | high | The company's own social accounts: follower counts, posting cadence, content themes |
| `company_filing` | high | Annual reports, investor materials, regulatory filings |
| `ad_library` | high | Meta Ad Library: active ads, start date, formats, regions; EU/UK reach where shown |
| `transparency_center` | high | Google Ads Transparency Center: advertiser verification, formats, regions, last shown |
| `creative_center` | medium | TikTok Creative Center top ads / Commercial Content Library (coverage varies by region) |
| `press_release`, `news`, `industry_report` | medium | Launches, disclosures, positioning, market context |
| `community`, `third_party_estimate`, `other` | low | Directional context only; never verifies or observes a claim |

## Evidence hierarchy for metrics

| Tier | Use when | Shown as |
| --- | --- | --- |
| `disclosed` | The company, a filing, an app store or a platform discloses the figure | Solid value |
| `third_party_estimate` | A named publisher estimates it; keep their range | Hatched, with "estimate · publisher" |
| `observed_signal` | You counted or saw it yourself on a primary source | Value with "observed" |
| `inferred` | Your reading of indirect evidence | Text only, with confidence |
| `unavailable` | Nothing reliable was found | Retained in JSON/CSV; summarize the decision boundary once, never 0 |

A third-party figure is never `disclosed`, even when it is widely quoted. A news article reporting
a company's own announcement can support `disclosed`; a news article quoting an analyst estimate
is `third_party_estimate`.

## Platform notes

- **Meta Ad Library**: search by advertiser or keyword and country. Outside the EU/UK and
  political ads, spend and reach are generally not shown. Record "active" status as of access.
- **Google Ads Transparency Center**: filter by advertiser, region, format and date shown.
  Record what the selected country actually discloses. Do not infer campaign type, targeting or
  performance from a format or CTA; additional disclosures differ by jurisdiction. See Google's
  [transparency documentation](https://support.google.com/adspolicy/answer/13733850).
- **TikTok**: Creative Center "Top Ads" rankings are platform-curated samples; the Commercial
  Content Library covers the EU. Check what the page states about its own coverage.
- **App stores and marketplaces**: ratings, review counts and rankings change daily; record them
  as of the access date and do not compare figures taken on different days without saying so.
- Availability and coverage differ by country and change over time. When a surface does not cover
  the target region, add an `EvidenceGap` instead of substituting a weaker source.

## Recording acquisition

One `AcquisitionObservation` per activity or clearly identical set: the profile, `channel_type`
and specific `channel`, `proposition_type` and a short `proposition`, a description in your own
words, and where shown the format, region, call to action, first/last seen dates and whether it
was active when accessed. Ad delivery figures go in `public_metric` only from an ad library,
transparency center or creative center. Do not download or embed competitor media.

For each item, preserve a short evidence trail in the brief: source URL → `evidence_locator`
(creative ID, version heading, dated post) → concrete observed fact → material limitation.
For `evidence_kind=paid_ad`, record the displayed advertiser, country filter and platform item;
check its connection to the product rather than trusting a keyword match. An agency advertiser
must remain identified as an agency; record how its landing page or creative establishes the
product relationship. Separate first/last shown dates from the research access date.

Useful public-source routes for a version-launch/returning-player brief:

| Decision | Strongest retrievable evidence | Boundary |
| --- | --- | --- |
| What reason to return is advertised? | Identified ad creative and linked official destination | Hook/CTA only; not audience or lift |
| What changed in the product? | Dated official version notes or store release history | Product context, not paid activity |
| Is a returning-player incentive currently usable? | Official rules with eligibility, dates and market | Generic login rewards are not returner-only offers |
| Is the return journey explained? | Public landing page, support guide or documented deep-link destination | Do not claim installation/login completion without observing it |
| What can the requested channel support? | Current platform documentation | A platform capability is not evidence a competitor uses it |

Search the brand/product and verified advertiser variants with the requested market and window.
Open the concrete item, not only a search result. Deduplicate variants and repeated country
results. If the requested ad surface is inaccessible, try the official destination, release
rules and public support material for the narrower claim they can establish; record the paid
coverage gap. Do not substitute a third-party rehost or unrelated market as proof.

## Synthesis check

A useful chain reads: “Competitor A's dated Meta card leads with a login reward and links to its
store page; audience eligibility is undisclosed. This suggests testing reward-first messaging
against our content-first baseline, not claiming that rewards improve return rates.” It does
not read: “O6 proves rewards work; use P1.” A second country view of the same card adds geographic
coverage, not independent support for a cross-competitor pattern.

Review source **relevance** separately from the type-derived reliability label. Official store
notes are reliable for the feature they describe but do not support budget allocation, a causal
claim about churn, or a paid-campaign audience. If no source distinguishes competing explanations,
keep the conclusion narrow or omit it. A short report with one defensible finding is preferable
to several generic tests padded with missing data.

## What not to do

- No logged-in tools, no scraping behind consent walls or rate limits, and no use of the user's
  advertising accounts or Pallas connections to read competitors.
- No invented examples, and no figures from unnamed "ad spy" or estimate tools presented as
  platform or company data.
- Do not recommend that the user buy or consult other analytics, market-intelligence or dashboard
  tools to close a gap. Describe the internal data that would help (sales, campaign, traffic,
  customer or retention data) and say the user can provide it to Pallas for comparison.
