<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 Reproducible Literature Synthesis with infrastructure/search and infrastructure/reference

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21298894-blue)](https://doi.org/10.5281/zenodo.21298894)

---

## Abstract

> This paper documents template_search_project, the literature-search exemplar shipped with the Research Project Template (https://github.com/docxology/template). The project demonstrates two configurable, reproducible pipelines sharing the same configuration file and the same infrastructure/search/ + infrastructure/reference/ modules. The standard pipeline (scripts/run_search_pipeline.py) handles a single SearchQuery end-to-end. The deep-search pipeline (scripts/run_deep_search.py, see ) fans out across a list of keywords (each capped at 100 papers per keyword from deep_search.max_results_per_keyword in manuscript/config.yaml), fully enriches every paper with its abstract and PDF fulltext, and (optionally) uses the local LLM to write a multi-section reading note for every paper. When a deep-search aggregate exists, the latest run covered 3 keyword(s) with unique paper(s) after cross-keyword deduplication. Both turn a free-text topic into: 1. a deduplicated, year-filtered set of papers drawn from arXiv, Crossref, optional local corpora, and (opt-in) Paperclip (https://paperclip.gxl.ai/); 2. a Pandoc-compatible references.bib byte-identical in style to the canonical exemplar in template_code_project (../../template_code_project/manuscript/references.bib) (file manuscript/references.bib); 3. cached abstracts and (optionally) extracted PDF full text, written to disk under stable per-paper identifiers; and 4. an LLM-synthesised reading report assembled from per-paper analyses and a cross-corpus thematic synthesis, all produced by a local Ollama model with pinned seed and temperature. All discovery logic lives in infrastructure/search/literature/ (source on GitHub (https://github.com/docxology/template/tree/main/infrastructure/search/literature)); all export logic lives in infrastructure/reference/citation/ (source on GitHub (https://github.com/docxology/template/tree/main/infrastructure/reference/citation)); LLM synthesis reuses the existing infrastructure/llm/ (source on GitHub (https://github.com/docxology/template/tree/main/infrastructure/llm)) bridge. The project itself contains only thin orchestration, manuscript prose, and a test suite — perfectly mirroring the two-layer architecture the template enforces. The motivating concern is reproducibility: a query at time $t_0$ should produce the same results at time $t_1$ unless the cache is explicitly invalidated. This is achieved by deterministic search caching keyed on canonical query identity, on-disk caching of every fetched abstract / PDF, and pinned LLM seeds. The same manuscript/config.yaml that drives the pipeline is also the only configuration any reviewer needs. Run snapshot. With the bundled manuscript/config.yaml, the most recent pipeline execution evaluated the query "reproducible research optimization" against local, returned 6 deduplicated paper(s) (4 carrying a DOI, 6 carrying an abstract), and recorded backend errors: none. Resolve `{{…}} tokens by running scripts/z_generate_manuscript_variables.py after run_search_pipeline.py; the script writes output/data/manuscript_variables.json and resolved markdown under output/manuscript/`, which the PDF-rendering stage prefers when present. Keywords: literature search, BibTeX automation, reproducible research, local LLM synthesis, scientific infrastructure

## Keywords

`literature search` · `automated reference management` · `BibTeX` · `reproducible research` · `local LLM synthesis`

## Methods

- **Multi-backend literature search with DOI/arXiv/title deduplication** — Queries configured backends (arXiv, Crossref, local corpora, optional Paperclip) and merges duplicates by DOI, then arXiv id, then title and year.
- **Deterministic SHA-256-keyed JSON search cache** — Writes one cache file per query, named by a hash of the canonical query identity, so identical reruns become file reads.
- **Abstract and PDF full-text enrichment with on-disk caching** — AbstractFetcher caches arXiv abstracts; FulltextFetcher downloads PDFs and extracts text with pypdf under stable per-paper identifiers.
- **BibTeX export matching the template's house references.bib format** — Converts each paper into a BibEntry with convention-based citation keys and venue-routed entry types, written in a fixed house format.
- **Per-paper and corpus LLM synthesis via local Ollama with pinned seed** — Two LLM passes produce structured per-paper notes and thematic corpus synthesis, run with seed 42 and temperature 0.0.

## Key Findings

- In the reported run, the query "reproducible research optimization" against the local backend returned 6 deduplicated papers (4 with a DOI, 6 with an abstract) and no backend errors.
- A second run with identical config produces byte-identical artifacts apart from cache timestamps, which the paper calls the property it exists to demonstrate.
- Results from live arXiv and Crossref are not reproducible across weeks; strict reproducibility requires pinning a local corpus, committing the cache, and pinning the LLM seed.
- The paper states its contribution is not a new algorithm but a demonstration that a reproducible literature workflow can be built from existing template infrastructure with no mocks and a single YAML config.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.5281/zenodo.21298894](https://doi.org/10.5281/zenodo.21298894)
- Zenodo record: [https://zenodo.org/records/21298894](https://zenodo.org/records/21298894)
- PDF: [Friedman_2026_Reproducible_003aed0d.pdf](Friedman_2026_Reproducible_003aed0d.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/21298894)

## Citation

> Daniel Ari Friedman (2026). *Reproducible Literature Synthesis with infrastructure/search and infrastructure/reference*. Zenodo. DOI: 10.5281/zenodo.21298894. URL: https://doi.org/10.5281/zenodo.21298894.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
