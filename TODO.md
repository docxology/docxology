# Active Backlog

This is the hand-maintained backlog for unfinished work. Completed work remains
in `CHANGELOG.md`, `AGENTS.md`, release snapshots, and dated reports; it is not
repeated here.

Each item has a stable ID, priority, owner, trigger, deliverable, acceptance
criteria, and dependencies. Re-review this file before each public release.

## P0 — Release and integrity

### DOC-001 — Close stale task-sync issues

- Priority: P0
- Owner: MAINTAINER
- Trigger: after the first verified public push following the July 2026 roadmap
- Deliverable: close or supersede GitHub issues #5, #6, and #7 with links to current counts, image-sitemap evidence, and the live verification report
- Acceptance: each issue is closed with an evidence comment; no stale 168/91, untracked-art, or unfinished-image-sitemap claim remains open
- Dependencies: current `reports/current_counts.md`, `reports/live_site_verification_*.json`, `sitemap-images.xml`

### DOC-002 — Release integrity and public artifact gate

- Priority: P0
- Owner: MAINTAINER
- Trigger: every release or Pages deployment
- Deliverable: regenerate `data/release-integrity.json` and `data/pages-artifact-manifest.json`
- Acceptance: source hashes, generator metadata, Pages file/byte counts, omitted-image policy, deployment metadata, and live verification are present; generated checks are clean
- Dependencies: `regenerate_all.py`, Pages workflow, live verification

### DOC-003 — Public privacy and claim safety

- Priority: P0
- Owner: MAINTAINER / RESEARCHER
- Trigger: every CV or evidence refresh
- Deliverable: keep public CV/source manifests free of local paths, secrets, unsafe URLs, and unsupported current claims
- Acceptance: `validate_repo.py` and the CV regression tests pass; uncertain, stealth, ongoing, and dated records retain their explicit status
- Dependencies: `code/src/public_integrity.py`, `resume/source.json`, `data/claims.json`

## P1 — Evidence, intake, and agent navigation

### DOC-004 — Review ambiguous publication pairs

- Priority: P1
- Owner: ARCHIVIST / RESEARCHER
- Trigger: each public-source refresh; review in batches of 10–15
- Deliverable: record accept, reject, supersede, or defer decisions for the current ambiguous queue in `data/paired-publication-decisions.json`
- Acceptance: no ambiguous candidate is auto-promoted; each decision cites the release, DOI, evidence, and permanent citation-key outcome
- Dependencies: latest `reports/paired_publications_*.json`

### DOC-005 — Classify uncatalogued repositories

- Priority: P1
- Owner: INTEGRATOR
- Trigger: GitHub inventory refresh
- Deliverable: update `data/repository-classification.json` and promote only manually reviewed repositories into `pages/SOFTWARE.md`
- Acceptance: all uncatalogued repositories have ownership, fork/archive state, catalog role, exclusion reason, and review status
- Dependencies: `data/github-repositories.json`

### DOC-006 — Refresh external evidence and coverage exceptions

- Priority: P1
- Owner: RESEARCHER
- Trigger: monthly or before a claim-sensitive release
- Deliverable: refresh ORCID, Crossref, Zenodo, PubMed, Europe PMC, GitHub, Scholar, organizational, teaching, art, and software evidence; review `data/coverage-exceptions.json`
- Acceptance: only verified metadata is applied, access dates and caveats remain visible, and current coverage is linked from agent and human discovery surfaces
- Dependencies: public-source APIs, primary profile pages, coverage report

### DOC-007 — Keep agent schemas and manifests current

- Priority: P1
- Owner: EDUCATOR / INTEGRATOR
- Trigger: any new public dataset or route
- Deliverable: update the versioned agent schema, examples, hashes, freshness guidance, Pages availability, fallbacks, and query recipes
- Acceptance: `data/agent-index.json` validates against the source datasets and all hosted/fallback URLs resolve locally
- Dependencies: generated manifest, Pages artifact manifest, count report

## P1 — CV, accessibility, UX, security, and SEO

### DOC-008 — Expand browser and progressive-enhancement QA

- Priority: P1
- Owner: WEB DEVELOPER
- Trigger: every interactive-layer or CSS change
- Deliverable: browser checks for no-JavaScript fallback, keyboard navigation, announcements, sorting/filter state, gallery/lightbox focus, reduced motion, forced colors, 320px widths, YouTube errors, console, and CSP
- Acceptance: the browser report records each scenario and passes at supported breakpoints; static accessibility remains green
- Dependencies: Playwright/browser runtime, `browser_smoke.py`, visual QA

### DOC-009 — Performance and asset budgets

- Priority: P1
- Owner: WEB DEVELOPER / MAINTAINER
- Trigger: monthly and after data or asset growth
- Deliverable: compact art/video indexes with detail loading, per-asset budgets, and Pages growth trend review
- Acceptance: current HTML, JS, JSON, hero, thumbnail, CV, and generated-data budgets are measured and remain below documented thresholds
- Dependencies: Pages artifact manifest, asset audit, browser QA

### DOC-010 — Security and SEO follow-up

- Priority: P1
- Owner: WEB DEVELOPER
- Trigger: every canonical, sitemap, CSP, iframe, or route-family change
- Deliverable: validate meta-policy limitations, CSP/URL/iframe/rel invariants, canonical and sitemap families, then record Search Console follow-up
- Acceptance: no inline handlers/scripts or unsafe schemes; approved YouTube origin only; every public family has canonical, metadata, schema, and sitemap policy coverage
- Dependencies: `seo_invariants.py`, `gsc_followup_preflight.py`, signed-in Search Console review

## P1 — Pages and repository growth

### DOC-011 — Maintain the bounded Pages projection

- Priority: P1
- Owner: MAINTAINER
- Trigger: every Pages deployment and monthly size review
- Deliverable: keep the repository as the complete archive and Pages as the bounded projection; omit only duplicated extracted paper-image binaries
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
