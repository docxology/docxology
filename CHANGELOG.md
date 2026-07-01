# Changelog

All notable public-index, website, bibliography, and discovery-layer changes are summarized here. The detailed operational record remains in `AGENTS.md`.

## 2026-07-01

- Massive metadata enrichment sweep: all 164 paper folders now have extended schema (domain, type, methods, key_findings, related_papers, checked_at) via `batch_enrich_metadata.py`. 44 previously-missing `metadata.json` files created, 119 existing ones extended with paper-specific content.
- Multi-agent triple audit completed: metadata completeness (164/164 pass), navigability (all SKILL.md cross-references valid, all bibliography rows linked), domain accuracy (0 discrepancies), HTML output quality (26 root pages + 183 work pages well-formed, JSON-LD valid), live site parity (14/14 checks pass, no drift).
- Quality improvement pass: replaced 3 placeholder key_findings, fixed 55 truncated findings with sentence-boundary extraction, replaced generic domain-template methods with paper-specific methods for 163 papers (e.g. "Uniparental marker haplotype analysis", "Lean 4 theorem proving", "CPRA legal analysis").
- Added `code/orchestrators/batch_enrich_metadata.py` (bulk metadata generation), `code/orchestrators/improve_metadata_quality.py` (paper-specific methods/findings), `code/src/paper_metadata_schema.py` (dataclass schema).
- Full `validate_repo.py --strict-reports` pipeline passes (30+ checks including browser smoke, accessibility, visual QA, live-site verification, sitemap, search index, external links).
- Added works **#180 "Sortition Upstream of NTQR"** (`zenodo.21083779`), **#181 "Exploratory Data Analysis: A Reproducible Notebook Template"** (`zenodo.21086292`), **#182 "A Domain Language for Specifying Controlled Methods"** (`zenodo.21086548`) — all 💻 Computational, with paper folders and full metadata.

## 2026-06-29

- Added work **#179 "Mapping William Blake's Works"** (`zenodo.21047573`, `docxology/blake` v0.1.0) via the canonical `sync_paired_publications.py --apply` path, plus benign `checked_at` metadata bumps on existing rows. Full local regenerate (works.json, exports, publications, work/domain/paper pages, resume, claims, catalog, search index, feed, sitemap, counts) and live-site snapshot refresh; `validate_repo` + pytest green. Also fixed 32 malformed bare-domain markdown links in `reports/publishing_status_megaindex.md`.

## 2026-06-27

- Added work **#178 "AlphaCOGANT: Recursive Corporate Self-Improvement as Active Inference"** (`zenodo.20976824`, `docxology/alphacogant` v1.0.1) with paper folder, PDF, and work page; updated "A template/ approach to Reproducible Generative Research" to Zenodo version v1.0.9. Regenerated the dependent layer and refreshed the live-site verification snapshot.
- `build_work_pages.py` now renders a **Platform availability card** on every canonical work page (Zenodo/GitHub/arXiv/OSF/HuggingFace/Software-Heritage/PyPI/site), driven by a new `data/publishing-status.json`; added `reports/publishing_status_megaindex.md`, a publishing-status mega-index across 272 items (works + software) with per-platform coverage and gaps. Began archiving origins to Software Heritage via anonymous Save Code Now.

## 2026-06-26

- Added works **#176 "A Living Meta-Analysis of the Modafinil Literature"** and **#177 "Refinement of Gold"** via the paired GitHub+Zenodo scan, with new paper folders (README/AGENTS/SKILL/CITATION.cff/metadata.json) and Zenodo PDFs; refreshed `checked_at` metadata on 27 existing paired works. Regenerated bibliography exports, publications/works/paper/domain pages, catalog, search index, feed, sitemap, resume, claims, evidence/reconciliation, and current counts; live-site snapshot refreshed.

## 2026-06-24

