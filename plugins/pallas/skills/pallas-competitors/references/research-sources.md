# Competitor research sources

Use public pages you can open without signing in. Record each one as a `Source` with the URL you
actually visited and today's access date. `source_type` sets reliability:

| source_type | Reliability | Typical use |
| --- | --- | --- |
| `ad_library` | high | Meta Ad Library: active ads, start date, formats, regions; EU/UK reach where shown |
| `transparency_center` | high | Google Ads Transparency Center: advertiser verification, ad formats, regions, last shown |
| `official_site` | high | Product claims, pricing, offers, landing-page messaging |
| `app_store` | high | App category, positioning, screenshots, ratings shown at access time |
| `creative_center` | medium | TikTok Creative Center top ads / Commercial Content Library (coverage varies by region) |
| `press_release`, `news`, `industry_report` | medium | Launches, positioning, market context |
| `third_party_estimate`, `other` | low | Directional context only; never verifies a finding |

## Platform notes

- **Meta Ad Library**: search by advertiser or keyword and country. Outside the EU/UK and
  political ads, spend and reach are generally not shown. Record "active" status as of access.
- **Google Ads Transparency Center**: filter by advertiser, region, format and date shown. It does
  not show spend, targeting or performance.
- **TikTok**: Creative Center "Top Ads" rankings are platform-curated samples; the Commercial
  Content Library covers the EU. Check what the page states about its own coverage.
- Availability and coverage differ by country and change over time. When a surface does not cover
  the target region, add an `EvidenceGap` instead of substituting a weaker source.

## Recording creative

One `CreativeObservation` per ad or clearly identical ad set: platform, region, format, angle,
a short description in your own words, call to action, first/last seen dates if shown, whether it
was active when accessed, and its source. Do not download or embed competitor media.

## What not to do

No logged-in tools, no scraping behind consent or rate limits, no use of the user's advertising
accounts or the Pallas connections to read competitors, no invented examples, and no metrics
copied from unnamed "ad spy" tools as if they were platform data.
