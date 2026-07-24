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

- Treat [`TODO.md`](TODO.md) as the active backlog: each unfinished item has a
  stable ID, priority, owner, trigger, deliverable, acceptance criteria, and
  dependencies. Completed work belongs in `CHANGELOG.md`, release snapshots,
  and dated reports.
- Runs [regenerate_docs.py](code/orchestrators/regenerate_docs.py) to rebuild documentation
- Runs [sync_publications_html.py](code/orchestrators/sync_publications_html.py) with `--apply` after edits to the unified bibliography table so [publications.html](publications.html) stays aligned
- Uses [docs/operations/publication-sync.md](docs/operations/publication-sync.md) and [sync_paired_publications.py](code/orchestrators/sync_paired_publications.py) to check GitHub releases against Zenodo records, apply strong publication pairs, and leave ambiguous pairs for review
- Runs [sync_software_html.py](code/orchestrators/sync_software_html.py) with `--apply` after edits to [pages/SOFTWARE.md](pages/SOFTWARE.md) so [software.html](software.html) and [data/software-ld.json](data/software-ld.json) stay aligned
- Runs [build_resume.py](code/orchestrators/build_resume.py) with `--all` after edits to [resume/source.json](resume/source.json), bibliography/software data, Scholar metrics, or claim data so [data/resume.json](data/resume.json), plaintext variants, and [resume/resume.pdf](resume/resume.pdf) stay aligned
- Validates documentation completeness across all paper folders (see [`papers/README.md`](papers/README.md), [`pages/BIBLIOGRAPHY.md`](pages/BIBLIOGRAPHY.md), and the generated [`reports/current_counts.md`](reports/current_counts.md) snapshot)
- Ensures consistent formatting and accurate metadata
- Manages the documentation generation pipeline
- Runs the ordered `regenerate_all.py` pipeline so coverage exceptions,
  repository classification, Pages artifact metadata, release integrity, and
  generated manifests stay aligned.

### 🖥️ WEB DEVELOPER

- Maintains the site-wide interactive layer: [js/tts-controls.js](js/tts-controls.js) (Web Speech API text-to-speech), [js/interactive.js](js/interactive.js) (reading progress bar, scroll-to-top, keyboard shortcuts overlay, search autocomplete, section anchor links, nav-toggle, tab-switcher, publication filters, art gallery controls, video controls), and [js/menu-esc.js](js/menu-esc.js) (menu Escape-to-close handler)
- Ensures every indexable HTML page includes both TTS + interactive + menu-esc script tags
- **CSP compliance**: all pages deploy a `<meta http-equiv="Content-Security-Policy">` tag with `script-src 'self'` — no inline event handlers (`onclick=`, `onchange=`, etc.) or inline `<script>` blocks are permitted. Use `code/orchestrators/deploy_seo_security.py` to add CSP/rel-me/hreflang to new pages and `code/orchestrators/migrate_inline_handlers.py` to convert inline handlers to `data-*` attributes
- Guards SEO invariants: canonical URLs, JSON-LD structured data (BreadcrumbList, Person, WebSite, WebPage, ProfessionalService), OG/Twitter meta, resource hints, `rel="me"`, `hreflang`
- Maintains PWA readiness: service worker ([sw.js](sw.js)), manifest ([manifest.json](manifest.json)), cache strategy
- Keeps the design system documentation ([docs/design/](docs/design/)) in sync with [style.css](style.css)
- Runs [code/orchestrators/accessibility_audit.py](code/orchestrators/accessibility_audit.py) (16 checks including `no_inline_handlers`) and [code/orchestrators/validate_repo.py](code/orchestrators/validate_repo.py) to gate SEO + a11y + generated-layer correctness

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
├── AGENTS.md          ← This file: active agent roles and operating rules
├── CHANGELOG.md       ← Human-readable summary of notable public-index, website, bibliography, and discovery-layer changes
├── index.html         ← GitHub Pages landing page with SEO and structured data
├── discovery.html     ← Canonical HTML discovery map for public-source APIs and identifiers
├── search.html        ← Human-facing search over works, software, pages, people, organizations, and claims
├── repositories.html  ← Generated full public GitHub repository inventory for docxology and AII
├── opensearch.xml     ← Browser/search-engine descriptor for site search
├── catalog.html       ← Schema.org DataCatalog page for public data exports
├── updates.html       ← Generated human-readable changelog page (HTML rendering of CHANGELOG.md)
├── exports.html       ← Generated HTML hub for citation/JSON exports
├── cite-verify.html   ← Citation and evidence layer: preferred citation, public identifiers, source-of-truth rules
├── evidence.html      ← Claim ledger: dated, sourced verification status for load-bearing claims
├── domains.html       ← Research-domain landing page index
├── domain-*.html      ← Domain-specific HTML pages for major research clusters
├── works/             ← Generated per-work HTML landing pages for each bibliography row
├── publications.html  ← Canonical HTML target for unified bibliography
├── software.html      ← Canonical HTML target for software catalog
├── collaborators.html ← Canonical HTML target for institutional network
├── media.html         ← Canonical HTML target for podcast/video appearances
├── art.html           ← Art gallery landing page (client-side rendered from data/artworks.json)
├── art/               ← Local copies of gallery artwork images
├── videos.html        ← Video/talks landing page
├── videos/            ← Generated per-video HTML landing pages
├── blog/              ← Hand-authored long-form writing (index.html plus per-post folders)
├── about.html         ← Short About page
├── style.css          ← Unified custom CSS core
├── sitemap.xml        ← SEO sitemap
├── robots.txt         ← Robot exclusion file
├── llms.txt           ← Agent-facing source map and source-of-truth rules
├── search-index.json  ← Generated site-wide search index
├── feed.xml           ← RSS feed for recent works and site updates
├── GENERATED.md       ← Generated-file manifest with source-to-output rebuild commands
├── TODO.md             ← Hand-maintained unfinished backlog; no completed history
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
│   ├── operations/    ← Runbooks (publication-sync.md: GitHub + Zenodo intake; maintenance-log.md: historical record)
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