- Added work **#175 "Realizing Emptiness: Operational Surrogates for No-Self-Evidence, QRF Opacification, and Bayesian Model Reduction"** (`zenodo.20834846`, `docxology/realizing_emptiness` v1.0.0) via `sync_paired_publications.py --apply`; refreshed `checked_at` metadata and software links for 25 existing works; fixed the `pages/BIBLIOGRAPHY.md` paper-folder prose count (156→157).
- Added `code/orchestrators/regenerate_all.py`: a single-command, dependency-ordered, local-only write-mode counterpart to `validate_repo.py`'s `--check` sequence (manifest last), replacing manual whack-a-mole after a publication-sync apply. `refresh_bibliography_counts` now also keeps the "**N** indexed paper folders" prose current. `validate_repo.py` now runs `sync_scholar_metrics.py --check`, catching Scholar-metric drift across README/BIBLIOGRAPHY/PROFILE/LINKS/DISCOVERY (previously unguarded).
- Pruned superseded dated QA screenshot sets under `reports/visual-qa` and `reports/browser-smoke` (validation only reads the latest); `reports/` 100 MB → 40 MB. `add_zenodo_only.py` now runs `regenerate_all.py` automatically after adding records.
- Softened unguarded external/domain prose counts that would drift as external repos grow (codomyrmex module counts, COGSEC bio paper/book counts); fixed `regenerate_all.py`'s report-producer ordering so write-mode indexes don't go stale relative to the dated reports they link.

## 2026-06-22

- Synced the **CogSecSkills** publication (`zenodo.20804585`, 💻) and hardened publication intake.

## 2026-06-21

- Added two Zenodo publications: **Template Madlib** (`zenodo.20786638`, 💻) — `docxology/template_madlib`, deterministic token injection for conditional IMRAD manuscripts — as work **172**, and **California Public Records** (`zenodo.20789899`, 🛡️) — a technical and legal reference for the post-AB 473 era — as work **173**. Downloaded both PDFs, generated work/paper pages, and registered `papers/README.md` entries. Bibliography **170→172**; paper folders **153→155**. Also added the previously-missing **COGANT-0.6.0.pdf** and removed a duplicate On-Policy Distillation folder.
- Repo-wide **Zenodo DOI concept-consistency** pass: switched **70** bibliography rows (plus the 4 newest works and the `itrace` / `ntqr_llm` / `on_policy_distillation` software-catalog links) from per-version DOIs to their **concept DOIs**, each verified against the Zenodo API `conceptdoi` field so the citation always resolves to the latest version. Deliberately excluded version-distinct works that share a single concept DOI (e.g. the AII Ecosystem v1/v2/v3 snapshots) to avoid duplicate DOIs.
- Added **AGEINT** (`docxology/AGEINT`) and **template_madlib** (`docxology/template_madlib`) to the software catalog: docxology owned **58→60**, Grand Total **92→94** (Education 5→6, Developer Tools 15→16); recomputed the GitHub-inventory curated split.
- Fixes: `sync_publications_html.py` now patches `twitter:image:alt` with the live work count (was stale at 170); removed a doubled "Abstract" heading and added the MIT `license` field in the On-Policy Distillation paper folder; reconciled that folder's metadata to its concept DOI.
- Design/a11y pass: reconciled `design-system.md` to the actual `style.css` (corrected background/radius/body-font/focus-color tokens, documented previously-missing tokens); added mobile-menu `aria-expanded` toggling, ESC-to-close, and a 44px WCAG touch target across all 20 nav pages and their generators; fixed heading-hierarchy skips (h1→h3/h2→h4) on domain and index pages; added `aria-label`s to 3 unlabelled search inputs; tokenized 26 hardcoded gold `rgba()` values into 14 `--gold-NN` tokens (no visual change); `accessibility_audit.py` now enforces single-h1, no-heading-skips, and form-control-labels (22/22 pages pass).
- Migrated the site body font from Georgia serif to **Inter** to match the design system (Playfair Display headings unchanged); centralized the duplicated menu-ESC handler into `site_nav.MENU_ESC_SCRIPT`; removed 26 lines of verified-dead CSS (duplicate footer block, zero-reference selectors) after confirming the two-layer base+newspaper override structure is intentional, not duplication.

## 2026-06-17

- Added **AGEINT: Agentic Intelligence** (`zenodo.20732275`, 💻) — `docxology/AGEINT` v0.1.0, a Synthetic Analytic Tradecraft curriculum-and-assurance atlas — as work **170** via the canonical `sync_paired_publications.py` apply path, scoped `--since 2026-06-16` to isolate the single new release. Stripped the `<p>` HTML the Zenodo abstract carried into `metadata.json`/`README.md`; renumbered the `papers/README.md` index strictly **1..152** (closed the gap at 111 left by the CEREBRUM dedup, plus a duplicate `152`). Regenerated all dependent surfaces. Bibliography **168→169**; paper folders **151→152**; software unchanged at **91**; Computational domain **27→28**. Identified **CEREBRUM** (`zenodo.15231156`) and **Self-Improvement Agent Harness** (`zenodo.20693012`) as re-versions of existing works `…010` / `…127` (newer version DOIs of already-curated concepts) — update-only, not new rows.

