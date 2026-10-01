---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "Reproducible Literature Synthesis with infrastructure/search and infrastructure/reference"
description: "This paper documents template_search_project, the literature-search exemplar shipped with the Research Project Template (https://github.com/docxology/template). The project demonstrates two configurable, reproducible pipelines sharing the same config..."
tags: ["literature-search", "automated-reference-management", "bibtex", "reproducible-research", "local-llm-synthesis"]
domain: "Computational"
citation: "Daniel Ari Friedman (2026). *Reproducible Literature Synthesis with infrastructure/search and infrastructure/reference*. Zenodo."
doi: "10.5281/zenodo.21298894"
---

# Reproducible Literature Synthesis with infrastructure/search and infrastructure/reference

**Daniel Ari Friedman** (2026) · Computational

## Context

This work addresses topics in **Computational**: literature search, automated reference management, BibTeX, reproducible research.

## Methods

Primary methods and techniques applied in this work:

- **Multi-backend literature search with DOI/arXiv/title deduplication** — Queries configured backends (arXiv, Crossref, local corpora, optional Paperclip) and merges duplicates by DOI, then arXiv id, then title and year.
- **Deterministic SHA-256-keyed JSON search cache** — Writes one cache file per query, named by a hash of the canonical query identity, so identical reruns become file reads.
- **Abstract and PDF full-text enrichment with on-disk caching** — AbstractFetcher caches arXiv abstracts; FulltextFetcher downloads PDFs and extracts text with pypdf under stable per-paper identifiers.
- **BibTeX export matching the template's house references.bib format** — Converts each paper into a BibEntry with convention-based citation keys and venue-routed entry types, written in a fixed house format.
- **Per-paper and corpus LLM synthesis via local Ollama with pinned seed** — Two LLM passes produce structured per-paper notes and thematic corpus synthesis, run with seed 42 and temperature 0.0.

## Key Findings

Core contributions and results:

- In the reported run, the query "reproducible research optimization" against the local backend returned 6 deduplicated papers (4 with a DOI, 6 with an abstract) and no backend errors.
- A second run with identical config produces byte-identical artifacts apart from cache timestamps, which the paper calls the property it exists to demonstrate.
- Results from live arXiv and Crossref are not reproducible across weeks; strict reproducibility requires pinning a local corpus, committing the cache, and pinning the LLM seed.
- The paper states its contribution is not a new algorithm but a demonstration that a reproducible literature workflow can be built from existing template infrastructure with no mocks and a single YAML config.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

See [BIBLIOGRAPHY.md](../../pages/BIBLIOGRAPHY.md) for related publications.

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.21298894
- PDF SHA-256: See zenodo_record
- Pairing confidence: unknown
- Last checked: 2026-07-10T19:31:12Z

## Prerequisites

- Familiarity with literature search, automated reference management, BibTeX
- Background in Computational fundamentals
- Access to source repository: N/A

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.21298894`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
