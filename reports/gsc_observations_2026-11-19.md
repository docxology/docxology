# Search Console follow-up — 2026-11-19

Provenance: direct assistant inspection of the signed-in Search Console UI for
both URL-prefix properties (`https://danielarifriedman.com/` and
`https://www.danielarifriedman.com/`), plus direct HTTP probes of every listed
non-indexed example URL on 2026-11-19. Page-indexing data was last updated
**2026-11-15** with **All known pages** selected. This is a dated console
observation, not a release attestation. No durable screenshot receipt was
retained.

## Totals (apex property)

Indexed **2.39K**; not indexed **252** across six reasons:

| Reason | Pages | Disposition |
| --- | ---: | --- |
| Crawled – currently not indexed | 160 | Mostly machine files (76 `papers/*/full_text.md`, `data/*.json`, ops `.md`/`.txt`/`.xml`) plus 25 since-pruned `reports/*` files and `docs/REDIRECTS.md`, now 404. Expected under the open-crawl policy. 18 `works/*.html` samples; several (238, 111) are now indexed per URL Inspection. |
| Page with redirect | 30 | 28 `search.html?q=…` (search-page.js rewrites the query with `history.replaceState`) + `meditations.html` and `research.html` stubs. Expected; the `?q=` variants come from generated links (see follow-up). |
| Excluded by ‘noindex’ tag | 26 | 24 `papers/{folder}/` pages + `about.html` (×2 incl. `?ref=`). Expected by policy. |
| Alternate page with proper canonical | 11 | 10 `search.html?q=…` + `/index.html`. Expected. |
| Discovered – currently not indexed | 16 | All 200, `index, follow`, self-canonical, in sitemap. Validation previously **Passed**. Selective indexing requested (below). |
| Not found (404) | 9 | See below. |

### Not found (404) examples, live status 2026-11-19

| URL | Live | Note |
| --- | --- | --- |
| `works/Friedman2025CEREBRUMCaseEnabledReasoning118.html` | 200 stub → `…010` | Fixed (2026-11-01 stub live) |
| `works/Friedman2026CogSecSkillsMultiharnessCognitiveSecurity174.html` | 200 stub → `…AgenticSkills174` | Fixed |
| `works/Friedman2026LiteratureReviewArchitectureActive110.html` | 200 stub → `…LivingMetaAnalysisArchitecture110` | Fixed |
| `papers/2024_PopulationSearch/` | 200, noindex → `…034` | Fixed |
| `works/Friedman2023ATLASQuestionOrientedApproach049.html` | **404** | Retired duplicate of kept work 136; redirect stub added in this change |
| `works/Friedman2026TemplateApproachReproducibleGenerative193.html` | **404** | Retired duplicate of kept work 001; redirect stub added in this change |
| `reports/browser-smoke/2026-05-15/manifest.json` | 404 | Pruned by report retention |
| `reports/visual-qa/2026-05-15/manifest.json` | 404 | Pruned by report retention |
| `reports/browser-smoke/2026-05-13/manifest.json` | 404 | Pruned by report retention |

The three QA manifests were removed under
[report retention](../docs/operations/report-retention.md); nothing in the
current output links to them, and they are accepted as permanent 404s. They
need no stub. Once the two new work stubs are deployed and return 200 live,
the 404 bucket may be submitted for **Validate fix**; Google may report the
three manifests as still failing, which is expected for intentionally removed
files.

## `www` property

`https://www.danielarifriedman.com/` shows **0 indexed / 6 not indexed**. This is
correct: every `www` URL returns 301 to the apex. Breakdown: Page with redirect 3
(`/`, `/index.html`, `/?ref=…`), noindex 2 (`about.html`, `about.html?ref=…`),
404 1 (`/store/p1/Complexity.html`, a pre-site store URL; the matching artwork
now lives at `artworks/13746159173-complexity.html`).

## Sitemaps

- Apex: only `/sitemap.xml`, **Success**, last read 2026-11-19, 2,413 discovered.
- `www`: the retired `/sitemap-images.xml` (**Couldn't fetch**, last read
  2026-08-28) was still listed on the **www** property and was **removed** on
  2026-11-19. `/sitemap.xml` (Success, 2,412 discovered) remains there.

## URL Inspection and indexing requests (apex)

**Request indexing** was accepted (“URL was added to a priority crawl queue”) for:

- `start-here.html`, `blake-pathway.html`, `projections.html`,
  `domain-aii-ecosystem.html` (all Discovered – currently not indexed)
- `works/Friedman2026ActiveInferenceLanguageModel231.html`,
  `works/Friedman20262026ActiveInferenceSymposium237.html`,
  `works/Friedman2026RikishiReproducibleOperationAnalysis236.html`,
  `works/Friedman2026ActiveInferencePowerSuite199.html` (Discovered)
- `works/Friedman2023CommentOrNotComment063.html` (Crawled, last crawl 2026-06-10),
  `works/Friedman2026AGEINTAgenticIntelligence170.html` (Crawled, last crawl 2026-06-18)

Inspected and already **indexed** (no request): works 233 (resolves the
2026-11-05 open item), 238, 111.

URL Inspection reported **Referring page: None detected** for
`blake-pathway.html` and works 231/236/237; the checkout shows
`blake-pathway.html` linked from only one other HTML page.

No **Validate fix** was requested for any bucket: the redirect, noindex and
alternate buckets are intended exclusions, and the 404 bucket still had live
404s at inspection time.

## Other Search Console reports (apex)

- **Video indexing:** 1.18K videos indexed, 0 not indexed.
- **Enhancements:** Breadcrumbs (47 valid), Datasets (36), Profile page (1) and
  Videos (5) have no invalid items. Videos carries two non-critical
  "Improve item appearance" issues on 5 items each: `uploadDate` is missing a
  timezone, and invalid datetime value for `uploadDate`. Every video page
  emits a date-only `uploadDate` (for example `2026-10-06`) from
  `build_video_pages.py`; examples include `videos/institute-4zc0Eh23LmI.html`
  and `videos/personal-KGB3qrRIZhY.html`.
- **Ownership verification:** verified by the **HTML file**
  (`googlef0f1a1a4a7ba4be8.html`). The HTML-tag method is not in use; the
  homepage `google-site-verification` meta carried the file token name rather
  than a meta token and is removed in this change.

## Follow-up

Resolved in this change: redirect stubs for retired keys 049 and 193, the
QA-manifest disposition, and removal of the malformed verification meta.
Remaining work is tracked in
[issue 85](https://github.com/docxology/docxology/issues/85): de-linking
generated `search.html?q=` and `collections.html?add=` URLs, `/` instead of
`index.html` in the shared navigation, timezone-qualified video `uploadDate`,
internal links for new hubs, and thin work pages. After deployment, verify the
two new stubs live, then validate the 404 bucket. Recheck Page indexing around
2026-11-26.
