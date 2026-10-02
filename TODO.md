# Active Backlog

This is the hand-maintained backlog for unfinished and recurring work. Completed
work belongs in [CHANGELOG.md](CHANGELOG.md), release snapshots, dated reports,
and [historical backlog notes](docs/operations/backlog-history.md).

Each item has a stable ID, priority, owner, trigger, deliverable, acceptance
criteria, and dependencies. Re-review this file before each public release.

- Status: active backlog
- Last reviewed: 2026-10-02; implementation progress and remaining evidence/access
  dependencies recorded separately from completed history.

## P0 — Release and integrity

### DOC-002 — Release integrity and public artifact gate

- Priority: P0
- Owner: MAINTAINER
- Trigger: every release or Pages deployment
- Deliverable: run `regenerate_all.py --validate`, then verify the Pages artifact and live deployment before each release
- Acceptance: source hashes, generator metadata, Pages file/byte counts, omitted-image policy, deployment metadata, fresh revision-bound browser/link/source/live evidence, and a deployment-SHA attestation are present; a second offline regeneration pass produces no content changes
- Dependencies: `regenerate_all.py`, Pages workflow, live verification

### DOC-003 — Public privacy and claim safety

- Priority: P0
- Owner: MAINTAINER / RESEARCHER
- Trigger: every CV or evidence refresh
- Deliverable: keep public CV/source manifests free of local paths, secrets, unsafe URLs, and unsupported current claims
- Acceptance: `validate_repo.py` and the CV regression tests pass; uncertain, stealth, ongoing, and dated records retain their explicit status
- Dependencies: `code/src/public_integrity.py`, `resume/source.json`, `data/claims.json`

## P1 — Evidence, intake, and agent navigation

### DOC-005 — Classify uncatalogued repositories

- Priority: P1
- Owner: INTEGRATOR
- Trigger: GitHub inventory refresh
- Deliverable: update `data/repository-classification.json` and promote only manually reviewed repositories into `pages/SOFTWARE.md`
- Acceptance: all uncatalogued repositories have ownership, fork/archive state, catalog role, exclusion reason, and review status
- Dependencies: `data/github-repositories.json`
- Review rule: standing-policy fork exclusions name their policy source;
  primary-repository promotion requires an individual source-backed decision.
  Review the current classification queue rather than relying on historical
  queue counts.

### DOC-006 — Refresh external evidence and coverage exceptions

- Priority: P1
- Owner: RESEARCHER
- Trigger: monthly or before a claim-sensitive release
- Deliverable: refresh ORCID, Crossref, Zenodo, PubMed, Europe PMC, GitHub, Scholar, organizational, teaching, art, and software evidence; review `data/coverage-exceptions.json`
- Acceptance: only verified metadata is applied, access dates and caveats remain visible, and current coverage is linked from agent and human discovery surfaces
- Dependencies: public-source APIs, primary profile pages, coverage report

### DOC-015 — Review moved AII governance and program claim values

- Priority: P1
- Owner: INTEGRATOR / EDUCATOR
- Trigger: official AII route migration or a public-source refresh that changes governance, advisory-board, or cohort wording
- Deliverable: record an applied, deferred, or rejected decision for every affected AII officer, board, advisory-board, and textbook-cohort claim before updating curated profile surfaces
- Acceptance: the dated evidence report and claim ledger identify the reviewed source, decision, owner, and rationale; approved edits regenerate dependent HTML, JSON, resume, and discovery outputs
- Dependencies: official AII governance/program pages, `reports/public_source_review_*.json`, `pages/EVIDENCE.md`, `data/claims.json`

### DOC-016 — Finish paper-archive curation and registry judgment calls

- Priority: P1
- Owner: RESEARCHER / ARCHIVIST
- Trigger: next bibliography pass, or any per-paper review
- Deliverable: resolve the remaining source-access, registry, and originating-
  publication discrepancies with recorded evidence and explicit decisions