## 2026-06-15

- Completed **COGANT** (`zenodo.20705351`, 💻) and **coasys** / **COGANT** software-catalog intake after commit `b6fa1b4`: added `2026_COGANT` to `papers/README.md` (151 folders), `paper_metadata.json`, and the Computational domain blurb (27 works); regenerated publications, software, sitemap, resume, evidence, search, feed, domain, and count exports. Bibliography **167→168**; software catalog **89→91** (58 owned + 33 AII); paper folders **150→151**.

## 2026-06-14

- Added two Zenodo-only publications via `add_zenodo_only.py`: **DemoCreate** (`zenodo.20693217`, 💻) and **ENTO** (`zenodo.20647443`, 💻); added the **GeneralizedNotationNotation (GNN)** software v2.0.0 (`zenodo.20671741`, 🧠) as a distinct work from the 2023 GNN paper (different Zenodo concept). Bibliography **165→167**.
- Completed the CEREBRUM dedup the 2026-06-10 pass flagged for the maintainer: removed the duplicate work `…118` (papers/2025_CEREBRUM2, the v1.4 deposit `zenodo.15231156`) outright, keeping the primary `…010` (papers/2025_CEREBRUM, `zenodo.15170907`). Retired the now-empty `WORK_CANONICAL_OVERRIDES` entry and its regression test; re-pointed the CEREBRUM software-catalog entry to the surviving paper folder. Removed-work numbers are retired, not renumbered, so existing work-page URLs stay stable — `sync_publications_html.validate_rows` now allows numbering gaps (strictly-increasing instead of exactly-sequential).
- Re-pointed the template/ Reproducible Generative Research bibliography entry (row 1) to its latest release `zenodo.20669283` (v3.4.0).
- Reconciled all volatile-count surfaces to **167 works / 150 paper folders** (BIBLIOGRAPHY header + per-domain counts, papers/README, index.html, DISCOVERY, and the regenerated data/exports); count-consistency drift clean, 92 tests passing.
- Hardened work identity without a URL migration (FirstPrinciples/RedTeam scoping concluded slug/DOI URLs would cost 168 forever-stubs on a no-redirect static host). `build_work_pages.py` now fails loud on a duplicate `citation_key` (was silent last-write-wins page overwrite); new `test_frozen_work_keys.py` freezes every `num → citation_key` so a retitle that would churn a live URL fails CI; documented `works/{citation_key}.html` as a permanent opaque contract in the canonical policy.
- Modularized `docs/` from 7 flat files into topic subdirectories (`operations/`, `seo/`, `design/`, `security/`, `releases/`) with a new `docs/README.md` navigation index; updated all inbound references across code, agent entrypoints, and the search index. `docs/AGENTS.md` retained as agent operational guidance.
- Documentation/signpost accuracy pass: reconciled five hand-maintained narrative pages (`LINKS`, `PROFILE`, `WIKIPEDIA`, `COLLABORATORS`, `MEDIA`) that had silently drifted to 125/154-work counts → **167**, and added them to `count_consistency` so they can no longer rot. Linked the new `docs/README.md` index from `README.md`, `AGENT_START.md`, and `llms.txt`; documented `data/works.json` as the canonical works registry and the `security.txt`/warrant-canary status under `docs/security/`.

## 2026-06-10

