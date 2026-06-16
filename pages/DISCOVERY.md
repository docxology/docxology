---
title: "DISCOVERY - Daniel Ari Friedman"
description: "Public-source discovery map for Daniel Ari Friedman: canonical IDs, APIs, search queries, and verification notes."
keywords: "Daniel Ari Friedman, discovery, ORCID, PubMed, Zenodo, GitHub, research graph"
---
<div align="center">

# Discovery Map — Daniel Ari Friedman, PhD

> **Navigation**: [🏠 Home](../README.md) | [📚 Bibliography](BIBLIOGRAPHY.md) | [💻 Software](SOFTWARE.md) | [🔗 Links](LINKS.md) | [🧭 Discovery](DISCOVERY.md) | [👤 Profile](PROFILE.md) | [🤝 Collaborators](COLLABORATORS.md) | [🎥 Media](MEDIA.md) | [📺 Videos](VIDEOS.md) | [📦 Resources](RESOURCES.md) | [📖 Wikipedia](WIKIPEDIA.md)

**Machine-readable public-source map for agents, search engines, and researchers**

*Last updated: 2026-06-09 from public APIs and official profile pages*

[Website version](../discovery.html) · [Search](../search.html) · [Data catalog](../catalog.html) · [Updates](../updates.html) · [Curated bibliography](../publications.html) · [All links](LINKS.md)

</div>

---

## Canonical Identity Anchors

