# A Living Meta-Analysis of the Modafinil Literature

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20931964.svg)](https://doi.org/10.5281/zenodo.20931964)

---

## Abstract

Manual synthesis cannot keep pace with a fast-growing research literature, and ad-hoc
reviews bind no evidence to a reproducible pipeline. We present a configurable,
reproducible meta-analysis framework that takes a single search term and produces a
complete quantitative portrait of its literature. For this instance the term is
Modafinil. The pipeline dispatches across 7 literature
engines (arXiv, OpenAlex, Semantic Scholar, Crossref, PubMed, SovietRxiv, and ChinaRxiv), each degrading gracefully to a skipped source when an API
key or the network is unavailable, then merges and de-duplicates records by a canonical
identifier hierarchy (DOI $&gt;$ arXiv ID $&gt;$ Semantic Scholar ID $&gt;$ OpenAlex ID $&gt;$ title
digest) into a corpus of $N = 2302$ records spanning 2000--2026
(26 years). Records are classified into a configurable 6-bucket
subfield taxonomy (Clinical Sleep, Cognition, Pharmacology, Psychiatry, Safety, and Neuroscience); the largest subfield is Clinical Sleep
(64.3\% of the classified corpus). The corpus grows at a compound annual
rate of 3.45\% (mean year-over-year growth 6.3\%, doubling time
11.3 years), peaking in 2025 with 112 records.

Non-negative matrix factorization extracts 5 latent topics over a
500-feature vocabulary, offline deterministic embeddings place every
title, abstract, and (when available) full text in a shared vector space, and
citation-network analysis exposes the corpus's internal structure (8,772
intra-corpus edges across 2204 nodes, 1377 communities,
graph density 0.18\%). Of 38,802 total outgoing
references, 22.6\% resolve to another record inside the corpus.
Abstract coverage stands at 55.5\%, open-access status is known for
14.4\% of records, and 40.9\% have a direct PDF link. An optional,
LLM-gated knowledge-graph stage scores the 6 hypotheses explored against
the evidence. This run produced 18 publication-quality figures.

Every domain-specific value in this manuscript — the search term, keyword set, engine
roster, subfield taxonomy, and hypotheses — is injected from a single configuration file
and the pipeline's own outputs; re-targeting the configuration re-targets the entire
paper. The result is a reusable architecture for living literature reviews:
continuously re-runnable, evidence-bound syntheses for any topic.

Keywords: modafinil, meta-analysis, literature retrieval, bibliometrics, record de-duplication, full-text mining, document embeddings, citation network, topic modeling, entity extraction, wakefulness, cognitive enhancement, reproducible research

---
Associated artifacts
GitHub release: v0.1.0 (https://github.com/docxology/template_literature_meta_analysis/releases/tag/v0.1.0)
DOI: https://doi.org/10.5281/zenodo.20931964
Zenodo: https://zenodo.org/records/20931964
PDF SHA-256: 412d4fcf4b0c2e14fb950f9080f107d81fd9a90dfdf216b9161a13833eff62ff

## Keywords

modafinil · meta-analysis · literature retrieval · bibliometrics · record de-duplication · full-text mining · document embeddings · citation network · topic modeling · entity extraction · wakefulness · cognitive enhancement · reproducible research

## Publication Details

| Field | Value |
|------|-------|
| **DOI** | [10.5281/zenodo.20931964](https://doi.org/10.5281/zenodo.20931964) |
| **Published** | 2026 |
| **Version** | 0.1.0 |
| **Zenodo record** | https://zenodo.org/records/20931965 |
| **GitHub release** | https://github.com/docxology/template_literature_meta_analysis/releases/tag/v0.1.0 |
| **Source repository** | https://github.com/docxology/template_literature_meta_analysis |

## Files

- `Friedman_2026_Living_412d4fcf.pdf` - Zenodo PDF

## Citation

> Friedman, D. A. (2026). *A Living Meta-Analysis of the Modafinil Literature*. Zenodo. https://doi.org/10.5281/zenodo.20931964

## Related

- Zenodo record: https://zenodo.org/records/20931965
- GitHub release: https://github.com/docxology/template_literature_meta_analysis/releases/tag/v0.1.0
- Source repository: https://github.com/docxology/template_literature_meta_analysis
- [Full Bibliography](../../pages/BIBLIOGRAPHY.md) · [All Papers](../README.md)
