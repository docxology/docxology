# Active Backlog

This is the hand-maintained backlog for unfinished and recurring work. Completed
work belongs in [CHANGELOG.md](CHANGELOG.md), release snapshots, dated reports,
and [historical backlog notes](docs/operations/backlog-history.md).

Each item has a stable ID, priority, owner, trigger, deliverable, acceptance
criteria, and dependencies. Re-review this file before each public release.

- Status: active backlog
- Last reviewed: 2026-10-18; only unfinished work and recurring checks remain.
  Completed implementation and source-review history lives in CHANGELOG.md and
  the linked dated reports. Effort estimates below are separate from priority.

## Remaining work by effort

| Effort | Unfinished work | Main dependency |
| --- | --- | --- |
| Minor | Search Console cleanup and selected URL inspections; retry unavailable source queries | Signed-in owner access, public source availability |
| Medium | Named visual review and revision-bound release attestation; fresh authenticated Scholar observation; current-candidate Lighthouse review; Pages growth/retention consumer migration; Scholar pilot eligibility/projection review | Reviewer/access, measured candidate evidence, reviewed source/projection contract |
| Major | Deferred licensed full-text acquisition and originating-paper corrections; manuscript format inspection and editorial review; managed-profile security scan and finding disposition | Rights holders, depositors/authors, editorial decisions, required scan runtime |

The Scholar same-directory PDF gap now has a [budget-safe pilot proposal](reports/scholar_pdf_placement_proposal_2026-10-13.md)
preserving permanent URLs and the artifact limit. No files have been migrated;
eligibility review and a validated projection contract precede implementation.
Actual Scholar indexing remains unverified.
Recurring checks below are operating obligations, not unfinished feature work.

## P0 — Release and integrity

### DOC-002 — Release integrity and public artifact gate

- Priority: P0
- Owner: MAINTAINER
- Trigger: every release or Pages deployment
- Deliverable: run `regenerate_all.py --validate`, then verify the Pages artifact and live deployment before each release; a named human reviewer inspects the post-deploy desktop and mobile visual-QA captures and records the review (`visual_qa.py --approve-existing --reviewed-by <reviewer>`, see [accessibility-qa.md](docs/operations/accessibility-qa.md))
- Acceptance: source hashes, generator metadata, Pages file/byte counts, omitted-image policy, deployment metadata, fresh revision-bound browser/link/source/live evidence, and a deployment-SHA attestation that includes the human visual-review record are present; a second offline regeneration pass produces no content changes
- Dependencies: `regenerate_all.py`, Pages workflow, live verification
- Status (2026-10-05): the human visual review and the full release attestation
  are not done. The newest capture set (`reports/visual-qa/2026-10-05/`) records
  `review.status: pending`. Automated browser, smoke, and hosted-artifact
  receipts are separate evidence and stand in for neither; a release-ready claim
  waits for `validate_repo.py --release` with the deployment attestation
  ([release-integrity.md](docs/operations/release-integrity.md)).

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
- Open work: none in the reviewed queue; retain this as a refresh-triggered
  classification check, not a pending catalog addition.

### DOC-006 — Refresh external evidence and coverage exceptions