- Status (2026-10-01): completed curation and keep/change decisions are in
  [the accuracy report](reports/bibliography_accuracy_2026-10-01.md).
  Current archive coverage follows [the generated snapshot](reports/current_counts.md).
  Permanent keys now come from `data/work-identifiers.json`; metadata corrections
  no longer require changing the public URL.
  Remaining:
- Acquire licensed full text for **#63** `2023_ToComment`,
  `2024_PaleolithicRockstars`, and `2026_FocusedAttentionMeditation`, then
  extract and summarize from those sources. Direct publisher/registry checks
  found no accessible licensed full text. Unsupported seed content has been
  cleared; the meditation chapter retains a labeled publisher synopsis.
- Remaining registry/document author discrepancies: **#33** Digital Twins
  (registry creator Cordes versus the document's organization/representative
  list), and **#29** Aligning AIO to SUMO (a registered concept-record creator
  does not appear on the title-page author list). Keep the registered creators
  pending depositor reconciliation; neither observation establishes a safe
  authorship change. Full-title corrections for #12, #26, and #74 and the
  publication-year correction for #159 were applied without changing URLs;
  see [the metadata decisions](reports/bibliography_metadata_review_2026-10-02.json).
- Content inconsistencies that the grounded summaries surfaced inside the
  papers themselves (for the author): CognitiveIntegrityFramework Part 2
  corpus size (950 vs 1,475), ConvergenceAnalysisGradient Discussion vs Table
  1, MarkdownDecisionProcess GPT-2 Medium vs Small, PopulationSearch graph
  counts, TemplateApproachReproducible "fourteen" vs "eleven", and
  DomainLanguageSpecifying six vs seven dimensions; DopamineForaging's
  reversed 113/160 transcript group assignments; FEPLean's aspirational vs
  runtime claims; Symergetics' 953 vs 757 tests; and MappingWilliamBlake's
  156 vs 162 works. Resolve in the originating publications, then update
  the archived versions and summaries with source evidence.
- Acceptance: each item has a recorded keep/change decision;
  `test_bibliography_authority.py` stays green
- Dependencies: `papers/*/full_text.md`, `data/work-authors.json`,
  `code/tests/fixtures/frozen-work-keys.json`

### DOC-007 — Keep agent schemas and manifests current

- Priority: P1
- Owner: EDUCATOR / INTEGRATOR
- Trigger: any new public dataset or route
- Deliverable: update the versioned agent schema, examples, hashes, freshness guidance, Pages availability, fallbacks, and query recipes
- Acceptance: `data/agent-index.json` validates against the source datasets and all hosted/fallback URLs resolve locally
- Dependencies: generated manifest, Pages artifact manifest, count report

## P1 — CV, accessibility, UX, security, and SEO

### DOC-008 — Maintain browser and progressive-enhancement QA

- Priority: P1
- Owner: WEB DEVELOPER
- Trigger: every interactive-layer or CSS change
- Deliverable: keep `browser_qa.py` and `browser_smoke.py` reports current for no-JavaScript fallback, keyboard navigation, announcements, sorting/filter state, gallery/lightbox focus, reduced motion, forced colors, 320px widths, YouTube policy, console, CSP, and visual output
- Acceptance: the latest browser QA report records each scenario and passes at supported breakpoints; known meta-CSP warnings are retained as warnings; static accessibility remains green
- Dependencies: Playwright/browser runtime, `browser_smoke.py`, `browser_qa.py`, visual QA

### DOC-009 — Performance and asset budgets

- Priority: P1
- Owner: WEB DEVELOPER / MAINTAINER
- Trigger: monthly and after data or asset growth
- Deliverable: retain compact artwork and video indexes with lazy detail loading, document per-asset budgets, and review Pages growth trends
- Acceptance: current HTML, JS, JSON, hero, thumbnail, CV, and generated-data budgets are measured and remain below documented thresholds; large interactive datasets do not load detail-only payloads before user need
- Dependencies: Pages artifact manifest, asset audit, browser QA
- Performance follow-up: use retained candidate-SHA Lighthouse diagnostics to
  improve pages below the aspirational performance 85, accessibility 95, and
  SEO 95 scores. Keep existing floors and measured results visible; passing
  the ratchet does not establish that every aspirational target was met.

