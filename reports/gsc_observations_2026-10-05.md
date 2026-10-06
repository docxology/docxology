> Provenance: read manually from the signed-in Search Console UI by the site owner on 2026-10-05 (operator handoff); not machine-verified.

# Search Console observations — 2026-10-05

Property: `https://danielarifriedman.com/`. Procedure: [gsc-followup.md](../docs/seo/gsc-followup.md). The machine-checked companion is the preflight receipt `reports/gsc_preflight_2026-10-05.json`. Values below are as read from the UI; the repo-side facts in the Sitemaps section were checked against the repository and the live site.

## Overview

| Measure | Value |
|---------|-------|
| Indexed pages | 1,338 |
| Not indexed pages | 210 |
| Web clicks since 2026-07-04 | 211 |

The Page-indexing filter behind "1,338 indexed / 210 not indexed" was not recorded in the handoff. These totals (1,548) do not sum to the 2,332 pages read from the submitted `sitemap.xml`; the Overview may be counting all known pages rather than submitted pages, but that is unverified. Future rechecks should record the filter used (all known pages vs all submitted pages) so week-over-week changes compare like with like.

## Sitemaps

| Sitemap | Status | Submitted | Last read | Pages | Notes |
|---------|--------|-----------|-----------|-------|-------|
| `sitemap.xml` | Success | 2026-07-21 | 2026-10-04 | 2,332 | Matches the deployed sitemap's URL count that day. The repository sitemap adds one work page (#224) after that read, so later preflight receipts count one more URL until Google re-reads it. Not resubmitted. |
| `sitemap-images.xml` | Couldn't fetch | not recorded | 2026-08-21 | 1 | File removed 2026-08-28 in commit `64dd484a`; live request returns 404 (confirmed 2026-10-05). **Action: remove the entry in GSC (not yet done)**; see Step 1b of the runbook. Never recreate or resubmit it. |

## URL inspection

| URL | Result | Canonical | Last crawl | Indexing request |
|-----|--------|-----------|------------|------------------|
| `/` (homepage) | Indexed | The inspected URL | 2026-10-04 | None made |
| A Blake work page (`works/<citation_key>.html`; the specific citation key was not recorded in the handoff) | Indexed | Matches | 2026-10-01 | Requested |
| `publications.html` | Indexed | Matches | 2026-08-17 (stale) | Requested |
| `repositories.html` | Indexed | Not recorded | 2026-09-28 | Requested |
| `videos.html` | Indexed | Matches | 2026-09-27 | Requested |
| `software.html` | Indexed | Not recorded | Not recorded | Requested |
| `exports.html` | Indexed | Not recorded | Not recorded | Requested |
| `catalog.html` | Indexed | Not recorded | Not recorded | Requested (errored once, succeeded on retry) |
| `cite-verify.html` | Indexed | Not recorded | Not recorded | Requested |
| `discovery.html` | Indexed | Not recorded | Not recorded | Requested |

Referring pages for `repositories.html` include `github.global.ssl.fastly.net/.../repositories.html`. That is the legacy GitHub Pages CDN host: direct requests to it return 404, and `repositories.html` is `index, follow` with a self-canonical. No action.

Request quota: about 10 requests per day, effectively used on 2026-10-05.

## Not yet inspected

- Individual work pages (`works/<citation_key>.html`) beyond the one Blake page above, and individual video pages (`videos/<id>.html`).
- Page indexing samples for the 210 not-indexed pages, to compare each exclusion bucket with the legitimate-exclusion list in the runbook (Step 3).

## Next

1. Remove the `sitemap-images.xml` entry in GSC Sitemaps (Step 1b).
2. From 2026-10-06, request indexing for selected work and video detail pages, spread across days for the quota. Indexable pages only: never the noindex `videos/` index or the redirect stubs.
3. Recheck Page indexing and the URL inspection results on or about 2026-10-12, then weekly for 2–4 weeks (to about 2026-11-02).
