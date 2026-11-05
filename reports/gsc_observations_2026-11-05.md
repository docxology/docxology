# Search Console follow-up — 2026-11-05

Provenance: direct assistant inspection of the signed-in Search Console UI
for the URL-prefix property `https://danielarifriedman.com/`. This is a dated
console observation before the current candidate deployment, not an independent
live-byte audit, human approval or Scholar metrics observation. No durable
screenshot receipt was retained for this inspection.

## Sitemap and inspected canonical pages

Only `/sitemap.xml` was listed: **Success**, last read **2026-11-04**, with
2,406 discovered URLs. Its original submission date was 2026-07-21. No sitemap
resubmission or retired image-sitemap change was needed.

URL Inspection reported the following canonical work routes **unknown to
Google**, with no crawl recorded in the inspected UI:

- `works/Friedman2026BlakeanEntomologySmallLives233.html`
- `works/Friedman2026StatesChangeBlakeanFederalism234.html`
- `works/Friedman2026ObserversAreAllYou235.html`

One **Request indexing** attempt for work 233 failed. The UI reported a
submission problem and inability to connect to the reCAPTCHA service. No
accepted request was observed; no challenge was bypassed. The other two work
routes were inspected without submitting requests.

## Expected exclusions and remaining checks

`agent-verify.html` and `reports.html` were unknown to Google in the inspected
UI. `about.html` was excluded by its `noindex` tag; the UI showed a successful
2026-11-03 fetch and agreement on the homepage canonical. These redirect stubs
were not submitted for indexing.

No bulk **Validate fix** was requested. The three legacy work redirects and
their targets identified in [the November 1 observation](gsc_observations_2026-11-01.md)
still require exact live-route verification for the current deployment and
subsequent Google recrawl. Historical QA-manifest custody remains unresolved;
the entire 404 bucket must not be marked fixed on the basis of those routes.

After candidate deployment, verify the selected work/PDF routes and the three
legacy aliases directly. Retry selective indexing when Google's submission
service is available and monitor the console weekly. Search Console does not
establish Scholar inclusion or citation metrics. The authenticated Scholar
snapshot and its receipt remain unchanged.
