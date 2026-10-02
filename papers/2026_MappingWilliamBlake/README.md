<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 Mapping William Blake's Works: Evidence ledgers, source provenance, text-image diagnostics, and rights-bounded release controls

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21047573-blue)](https://doi.org/10.5281/zenodo.21047573)

---

## Abstract

> A reproducible, rights-bounded digital-humanities workflow that builds and audits a target-ledgered William Blake corpus (texts, images, metadata, analysis, visual summaries) and separates open-source code and project-authored aggregate analytics from provider-supplied source materials. This record contains the working-paper PDF (rights-safe: Blake Archive image mosaics omitted) and the open-source software release bundle. The MIT license covers project code and project-authored outputs only; provider-supplied Blake Archive TEI, transcriptions, images, and fallback source texts are excluded and remain under their source-provider terms.

## Keywords

`William Blake` · `digital humanities` · `corpus acquisition` · `source provenance` · `rights-bounded release`

## Methods

- **7-phase DAG pipeline (blake) from discovery to reports** — The corpus is built by a directed pipeline of discovery, acquisition, metadata, analysis, visualizations, export, and reports, whose JSON artifacts also populate the manuscript.
- **Versioned canonical target ledger of 104 work-level Blake targets** — A ledger derived from Blake bibliographies, editions, Archive identifiers, and visual catalogues serves as the denominator for coverage claims.
- **Tiered source registry with the William Blake Archive as primary authority** — The registry holds the Blake Archive, Project Gutenberg, and Internet Archive, with the Archive given priority when sources disagree and others used as fallback or corroboration.
- **Descriptive text metrics: tokenization, type-token ratio, lexical sentiment** — Each text-bearing work is tokenized to compute word counts, sentiment, vocabulary richness, and themes, treated as descriptors rather than literary judgments.
- **TF-IDF vectors with deterministic PCA/LSA projection over 162 works** — A 120-term TF-IDF vocabulary is built across text-bearing works and projected onto PCA/LSA axes as a reading instrument over local evidence.

## Key Findings

- The saved run represents 102 of 104 ledger targets (98.1%) but fully meets the required text/image evidence profile for only 90 (86.5%); 12 are partial and 2 missing.
- The text-bearing subset contains 156 works and 216878 words, and joint text-image diagnostics are available for 33 works.
- The ontology module produced a work-theme graph of 356 nodes and 297 edges, including 16 theme nodes.
- The local analysis ledger reports all 340 works analyzed with 0 recorded analysis errors.
- The author frames the contribution as an auditable corpus-governance method, not a completed or exhaustive analysis of Blake's works.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [docxology/blake](https://github.com/docxology/blake)
- GitHub release: [v0.1.0](https://github.com/docxology/blake/releases/tag/v0.1.0)
- DOI: [10.5281/zenodo.21047573](https://doi.org/10.5281/zenodo.21047573)
- Zenodo record: [https://zenodo.org/records/21047573](https://zenodo.org/records/21047573)
- PDF: [blake_working_paper.pdf](blake_working_paper.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/21047573)

## Citation

> Daniel Ari Friedman (2026). *Mapping William Blake's Works: Evidence ledgers, source provenance, text-image diagnostics, and rights-bounded release controls*. Zenodo. DOI: 10.5281/zenodo.21047573. URL: https://doi.org/10.5281/zenodo.21047573.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