## Maintenance history

The completed maintenance record is kept in [docs/operations/maintenance-log.md](docs/operations/maintenance-log.md) and [CHANGELOG.md](CHANGELOG.md). Keep this file focused on active operating rules; open the on-demand history when investigating a prior change.

---

## Active operating preferences

- Keep the entire public site crawlable: `robots.txt` uses `Allow: /` with no `Disallow` rules; index discipline via sitemap + canonicals + targeted `noindex` on redirect stubs—not robots blocking.
- Bibliography primary index target: `works/{citation_key}.html`; `papers/{folder}/` pages use `noindex, follow` with canonical to the matching work page.
- Prefer apex site URLs `https://danielarifriedman.com/` for HTML canonicals, `og:url`, and sitemap `loc` entries so they match `CNAME` and reduce www/apex mismatch issues in Search Console.
- Omit redirect-only stub pages from `sitemap.xml` when their canonical is the homepage; keep the stub files for inbound links but avoid listing them so crawl signals are not contradictory.
- Keep Wikidata anchored on `https://www.wikidata.org/wiki/Q138781444`: Person JSON-LD in `index.html` must list this URL first in `sameAs`, and body copy (`rel="me"`), `README.md` snippets, LINKS/WIKIPEDIA tables, and anywhere else must use **Q138781444** rather than merged duplicate **Q85887463**.
- After Google Scholar metrics change, update `data/scholar-snapshot.json`, run `code/orchestrators/sync_scholar_metrics.py`, and regenerate claim/resume/public outputs; keep hand-authored docs pointed at the snapshot instead of repeating the current count.
- Homepage teaching blurbs: BIOL-1 General Biology — College of the Redwoods, Pelican Bay, Spring 2026; BIOL-8 — Human Biology, College of the Redwoods, Spring 2026.
- AII Textbook Group site copy: 10 cohorts through 2026; link the Parr/Pezzulo/Friston MIT Press OA monograph and the Namjoshi Fundamentals monograph as in the Educator line.
- On SEO passes for `index.html`, remove legacy Twitter card meta and drop Twitter from Person `sameAs` when the user requests a Twitter-free head.
- After substantive repo edits, run `uv run python3 -m pytest code/tests -q` (Python via `uv`) to confirm the suite still passes.
- Prefer full-catalog regeneration of `software.html` from `pages/SOFTWARE.md` (all owned + AII catalog rows, not a highlight subset), mirroring the publications.html / `sync_publications_html.py` pattern.

