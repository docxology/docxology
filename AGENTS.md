# AGENTS.md — docxology

**Repository**: [docxology/docxology](https://github.com/docxology/docxology)
**Purpose**: Master profile repository indexing 100+ publications, 46+ software repositories, and research documentation across Entomology, Active Inference, Cognitive Security, and Art & Synergetics.

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

### 🛠️ MAINTAINER

- Runs [regenerate_docs.py](papers/regenerate_docs.py) to rebuild documentation
- Validates documentation completeness across all 99 paper folders
- Ensures consistent formatting and accurate metadata
- Manages the documentation generation pipeline

---

## Repository Structure

```
docxology/
├── README.md          ← Profile page with domain matrix, consulting info, and deep-links
├── pages/BIBLIOGRAPHY.md    ← Unified sortable table of 107 publications with DOI links
├── pages/SOFTWARE.md        ← 46 owned repos + 31 AII contributions
├── pages/               ← Documentation hub for videos, resources, pathways, and repos
├── pages/LINKS.md           ← Comprehensive directory of all web presences and profiles
├── pages/PROFILE.md         ← Detailed biographical profile (education, research, art, orgs)
├── pages/COLLABORATORS.md   ← Key collaborators and institutional research network
├── pages/MEDIA.md           ← Talks, podcasts, video series, courses, and press coverage
├── AGENTS.md          ← This file: agent roles and maintenance log
├── index.html         ← GitHub Pages landing page with SEO and structured data
├── sitemap.xml        ← SEO sitemap
├── robots.txt         ← Robot exclusion file
├── docs/              ← Documentation for the entire repository
├── code/              ← Repository source code and executable orchestrators
│   ├── orchestrators/ ← Thin orchestrators and pipeline controllers
│   ├── src/           ← Source code and submodules
│   └── tests/         ← Test suites and validation tests
└── papers/            ← 99 per-paper folders
    ├── README.md      ← Papers directory index
    ├── AGENTS.md      ← Papers-level agent roles
    ├── paper_metadata.json
    ├── regenerate_docs.py
    └── Friedman_YYYY_Topic/
        ├── README.md   ← Paper overview, abstract, keywords, citation
        ├── AGENTS.md   ← Paper-specific agent roles and extraction log
        ├── SKILL.md    ← Claude Code-compatible skill definition
        └── *.pdf       ← Source PDF (95/99 available)
```

---

## Maintenance Log

| Date | Agent | Action | Status |
|------|-------|--------|--------|
| 2026-03-08 | ARCHIVIST | Rebuilt pages/BIBLIOGRAPHY.md as unified sortable table (106 entries) | ✅ |
| 2026-03-08 | RESEARCHER | Verified all 99 paper folders have complete documentation | ✅ |
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
| 2026-03-25 | RESEARCHER | 5-round deep Perplexity research audit: verified h-index 15, i10-index 17, 727 citations, 251 GitHub repos | ✅ |
| 2026-03-25 | INTEGRATOR | Added Conor Heins & Tim Verbelen (VERSES AI) to pages/COLLABORATORS.md, pages/PROFILE.md, pages/WIKIPEDIA.md | ✅ |
| 2026-03-25 | ARCHIVIST | Added PubMed, Zenodo links to pages/LINKS.md; added Denise Holt press feature across LINKS/MEDIA | ✅ |
| 2026-03-25 | INTEGRATOR | Updated Scholar badges to 727 across README, BIBLIOGRAPHY, index.html; added h-index/i10-index to PROFILE | ✅ |
| 2026-03-25 | MAINTAINER | Updated sitemap.xml dates, enhanced pages/WIKIPEDIA.md with VERSES AI and first-ETH Christie's detail | ✅ |
| 2026-03-25 | RESEARCHER | Round 2 Perplexity audit: verified AII board (6 members), officers (Mikhailova VP/Secretary 2025+), Delaware incorporation, 501(c)(3) 2024 | ✅ |
| 2026-03-25 | ARCHIVIST | Verified Curio Cards: Card 24 \"Complexity\" (333 copies), Card 25 (222), Card 26 (106); 7 artists; Christie's $1.2M/393 ETH | ✅ |
| 2026-03-25 | INTEGRATOR | Added SAB links (Friston, Ramstead, Albarracin, Fields) to pages/COLLABORATORS.md; citation counts (88, 45, 41, 31 for top papers) | ✅ |
| 2026-03-25 | INTEGRATOR | Added 7 AII pages to pages/LINKS.md (SAB, Strategy, Partnership, Substack, History, Board); CR link; 251 repos | ✅ |
| 2026-03-25 | MAINTAINER | Enriched pages/PROFILE.md with AII programs (Textbook 7 cohorts, Internship, Fellows, Mentorship), Curio Cards art descriptions | ✅ |
| 2026-03-25 | ARCHIVIST | Added paper folder Friedman_2026_ReproducibleResearch (template/ paper, DOI 10.5281/zenodo.19139090); updated BIBLIOGRAPHY to 107 works | ✅ |
| 2026-03-25 | RESEARCHER | Round 3 Perplexity audit: verified COGSEC founding (2018), P3IF affiliations, NM field site, ALIUS team | ✅ |
| 2026-03-25 | INTEGRATOR | Enriched pages/PROFILE.md with COGSEC history, named volumes (IRT-20, NIM-21, CAT-22, ATLAS), and P3IF affiliations | ✅ |
| 2026-03-25 | ARCHIVIST | Updated pages/WIKIPEDIA.md, pages/COLLABORATORS.md (RJ Cordes), and pages/LINKS.md with verified COGSEC & ALIUS details | ✅ |
| 2026-04-01 | MAINTAINER | Established pages/ hub architecture; rigidly verified AGENTS.md and README.md alignments | ✅ |
| 2026-04-01 | MAINTAINER | Migrated all root .md files to pages/; mass-updated 100+ deep-links across papers/ | ✅ |
| 2026-04-01 | INTEGRATOR | Injected YAML frontmatter, navigation headers, and footers across 9 pages/ files | ✅ |
| 2026-04-01 | MAINTAINER | Renamed videos.md/resources.md to VIDEOS.md/RESOURCES.md for naming parity | ✅ |
| 2026-04-01 | INTEGRATOR | Added code/ (orchestrators/, src/, tests/) and docs/ to repository structure | ✅ |
| 2026-04-01 | MAINTAINER | Comprehensive index.html overhaul: WCAG 2.2 (skip-link, ARIA, focus-visible, reduced-motion), ScholarlyArticle/CreativeWork/ItemList JSON-LD schemas, Twitter summary_large_image, PWA manifest, service worker, print styles | ✅ |
| 2026-04-01 | INTEGRATOR | Created pages/README.md hub index with full navigation table | ✅ |
| 2026-04-01 | MAINTAINER | Expanded sitemap.xml (15 URLs: added WIKIPEDIA, VIDEOS, RESOURCES, reordered); enhanced robots.txt with allow/disallow rules | ✅ |
| 2026-04-01 | MAINTAINER | Created manifest.json (PWA) and sw.js (service worker with stale-while-revalidate) | ✅ |
