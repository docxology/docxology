# Search Console follow-up — 2026-11-01

Provenance: direct assistant inspection of the signed-in Search Console UI for
the URL-prefix property `https://danielarifriedman.com/`, followed by direct
browser requests to the affected work URLs. This is a pre-deployment observation,
not a human visual approval or release attestation.

## Sitemap and report scope

- The Submitted sitemaps table contains only `/sitemap.xml`, with status
  **Success** and last read **2026-11-01**. The retired image sitemap is absent;
  no resubmission or removal was needed.
- Page indexing was inspected with **All known pages** selected. Its data was
  last updated **2026-10-22**; it does not establish current deployment status.
- No bulk validation or indexing request was submitted.

## Reported 404 examples

The following three work URLs returned HTTP 404 in the live browser check.
Compatibility redirects now map them to the existing canonical identities;
deployment and Google's subsequent recrawl remain separate checks.

| Historical key | Canonical work key |
| --- | --- |
| `Friedman2025CEREBRUMCaseEnabledReasoning118` | `Friedman2025CEREBRUMCaseEnabledReasoning010` |
| `Friedman2026CogSecSkillsMultiharnessCognitiveSecurity174` | `Friedman2026CogSecSkillsMultiharnessAgenticSkills174` |
| `Friedman2026LiteratureReviewArchitectureActive110` | `Friedman2026LivingMetaAnalysisArchitecture110` |

All paths above are under `works/` with an `.html` extension. Identifier 118
remains retired in the identity registry; the redirect does not create a
bibliography row or reuse that identifier. Only the canonical destinations
belong in the sitemap.

The reported `papers/2024_PopulationSearch/` example currently returns HTTP 200
and canonicalizes to work `Friedman2024EnhancingPopulationBasedSearch034`.
Google's older 404 observation does not describe that current response.

The bucket also lists three historical QA manifest paths:

- `reports/browser-smoke/2026-05-15/manifest.json`
- `reports/visual-qa/2026-05-15/manifest.json`
- `reports/browser-smoke/2026-05-13/manifest.json`

These paths are absent from the current checkout. Their original custody and
retention disposition were not established in this pass; no historical receipt
was recreated. Do not validate the entire 404 bucket as fixed on the strength
of the work redirects alone.

## Follow-up

After deployment, verify all three legacy routes and their canonical targets.
Recheck Google's delayed indexing report around 2026-11-02 and continue on the
runbook's weekly schedule. Request indexing only for selected indexable canonical
pages; redirect aliases and intentionally noindex pages remain excluded.
