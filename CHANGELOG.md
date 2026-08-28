# Changelog

All notable public-index, website, bibliography, and discovery-layer changes are summarized here. The detailed operational record is on demand in [`docs/operations/maintenance-log.md`](docs/operations/maintenance-log.md); machine-readable evidence remains in dated `reports/` snapshots.

## 2026-08-26

- **Release-blocking link repair:** corrected the canonical Science DOI for *Defining events: 2020 in hindsight*, removed three verified-dead AII software aliases rather than inventing replacement ownership, and migrated moved AII governance/program links to their live canonical routes.
- **Bounded link-gate coverage:** external-link validation now scans every root-level public HTML route, while excluding only URLs used as CSP source expressions; real YouTube embed paths remain in scope. This exposed and corrected three additional generated domain/pillar links before publication.
- **Review discipline:** current AII governance, advisory-board, and textbook-program wording remains explicitly queued for human review rather than silently changing time-sensitive profile claims.
- **Post-deploy evidence boundary:** external-link triage is now recognized as a narrowly date-stamped post-deploy derivative only after its deterministic check matches the refreshed link report; malformed and unrelated report paths remain release-blocking source drift. Deterministic source renderers now resolve dated reports from Git-tracked source only, and the Pages manifest rejects dirty tracked post-deploy receipts, so temporary evidence cannot make a committed artifact pass locally but fail in a clean checkout.

## 2026-08-25

- **Public-main release-integrity controls:** established a source-payload versus control-tail provenance model so deterministic manifests, artifact budgets, and review records can be checked without masking source drift. Publication, software, paper-document, pillar-page, redirect, and generation-plan checks now fail on stale source-rendered output.
- **Release deployment gate:** GitHub Pages now runs the repository validator, full test suite, and pinned W605 Ruff gate before it assembles or deploys the bounded artifact. A release-ready claim remains blocked until the deployed SHA has fresh browser/link/live evidence and a post-deploy attestation.
- **Source visibility and JSON-LD:** bibliography projections now use Git-tracked/non-ignored source visibility rather than machine-local derived files; publication and software CollectionPage JSON-LD replacement now shares one output-preserving renderer.
- **Scholar provenance:** added `data/scholar-verification-receipt.json`, a SHA-256-bound baseline record for the existing 2026-06-09 direct logged-in snapshot. Any future snapshot edit invalidates the receipt and makes `sync_scholar_metrics.py --check` fail until a new direct-authenticated observation is reviewed and recorded; no Scholar metrics were changed in this release work.
- **Artifact and generated-write reliability:** Pages retains provenance for omitted visual QA image binaries while enforcing its 900 MiB ceiling, and real-filesystem tests cover late hard-link aliases during atomic generated-output replacement.

## 2026-08-17