## Learned Workspace Facts

- Repo `docxology/docxology` powers the profile site; GitHub Pages custom domain in root `CNAME` is `danielarifriedman.com` (apex, no `www`).
- **Volatile totals** (works count, indexed paper-folder count, Type-column breakdowns, domain breakdowns, software catalog counts, and public GitHub inventory counts): generated/plaintext summary lives in [`reports/current_counts.md`](reports/current_counts.md), backed by `data/current-counts.json`. Hand-authored docs should link there, to `pages/BIBLIOGRAPHY.md`, `papers/README.md`, `pages/SOFTWARE.md`, and `data/github-repositories.json`, instead of repeating current values. `code/src/count_consistency.py` and `code/orchestrators/build_current_counts.py --check` are run by `validate_repo.py`.
- Regenerate `publications.html` head meta and `data/publications-ld.json` (**mainEntity**) from `pages/BIBLIOGRAPHY.md` via `code/orchestrators/sync_publications_html.py --apply` after table edits; catalog UI loads `data/works.json` via `js/publications.js`. Run `export_bibliography.py` when works.json must refresh. The **INTEGRATOR** role in `papers/AGENTS.md` keeps publications surfaces aligned when totals change.
- Regenerate `software.html` repo grids and `data/software-ld.json` (**mainEntity**) from `pages/SOFTWARE.md` via `code/orchestrators/sync_software_html.py --apply` after catalog edits; run `export_agent_data.py` for `data/software.json`. Full-catalog sync, not a highlight subset.
- `discovery.html` is the canonical website discovery HTML; pair with `pages/DISCOVERY.md`, `llms.txt`, and `exports.html` (citation/JSON export hub in sitemap and nav). Machine-readable citations/software: `CITATION.cff` and `codemeta.json`.
- `code/src/sitemap_policy.py` defines the current index-priority URL set for `sitemap.xml` and IndexNow (promotion list, not crawl gate). `code/orchestrators/submit_indexnow.py` and `.github/workflows/indexnow-on-push.yml` handle IndexNow. `GENERATED.md` and `data/generated-manifest.json` from `build_generated_manifest.py` map generated outputs—refresh when pipelines change.
- Google Search Console operations (sitemap resubmit, URL inspection) require a signed-in browser—no GSC API in the repo.
- **Google Scholar** single source of truth: `data/scholar-snapshot.json`, propagated by `code/orchestrators/sync_scholar_metrics.py` (idempotent; `--check` exits 1 on drift). `export_agent_data.py` reads the snapshot for claims. Publish only after a **direct** (non-anonymous/non-cached UI) Scholar verify: update snapshot (`as_of`, `method`, append to `history`), run the sync orchestrator, regenerate `data/claims.json` and the evidence page; never publish a citation count above the latest direct-fetch value. Public metrics use profile `DXjPFtYAAAAJ`; ORCID also links `Y2bMf3MAAAAJ`—consolidate to avoid split graphs.
- `ActiveInferenceInstitute` on GitHub is a **User** account (use `https://api.github.com/users/ActiveInferenceInstitute`, not `/orgs/...`); recorded in `organizations.json` as `github_account_type: user`.
- Independent anchors: AII **EIN 88-2985125** (see [ProPublica Nonprofit Explorer](https://projects.propublica.org/nonprofits/organizations/882985125)); NSF PRFB **DBI-2010290** (Grantome/NSF record; budgeted 2020–2022, describe 2023 as no-cost extension not a funded year). `pages/VERIFICATION_LOG.md` + `data/verification-log.json` record the 2026-05-16 multi-source pass and should stay paired when updated.
- College of the Redwoods Spring-2026 teaching (BIOL-1 at Pelican Bay; BIOL-8 Human Biology) is **principal-confirmed instructor-of-record**; do not remove or soften because a public WebAdvisor schedule is not yet visible.
- Python tooling under `code/`; run `uv run python3 -m pytest code/tests -q` and validate with `code/orchestrators/validate_repo.py`. Repo-wide **reports** may fail or warn for CDN latency or bot protection—triage before rewriting site copy. Representative Zenodo anchors: GNN `10.5281/zenodo.19600217`, Journal-Utilities `10.5281/zenodo.18686966`.
