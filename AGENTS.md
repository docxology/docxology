# AGENTS.md — docxology

**Repository**: [docxology/docxology](https://github.com/docxology/docxology)
**Purpose**: Master profile repository indexing the unified bibliography, curated software catalog, full generated GitHub inventory, and research documentation across Entomology, Active Inference, Cognitive Security, and Art & Synergetics.

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

- Runs [regenerate_docs.py](code/orchestrators/regenerate_docs.py) to rebuild documentation
- Runs [sync_publications_html.py](code/orchestrators/sync_publications_html.py) with `--apply` after edits to the unified bibliography table so [publications.html](publications.html) stays aligned
- Uses [docs/operations/publication-sync.md](docs/operations/publication-sync.md) and [sync_paired_publications.py](code/orchestrators/sync_paired_publications.py) to check GitHub releases against Zenodo records, apply strong publication pairs, and leave ambiguous pairs for review
- Runs [sync_software_html.py](code/orchestrators/sync_software_html.py) with `--apply` after edits to [pages/SOFTWARE.md](pages/SOFTWARE.md) so [software.html](software.html) and [data/software-ld.json](data/software-ld.json) stay aligned
- Runs [build_resume.py](code/orchestrators/build_resume.py) with `--all` after edits to [resume/source.json](resume/source.json), bibliography/software data, Scholar metrics, or claim data so [data/resume.json](data/resume.json), plaintext variants, and [resume/resume.pdf](resume/resume.pdf) stay aligned
- Validates documentation completeness across all paper folders (see [`papers/README.md`](papers/README.md), [`pages/BIBLIOGRAPHY.md`](pages/BIBLIOGRAPHY.md), and the generated [`reports/current_counts.md`](reports/current_counts.md) snapshot)
- Ensures consistent formatting and accurate metadata
- Manages the documentation generation pipeline

---

## Repository Structure

```text
docxology/
├── README.md          ← Profile page with domain matrix, consulting info, and deep-links
├── pages/BIBLIOGRAPHY.md    ← Unified sortable bibliography source table with DOI links and paper-folder deep-links
├── pages/SOFTWARE.md        ← Curated owned-repo and AII-contribution software catalog
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
├── resume/            ← Structured resume/CV source plus generated plaintext variants and PDF
├── reports/           ← Public-source snapshots, reconciliation reports, link reports, accessibility reports, and visual QA screenshots
├── docs/              ← Documentation for the entire repository (index: docs/README.md; agents: docs/AGENTS.md)
│   ├── operations/    ← Runbooks (publication-sync.md: GitHub + Zenodo intake)
│   ├── seo/           ← canonical-policy.md, gsc-followup.md
│   ├── design/        ← design-system.md
│   ├── security/      ← security-posture.md
│   └── releases/      ← Archived point-in-time release snapshots
├── code/              ← All repository source code and executable orchestrators (see code/AGENTS.md)
│   ├── orchestrators/ ← Runnable orchestrators (regenerate_docs.py, sync_publications_html.py, sync_software_html.py, export_*, build_*)
│   ├── src/           ← Shared libraries/parsers (biblio_table.py 8-column BIBLIOGRAPHY parser, software_table.py, count_consistency.py)
│   └── tests/         ← Test suites and validation tests
└── papers/            ← Per-paper folders (`YYYY_Topic`) for bibliography rows with in-tree documentation
    ├── README.md      ← Papers directory index
    ├── AGENTS.md      ← Papers-level agent roles
    ├── paper_metadata.json
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
| 2026-05-16 | MAINTAINER | Integrity-remediation pass (independent 12-source verification): introduced dated Scholar-metrics snapshot (`data/scholar-snapshot.json`) + `sync_scholar_metrics.py` generator, corrected citation figure 812→**764** (live dual-fetch, as of 2026-05-16) across all surfaces and the claims ledger, replaced the "do not overwrite" caveat with a provenance-envelope rule; added primary-source anchors (AII EIN 88-2985125 / ProPublica / IRS ruling March 2024; NSF award DBI-2010290); clarified officer roster (Mikhailova VP+Secretary 2025–; Knight prior Secretary / current Board); softened unverifiable specifics (Christie's lot first-party-only, SAB "2026 cohort", NSF 2020–2022 budget vs 2023 affiliation, "107 indexed pubs"); fixed dead `nft.html`→`art.html`; noted dual Scholar ID + AII-User-not-Org; synced codomyrmex 127/424→**128/600**; added `pages/VERIFICATION_LOG.md` + `data/verification-log.json` | ✅ |
| 2026-05-26 | MAINTAINER | Thermo-nuclear + web stack pass: count drift guard (`code/src/count_consistency.py`), `publications.html` shell loads `data/works.json` via `js/publications.js`, CollectionPage JSON-LD externalized to `data/publications-ld.json`, `docs/SECURITY.md` + `docs/DESIGN_SYSTEM.md`, shared nav (`code/src/site_nav.py`) on work + domain pages | ✅ |
| 2026-05-26 | ARCHIVIST | Added `2026_BiologyTextbook` (DOI 10.5281/zenodo.20286478); Computational 7→8; Books 3→4; bibliography 116→117 (row 117); paper folders and metadata 109→110; README/AGENTS/SKILL/CITATION.cff/metadata.json; publications + works.json resynced | ✅ |
| 2026-05-26 | INTEGRATOR | Added `papers/software_table.py` + `papers/sync_software_html.py`: full 82-row `software.html` repo grids + `data/software-ld.json` from `pages/SOFTWARE.md`; `biology_textbook` on software surface; SOFTWARE.md subtotal 49→50; domain/work cross-links | ✅ |
| 2026-05-28 | ARCHIVIST | Deduplicated exact-title 2026 Zenodo version supersessions: kept newest DOI records in canonical non-`2` folders, unified bibliography/publications/data works at 125, paper folders at 118, and hardened paired-publication sync against same-title same-repo duplicates | ✅ |
| 2026-05-29 | INTEGRATOR | GSC indexing remediation: `works/*.html` primary canonical; `papers/*/` `noindex` + canonical to works; slim sitemap (~157 index-priority URLs); open `robots.txt`; `exports.html` hub; IndexNow filtered via `indexnow_urls.py`; redirect stubs `noindex`; `nft.html` + winged-snowflake stubs | ✅ |
| 2026-05-29 | MAINTAINER | Added `submit_indexnow.py` orchestrator (bulk GSC-priority POST + per-URL pass); CI workflow delegates to it; tests in `test_submit_indexnow.py` | ✅ |
| 2026-05-29 | MAINTAINER | SEO follow-up: `seo_invariants.py` + validate_repo enforcement; paper pages drop JSON-LD; publications.js links titles to works; IndexNow single bulk POST; dynamic exports.html works count | ✅ |
| 2026-05-29 | INTEGRATOR | Added `docs/GSC_FOLLOWUP.md` manual Search Console runbook + `gsc_followup_preflight.py` + `data/gsc-followup-checklist.json` | ✅ |
| 2026-06-04 | MAINTAINER | Applied four strong GitHub+Zenodo publication pairs (`template_autoscientists`, `ntqr_llm`, `template_newspaper`, `template_textbook`), refreshed represented DOI pairs, added six owned software rows, recorded GitHub API counts in generated reports, and expanded count drift validation across source/generated surfaces | ✅ |
| 2026-06-15 | MAINTAINER | Reconciled COGANT/coasys intake drift: **168 works / 151 paper folders / 91 software** across generated surfaces, sitemap, resume, tests, and guarded narrative pages | ✅ |
| 2026-06-14 | ARCHIVIST | Added DemoCreate/ENTO/GNN-v2.0.0; removed the duplicate CEREBRUM2 work (numbers retired, not renumbered — `validate_rows` now allows gaps); re-pointed the template entry to v3.4.0; reconciled all surfaces to **167 works / 150 folders** | ✅ |
| 2026-06-14 | INTEGRATOR | Hardened work identity without a URL migration: `build_work_pages.py` rejects duplicate `citation_key`; `test_frozen_work_keys.py` freezes every `num→citation_key`; documented `works/{citation_key}.html` as a permanent contract. Modularized `docs/` into topic subdirs + `docs/README.md` index. Guarded 5 previously-unchecked narrative pages (LINKS/PROFILE/WIKIPEDIA/COLLABORATORS/MEDIA, had drifted to 125/154) in `count_consistency`. Added RFC 9116 `security.txt` | ✅ |
| 2026-06-16 | INTEGRATOR | Evergreen volatile totals: narrative pages signpost `reports/current_counts.md`; `count_consistency` + tests derive from bibliography/software parsers; `sync_*_html.py` syncs twitter descriptions with og/meta; index domain cards drop stale per-domain literals | ✅ |
| 2026-06-17 | INTEGRATOR | Added **AGEINT** (`zenodo.20732275`, `docxology/AGEINT` v0.1.0) as work 170 via scoped `sync_paired_publications.py --since 2026-06-16 --apply`; stripped leaked `<p>` HTML from the Zenodo abstract; renumbered `papers/README.md` index to strict 1..152 (closed gap 111 + duplicate 152); reconciled all surfaces to **169 works / 152 paper folders / 91 software**; `validate_repo` + 100 tests green. CEREBRUM (`zenodo.15231156`) and Self-Improvement Agent (`zenodo.20693012`) confirmed as re-versions — update-only, not new rows | ✅ |

---

## Learned User Preferences

- Keep the entire public site crawlable: `robots.txt` uses `Allow: /` with no `Disallow` rules; index discipline via sitemap + canonicals + targeted `noindex` on redirect stubs—not robots blocking.
- Bibliography primary index target: `works/{citation_key}.html`; `papers/{folder}/` pages use `noindex, follow` with canonical to the matching work page.
- Prefer apex site URLs `https://danielarifriedman.com/` for HTML canonicals, `og:url`, and sitemap `loc` entries so they match `CNAME` and reduce www/apex mismatch issues in Search Console.
- Omit redirect-only stub pages from `sitemap.xml` when their canonical is the homepage; keep the stub files for inbound links but avoid listing them so crawl signals are not contradictory.
- Keep Wikidata anchored on `https://www.wikidata.org/wiki/Q138781444`: Person JSON-LD in `index.html` must list this URL first in `sameAs`, and body copy (`rel="me"`), `README.md` snippets, LINKS/WIKIPEDIA tables, and anywhere else must use **Q138781444** rather than merged duplicate **Q85887463**.
- After Google Scholar metrics change, update `data/scholar-snapshot.json`, run `code/orchestrators/sync_scholar_metrics.py`, and regenerate claim/resume/public outputs; keep hand-authored docs pointed at the snapshot instead of repeating the current count.
- Homepage teaching blurbs: BIOL-1 General Biology — College of the Redwoods, Pelican Bay, Spring 2026; BIOL-8 — Human Biology, College of the Redwoods, Spring 2026.
- AII Textbook Group site copy: 10 cohorts through 2026; link the Parr/Pezzulo/Friston MIT Press OA monograph and the Namjoshi Fundamentals monograph as in the Educator line.
- On SEO passes for `index.html`, remove legacy Twitter card meta and drop Twitter from Person `sameAs` when the user requests a Twitter-free head.
- After substantive repo edits, run `uv run pytest` in `code/tests` (Python via `uv`) to confirm the suite still passes.
- Prefer full-catalog regeneration of `software.html` from `pages/SOFTWARE.md` (all owned + AII catalog rows, not a highlight subset), mirroring the publications.html / `sync_publications_html.py` pattern.

## Learned Workspace Facts

- Repo `docxology/docxology` powers the profile site; GitHub Pages custom domain in root `CNAME` is `danielarifriedman.com` (apex, no `www`).
- **Volatile totals** (works count, indexed paper-folder count, Type-column breakdowns, domain breakdowns, software catalog counts, and public GitHub inventory counts): generated/plaintext summary lives in [`reports/current_counts.md`](reports/current_counts.md), backed by `data/current-counts.json`. Hand-authored docs should link there, to `pages/BIBLIOGRAPHY.md`, `papers/README.md`, `pages/SOFTWARE.md`, and `data/github-repositories.json`, instead of repeating current values. `code/src/count_consistency.py` and `code/orchestrators/build_current_counts.py --check` are run by `validate_repo.py`.
- Regenerate `publications.html` head meta and `data/publications-ld.json` (**mainEntity**) from `pages/BIBLIOGRAPHY.md` via `code/orchestrators/sync_publications_html.py --apply` after table edits; catalog UI loads `data/works.json` via `js/publications.js`. Run `export_bibliography.py` when works.json must refresh. The **INTEGRATOR** role in `papers/AGENTS.md` keeps publications surfaces aligned when totals change.
- Regenerate `software.html` repo grids and `data/software-ld.json` (**mainEntity**) from `pages/SOFTWARE.md` via `code/orchestrators/sync_software_html.py --apply` after catalog edits; run `export_agent_data.py` for `data/software.json`. Full-catalog sync, not a highlight subset.
- `discovery.html` is the canonical website discovery HTML; pair with `pages/DISCOVERY.md`, `llms.txt`, and `exports.html` (citation/JSON export hub in sitemap and nav). Machine-readable citations/software: `CITATION.cff` and `codemeta.json`.
- `code/src/sitemap_policy.py` defines ~157 index-priority URLs for `sitemap.xml` and IndexNow (promotion list, not crawl gate). `code/orchestrators/submit_indexnow.py` and `.github/workflows/indexnow-on-push.yml` handle IndexNow. `GENERATED.md` and `data/generated-manifest.json` from `build_generated_manifest.py` map generated outputs—refresh when pipelines change.
- Google Search Console operations (sitemap resubmit, URL inspection) require a signed-in browser—no GSC API in the repo.
- **Google Scholar** single source of truth: `data/scholar-snapshot.json`, propagated by `code/orchestrators/sync_scholar_metrics.py` (idempotent; `--check` exits 1 on drift). `export_agent_data.py` reads the snapshot for claims. Publish only after a **direct** (non-anonymous/non-cached UI) Scholar verify: update snapshot (`as_of`, `method`, append to `history`), run the sync orchestrator, regenerate `data/claims.json` and the evidence page; never publish a citation count above the latest direct-fetch value. Public metrics use profile `DXjPFtYAAAAJ`; ORCID also links `Y2bMf3MAAAAJ`—consolidate to avoid split graphs.
- `ActiveInferenceInstitute` on GitHub is a **User** account (use `https://api.github.com/users/ActiveInferenceInstitute`, not `/orgs/...`); recorded in `organizations.json` as `github_account_type: user`.
- Independent anchors: AII **EIN 88-2985125** (see [ProPublica Nonprofit Explorer](https://projects.propublica.org/nonprofits/organizations/882985125)); NSF PRFB **DBI-2010290** (Grantome/NSF record; budgeted 2020–2022, describe 2023 as no-cost extension not a funded year). `pages/VERIFICATION_LOG.md` + `data/verification-log.json` record the 2026-05-16 multi-source pass and should stay paired when updated.
- College of the Redwoods Spring-2026 teaching (BIOL-1 at Pelican Bay; BIOL-8 Human Biology) is **principal-confirmed instructor-of-record**; do not remove or soften because a public WebAdvisor schedule is not yet visible.
- Python tooling under `code/`; run `uv run pytest` from `code/tests` and validate with `code/orchestrators/validate_repo.py`. Repo-wide **reports** may fail or warn for CDN latency or bot protection—triage before rewriting site copy. Representative Zenodo anchors: GNN `10.5281/zenodo.19600217`, Journal-Utilities `10.5281/zenodo.18686966`.

## Imported Claude Cowork project instructions

Diligent public open source
