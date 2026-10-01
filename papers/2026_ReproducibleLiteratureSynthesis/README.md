<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 Reproducible Literature Synthesis with infrastructure/search and infrastructure/reference

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21298894-blue)](https://doi.org/10.5281/zenodo.21298894)

---

## Abstract

> This paper documents template_search_project, the literature-search exemplar shipped with the Research Project Template (https://github.com/docxology/template). The project demonstrates two configurable, reproducible pipelines sharing the same configuration file and the same infrastructure/search/ + infrastructure/reference/ modules. The standard pipeline (scripts/run_search_pipeline.py) handles...

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
