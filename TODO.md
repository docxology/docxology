# Active Backlog

This is the hand-maintained backlog for unfinished work. Completed work remains
in `CHANGELOG.md`, `AGENTS.md`, release snapshots, and dated reports; it is not
repeated here.

Each item has a stable ID, priority, owner, trigger, deliverable, acceptance
criteria, and dependencies. Re-review this file before each public release.

- Status: active backlog
- Last reviewed: 2026-08-26 (public-main release-integrity review; deferred
  package migration remains staged behind a deployment-SHA-attested release)

## Completed / Closed (2026-08-01)

Implemented and verified (validated against source; the 231-test suite and the
affected orchestrators' `--check` gates pass):

Review-pass fixes:
- `code/orchestrators/submit_indexnow.py` — catch `URLError` (exit 1, no traceback).
- `code/orchestrators/ensure_social_meta.py` — HTML-escape injected og/twitter values.
- `code/orchestrators/build_evidence_page.py` — guard empty `claim["sources"]`.
- `code/orchestrators/build_catalog.py` — remove fabricated stale fallback counts
  (works/software are required inputs).
- `code/orchestrators/generate_feed.py` — guard non-numeric `year` in the sort key.
- `code/orchestrators/build_paper_pages.py` — fail loudly on per-work render errors.
- `code/orchestrators/migrate_inline_handlers.py` — correct the `data-nav-toggle` docstring.
- `code/orchestrators/generate_citation_cff.py` — YAML-escape title/version/names;
  grant the DAF ORCID only to Daniel Friedman.
- `code/src/youtube_fetcher.py` — reject impossible `upload_date` values.
- `GENERATED.md` — matrix rows for `build_reproducibility_ledger.py` and
  `fetch_work_authors.py`; relabel `deploy_seo_security.py`.
- `code/AGENTS.md` — stale "~20 orchestrators" → "~26".

Comprehensive follow-up pass:
- **SEC-001 (path traversal):** `add_zenodo_only.py` and
  `sync_paired_publications.py` now sanitize the Zenodo file `key` to its
  basename and verify the resolved target stays inside the paper folder
  (`_pdf_target` helper). + `code/tests/test_zenodo_pdf_safety.py` (4 tests).
- **Test-mock removal:** `youtube_fetcher.fetch_tab`/`fetch_channel` accept an
  injectable `runner`; `submit_bulk` accepts an injectable `opener`. Rewrote
  `test_youtube_fetcher.py` and `test_submit_indexnow.py` to use real injected
  fakes and to assert the constructed request — no `unittest.mock` left in the
  fetch/indexnow tests.
- **Tautological test:** `test_search_utils.py` now executes the real `esc()`
  through Node on concrete inputs (skips if node absent).
- **Negative-fixture coverage:** `test_seo_invariants.py` now proves
  `check_social_meta`, `check_work_descriptions`, `check_sitemap_policy`, and
  `check_paper_pages` each flag a constructed violation (tmp_path).
- **`errors="ignore"` → `errors="replace"`:** `fetch_video_transcripts.py`,
  `audit_publication_skills.py` (refresh_public_source_inventory already used
  replace/strict).
- **Stale dated-report fallbacks removed:** `build_catalog.py`,
  `build_evidence_page.py`, `build_generated_manifest.py`, `build_agent_index.py`,
  `build_search_index.py`, `export_agent_data.py` now fail cleanly when a report
  is missing instead of emitting a hardcoded 2026-05/06 path.
- **`export_agent_data.py`:** claim `sources` now cite the computed latest
  snapshot path (`_SNAPSHOT_SOURCE`) instead of a hardcoded 2026-06-09 file.
- **Hardcoded `dateModified`:** `build_evidence_page.py` and
  `build_exports_page.py` derive it from `data/current-counts.json` generated_at.
- **Misc robustness:** `build_video_pages.py` skips id-less records and makes
  `iso_date` safe; `verify_live_site.py` guards malformed `.get("datasets")` /
  `.get("items")` shapes; `build_image_sitemap.py` warns when the 1000-image cap
  truncates; `build_domain_pages.py` guards non-numeric `year` in the sort key.
- **Test brittleness:** `test_resume_data.py` asserts Scholar citations against
  `data/scholar-snapshot.json` instead of the hardcoded `777`.

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

### DOC-004 — Review ambiguous publication pairs

- Priority: P1
- Owner: ARCHIVIST / RESEARCHER
- Trigger: each public-source refresh; review in batches of 10–15
- Deliverable: record accept, reject, supersede, or defer decisions for every non-empty ambiguous queue in `data/paired-publication-decisions.json`
- Acceptance: no ambiguous candidate is auto-promoted; the latest report has zero unreviewed candidates or every candidate has a cited decision with release, DOI, evidence, and permanent citation-key outcome
- Dependencies: latest `reports/paired_publications_*.json`

### DOC-005 — Classify uncatalogued repositories

- Priority: P1
- Owner: INTEGRATOR
- Trigger: GitHub inventory refresh
- Deliverable: update `data/repository-classification.json` and promote only manually reviewed repositories into `pages/SOFTWARE.md`
- Acceptance: all uncatalogued repositories have ownership, fork/archive state, catalog role, exclusion reason, and review status
- Dependencies: `data/github-repositories.json`
- Remaining primary-review items (do not auto-promote): `ActiveInferenceInstitute/Active_Inference_Un0`, `docxology/GrowthModel`, `docxology/multi-time` (all `description_quality: missing`), and `docxology/math4wisdom-superhuman-docs-archive` (`substantive`, still needs a cited human decision). Forks stay `fork_not_curated`.

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

### DOC-014 — Stage the Python package migration after a green release

- Priority: P2
- Owner: MAINTAINER
- Trigger: a deployment-SHA-attested release has passed; do not combine with a release-integrity change
- Deliverable: migrate ad-hoc `sys.path` imports into a `docxology_tools` package with thin, backwards-compatible CLI wrappers on a dedicated follow-up branch
- Acceptance: every current CLI command remains callable, no runtime path mutation is required outside wrappers, full tests/validation/lint pass, and the migration has its own review and release evidence
- Dependencies: DOC-002 release attestation, generator-plan coverage, Python packaging decision

### SEC-002 — Re-run the managed-profile deep security scan

- Priority: P1
- Owner: MAINTAINER / SECURITY REVIEWER
- Trigger: the required managed filesystem permission profile becomes available; also before a security-sensitive release
- Deliverable: run `codex-security:deep-security-scan` against the clean candidate and record its scope, evidence, validated findings, and explicit limitations
- Acceptance: the scan has actually run under its required profile and every validated finding is fixed, deferred with an owner, or otherwise resolved; lack of the profile remains an explicit blocked state, never a pass
- Dependencies: managed filesystem permission profile, clean candidate checkout, `codex-security:deep-security-scan`

## Deferred leftovers

The 2026-08-01 review deferrals (domain-inference centralization, catalog test
pins, link-check/prune/feed, `export_agent_data` import-time IO) shipped on
2026-08-13. Stored paper domains were **not** rewritten: text-only re-inference
would reclassify 110 of 191 `metadata.json` files; bibliography remains the
catalog authority.

No further deferred code items from that review remain open. Intake still
blocked on DOC-004 (paired-publication `needs_review`) and the four DOC-005
primary deferrals above.