- Priority: P1
- Owner: RESEARCHER
- Trigger: monthly, before a claim-sensitive release, or when the weekly `freshness.yml` run opens or comments on the "Public-source freshness drift detected" issue (the reviewed baseline `reports/public_source_snapshot_2026-10-07.json` resolved #44; a later drift opens a new issue, which is closed by hand once a reviewed refresh is the committed baseline)
- Open work: review ResearchGate, SciProfiles, and PhilPeople when their access
  restrictions permit; repeat source refreshes on their declared triggers.
  Refresh Scholar only after a direct authenticated observation. A live Flickr
  refresh needs its approved API-key workflow.
- Latest check (2026-10-18): refreshed the live snapshot, paginated source
  inventory, complete GitHub inventory and full GitHub/Zenodo pairing scan.
  Publication and software decisions, archive boundaries and access limitations
  are recorded in [the refresh review](reports/publication_refresh_review_2026-10-16.json).
  The current [source review](reports/public_source_review_2026-10-18.md) keeps
  ambiguous historical release pairs and inaccessible profiles explicit.
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
- Open work: none from the reviewed migration; repeat only when official
  wording changes. Prior decisions remain in the claim ledger and dated review.

### DOC-016 — Finish paper-archive curation and registry judgment calls

- Priority: P1
- Owner: RESEARCHER / ARCHIVIST
- Trigger: next bibliography pass, or any per-paper review
- Deliverable: resolve the remaining source-access, registry, and originating-
  publication discrepancies with recorded evidence and explicit decisions
- Full-text acquisition is deferred. Retain the explicit source gaps for **#63** `2023_ToComment`,
  `2024_PaleolithicRockstars`, and `2026_FocusedAttentionMeditation`, then
  extract and summarize from those sources. Direct publisher/registry checks
  found no accessible licensed full text. Distribution copies remain unavailable;
  do not infer redistribution permission. Unsupported seed content has been
  cleared; the meditation chapter retains a labeled publisher synopsis.
- Authorship questions for **#29** SUMO and **#33** Digital Twins are resolved:
  retain Scott Ryan Maybell in the registered SUMO creators and R.J. Cordes
  as Digital Twins first author. The representative list is not inferred to
  be a byline. Current source-backed decisions are recorded in
  [the consistency review](reports/publication_consistency_review_2026-10-13.json);
  the earlier review remains historical evidence.
- Current-source review and corrections for all ten publication questions
  are recorded in [the consistency review](reports/publication_consistency_review_2026-10-13.json).
  [The corrected-source review](reports/publication_source_corrections_2026-10-19.json)
  records the active manuscript revisions, implementation fixes and validation
  limits. Current work and paper pages label the preserved historical summaries
  and link to immutable corrected source. Remaining evidence work concerns
  MarkdownDecisionProcess checkpoint,
  participant and statistical provenance; PopulationSearch's table-specific
  graph/run denominator; and MappingWilliamBlake's historical run membership.
  DopamineForaging is outside this revision scope; its published archive remains unchanged.
  Current compiler/test/source corrections do not establish broader scientific
  validity or revise archived PDFs. Any corrected archival publication needs
  a separately reviewed revision, followed by source-backed archive and summary
  updates. Native, installed and final-release acceptance remain governed by
  their originating repositories.
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
- Retained candidate review: commit `4b2af321e` reports performance 99 and
  130 ms blocking time for `art.html`; all eight sampled pages meet the
  aspirational category targets. The [exact-candidate review](reports/lighthouse_review_2026-10-17.json)
  retains source hashes, environment limits, and the measured 404 target-size
  follow-up. Re-measure after future growth; these observations do not establish
  universal scores. Prior fixture/parity repairs remain historical evidence in
  [the performance report](reports/lighthouse_gap_2026-10-06.md).

### DOC-010 — Security and SEO follow-up

- Priority: P1
- Owner: WEB DEVELOPER
- Trigger: every canonical, sitemap, CSP, iframe, or route-family change
- Deliverable: validate meta-policy limitations, CSP/URL/iframe/rel invariants, canonical and sitemap families, then record Search Console follow-up
- Acceptance: no inline handlers/scripts or unsafe schemes; approved YouTube origin only; every public family has canonical, metadata, schema, and sitemap policy coverage
- Dependencies: `seo_invariants.py`, `gsc_followup_preflight.py`, signed-in Search Console review
- Scholar planning: keep permanent URLs and the artifact ceiling. Review the
  [measured pilot proposal](reports/scholar_pdf_placement_proposal_2026-10-13.md)
  before any same-directory web projection; no copies have been applied. Metadata
  checks and the [prerequisite audit](reports/scholar_readiness.md) are implemented.
  Content/PDF eligibility and actual indexing still require separate review;
  see [scholar-inclusion.md](docs/seo/scholar-inclusion.md).
- Access: the owner's signed-in Search Console property was available on
  2026-10-05; observations are in
  [the dated report](reports/gsc_observations_2026-10-05.md) and the procedure
  in [gsc-followup.md](docs/seo/gsc-followup.md). Open Search Console actions:
  - Remove the retired `sitemap-images.xml` entry from the Sitemaps report. The
    file and its generator were retired on 2026-08-28 and the URL returns 404 by
    design; never recreate it to clear the entry.
  - From 2026-10-06, request indexing for selected indexable work and video
    detail pages, spread across days for the quota; never the noindex `videos/`
    index or redirect stubs.
  - Recheck Page indexing and the inspected URLs around 2026-10-12, then weekly
    through about 2026-11-02.

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

## P2 — Operating model

### DOC-013 — Keep runbooks and release checklist aligned

- Priority: P2
- Owner: MAINTAINER
- Trigger: any workflow or generator change
- Deliverable: maintain runbooks for intake, repository classification, CV release, Pages release, live verification, retention, claims, accessibility, and visual QA
- Acceptance: `AGENT_START.md`, `AGENTS.md`, `CLAUDE.md`, `docs/README.md`, `GENERATED.md`, and the release checklist point to the same ordered commands
- Dependencies: generated manifest and CI workflows

### DOC-017 — Manuscript rendering, references, and editorial review

- Priority: P2
- Owner: RESEARCHER / MAINTAINER
- Trigger: before any claim that the repository-methods draft is rendered, reviewed, or publication-ready
- Deliverable: inspect the requested rendered formats and their cross-references; obtain editorial and human visual review before publication
- Acceptance: a declared render command produces output whose figures and references have been inspected, changed bibliography entries pass a real-parser syntax check outside the structural gate, and a named editorial reviewer's decision is recorded; until then `validate_manuscript.py` is reported only as structural source validation
- Dependencies: `docs/manuscript/config.yaml`, `code/orchestrators/validate_manuscript.py`, [MANUSCRIPT_STATUS.md](docs/manuscript/MANUSCRIPT_STATUS.md)
- Open work: complete presentation-format inspection and named editorial/human approval.
  Native-template PDF rendering, bibliography checks, and an informative vector
  cover are implemented. Assistant inspection covered all eight PDF pages;
  automated and assistant checks remain separate from human approval.
  The pinned render command, real-parser checks, and CC BY 4.0 manuscript license
  are declared in [the manuscript guide](docs/manuscript/README.md); repeat
  verification whenever sources or rendering tools change.


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
