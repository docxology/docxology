# AGENTS.md — docxology

**Repository**: [docxology/docxology](https://github.com/docxology/docxology)
**Purpose**: Master profile repository indexing the unified bibliography (115 works), 49 owned software repositories (+32 AII contributions), full generated GitHub inventory, and research documentation across Entomology, Active Inference, Cognitive Security, and Art & Synergetics.

---

## Agent Roles

### 📖 ARCHIVIST

- Maintains the unified [pages/BIBLIOGRAPHY.md](pages/BIBLIOGRAPHY.md) catalog of all publications
- Ensures every publication has a corresponding paper folder with documentation
- Cross-references DOIs, venues, and citation metadata
- Tracks publication counts and domain coverage

### 🔬 RESEARCHER

- Extracts key findings, methods, and contributions from each paper
- Populates per-paper README.md and SKILL.md with accurate metadata
- Maps interdisciplinary connections across domains
- Maintains [paper_metadata.json](papers/paper_metadata.json) with structured data

### 🎓 EDUCATOR

- Generates Claude Code-compatible SKILL.md files for each publication
- Creates learning pathways across the bibliography
- Maintains clear documentation hierarchy (README → pages/ → BIBLIOGRAPHY → papers/)
- Ensures YAML frontmatter, tags, and Instructions sections are present

### 🔗 INTEGRATOR

- Deep-links across [pages/BIBLIOGRAPHY.md](pages/BIBLIOGRAPHY.md), [pages/SOFTWARE.md](pages/SOFTWARE.md), and [papers/](papers/)
- Maps papers to their associated software repositories
- Connects the 8 research domains through cross-references
- Keeps the repository map in [README.md](README.md) current
- Keeps [pages/DISCOVERY.md](pages/DISCOVERY.md) current with canonical public identifiers, API endpoints, query recipes, and verification cautions
- Keeps teaching and AII program lines aligned across [index.html](index.html) (visible on GitHub Pages), [pages/PROFILE.md](pages/PROFILE.md), [pages/VIDEOS.md](pages/VIDEOS.md), and the **Educator** bullet in [README.md](README.md) (e.g. CR BIOL courses, AII Textbook cohort count, textbook monograph links)

### 🛠️ MAINTAINER

- Runs [regenerate_docs.py](papers/regenerate_docs.py) to rebuild documentation
- Runs [sync_publications_html.py](papers/sync_publications_html.py) with `--apply` after edits to the unified bibliography table so [publications.html](publications.html) stays aligned
- Validates documentation completeness across all paper folders (108 as of 2026-05-15)
- Ensures consistent formatting and accurate metadata
- Manages the documentation generation pipeline

---

## Repository Structure

```text
docxology/
├── README.md          ← Profile page with domain matrix, consulting info, and deep-links
├── pages/BIBLIOGRAPHY.md    ← Unified sortable bibliography (115 works; DOI links and paper-folder deep-links)
├── pages/SOFTWARE.md        ← 49 owned repos + 32 AII contributions
├── pages/               ← Documentation hub for videos, resources, pathways, and repos
├── pages/LINKS.md           ← Comprehensive directory of all web presences and profiles
├── pages/DISCOVERY.md       ← Public-source discovery map for agents, APIs, and search indexes
├── pages/PROFILE.md         ← Detailed biographical profile (education, research, art, orgs)
├── pages/COLLABORATORS.md   ← Key collaborators and institutional research network
├── pages/MEDIA.md           ← Talks, podcasts, video series, courses, and press coverage
├── AGENTS.md          ← This file: agent roles and maintenance log
├── index.html         ← GitHub Pages landing page with SEO and structured data
├── discovery.html     ← Canonical HTML discovery map for public-source APIs and identifiers
├── search.html        ← Human-facing search over works, software, pages, people, organizations, and claims
├── repositories.html  ← Generated full public GitHub repository inventory for docxology and AII
├── opensearch.xml     ← Browser/search-engine descriptor for site search
├── catalog.html       ← Schema.org DataCatalog page for public data exports
├── updates.html       ← Generated human-readable changelog page
├── domains.html       ← Research-domain landing page index
├── domain-*.html      ← Domain-specific HTML pages for major research clusters
├── works/             ← Generated per-work HTML landing pages for each bibliography row
├── publications.html  ← Canonical HTML target for unified bibliography
├── software.html      ← Canonical HTML target for software catalog
├── collaborators.html ← Canonical HTML target for institutional network
├── media.html         ← Canonical HTML target for podcast/video appearances
├── style.css          ← Unified custom CSS core
├── sitemap.xml        ← SEO sitemap
├── robots.txt         ← Robot exclusion file
├── llms.txt           ← Agent-facing source map and source-of-truth rules
├── search-index.json  ← Generated site-wide search index
├── feed.xml           ← RSS feed for recent works and site updates
├── GENERATED.md       ← Generated-file manifest with source-to-output rebuild commands
├── AGENT_START.md     ← Agent task recipes and source-of-truth rules
├── humans.txt         ← Human credits, contact, and site metadata
├── .well-known/security.txt ← Responsible disclosure metadata
├── CITATION.cff       ← Machine-readable citation metadata
├── codemeta.json      ← CodeMeta software/source metadata
├── bibliography.bib / bibliography.csl.json / bibliography.ris ← citation-manager exports
├── data/              ← Agent JSON indexes for works, software, people, organizations, claims, catalog, enrichment, and generated files
├── reports/           ← Public-source snapshots, reconciliation reports, link reports, accessibility reports, and visual QA screenshots
├── docs/              ← Documentation for the entire repository (see docs/AGENTS.md)
├── code/              ← Repository source code and executable orchestrators (see code/AGENTS.md)
│   ├── orchestrators/ ← Thin orchestrators and pipeline controllers
│   ├── src/           ← Source code and submodules
│   └── tests/         ← Test suites and validation tests
└── papers/            ← 108 per-paper folders (`YYYY_Topic`)
    ├── README.md      ← Papers directory index
    ├── AGENTS.md      ← Papers-level agent roles
    ├── paper_metadata.json
    ├── biblio_table.py       ← Shared iterator for 8-column BIBLIOGRAPHY.md rows
    ├── regenerate_docs.py
    ├── sync_publications_html.py  ← Regenerates publications.html PUBS + JSON-LD mainEntity
    └── YYYY_Topic/
        ├── README.md   ← Paper overview, abstract, keywords, citation
        ├── AGENTS.md   ← Paper-specific agent roles and extraction log
        ├── SKILL.md    ← Claude Code-compatible skill definition
        └── *.pdf       ← Source PDF (most folders; filenames vary)
```

---

## Maintenance Log

| Date | Agent | Action | Status |
| --- | --- | --- | --- |
| 2026-03-08 | ARCHIVIST | Rebuilt pages/BIBLIOGRAPHY.md as unified sortable table | ✅ |
| 2026-03-08 | RESEARCHER | Verified paper-folder documentation completeness | ✅ |
| 2026-03-08 | EDUCATOR | Fixed SKILL.md for CryptoJews and EhrlichialInfection | ✅ |
| 2026-03-08 | INTEGRATOR | Redesigned README.md with domain matrix and deep-links | ✅ |
| 2026-03-08 | MAINTAINER | Created root AGENTS.md and papers/AGENTS.md | ✅ |
| 2026-03-24 | INTEGRATOR | Added pages/LINKS.md — comprehensive directory of all web presences | ✅ |
| 2026-03-24 | RESEARCHER | Added pages/PROFILE.md — detailed biographical profile with education, orgs, art | ✅ |
| 2026-03-24 | INTEGRATOR | Added pages/COLLABORATORS.md — key collaborators with joint publication links | ✅ |
| 2026-03-24 | ARCHIVIST | Fixed Google Scholar ID (DXjPFtYAAAAJ), added ORCID (0000-0001-6232-9096) | ✅ |
| 2026-03-24 | INTEGRATOR | Updated README.md with new file links, badges, corrected profiles | ✅ |
| 2026-03-24 | INTEGRATOR | Updated pages/BIBLIOGRAPHY.md with ORCID, ResearchGate, corrected Scholar ID | ✅ |
| 2026-03-24 | MAINTAINER | Updated index.html with new links, badges, structured data, ORCID | ✅ |
| 2026-03-24 | INTEGRATOR | Added links: danielarifriedman.com, Curio Cards, Complexity Weekend, Wikidata | ✅ |
| 2026-03-24 | RESEARCHER | Added pages/MEDIA.md — talks, podcasts, video series, courses, interviews, press | ✅ |
| 2026-03-24 | INTEGRATOR | Added Semantic Scholar, SciProfiles, ArXiv, Foundation.app, Apple Podcasts links | ✅ |
| 2026-03-24 | INTEGRATOR | Added Stanford dissertation purl, Complexity Adventures organizer profile | ✅ |
| 2026-03-24 | INTEGRATOR | Added Active Inference Research page link to pages/LINKS.md | ✅ |
| 2026-03-24 | RESEARCHER | Deep Perplexity research: corrected Google Scholar citations (700+), verified Curio Cards (May 9, 2017) | ✅ |
| 2026-03-24 | INTEGRATOR | Added AII 501(c)(3) status, current officers (Mikhailova VP 2025+), co-founders across all files | ✅ |
| 2026-03-24 | ARCHIVIST | Added Thomas Parr (UCL) as collaborator, ALIUS Research Group context, Christie's auction (Oct 2021) | ✅ |
| 2026-03-24 | INTEGRATOR | Added ScholarGPS, ISSS wiki, NFT Archaeology, Christie's lot links to pages/LINKS.md | ✅ |
| 2026-03-24 | MAINTAINER | Fact-checked all files via deep internet research (Perplexity); updated index.html, sitemap.xml | ✅ |
| 2026-03-25 | INTEGRATOR | Added Conor Heins & Tim Verbelen (VERSES AI) to pages/COLLABORATORS.md, pages/PROFILE.md, pages/WIKIPEDIA.md | ✅ |
| 2026-03-25 | ARCHIVIST | Added PubMed, Zenodo links to pages/LINKS.md; added Denise Holt press feature across LINKS/MEDIA | ✅ |
| 2026-03-25 | MAINTAINER | Updated sitemap.xml dates, enhanced pages/WIKIPEDIA.md with VERSES AI and first-ETH Christie's detail | ✅ |
| 2026-03-25 | RESEARCHER | Round 2 Perplexity audit: verified then-current AII board (6 members), officers (Mikhailova VP/Secretary 2025+), Delaware incorporation, 501(c)(3) 2024 | ✅ |
| 2026-03-25 | ARCHIVIST | Verified Curio Cards: Card 24 \"Complexity\" (333 copies), Card 25 (222), Card 26 (106); 7 artists; Christie's $1.2M/393 ETH | ✅ |
| 2026-03-25 | INTEGRATOR | Added SAB links (Friston, Ramstead, Albarracin, Fields) to pages/COLLABORATORS.md; citation counts (88, 45, 41, 31 for top papers) | ✅ |
| 2026-03-25 | INTEGRATOR | Added 7 AII pages to pages/LINKS.md (SAB, Strategy, Partnership, Substack, History, Board); CR link; 251 repos | ✅ |
| 2026-03-25 | MAINTAINER | Enriched pages/PROFILE.md with AII programs (Internship, Fellows, Mentorship, Textbook Group), Curio Cards art descriptions | ✅ |
| 2026-03-25 | ARCHIVIST | Added paper folder 2026_ReproducibleResearch (template/ paper, DOI 10.5281/zenodo.19139090); updated BIBLIOGRAPHY work count | ✅ |
| 2026-03-25 | RESEARCHER | Round 3 Perplexity audit: verified COGSEC founding (2018), P3IF affiliations, NM field site, ALIUS team | ✅ |
| 2026-03-25 | INTEGRATOR | Enriched pages/PROFILE.md with COGSEC history, named volumes (IRT-20, NIM-21, CAT-22, ATLAS), and P3IF affiliations | ✅ |
| 2026-03-25 | ARCHIVIST | Updated pages/WIKIPEDIA.md, pages/COLLABORATORS.md (RJ Cordes), and pages/LINKS.md with verified COGSEC & ALIUS details | ✅ |
| 2026-04-01 | MAINTAINER | Established pages/ hub architecture; rigidly verified AGENTS.md and README.md alignments | ✅ |
| 2026-04-01 | MAINTAINER | Migrated all root .md files to pages/; mass-updated 100+ deep-links across papers/ | ✅ |
| 2026-04-01 | INTEGRATOR | Injected YAML frontmatter, navigation headers, and footers across 9 pages/ files | ✅ |
| 2026-04-01 | MAINTAINER | Renamed videos.md/resources.md to VIDEOS.md/RESOURCES.md for naming parity | ✅ |
| 2026-04-01 | INTEGRATOR | Added code/ (orchestrators/, src/, tests/) and docs/ to repository structure | ✅ |
| 2026-04-01 | MAINTAINER | Comprehensive index.html overhaul: WCAG 2.2 (skip-link, ARIA, focus-visible, reduced-motion), ScholarlyArticle/CreativeWork/ItemList JSON-LD schemas, PWA manifest, service worker, print styles | ✅ |
| 2026-04-01 | INTEGRATOR | Created pages/README.md hub index with full navigation table | ✅ |
| 2026-04-01 | MAINTAINER | Expanded sitemap.xml (15 URLs: added WIKIPEDIA, VIDEOS, RESOURCES, reordered); enhanced robots.txt with allow/disallow rules | ✅ |
| 2026-04-01 | MAINTAINER | Created manifest.json (PWA) and sw.js (service worker with stale-while-revalidate) | ✅ |
| 2026-04-03 | MAINTAINER | Structural integrity audit: Migrated 4 main markdown lists to canonical HTML pages (publications, software, collaborators, media) to fix indexability; fixed JSON-LD jobTitle mapping; standardized "March 2026" metrics dating. | ✅ |
| 2026-04-15 | ARCHIVIST | Added Ento-Linguistics (Zenodo) to pages/BIBLIOGRAPHY.md; synced papers/README index, papers/AGENTS.md counts, publications.html PUBS + JSON-LD; paper_metadata.json entry 2026_EntoLinguistics | ✅ |
| 2026-04-15 | INTEGRATOR | Aligned index.html / publications.html / README counts (109 works); removed duplicate Person JSON-LD on index; added ento_linguistics to SOFTWARE.md, software.html, repo totals 47+31; sitemap lastmod | ✅ |
| 2026-04-15 | INTEGRATOR | PROFILE.md metrics table (109/107 split); README domain matrix + Entomology selected-pubs table; index.html Computational tag 47 owned | ✅ |
| 2026-04-19 | ARCHIVIST | Added 2026_ActInfMetaAnalysis (DOI 10.5281/zenodo.19461934, Active Inference Journal); README.md, AGENTS.md, SKILL.md created; bibliography row 108; Active Inference domain 19→20; all counts updated 109→110 | ✅ |
| 2026-04-19 | ARCHIVIST | Added 2026_FocusedAttentionMeditation (DOI 10.1007/978-3-032-16955-6_11, Springer IWAI 2025); README.md, AGENTS.md, SKILL.md created; bibliography row 109; Active Inference domain 20→21; all counts updated 110→111; no PDF available noted | ✅ |
| 2026-04-23 | ARCHIVIST | Added 2026_CognitiveCaseDiagrams (DOI 10.5281/zenodo.19695260, Active Inference Journal v1); per-paper README/AGENTS/SKILL; BIBLIOGRAPHY row 110; Active Inference domain 21→22; paper_metadata; publications.html + index.html 112 works; SOFTWARE.md + software.html repo 48; papers/README index 105 | ✅ |
| 2026-04-24 | ARCHIVIST | Added 2026_FEPLean (DOI 10.5281/zenodo.19699234); per-paper README/AGENTS/SKILL; BIBLIOGRAPHY row 111; 113 works; papers 106; Active Inference 23; SOFTWARE AII 32 + FEP_Lean; publications.html + index | ✅ |
| 2026-04-25 | INTEGRATOR | Sitemap: added `about.html`; normalized `https://danielarifriedman.com/` (apex) across README, pages/LINKS.md, pages/PROFILE.md, art/README.md, art metadata JSON — aligns with CNAME and canonical HTML | ✅ |
| 2026-04-25 | MAINTAINER | Synced Google Scholar citation count to **812** (April 2026) across README, pages/BIBLIOGRAPHY.md, LINKS, PROFILE, WIKIPEDIA draft; README blockquote now distinguishes **251** public repos vs **80** catalogued software rows; added `code/AGENTS.md`, `docs/AGENTS.md` | ✅ |
| 2026-04-25 | INTEGRATOR | SEO pass: `og-image.jpg` + `og:*` + JSON-LD (Person, WebSite+SearchAction, ProfessionalService, BreadcrumbList) on `index` and subpages; removed Twitter card meta; IndexNow key file; `art.html`/`videos.html` head metadata ordered before styles; PWA+OG on `about.html` and `blog/index.html` redirects; `.github/workflows/indexnow-on-push.yml` | ✅ |
| 2026-04-25 | INTEGRATOR | README + AGENTS doc sync: root README Educator line (AII Textbook 10 cohorts through 2026, Parr/Pezzulo/Friston 2022 + Namjoshi 2026 links, CR BIOL-1 Pelican Bay / BIOL-8 Human Biology Spring 2026); `pages/README` paper-folder count 106; `papers/AGENTS` + `docs/AGENTS` hub accuracy | ✅ |
| 2026-04-25 | MAINTAINER | Retired outdated copy: BIBLIOGRAPHY summary line (103/99), duplicate 727-citation log rows, Twitter-era index.html log phrasing, stale CR/BIOL-8 and repo 47/31 counts across `pages/*`; WIKIPEDIA teaching sentence + PROFILE ref path | ✅ |
| 2026-05-04 | MAINTAINER | Renamed all `papers/Friedman_*` dirs to `YYYY_Topic`; added `2020_FacilitatorsCatechism` (Zenodo 4203765); bibliography & site counts 113→114; `regenerate_docs.py` parses 8-col BIBLIOGRAPHY table | ✅ |
| 2026-05-04 | INTEGRATOR | `papers/biblio_table.py` + `papers/sync_publications_html.py`: `publications.html` **PUBS** + JSON-LD **mainEntity** (114) match `pages/BIBLIOGRAPHY.md` row order; domain blurbs (Art/Computational); `papers/AGENTS` **Works** counts from Domain column | ✅ |
| 2026-05-12 | MAINTAINER | Repo-wide AGENTS.md + README.md audit (Perplexity-verified): public repo total **251 → 285** (GitHub count at audit time); BIBLIOGRAPHY header papers count **93 → 96** to match 96 Paper-type rows; SOFTWARE.md fork-inclusive total **260+ → 285+** | ✅ |
| 2026-05-12 | INTEGRATOR | README domain figures synced to BIBLIOGRAPHY Type-column ground truth: Active Inference selected-pubs **22 → 23**; Cognitive Security **3 books + 16 papers → 3 books + 17 papers**; Computational matrix **6 → 7 papers** (ReproducibleResearch); Computational section **6 papers + 47 repos → 7 papers + 48 owned + 32 AII**; **31 → 32 AII contributions** | ✅ |
| 2026-05-12 | RESEARCHER | Verified via Perplexity research (May 2026): Scholar `DXjPFtYAAAAJ` shows 758 citations (cache may differ from manual 812 sync); AII officers — **Daniel = President + Treasurer**, **Mikhailova = VP + Secretary**; AII Board = 10 members; new **33-member Scientific Advisory Board** announced in January 2026 newsletter | ✅ |
| 2026-05-13 | ARCHIVIST | Added `2026_BlakeJiang` (Zenodo DOI 10.5281/zenodo.20144984); BIBLIOGRAPHY and publications.html **114→115**; paper folders and metadata **107→108**; Art & Synergetics **14→15**; GitHub public repo count **285→286** | ✅ |
| 2026-05-13 | INTEGRATOR | Added `discovery.html` and `pages/DISCOVERY.md` for agentic source discovery; public API snapshots: ORCID 20 work groups, PubMed 8 exact-author records, Europe PMC 10 exact-author results, Crossref 15 ORCID DOI records, Zenodo 36 exact-name / 82 ORCID-linked records, AII GitHub 50 public repos | ✅ |
| 2026-05-13 | MAINTAINER | Deep Research pass: added `llms.txt`, `CITATION.cff`, and `codemeta.json`; added AII Wikidata `Q139600792`; verified Zenodo software DOIs for GNN and Journal-Utilities; refreshed selected AII repository stars; softened early-NFT language where primary-source support is nuanced | ✅ |
| 2026-05-13 | MAINTAINER | Comprehensive discovery expansion: generated BibTeX/CSL/RIS and `data/*.json`; added domain landing pages, `pages/DOMAINS.md`, `pages/CITE_VERIFY.md`, `pages/EVIDENCE.md`, public-source refresh reports, CI validation, publication filters, and tailored OG images | ✅ |
| 2026-05-13 | MAINTAINER | Added per-work landing pages, `search-index.json`, `feed.xml`, `CHANGELOG.md`, `docs/REDIRECTS.md`, issue templates, reconciliation JSON/report, static accessibility report, and Playwright visual QA screenshots | ✅ |
| 2026-05-13 | INTEGRATOR | Added human `search.html`, `opensearch.xml`, `catalog.html` / `data/catalog.json`, work-page enrichment extraction, `GENERATED.md`, scoped external-link reporting, weekly freshness workflow, Dependabot, and workflow hardening | ✅ |
| 2026-05-13 | MAINTAINER | Added `updates.html`, `AGENT_START.md`, `humans.txt`, `.well-known/security.txt`, richer per-work JSON-LD, external-link triage, asset-size audit, browser smoke report, and live-site verification reporting | ✅ |
| 2026-05-15 | MAINTAINER | Implemented completeness/accuracy upgrade: Linux-safe art links, tracked bytecode cleanup, v2/v3 DOI corrections, generated GitHub repository inventory, expanded evidence claims, public-source inventory report, freshness fact comparison, and stale live-site check enforcement | ✅ |

---

## Learned User Preferences

- Prefer apex site URLs `https://danielarifriedman.com/` for HTML canonicals, `og:url`, and sitemap `loc` entries so they match `CNAME` and reduce www/apex mismatch issues in Search Console.
- Omit redirect-only stub pages from `sitemap.xml` when their canonical is the homepage; keep the stub files for inbound links but avoid listing them so crawl signals are not contradictory.
- When maintaining `index.html` Person JSON-LD, put Wikidata `https://www.wikidata.org/wiki/Q138781444` first in the `sameAs` array (canonical entity anchor for the person).
- After Google Scholar metrics change, sync the citation count across README, `pages/BIBLIOGRAPHY.md`, `pages/LINKS.md`, `pages/PROFILE.md`, `pages/WIKIPEDIA.md`, and main HTML stats for consistency.
- Homepage teaching blurbs: BIOL-1 General Biology — College of the Redwoods, Pelican Bay, Spring 2026; BIOL-8 — Human Biology, College of the Redwoods, Spring 2026.
- AII Textbook Group site copy: 10 cohorts through 2026; link the Parr/Pezzulo/Friston MIT Press OA monograph and the Namjoshi Fundamentals monograph as in the Educator line.
- On SEO passes for `index.html`, remove legacy Twitter card meta and drop Twitter from Person `sameAs` when the user requests a Twitter-free head.
- After substantive repo edits, run `uv run pytest` in `code/tests` (Python via `uv`) to confirm the suite still passes.

## Learned Workspace Facts

- Repo `docxology/docxology` powers the profile site; GitHub Pages custom domain in root `CNAME` is `danielarifriedman.com` (apex, no `www`).
- `publications.html` **PUBS** and JSON-LD **mainEntity** are generated from [`pages/BIBLIOGRAPHY.md`](pages/BIBLIOGRAPHY.md) by [`papers/sync_publications_html.py`](papers/sync_publications_html.py) (`--apply` after table edits); the interactive table also needs on-page counts in that HTML file.
- The INTEGRATOR role in `papers/AGENTS.md` includes keeping `publications.html` / `PUBS` aligned when unified bibliography totals change.
- `discovery.html` is the canonical website discovery page; `pages/DISCOVERY.md` is the agentic Markdown companion for canonical public identifiers, exact API endpoints, query recipes, and cautions about public index count mismatches.
- `llms.txt` is the compact agent-facing source map. `CITATION.cff` and `codemeta.json` provide machine-readable citation and software metadata for repository discovery.
- `bibliography.bib`, `bibliography.csl.json`, `bibliography.ris`, and `data/works.json` are generated from `pages/BIBLIOGRAPHY.md` by `code/orchestrators/export_bibliography.py`.
- `data/software.json`, `data/people.json`, `data/organizations.json`, and `data/claims.json` are generated by `code/orchestrators/export_agent_data.py`.
- `domains.html`, `domain-*.html`, and `pages/DOMAINS.md` are generated by `code/orchestrators/build_domain_pages.py`.
- `works/index.html` and `works/*.html` are generated by `code/orchestrators/build_work_pages.py`.
- `evidence.html` and `pages/EVIDENCE.md` are generated by `code/orchestrators/build_evidence_page.py` from `data/claims.json`.
- `search-index.json` is generated by `code/orchestrators/build_search_index.py`; `feed.xml` is generated by `code/orchestrators/generate_feed.py`; `sitemap.xml` is generated by `code/orchestrators/build_sitemap.py`.
- `data/reconciliation.json` and `reports/reconciliation_2026-05-15.md` are generated by `code/orchestrators/build_reconciliation_report.py`.
- `data/github-repositories.json` and `repositories.html` are generated by `code/orchestrators/build_github_inventory.py`.
- `reports/public_source_inventory_2026-05-15.json` is generated by `code/orchestrators/refresh_public_source_inventory.py`.
- `search.html` reads `search-index.json`; `opensearch.xml` advertises that search endpoint to browsers and search tools.
- `catalog.html` and `data/catalog.json` are generated by `code/orchestrators/build_catalog.py` as the public DataCatalog layer.
- `GENERATED.md` and `data/generated-manifest.json` are generated by `code/orchestrators/build_generated_manifest.py`; update them whenever generated artifacts or commands change.
- `reports/external_links_2026-05-13.json` is generated by `code/orchestrators/check_external_links.py`; scoped warnings can be bot protection, rate limiting, or link failures and should be triaged before copy changes.
- `reports/external_links_triage_2026-05-13.*` is generated by `code/orchestrators/build_external_link_triage.py`.
- `reports/asset_size_2026-05-13.json` is generated by `code/orchestrators/audit_assets.py`.
- `reports/browser-smoke/2026-05-13/` is generated by `code/orchestrators/browser_smoke.py`.
- `reports/live_site_verification_2026-05-13.json` is generated by `code/orchestrators/verify_live_site.py`; live failures can simply mean GitHub Pages is still building or CDN caches are stale.
- `reports/accessibility_static_2026-05-13.json` is generated by `code/orchestrators/accessibility_audit.py`; `reports/visual-qa/2026-05-13/` is generated by `code/orchestrators/visual_qa.py`.
- `reports/public_source_snapshot_*.json` are generated by `code/orchestrators/refresh_public_sources.py`; they are freshness reports, not automatic claim changes.
- Verified software-release anchors: GNN software DOI `10.5281/zenodo.19600217`; Journal-Utilities v0.1.0 DOI `10.5281/zenodo.18686966`.
- Python tooling for the repo lives under `code/`; automated checks use `pytest` in `code/tests`, and repository validation uses `code/orchestrators/validate_repo.py`.

## Imported Claude Cowork project instructions

Diligent public open source