### DOC-010 — Security and SEO follow-up

- Priority: P1
- Owner: WEB DEVELOPER
- Trigger: every canonical, sitemap, CSP, iframe, or route-family change
- Deliverable: validate meta-policy limitations, CSP/URL/iframe/rel invariants, canonical and sitemap families, then record Search Console follow-up
- Acceptance: no inline handlers/scripts or unsafe schemes; approved YouTube origin only; every public family has canonical, metadata, schema, and sitemap policy coverage
- Dependencies: `seo_invariants.py`, `gsc_followup_preflight.py`, signed-in Search Console review
- Access check (2026-10-02): the available signed-in browser has no accessible
  Search Console property for the domain; owner-granted property access is needed.
  No ownership, DNS, or account settings were changed.

## P1 — Pages and repository growth

### DOC-011 — Maintain the bounded Pages projection

- Priority: P1
- Owner: MAINTAINER
- Trigger: every Pages deployment and monthly size review
- Deliverable: keep the repository as the complete archive and Pages as the bounded projection; apply the declared projection policy for extracted images, QA screenshots, and superseded reports
- Acceptance: artifact remains below the safety ceiling, manifest preserves GitHub tree/raw fallbacks, and retention changes are recorded
- Dependencies: `build_pages_artifact.py`, `docs/operations/github-pages-artifact.md`

### DOC-012 — Retain historical reports deliberately

- Priority: P1
- Owner: MAINTAINER
- Trigger: quarterly report-size review or before deleting any QA/snapshot set
- Deliverable: apply current/archival/deletion retention tiers with provenance-preserving manifest entries
- Acceptance: current reports remain hosted/indexed; historical reports remain in GitHub or release archives; no evidence is deleted silently
- Dependencies: Pages growth report, release-integrity manifest

### ART-001 — Flickr-side metadata enrichment for artwork pages

- Priority: P1
- Owner: DAF (on Flickr) / WEB DEVELOPER (site-side re-sync)
- Trigger: after tagging/describing works on Flickr; re-run
  `sync_flickr_artworks.py` then the `artwork-pages` step
- Deliverable: Flickr records enriched so no artwork page is thin and every
  collection membership is tag-driven; site re-synced and rebuilt
- Acceptance: 0 thin (noindex) artwork pages hold; the 14 untagged records
  gain Flickr tags; *Solstice (Turning Point)* (55349041831) tagged (currently
  the only untagged record with a description) and joins a themed collection
- Dependencies: Flickr account edits (out of repo scope);
  `code/orchestrators/sync_flickr_artworks.py`; `pages/ART_COLLECTIONS.md`

## P2 — Operating model

### DOC-013 — Keep runbooks and release checklist aligned

- Priority: P2
- Owner: MAINTAINER
- Trigger: any workflow or generator change
- Deliverable: maintain runbooks for intake, repository classification, CV release, Pages release, live verification, retention, claims, accessibility, and visual QA
- Acceptance: `AGENT_START.md`, `AGENTS.md`, `CLAUDE.md`, `docs/README.md`, `GENERATED.md`, and the release checklist point to the same ordered commands
- Dependencies: generated manifest and CI workflows

### SEC-002 — Re-run the managed-profile deep security scan

- Priority: P1
- Owner: MAINTAINER / SECURITY REVIEWER
- Trigger: the required managed filesystem permission profile becomes available; also before a security-sensitive release
- Deliverable: run `codex-security:deep-security-scan` against the clean candidate and record its scope, evidence, validated findings, and explicit limitations
- Acceptance: the scan has actually run under its required profile and every validated finding is fixed, deferred with an owner, or otherwise resolved; lack of the profile remains an explicit blocked state, never a pass
- Dependencies: managed filesystem permission profile, clean candidate checkout, `codex-security:deep-security-scan`
- Status: a successful scan under the required permission profile is still
  needed. The prior runtime refusal produced no scan evidence; re-check the
  runtime prerequisite when this item is triggered.