- SEO/discoverability pass. Fixed work-page meta descriptions that were hard-cut mid-word: `build_work_pages.py` now clips on a word boundary with an ellipsis via new `clip_description()` in `code/src/site_nav.py` (145 of 165 work descriptions corrected; rendered length ≤160).
- Added Twitter Card (`summary_large_image`) and `og:image:alt` tags site-wide. Generators (`build_work_pages`, `build_domain_pages`, `build_catalog`, `build_exports_page`, `build_evidence_page`, `build_updates_page`, `build_github_inventory`) emit them; hand-maintained pages (index, publications, art, videos, collaborators, search, discovery, cite-verify, media, software) are covered by a new idempotent `code/orchestrators/ensure_social_meta.py`.
- Added the sixth research-domain landing page `domain-biomedicine.html` (Genetics & Biomedicine, 🧬, 15 works) with `og-biomedicine.jpg`; added to `sitemap_policy.py`; relinked the homepage card from a raw `pages/BIBLIOGRAPHY.md#…` anchor to the new page.
- Polished homepage: removed duplicate `theme-color` and standardized to `#0c0c0e` (matches manifest); tightened the meta/og description to 153 chars; added word separators between publication-card title/venue/citation spans so text extractors and screen readers no longer read them run-together.
- New SEO invariants in `code/src/seo_invariants.py` (`check_social_meta`, `check_work_descriptions`) with tests in `test_seo_invariants.py` and `test_site_nav.py`; full suite 88 passing.
- Deep-scan follow-ups: work-page fallback meta descriptions now include the title (eliminated 17 duplicate/templated descriptions across same-type works; 162/165 work descriptions now unique). Enriched `ScholarlyArticle.author` JSON-LD with inline `@type`/`name`/`url` (not just a cross-document `@id`) so search engines reliably attribute authorship for rich results. Applied the same word-boundary `clip_description()` to `build_paper_pages.py` (148 paper-folder pages no longer truncate mid-word). Verified site-wide: 373 JSON-LD blocks all valid, full image-alt coverage (incl. the JS-rendered art gallery via `artAlt()`), no broken internal links.
- Reviewed Google Search Console (3-month window): 74 clicks / 3.25K impressions / 2.3% CTR / avg position 9; 118 indexed vs 111 not (43 "crawled-not-indexed" + 50 "discovered-not-indexed" thin/templated work pages — the description/author fixes target these). Confirmed the lone "Not found (404)" (`papers/2024_PopulationSearch/`) is stale (crawled before publish; now live, noindex, canonicalized). Findings + roadmap recorded in `reports/seo-discoverability-audit-2026-06-10.md`.
- Added a Google image sitemap (`sitemap-images.xml`, new `build_image_sitemap.py`) declaring 942 gallery artworks for Google Images discovery — preferring the same-domain `/art/*.jpg` copies (939) over Flickr, since `art.html` renders client-side and the images are otherwise invisible to crawlers. Registered in `robots.txt`; well-formedness + freshness covered by `test_build_image_sitemap.py`.
- Deduplicated the CEREBRUM pair: work `…118` (papers/2025_CEREBRUM2, the v1.4 deposit) now sets `rel=canonical` + `og:url` to the primary entry `…010` (papers/2025_CEREBRUM), consolidating ranking signals for the same paper. Added a shared `WORK_CANONICAL_OVERRIDES`/`canonical_work_key` in `code/src/site_nav.py`, used by both the work-page generator and the `check_work_pages` invariant, with a regression test.
- Corrected three mis-attributed paper abstracts (source READMEs had the wrong paper's text), sourced from authoritative records: `2023_HoneyBeeGeneExpression` (Zenodo TSGE meta-analysis abstract), `2023_AII_v1` (AII overview, recovered from the file's own schema block — the body had TrustFinder text), and `2023_ToComment` (a *Physics of Life Reviews* commentary on Manrique & Walker's "To copy or not to copy?", per Semantic Scholar — not the digital-memes text it carried). All 165 work-page meta descriptions are now unique. Confirmed `www`→apex 301 redirect and self-canonical (no duplicate-content split). Flagged: works `…010`/`…118` are the same CEREBRUM paper (DOI `zenodo.15170907` resolves to `15231156`, v1.4) — a bibliography dedup/curation decision left to the maintainer.

## 2026-06-04

- Applied four strong GitHub release + Zenodo publication pairs: `2026_DeterministicTestbedSelf`, `2026_RecoveringLLMPersona`, `2026_Triplicate`, and `2026_TemplateTextbook`; bibliography **150→154**, paper folders **143→147**.
- Refreshed represented GitHub/Zenodo publication pairs for existing works, including `WhenDoBugs`, `MusicNeverStopped`, `BeeStack`, `BiologyTextbook`, `CrescentCity`, and template-derived exemplars; left review-only pairings untouched.
- Added six owned repositories to the curated software catalog (`template_autoscientists`, `template_newspaper`, `template_textbook`, `ntqr_llm`, `grateful_data`, `cohereants`); software catalog **50→56 owned**, **82→88 total**.
- Recorded June 4 public API counts: docxology GitHub **305** public repositories, AII **51**, Zenodo exact-name **40**, Zenodo ORCID-linked **98**; treated `docxology/template` DOI [10.5281/zenodo.20469500](https://doi.org/10.5281/zenodo.20469500) as software/version metadata, not a bibliography work row.
- Expanded volatile-count validation across README, AGENTS files, BIBLIOGRAPHY summaries, Discovery, `llms.txt`, software JSON/LD, and GitHub inventory counts.

## 2026-05-26

- Thermo-nuclear documentation pass: aligned volatile counts (116 works / 109 paper folders) across `llms.txt`, release notes, and publications head meta; added count-consistency validation (`code/src/count_consistency.py`).
- Refactored `publications.html` to load catalog rows from `data/works.json` via `js/publications.js`; externalized CollectionPage JSON-LD to `data/publications-ld.json` (166-line shell).
- Added `docs/SECURITY.md`, `docs/DESIGN_SYSTEM.md`, `reports/web_assessment_2026-05-26.md`, shared nav (`code/src/site_nav.py`) on work and domain pages; removed Inter from body typography in favor of system-ui stack.
- Added `2026_BiologyTextbook` — *Introduction to Biology: A Generative Approach* (DOI [10.5281/zenodo.20286478](https://doi.org/10.5281/zenodo.20286478); repo `docxology/biology_textbook`); bibliography **116→117**; paper folders **109→110**; Computational domain **7→8**; Books **3→4**.
- Added `papers/software_table.py` and `papers/sync_software_html.py`: full 82-row software catalog sync from `pages/SOFTWARE.md` to `software.html` + `data/software-ld.json`; fixed SOFTWARE.md subtotal **49→50**; `biology_textbook` on software surface; work-page source-repo links from `metadata.json`.

## 2026-05-19

- Added `2026_CrescentCity` — *Crescent City in Living Waves: Space, Time, People, and Minds on the Southern Cascadian Coast* (DOI [10.5281/zenodo.20286171](https://doi.org/10.5281/zenodo.20286171); repo `docxology/crescent_city`), filed under 🛡️ Cognitive Security.
- Created the per-paper documentation set: `README.md`, `AGENTS.md`, `SKILL.md`, `CITATION.cff`, and `metadata.json`.
- Registered the work in `papers/paper_metadata.json`, the `papers/README.md` index, and `papers/AGENTS.md` (counts + maintenance log + domain coverage).
- Added bibliography table row 116 in `pages/BIBLIOGRAPHY.md` and the 🛡️ Cognitive Security domain index; regenerated `data/works.json` and bibliography exports via `export_bibliography.py`.
- Resynced `publications.html` PUBS + JSON-LD `mainEntity` and regenerated downstream artifacts (search index, domain/work/catalog pages, evidence, feed, sitemap, updates).
- Updated current counts to 116 curated works, 109 per-paper folders at the latest check.

## 2026-05-13

- Added machine-readable discovery artifacts: `llms.txt`, `CITATION.cff`, `codemeta.json`, bibliography exports, and structured `data/*.json`.
- Added domain landing pages, per-work landing pages, a generated search index, and an RSS feed.
- Added `search.html`, `opensearch.xml`, `catalog.html`, `data/catalog.json`, `GENERATED.md`, and `data/generated-manifest.json` for human search, browser discovery, dataset discovery, and generated-file rebuild provenance.
- Enriched generated work pages and the search index with abstracts, keywords, methods, and findings extracted from per-paper README/SKILL files.
- Added scoped external-link reporting plus a weekly freshness workflow, Dependabot, tighter workflow permissions, and workflow concurrency controls.
- Added `updates.html`, `AGENT_START.md`, `humans.txt`, `.well-known/security.txt`, external-link triage, live-site verification, asset-size audit, and selector-based browser smoke reporting.
- Expanded per-work JSON-LD with citation text, DOI identifiers, keywords, documentation links, and structured publisher/about fields.
- Added citation and evidence pages with claim confidence, caveats, maintenance ownership, and public-source reconciliation.
- Added fresh Open Graph images for the homepage, major sections, and research domains.
- Added source-refresh, bibliography export, software export, work-page, evidence, sitemap, reconciliation, accessibility, and visual-QA orchestrators.
- Added GitHub Actions validation for generated files, local links, JSON-LD, sitemap targets, and the Python test suite.
- Updated current counts to 115 curated works, 108 per-paper folders, 48 owned software repositories, 32 AII catalogued contributions, and 286 public docxology GitHub repositories at the latest API check.

## 2026-05-12

- Performed repo-wide README and AGENTS audit.
- Updated public GitHub repository count and domain figures from bibliography ground truth.
- Verified public-source discrepancies around Google Scholar cache, AII officers, board size, and Scientific Advisory Board context.

## 2026-05-04

- Renamed paper folders from author-title form to `YYYY_Topic`.
- Added `2020_FacilitatorsCatechism`.
- Added shared bibliography-table parser and publication HTML synchronization script.