| Source | Link | Use |
|--------|------|-----|
| Wikidata | [Q138781444](https://www.wikidata.org/wiki/Q138781444) | Canonical entity anchor for knowledge graph reconciliation |
| ORCID | [0000-0001-6232-9096](https://orcid.org/0000-0001-6232-9096) | Persistent researcher identifier; public record currently groups 20 works |
| Google Scholar | [DXjPFtYAAAAJ](https://scholar.google.com/citations?user=DXjPFtYAAAAJ&hl=en) | **Canonical** citation profile. Metrics recorded as a dated snapshot in [`data/scholar-snapshot.json`](../data/scholar-snapshot.json) (764 citations, h-index 15, i10-index 17, as of 2026-05-16; direct dual-fetch). A secondary Scholar profile (`Y2bMf3MAAAAJ`) is linked from ORCID and should be consolidated/disambiguated — do not mix metrics across the two. |
| GitHub | [@docxology](https://github.com/docxology) | Primary software profile; latest generated API snapshot and public repo count are recorded in [`../reports/current_counts.md`](../reports/current_counts.md) and [`../data/github-repositories.json`](../data/github-repositories.json) |
| Main Site | [danielarifriedman.com](https://danielarifriedman.com/) | Canonical public homepage and SEO target |

## Research Indexes

| Index | Link | Notes |
|-------|------|-------|
| PubMed | [Daniel Ari Friedman author search](https://pubmed.ncbi.nlm.nih.gov/?term=Daniel+Ari+Friedman%5BAuthor%5D) | NCBI E-utilities returned 8 records for the exact author query on 2026-06-09 |
| Europe PMC | [Daniel Ari Friedman author search](https://europepmc.org/search?query=AUTH:%22Daniel%20Ari%20Friedman%22) | Europe PMC returned 10 exact-author results, including preprints, on 2026-06-09 |
| Crossref API | [ORCID DOI records](https://api.crossref.org/works?filter=orcid:0000-0001-6232-9096) | Crossref returned 15 DOI records attached to the ORCID on 2026-06-09 |
| Zenodo | [Exact-name creator search](https://zenodo.org/search?q=metadata.creators.person_or_org.name%3A%22Friedman%2C%20Daniel%20Ari%22) | Zenodo returned 40 exact-name records on 2026-06-09 |
| Zenodo API | [ORCID-linked records](https://zenodo.org/api/records?q=metadata.creators.person_or_org.identifiers.identifier%3A%220000-0001-6232-9096%22) | ORCID-linked query returned 98 records on 2026-06-09, including versioned deposits and software archives |
| Semantic Scholar | [Exact-name search](https://www.semanticscholar.org/search?q=%22Daniel%20Ari%20Friedman%22&sort=relevance) | AI-curated citation graph; verify candidate author merges before using as profile evidence |
| DBLP | [Author page](https://dblp.org/pid/346/2173.html) | Computer-science bibliography mirror |
| PubMed Central / NCBI | [PubMed query](https://pubmed.ncbi.nlm.nih.gov/?term=Daniel+Ari+Friedman%5BAuthor%5D) | Use for biomedical indexing and PMID lookup |

## Verified Software Releases

| Release | Link | Notes |
|---------|------|-------|
| GeneralizedNotationNotation (GNN) | [10.5281/zenodo.19600217](https://doi.org/10.5281/zenodo.19600217) | Zenodo software record found in exact-name creator search; keep distinct from the GNN paper row |
| Journal-Utilities v0.1.0 | [10.5281/zenodo.18686966](https://doi.org/10.5281/zenodo.18686966) | Active Inference Institute video-processing software release; authors include Active Inference Institute and Daniel Ari Friedman |
| docxology/template v3.3.0 | [10.5281/zenodo.20584820](https://doi.org/10.5281/zenodo.20584820) | Latest Zenodo software/version metadata for the research template repository; keep distinct from bibliography work rows |

## Software & Organization APIs

| Source | Link | Notes |
|--------|------|-------|
| GitHub API — docxology | [api.github.com/users/docxology](https://api.github.com/users/docxology) | Public repo count, profile timestamps, and profile metadata |
| GitHub API — AII | [api.github.com/users/ActiveInferenceInstitute](https://api.github.com/users/ActiveInferenceInstitute) | Latest generated API snapshot and local catalog count are recorded in [`../reports/current_counts.md`](../reports/current_counts.md) and [`../data/github-repositories.json`](../data/github-repositories.json). **Note:** the `ActiveInferenceInstitute` account is a GitHub **User**, not an Organization — use `/users/`; `/orgs/ActiveInferenceInstitute` returns 404. |
| AII public landing page | [activeinference.org](https://activeinference.org/) | Current public landing page; governance/source pages remain on activeinference.institute |
| GitHub Search | [docxology repositories](https://github.com/docxology?tab=repositories) | Human-browsable repository list including forks and profile repos |
| AII GitHub | [ActiveInferenceInstitute](https://github.com/ActiveInferenceInstitute) | Institute software and educational repositories |
| AII Wikidata | [Q139600792](https://www.wikidata.org/wiki/Q139600792) | Organization knowledge-graph anchor; useful for reconciliation, but currently lightly referenced |
| LLMs.txt | [llms.txt](../llms.txt) | Compact agent-facing map of canonical pages and source-of-truth rules |
| Human search | [search.html](../search.html) | Browser search over works, software, pages, people, organizations, and claims |
| OpenSearch | [opensearch.xml](../opensearch.xml) | Browser/search-engine descriptor for site search |
| Agent start guide | [AGENT_START.md](../AGENT_START.md) | Task recipes for agents using the repository |
| CodeMeta | [codemeta.json](../codemeta.json) | Machine-readable software/source metadata for repository indexes |
| Citation metadata | [CITATION.cff](../CITATION.cff) | Machine-readable citation metadata for this public research index |
| Data catalog | [catalog.html](../catalog.html) / [data/catalog.json](../data/catalog.json) | Schema.org DataCatalog for public JSON, citation, and report exports |
| Works JSON | [data/works.json](../data/works.json) | Structured export of the 168-work bibliography |
| Software JSON | [data/software.json](../data/software.json) | Structured export of the curated software catalog; current count is in [`../reports/current_counts.md`](../reports/current_counts.md) |
| GitHub repository inventory | [repositories.html](../repositories.html) / [data/github-repositories.json](../data/github-repositories.json) | Generated full public repository inventory, including forks and uncataloged repos; current owner counts are in [`../reports/current_counts.md`](../reports/current_counts.md) |
| People JSON | [data/people.json](../data/people.json) | Compact people index for agentic context |
| Organizations JSON | [data/organizations.json](../data/organizations.json) | Compact organization index for agentic context |
| Claims JSON | [data/claims.json](../data/claims.json) | Evidence ledger data for key public claims |
| Reconciliation JSON | [data/reconciliation.json](../data/reconciliation.json) | Curated-local vs public-index count comparison |
| Search index | [search-index.json](../search-index.json) | Lightweight site-wide index for works, software, people, organizations, pages, and claims |
| Work enrichment JSON | [data/work-enrichment.json](../data/work-enrichment.json) | Extracted abstracts, keywords, methods, and findings used by generated work pages and search |
| RSS feed | [feed.xml](../feed.xml) | Recent work and site-update feed |
| Per-work pages | [works/](../works/) | Generated HTML pages for individual bibliography entries |
| Generated-file manifest | [GENERATED.md](../GENERATED.md) / [data/generated-manifest.json](../data/generated-manifest.json) | Rebuild commands and source-to-output mapping for generated artifacts |
| Updates | [updates.html](../updates.html) / [CHANGELOG.md](../CHANGELOG.md) | Human-facing update history and source changelog |
| Humans / security | [humans.txt](../humans.txt) / [security.txt](../.well-known/security.txt) | Contact, credits, and responsible disclosure metadata |
| Public-source snapshot | [reports/public_source_snapshot_2026-06-09.json](../reports/public_source_snapshot_2026-06-09.json) | Latest public API freshness report |
| Public-source inventory | [reports/public_source_inventory_2026-06-09.json](../reports/public_source_inventory_2026-06-09.json) | Paginated public-source inventory for ORCID, Crossref, PubMed, Europe PMC, Zenodo, Wikidata, Semantic Scholar, GitHub, and AII pages |
| Reconciliation report | [reports/reconciliation_2026-06-09.md](../reports/reconciliation_2026-06-09.md) | Human-readable comparison of curated counts and public-source counts |
| External-link report | [reports/external_links_2026-05-15.json](../reports/external_links_2026-05-15.json) | Cached scoped network check for site-critical outbound links |
| External-link triage | [reports/external_links_triage_2026-05-15.md](../reports/external_links_triage_2026-05-15.md) | Categorized link warnings: bot-protected, transient, timeout, stale, and review |
| Live-site verification | [reports/live_site_verification_2026-05-15.json](../reports/live_site_verification_2026-05-15.json) | Deployed-site checks for expected markers, CDN headers, and GitHub Pages status |
| Asset-size audit | [reports/asset_size_2026-06-09.json](../reports/asset_size_2026-06-09.json) | Size budget report for public assets and generated exports |
| Static accessibility report | [reports/accessibility_static_2026-06-09.json](../reports/accessibility_static_2026-06-09.json) | Static accessibility checks for root HTML pages |
| Browser smoke manifest | [reports/browser-smoke/2026-05-28/manifest.json](../reports/browser-smoke/2026-05-28/manifest.json) | Browser-rendered smoke screenshots for high-priority pages |
| Visual QA manifest | [reports/visual-qa/2026-05-28/manifest.json](../reports/visual-qa/2026-05-28/manifest.json) | Playwright screenshot manifest for key pages and mobile/desktop viewports |
| Citation exports | [BibTeX](../bibliography.bib) · [CSL JSON](../bibliography.csl.json) · [RIS](../bibliography.ris) | Citation-manager formats generated from `BIBLIOGRAPHY.md` |

## Official Organization Pages

| Page | Link | Verification Use |
|------|------|------------------|
| AII public landing page | [activeinference.org](https://activeinference.org/) | Current public landing page |
| AII Officers | [activeinference.institute/officers](https://www.activeinference.institute/officers) | Confirms Daniel Friedman as President and Treasurer |
| AII Board | [activeinference.institute/board-of-directors](https://www.activeinference.institute/board-of-directors) | Current board roster and governance notes |
| AII Scientific Advisory Board | [activeinference.institute/scientific-advisory-board](https://www.activeinference.institute/scientific-advisory-board) | 2026 SAB cohort and prior advisory-board context |
| AII Textbook Group | [activeinference.institute/textbook-group](https://www.activeinference.institute/textbook-group) | Program context for textbook cohorts |
| AII Livestreams | [activeinference.institute/livestreams](https://www.activeinference.institute/livestreams) | Institute video and educational session context |

## Query Recipes

Use these queries when refreshing the repository:

```text
"Daniel Ari Friedman" ORCID
"Daniel Ari Friedman" "Active Inference Institute"
"Daniel Ari Friedman" "Pogonomyrmex"
"Daniel Ari Friedman" "Curio Cards"
"Daniel Ari Friedman" Zenodo
"Daniel Ari Friedman" PubMed
"Daniel Ari Friedman" "Journal-Utilities"
"Active Inference Institute" Wikidata
site:activeinference.institute "Daniel Friedman"
site:github.com/docxology "Daniel Ari Friedman"
```

## Verification Notes

- Treat [`pages/BIBLIOGRAPHY.md`](BIBLIOGRAPHY.md) as the curated publication source of truth for this repository.
- Treat public APIs as freshness checks, not replacements for the curated bibliography. API counts can include duplicate versions, software archives, preprints, or name-variant merges.
- Treat Wikidata as a useful entity anchor, not proof by itself; reconcile lightly referenced statements against official pages or primary records before importing them as claims.
- OpenAlex search currently returns ORCID-linked and name-variant results that may be over-merged; use it cautiously and reconcile against ORCID, DOI, and the local bibliography before importing claims.
- Google Scholar citation counts can vary by cache and access path; update site-wide citation metrics only after a deliberate manual sync.

---

<div align="center">

*Part of [docxology/docxology](https://github.com/docxology/docxology) — See [LINKS.md](LINKS.md) for public profile links and [BIBLIOGRAPHY.md](BIBLIOGRAPHY.md) for the curated work catalog*

</div>