- **Publication Intake — docxplus (#212):**
  - Cataloged new Zenodo publication record `21985580` (concept DOI `10.5281/zenodo.21983948`, version DOI `10.5281/zenodo.21985580`): *docxplus — the Intelligent Document Container*.
  - Added paper documentation folder `papers/2026_DocxplusIntelligentDocument/` with full metadata, skill, and extracted text representations.
  - Updated active cataloged bibliography works count to **209** (212 work rows across 192 indexed paper folders).
  - Regenerated all 40 local surfaces, search indices, sitemaps, JSON-LD structured data, and release integrity manifests.

## 2026-08-14

- **SEO/GEO Optimization Pass & Technical Defects Resolved:**
  - **Hreflang elimination**: Removed non-self-referential alternate links pointing 1,563 pages at the homepage from  () and .
  - **noindex + cross-canonical consolidation**: Removed conflicting  directives from paper pages and , keeping clean  consolidation to  landing pages.
  - **Video title disambiguation**: Implemented series/lecture token preservation in , eliminating all 30 duplicate  collision groups across 1,127 video pages.
  - **Work page title bounding**: Bounded all work landing page  lengths to $\le 70$ characters on clean word boundaries.
  - **Schema & Entity hygiene**: Fixed  to point to , enriched  with LinkedIn/YouTube/Bluesky, and deduplicated the  Organization node in .
  - **Service Worker optimization**: Removed the 1.7MB  from  pre-caching in  to protect offline installation while keeping lazy network-first search indexing.
  - **Static SSR for publications table**: Enhanced  to statically emit all 206 publication  elements into  at build time for AI crawler indexing (GPTBot, ClaudeBot, PerplexityBot).
  - **Video index equity**: Consolidated search equity by pointing  canonical to .
  - **Scholarly citation graph**: Enriched  structured data across all work pages with  and  metadata.
- **Pillar Content & Generative Engine Optimization (GEO):**
  - **5 Hand-crafted pillar research explainers authored**:
    - : "What Is Cognitive Security? Theory, Threat Models, and Multi-Agent Defense" (~2,200 words,  +  JSON-LD).
    - : "Computational Entomology: Algorithms, Models, and Digital Insect Colonies" (~2,100 words,  +  JSON-LD).
    - : "Insect Cognition & Collective Intelligence: How Ant Colonies Think Without a Brain" (~2,100 words,  +  JSON-LD).
    - : "Active Inference & The Free Energy Principle: A Practical Tutorial" (~2,500 words,  +  JSON-LD).
    - : "Neurosymbolic AI & Active Inference: Bridging Symbolic Reasoning and Generative Agents" (~2,200 words,  +  JSON-LD).
  - **GEO & AI Agent Provenance Layer**: Thickened  with verifiable agent provenance principles and a GEO architecture case study.
  - **Site-wide editorial wiring**: Added dedicated Research Guides section to , wired learning pathways in , registered routes in , , , and , and generated dedicated Open Graph cards in .

## 2026-08-13

- **DOC-005:** promoted three paper-paired Active Inference Institute repositories into `pages/SOFTWARE.md` after they gained descriptions: `Active_Fedference` (paper `2026_RobustBeliefSharing`), `Active_Skillference` (paper `2026_ActiveSkillference`), and `active_inference_power` (paper `2026_ActiveInferencePower`). AII catalogued 38→**41**; curated software total 143→**146**. Left as explicit deferrals (description-less or not auto-promoted): `Active_Inference_Un0`, `docxology/GrowthModel`, `docxology/multi-time`, and `docxology/math4wisdom-superhuman-docs-archive`. Forks were not auto-promoted.
- **Domain inference centralized** into `code/src/domain_inference.py` (whole-word matching; computational before entomology). `add_zenodo_only.py`, `batch_enrich_metadata.py`, `regenerate_docs.py`, and `publication_pairing.py` now delegate. A metadata/bibliography diff showed text-only re-inference would reclassify 110 stored domains; **no `papers/*/metadata.json` or `pages/BIBLIOGRAPHY.md` rewrites were accepted**.
- **Review/CI/CSP:** repository inventory pages load `/js/repo-inventory.js` instead of inline filter JS (CSP `script-src 'self'`); `--check-manifest` no longer requires an unwritten today's growth report; Pages deploy no longer cancels in-progress jobs; `live-verify.yml` and `indexnow-on-push.yml` run after a successful Pages deploy; Action bumps `checkout@v7`, `setup-python@v7`, `configure-pages@v6`, `deploy-pages@v5`.
- **Robustness backlog:** shared `esc()` from `js/search-utils.js`; TTS panel `aria-hidden` tracks open state; `?` keyboard shortcut works; `check_external_links.py` URL accounting and tab stripping; `prune_old_reports.py` scans the working tree; feed site-updates moved to `data/site-updates.json`; `export_agent_data.py` import is IO-free; brittle catalog pins replaced with structure/count assertions; `add_zenodo_only.render_citation` YAML-quotes version and names; `regenerate_all.py` re-runs `sync_site_facts.py` after the second accessibility audit.
- Live-site snapshot refreshed: 12/17 markers passing with deployment pending until this commit is on Pages.

## 2026-08-10

- **Two new Zenodo software publications catalogued** with full paper-folder documentation (README/AGENTS/SKILL/CITATION.cff/metadata.json + PDF) and regenerated bibliography, exports, work pages, domain pages, catalog, feed, sitemap, resume, accessibility, and Pages-manifest surfaces (works 206→**208**):
  - **#210** Robust Belief Sharing in Federated Active Inference: A Recovery-Tested Generalized-Variational Framework for Categorical Contamination-Aware Consensus (🧠, concept DOI `zenodo.21864003`; source repository [`ActiveInferenceInstitute/active_fedference`](https://github.com/ActiveInferenceInstitute/active_fedference)).
  - **#211** Active Skillference: A Validated Prerequisite Graph, Computational Claim Registry, and SkillTree Delivery Contract (🧠, concept DOI `zenodo.21865643`; source repository [`ActiveInferenceInstitute/active_skillference`](https://github.com/ActiveInferenceInstitute/active_skillference)).
- **45 paired-publication `update_existing` refreshes applied**: version/PDF/metadata + software-link updates across already-catalogued works (template exemplars, DigiPPPiP, PROJECT BOND, Codomyrmex v1.3.0-paper, AlphaCOGANT, Active Inference Power Suite, prior_cognitive_art, BeeStack, COGANT, and more).
- **Fix: string-form paired-publication decisions are now honored** (`code/orchestrators/sync_paired_publications.py`). Decisions R25-R27 stored `raw_candidates` as bare release-URL strings, which `reviewed_pair_decisions()` silently dropped — re-surfacing a `create_new` duplicate for an already-decided pair. The parser now accepts both dict and URL-string candidates, the three decisions were normalized to dict form, and a regression test was added. The CogSecSkills v1.0.0/`zenodo.20804585` false positive is again correctly reported `already_reviewed` instead of `create_new` (report: **0 new**, 28 already reviewed).


## 2026-08-07

- **Two new Zenodo publications catalogued** with paper-folder documentation and regenerated bibliography, exports, work pages, feeds, sitemap, resume, accessibility, and Pages-manifest surfaces:
  - **#208** PROJECT BOND — The Special-Agent Operations Compendium (💻, concept DOI `zenodo.21843592`; source repository [`docxology/bond`](https://github.com/docxology/bond)).
  - **#209** DigiPPPiP: Digital Partner Pen Play in Parallel (🛡️, concept DOI `zenodo.21815704`; authors Siddhant Shrivastava, Evelyn C. Goh, Alexandra Mikhailova, and Daniel Ari Friedman).
- **Repository catalog updated**: added `docxology/bond` to the owned Developer Tools list; owned-repository count 94→95 and total curated software count 132→133.
- **Canonical DOI corrected** for kept ATLAS row #136 from version DOI `zenodo.10362561` to concept DOI `zenodo.10296601`; the retired #49 duplicate remains a permanent gap.
- **Zenodo stale-version exceptions documented**: records `21418901` (SynthOBS), `20804586` (CogSecSkills), and `19139090` (retired Template/Reproducible duplicate) are not new publications and are not added.
- **Release metadata**: CITATION.cff bumped to `2026.08.07`.
- **DOC-005 triage pass - ten more repositories promoted to `pages/SOFTWARE.md`** after manual review of the authenticated inventory (forks cleared by the owner are now reflected; inventory is 241 public repos = 154 primary + 87 forks): the six research-practice line-set repos (`line_set`, `black_line`, `white_line`, `golden_line`, `red_line`, `witness_register`, new **Research Practice** summary category, 6), the DigiPPPiP computational companion `Digi-PPPiP` (Other), the whole-colony simulation scaffold `BeeStack` (Developer Tools), the `template_advanced_literature_review` exemplar (Developer Tools), and `crescent-city-intel` (Data & Policy). Owned repositories 95->**105**; curated total 133->**143**; `data/repository-classification.json` uncatalogued queue 112->**101** with 4 primary-review non-fork items remaining (`active_inference_power`, `Active_Inference_Un0`, `GrowthModel`, `multi-time` - all description-less, deferred for human review).
- **DOC-004 decision R25 recorded** in `data/paired-publication-decisions.json`: the single new-candidate action from the paired-publication refresh (CogSecSkills v1.0.0 GitHub release paired with old concept `zenodo.20804585`) is **rejected** as a superseded-version false positive - bibliography row #174 already cites concept `zenodo.21513316`.
- **DOC-004 decisions R26-R27 recorded** in `data/paired-publication-decisions.json`: the 9 CogSecSkills release pairs under concept `zenodo.21513316` (row #174) and 18 Codomyrmex release pairs under `zenodo.21750800` (row #206) are **superseded/version-history** relations; no duplicate bibliography rows were created.
- **Authenticated GitHub inventory refresh** (241 repos, `data/github-repositories.json` 2026-08-07) and refreshed `reports/paired_publications_2026-08-07.json`; the curated flag is now computed against the full 143-row catalog.
- **Authenticated paired-publication refresh** wrote `reports/paired_publications_2026-08-07.json`: 402 pairs, 1 new candidate, 38 updates, and 363 items still requiring manual review under DOC-004; no candidates were auto-promoted.

## 2026-08-02

- **Seven new Zenodo publications catalogued** via `add_zenodo_only.py` as the DAF "line set" research-practice instruments plus a software release, each with full paper-folder documentation (README/AGENTS/SKILL/CITATION.cff/metadata.json + PDF) and regenerated downstream surfaces:
  - **#200** The Witness Register: Co-Registration Without Aggregation (💻, `zenodo.21754245`)
  - **#201** The Line Set: Holding Instruments Apart (💻, `zenodo.21754243`)
  - **#202** White Line: A Typed Ledger for the Edge of the Claim (💻, `zenodo.21754241`)
  - **#203** Personal Red Lines for Development (🛡️, `zenodo.21754239`)
  - **#204** Golden Line: Toward What Matters (💻, `zenodo.21754237`)
  - **#205** Black Line: Strong Work in Public (🛡️, `zenodo.21754235`)
  - **#206** Codomyrmex: An Artificial Ecology for Agentic Software Development (💻, `zenodo.21750800`)
- **Authors populated** on all seven new rows (Friedman, Daniel Ari).
- **Zenodo uncatalogued queue cleared** (0 new remaining; the SynthOBS `21418901` and CogSecSkills `20804586` flags are stale-version duplicate detections of already-catalogued works and were intentionally not added; the AII-Ecosystem `17982447` non-canonical-DOI note remains the documented exception).
- **GitHub paired-publication sync deferred**: `sync_paired_publications.py` could not complete due a GitHub API rate limit (HTTP 403). `codomyrmex`'s GitHub repo is already catalogued in `SOFTWARE.md` (Developer Tools); new line-set GitHub repos remain an open DOC-005 triage item pending a manual review pass.
- **Duplicate publications retired (2 rows)** after a full duplicate audit (0 duplicate DOIs; 2 genuine title/DOI duplications found and removed, keeping the canonical rows): removed **#49** (ATLAS concept-DOI `zenodo.10296601`, duplicate of kept **#136** `/10362561`) and **#193** (Template/Reproducible v1 concept `zenodo.19139089`, duplicate of kept **#1** `/16903351`). Retired numbers are left as gaps (49, 118, 193) per the repo's immutable-catalog convention — no renumbering, so every later work URL is preserved. Removed the retired paper folders (`papers/2023_ATLAS/`, `papers/2026_TemplateApproachReproducible2/`) and their work pages; `paper_metadata.json` 189→187; `papers/README.md` and BIBLIOGRAPHY header updated. Works 206→**204**, Papers 185→183. `#123` (template_ approach, `template_template`) confirmed distinct and retained.
- **One new Zenodo publication catalogued** — **#207** THALIA: Typed Harness with Analytical Lexical-Integrated Architecture (💻, `zenodo.21763244`, 2026-08-02), a typed agentic harness for reproducible long-context memory experiments, with paired GitHub repo [`docxology/thalia`](https://github.com/docxology/thalia) added to `pages/SOFTWARE.md` (owned-repos table; software catalog rows 93→94).
- **README signposting & completeness pass**: expanded the Quick Links line and Repository Map so **every** site page is reached from the README — added `research.html`, `reports.html`, `reproducibility.html`, `agent-verify.html`, `art.html`, `nft.html`, `meditations.html`, `about.html`, `exports.html` and the `pages/…` sources (`WIKIPEDIA.md`, `EVIDENCE.md`, `RESOURCES.md`, `VIDEOS.md`, `README.md`); enumerated the eight `domain-*.html` clusters under the `domains.html` hub. Verified all 114 relative link targets resolve on disk (0 broken), all non-domain root `.html` and all `pages/*.md` are linked, and the Repository Map table is well-formed.
- **README + repo-organization pass**: added the 2026 line-set research-practice works and new software to the relevant domain sections, added a "🔬 Research-Practice Line Set" subsection under Computational, surfaced THALIA + Active Inference Power Suite + Codomyrmex / line-set works in the domain tables, and added Thalia + the line-set repos to the highlighted-repositories list. Verified AGENTS.md-referenced orchestrators (regenerate_docs, sync_publications_html, sync_software_html, export_bibliography, export_agent_data, sync_scholar_metrics) all exist.
- **Accessibility/usability fix — site header was unusable**: the global
  `nav{position:fixed;top:0;z-index:200;background;...}` rule in `style.css`
  applies to every `<nav>` element, so the breadcrumb `<nav>` rendered as a
  second full-width fixed dark bar painted directly over the primary
  navigation. On every page and viewport the logo, middle nav links, and the
  mobile hamburger were hidden/unclickable behind the breadcrumb bar. Fixed by
  pinning the breadcrumb as a slim bar directly below the nav
  (`position:fixed;top:74px;z-index:150`) at a z-index below the nav (200), in
  `code/src/site_nav.py` `BREADCRUMB_CSS` (generated pages), the inline
  breadcrumb `<style>` on the 11 hand-authored pages, and the work-page
  template in `code/orchestrators/build_work_pages.py` (230 breadcrumb pages
  total). Verified via Playwright: mobile hamburger receives taps and opens the
  menu, desktop nav links are no longer covered (0/11 covered), breadcrumb sits
  below the nav and non-hero pages stay clear. `pytest` 231 green,
  `validate_repo` green.
- Bibliography **199→206**; paper folders **181→188**.
- CITATION.cff version/date-released bumped to `2026.08.02`.

## 2026-07-30

- **One new Zenodo publication catalogued** via `add_zenodo_only.py`: **#199** Active Inference Power Suite: Conditional Statistical Power under Controlled Generative Settings (🧠, `zenodo.21695160`), with full paper folder documentation and regenerated downstream surfaces.
- **Two existing works updated** to newer Zenodo records (same work, re-deposited): **#174** CogSecSkills (`20804585` → `21513316`, domain corrected to 🛡️) and **#198** SynthOBS & FractiSynth (`21418687` → `21418782`). Duplicate rows #200–#201 retired.
- **Comprehensive repo audit**: Zenodo uncatalogued queue cleared (0 remaining), paired-publication scan (0 new pairs), all local `validate_repo.py` checks pass (39/40 — live-site mismatch at 197 vs 199 is expected pre-push), 216 pytest green, 1540/1540 static accessibility passes, 0 asset-size warnings, all count-consistency surfaces aligned.
- Bibliography **197→199**; paper folders **180→181**.

## 2026-07-24

- **Repo-wide functional and signposting audit implemented**: Pages growth reports are date-stable control metadata across UTC rollovers; release-integrity now records explicit deployment-pending reasons and supports a strict `--require-deployed` gate; accessibility commands use the supported `--check` flag; public-page SEO guidance distinguishes indexable pages from intentional paper/redirect exceptions; cache-buster documentation matches the generated layer; and the historical maintenance table moved out of always-loaded `AGENTS.md`.
- **Regeneration tail made one-pass idempotent**: `build_generated_manifest.py` now runs before `build_agent_index.py`, so the agent route manifest hashes the current command matrix on its first pass; a final manifest pass still closes the release-integrity envelope. The ordering is regression-tested in `test_regenerate_all.py`.

## 2026-07-17

- **Compact video projection and repository triage added**: the interactive timeline now loads generated `data/videos-index.json` (`VideoIndex.v1`, 1127 compact records) while the complete `data/videos.json` remains available for downloads and detail pages; the repository classification queue now preserves description, language, topics, privacy, update, and derived description-quality fields for all 292 uncatalogued repositories (45 missing, 43 short, 204 substantive descriptions) without auto-promotion.
- **Operating runbooks expanded**: added repository-classification, CV release, evidence-refresh, accessibility/browser/visual QA, and live-verification runbooks; linked them from `docs/README.md` and `AGENT_START.md`. The ordered regeneration chain now re-runs asset and static accessibility reports after catalog rendering so generated report checks remain current when the catalog grows.
- **Regeneration pipeline made genuinely idempotent**: fixed local-vs-UTC report selection at the date boundary, moved the agent manifest behind its report and Pages dependencies, and added body-aware timestamp reuse across generated snapshots, exports, CV, feeds, and indexes. A complete second `regenerate_all.py` pass now produces zero file-content changes; the Pages artifact also treats `GENERATED.md` as control metadata so the integrity tail cannot invalidate its own manifest.
- **Progressive browser QA added**: `browser_qa.py` now exercises no-JavaScript fallbacks, mobile menu Escape/focus, publication filtering and sorting, gallery lightbox focus, reduced motion at 320px, forced colors, console/page errors, and YouTube iframe origin/title/referrer policy. The fresh report passes 7/7; browser smoke passes 10/10 and visual QA covers 26 screenshots.
- **Artwork gallery payload split**: added generated `data/artworks-index.json` (942 grid records, 712 KiB versus the 3.1 MiB full export) and lazy full-detail loading for description search and lightbox resolution links. The complete `data/artworks.json` export remains available for agents and downloads.
- **Backlog and documentation cleaned**: removed the completed stale issue-sync item from `TODO.md`, kept remaining release work as recurring gates, corrected the animation documentation's obsolete inline-script reference, and documented the GitHub Pages meta-CSP `frame-ancestors` limitation.
- **Public-source refresh completed without unreviewed promotion**: refreshed the dated public-source/inventory, repository, coverage, and pairing reports; the current pairing scan found one represented update and no new or ambiguous rows. Repository validation passes 1531/1531 static accessibility checks, 186 tests, the 17/17 live snapshot gate, strict report validation, Pages artifact checks, and GSC preflight.

## 2026-07-16

- **Service worker v20 — content data is network-first**: `data/*.json` and `search-index.json` were served cache-first, and each page fetches them at a stable `?v=` query that does not change when the data does — so a returning visitor kept seeing the *previous* publication list (e.g. 193 works after #195 was added) until the SW version happened to bump. These content-data requests are now network-first (cache fallback for offline), matching navigations; static assets (JS/CSS/images/fonts) stay cache-first for speed. Bumped v19 → v20 to clear existing stale caches. This is why a freshly-added publication now appears immediately.
- **New publication catalogued — Active FractalRabbit**: added *"Active FractalRabbit: A Synthetic Benchmark for Belief Filtering Under Sparse Waypoint Observations"* (Daniel Ari Friedman, Zenodo 2026-07-13, canonical concept DOI `10.5281/zenodo.21330636`) as work #195 via `add_zenodo_only.py`. Created `papers/2026_ActiveFractalRabbit/` (README/AGENTS/SKILL/CITATION.cff/metadata.json + PDF), the `works/…195.html` page, and regenerated the bibliography, works/software exports, catalog, search index, feed, sitemaps, and counts (bibliography works 193 → 194). `check_zenodo_uncatalogued.py` now reports the bibliography caught up (0 uncatalogued). Scope note: "0 uncatalogued" covers the Zenodo/ORCID deposit channel (DAF's primary archival target) — curated software (`SOFTWARE.md`) and presentations are deliberately-curated subsets, not auto-swept, and Google Scholar citation metrics (`data/scholar-snapshot.json`, `as_of 2026-06-09`) require DAF's own signed-in browser fetch per repo policy and were not updated. The record-17982447 non-canonical-DOI note is the documented AII-Ecosystem yearly-snapshot exception and is intentionally unchanged.
- **`add_zenodo_only.py` DOI fix**: the tool wrote the version-specific DOI into the per-paper folder files (README/AGENTS/SKILL/CITATION.cff/metadata.json) while the bibliography and `paper_metadata.json` used the canonical concept DOI — splitting one work across two DOIs and failing `test_paper_readme_contracts.py`. Added a `canonical_doi(rec, meta)` helper (concept-DOI-first, mirroring the bibliography derivation) and routed every folder renderer through it; the version id is retained separately as `record_id`. Future Zenodo-only additions are now concept-DOI-consistent by construction.

- **CSP inline-script breakage fixed (art gallery restored)**: the `script-src 'self'` CSP deployed 2026-07-12 silently blocked the inline `<script>` blocks still shipping on art.html, videos.html, search.html, repositories.html, repositories-forks.html, and index.html — /art rendered zero of its 942 artworks and its search box only surfaced site-wide paper suggestions. All six pages' scripts externalized to `js/art-gallery.js`, `js/videos-page.js`, `js/search-page.js`, `js/repo-inventory.js` (shared by both repo pages), and `js/index-page.js`.
- **Art gallery search is art-local again**: new `data-local-search` attribute on the /art search input opts it out of the site-wide `search-index.json` autocomplete in `js/interactive.js`; gallery filtering (title/description/tags over all 942 works) is handled by `js/art-gallery.js`. Also fixed a latent error-path bug (`getElementById('empty')` → `emptyState`) and a duplicated `tts-controls.js` include.
- **Lightbox double-advance fixed**: the /art lightbox sort/size/nav controls carry `data-*` attributes already delegated by `js/interactive.js` to `window.*` globals; `js/art-gallery.js` was additionally `addEventListener`-wiring the same buttons, so each ‹/› click advanced two artworks. `art-gallery.js` now wires only the search input, Escape/arrow keys, and overlay-click and defers the delegated controls to `interactive.js` (caught by cross-vendor review).
- **videos.html skip-link**: inline `onfocus`/`onblur` (CSP-blocked) replaced with a CSS `:focus` reveal rule.
- **Font loading un-broken CSP-safely**: the `media="print" onload="this.media='all'"` pattern (blocked by CSP, so Google Fonts never applied on nine pages) replaced with `media="print" data-media-swap="all"` + an external swap in `js/interactive.js`; `optimize_font_loading.py` updated to emit and migrate to the new pattern.
- **publications.html search input**: CSP-blocked inline `oninput="filterPubs()"` replaced with `addEventListener` wiring in `js/publications.js`.
- **Service worker v19**: cache bumped; new per-page JS modules added to the precache list.

## 2026-07-12 (session 5)

- **Non-render-blocking Google Fonts**: All 17 HTML pages with Google Fonts links converted to `media="print" onload="this.media='all'"` pattern, eliminating render-blocking CSS on first paint. New `code/orchestrators/optimize_font_loading.py` orchestrator.
- **Twitter Card tags on about.html**: Added `twitter:card`, `twitter:title`, `twitter:description`, `twitter:image` meta tags for social sharing parity with OG tags.
- **apple-touch-icon optimized**: Reduced from 77KB to 39KB (48% reduction) via PNG quantization to 128 colors, with no visible quality loss at 180x180.
- **extract_paper_texts.py error logging**: Silent `except Exception: continue` now logs the exception with page number, image index, and PDF filename to stderr before continuing, preventing silent extraction failures.
- **Descriptive image alt text**: Paper page thumbnail alt text now uses `"Figure from [paper_name], page N"` instead of raw filenames, improving screen reader usability and SEO.
- **Service worker v18**: Cache version bumped to serve updated JS assets (CSP-compliant scripts, search badges, count badges).

## 2026-07-12 (session 4)

- **CITATION.cff generated for all 176 papers**: New `generate_citation_cff.py` script creates CFF 1.2.0 files from `metadata.json`. 47 papers that were missing CITATION.cff now have it. Year extracted from folder names for older papers. Multi-line author format with ORCID for DAF.
- **2024_BioFirm PPTX extraction**: Downloaded `BIOFIBIOFIRM_v2.pptx` from Zenodo, extracted 11 slides of text + 8 images using python-pptx. 173 of 176 papers now have full_text.md (98.3% coverage).
- **Content-Security-Policy deployed**: CSP meta tag (`script-src 'self'`) now on all 23 indexable HTML pages, blocking inline event handlers and inline `<script>` blocks. Documented in `docs/security/security-posture.md`.
- **Inline event handlers eliminated**: all 68 `onclick`/`onchange`/`onsubmit` handlers across 23 pages migrated to `data-*` attributes wired via `addEventListener` in `js/interactive.js`. New `code/orchestrators/migrate_inline_handlers.py` orchestrator.
- **rel="me" social verification links** expanded from 3 pages to all 21 indexable pages (Scholar, ORCID, GitHub, LinkedIn, YouTube, Wikidata, Bluesky).
- **hreflang alternate links** expanded from 1 page (index.html) to all 21 indexable pages.
- **External `js/menu-esc.js`**: menu Escape-to-close handler moved from inline `<script>` to external file for CSP compliance.
- **Service worker bumped to v17**: cache version updated for new JS assets.
- **Accessibility audit enhanced**: `accessibility_audit.py` now checks for `no_inline_handlers` as a gate (16 checks, up from 15). All 23 pages pass.
- **art.html nav-toggle button**: added missing `.menu-btn` for keyboard-accessible menu toggle on the art gallery page.
- **New orchestrators**: `deploy_seo_security.py` (idempotent CSP/rel-me/hreflang deployment), `migrate_inline_handlers.py` (inline handler → data-attribute conversion).
- **Shared head extras**: `HEAD_EXTRAS` constant in `code/src/site_nav.py` centralizes CSP + rel-me + hreflang + dns-prefetch for generated HTML templates (domain, work, paper, video pages).
- All generated surfaces, sitemap, manifest, and asset-size report refreshed. All validation + 154 tests green.

## 2026-07-12 (session 3)

- **Image thumbnail previews on paper landing pages**: `image_gallery_link()` in `build_paper_pages.py` now shows up to 6 thumbnail previews of extracted figures with lazy loading and a "+N more" indicator. All 176 paper pages regenerated.
- **CSS classes for thumbnails**: `.image-thumbs`, `.thumb-link`, and `.muted` added to `style.css`, replacing inline styles for cleaner maintenance and consistent rendering.
- **Search index image_count**: `build_search_index.py` now includes `image_count` for works with extracted images (140 works). Search results page shows "Full Text" and "N Images" badges on matching works.
- **llms.txt stale counts corrected**: 171→172 full text papers, 139→168 image galleries, 8986→9938 images.
- **PPTX text extraction**: Extracted text from `BIOFIBIOFIRM_v2.pptx` (11 slides) for 2025_BiofirmDevelopmentWith. 172 of 176 papers now have full_text.md (97.7% coverage).
- All generated surfaces, sitemap, manifest, and asset-size report refreshed. All validation + 154 tests green.

## 2026-07-12

- Added work **#194 "Prior Cognitive Art"** (`zenodo.21316510`, `docxology/prior_cognitive_art` v0.1.0) via the canonical `sync_paired_publications.py --apply` path. Paper folder, bibliography row, work page, domain page, search index, sitemap, and all generated surfaces updated.
- **Enhanced full-text extraction pipeline**: `extract_paper_texts.py` now embeds inline image references in `full_text.md` at the correct page positions, so readers and crawlers can discover extracted figures in context.
  - **171 papers** now have `full_text.md` (was 166 — gained 5 from ODT/DOCX/PDF source extractions)
  - **8,986 images** extracted across **139 papers** (was 3,057 across 136)
  - **8,924 image references** embedded inline in `full_text.md` with 0 broken links
  - Downloaded and extracted text from 4 Zenodo ODT/DOCX transcript files and 1 misnamed PDF
  - `format_markdown()` now accepts an `images` parameter and groups image refs by page
  - `extract_images()` now returns `(page_num, filename)` tuples for page-aware embedding
- **Image sitemap expansion**: `build_image_sitemap.py` now includes paper-extracted figures in `sitemap-images.xml` (9,928 total images, was 942 — 139 paper pages with image galleries)
- **Full-text extraction pipeline**: new `code/orchestrators/extract_paper_texts.py` extracts page-level text and embedded images from all paper PDFs using PyMuPDF (with OCR fallback via tesseract for scanned PDFs).
  - **166 papers** now have `full_text.md` with complete page-by-page text extraction
  - **3,057 images** extracted to per-paper `images/` subdirectories across **136 papers**
  - **0 errors** across all 166 extractions (10 papers have no PDF — Zenodo-only metadata, slides, or non-PDF artifacts)
  - Paper landing pages (`papers/*/index.html`) now link to `full_text.md` and the `images/` gallery
  - Work pages now include JSON-LD `encoding` field (Schema.org `TextObject`) for all 166 works with full text
  - Search index includes `full_text_url` for all 166 works with extracted text
  - `papers/README.md` updated to document `full_text.md` and `images/` as standard folder contents
  - `llms.txt` updated with full-text extraction pipeline link
  - Fixed `regenerate_all.py` to use `sys.executable` instead of hardcoded `python3` (was breaking on Python 3.9 vs 3.14 `datetime.UTC` import)
  - Fixed `build_current_counts.py` Python 3.9 compatibility (`datetime.UTC` → `datetime.timezone.utc`)
  - Fixed `build_resume.py` to gracefully skip PDF generation when reportlab is not installed
  - Fixed `validate_repo.py` to skip `full_text.md` files in local-link validation (academic paper internal references)
  - Fixed `build_sitemap.py` to not list `/papers/` URLs (SEO invariant compliance)
  - All 22 local generated surfaces regenerated (bibliography, publications, software, domains, works, paper pages, exports, evidence, catalog, search index, RSS feed, sitemap, manifest)

## 2026-07-05

- Comprehensive interactive-layer buildout across all 23 indexable pages:
  - **Text-to-Speech (TTS)**: Web Speech API integration (`js/tts-controls.js`) — floating control panel, speed/voice selection, paragraph highlighting, keyboard shortcut `T`
  - **Interactive features** (`js/interactive.js`): reading progress bar, scroll-to-top button, keyboard shortcuts overlay (`?`), section anchor copy-links, search autocomplete from `search-index.json`, image lazy loading, external link safety
  - **+515 lines CSS** for all new components with responsive, print, and reduced-motion overrides
  - **Service Worker v16** — caches new JS modules, drops stale cache
  - **Performance**: 5 hero-art image preloads, resource hints (dns-prefetch, prefetch) across all pages, `preconnect` for Scholar/ORCID
  - **SEO**: `rel="me"` social profile verification links, `hreflang` support, WebPage JSON-LD on homepage
  - **Docs**: `SKILL.md`, `docs/design/components/tts.md`, `docs/design/animations.md`; updated `AGENTS.md` with WEB DEVELOPER role, `CLAUDE.md` with interactive layer commands, design-system docs with new components
- 5 `noindex` redirect stubs intentionally skipped (about, research, meditations, nft, google verification)

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
