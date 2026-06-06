# Changelog

All notable public-index, website, bibliography, and discovery-layer changes are summarized here. The detailed operational record remains in `AGENTS.md`.

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
