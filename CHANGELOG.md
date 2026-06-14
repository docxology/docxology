# Changelog

All notable public-index, website, bibliography, and discovery-layer changes are summarized here. The detailed operational record remains in `AGENTS.md`.

## 2026-06-14

- Added two Zenodo-only publications via `add_zenodo_only.py`: **DemoCreate** (`zenodo.20693217`, 💻) and **ENTO** (`zenodo.20647443`, 💻); added the **GeneralizedNotationNotation (GNN)** software v2.0.0 (`zenodo.20671741`, 🧠) as a distinct work from the 2023 GNN paper (different Zenodo concept). Bibliography **165→167**.
- Completed the CEREBRUM dedup the 2026-06-10 pass flagged for the maintainer: removed the duplicate work `…118` (papers/2025_CEREBRUM2, the v1.4 deposit `zenodo.15231156`) outright, keeping the primary `…010` (papers/2025_CEREBRUM, `zenodo.15170907`). Retired the now-empty `WORK_CANONICAL_OVERRIDES` entry and its regression test; re-pointed the CEREBRUM software-catalog entry to the surviving paper folder. Removed-work numbers are retired, not renumbered, so existing work-page URLs stay stable — `sync_publications_html.validate_rows` now allows numbering gaps (strictly-increasing instead of exactly-sequential).
- Re-pointed the template/ Reproducible Generative Research bibliography entry (row 1) to its latest release `zenodo.20669283` (v3.4.0).
- Reconciled all volatile-count surfaces to **167 works / 150 paper folders** (BIBLIOGRAPHY header + per-domain counts, papers/README, index.html, DISCOVERY, and the regenerated data/exports); count-consistency drift clean, 92 tests passing.
- Hardened work identity without a URL migration (FirstPrinciples/RedTeam scoping concluded slug/DOI URLs would cost 168 forever-stubs on a no-redirect static host). `build_work_pages.py` now fails loud on a duplicate `citation_key` (was silent last-write-wins page overwrite); new `test_frozen_work_keys.py` freezes every `num → citation_key` so a retitle that would churn a live URL fails CI; documented `works/{citation_key}.html` as a permanent opaque contract in the canonical policy.
- Modularized `docs/` from 7 flat files into topic subdirectories (`operations/`, `seo/`, `design/`, `security/`, `releases/`) with a new `docs/README.md` navigation index; updated all inbound references across code, agent entrypoints, and the search index. `docs/AGENTS.md` retained as agent operational guidance.

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
