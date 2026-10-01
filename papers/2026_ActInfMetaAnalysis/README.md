<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 🧠 A Living Meta-Analysis Architecture for Active Inference: Assertion Extraction, Nanopublications, and Hypothesis Scoring

**Daniel Ari Friedman, Joel Dietz** (2026) · *Active Inference Journal*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.19461933-blue)](https://doi.org/10.5281/zenodo.19461933)

---

## Abstract

> No prior automated system tracks hypothesis-level evidence across the full Active Inference and Free Energy Principle (FEP) literature. Manual synthesis cannot keep pace with a field that has grown at a compound annual rate of 20.36% across 2005–2026, and the FEP’s theoretical generality has invited falsifiability critiques that only hypothesis-specific evidence profiling can address. Building on...

## Keywords

`Active Inference` · `meta-analysis` · `nanopublications` · `assertion extraction` · `citation-weighted scoring` · `literature review architecture` · `Free Energy Principle` · `computational bibliography`

## Methods

- **Multi-source retrieval (arXiv, Semantic Scholar, OpenAlex) with ID-hierarchy dedup** — Literature was retrieved from three databases and deduplicated to 819 papers using a DOI > arXiv > Semantic Scholar > OpenAlex identifier hierarchy.
- **Keyword-based A/B/C domain taxonomy (200+ indicators, 8 categories)** — Papers were classified into Core Theory, Tools & Translation and Application Domains by keyword matching rather than expert annotation.
- **Abstract-only LLM assertion extraction with gemma3:4b on local Ollama** — Each abstract was assessed against eight hypotheses via a JSON-schema prompt returning direction, confidence and reasoning.
- **Nanopublication knowledge graph with citation-weighted hypothesis scoring** — Extracted assertions became structured nanopublications in an RDF-compatible knowledge graph scored by a citation-weighted evidence function.
- **NMF topic modelling and intra-corpus citation network analysis** — Non-negative matrix factorization was used to find latent topics, and citation edges among corpus papers were analyzed for network topology.

## Key Findings

- Application domains dominated the corpus (Domain C 64.0%), with tools (B) at 20.8% and core theory (A) at 15.2%.
- The citation network was sparse: 2,176 intra-corpus edges out of 29,323 outgoing references (7.4% resolution), anchored by hub papers.
- LLM-derived hypothesis scores clustered into tiers, with H1 FEP Universality in a diffuse tier (about +0.48) where a large neutral plurality reflects broad invocation of the principle without explicit empirical test.
- The authors caution that all assertions are automatically generated and not manually validated, so hypothesis scores are preliminary.
- Preliminary experiments indicated about 15-20% over-extraction, and error rates for the 819-paper run were not quantified.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.5281/zenodo.19461933](https://doi.org/10.5281/zenodo.19461933)
- Zenodo record: [https://zenodo.org/records/19461933](https://zenodo.org/records/19461933)
- PDF: [act_inf_metaanalysis_v2_04-30-2026.pdf](act_inf_metaanalysis_v2_04-30-2026.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/19461933)

## Citation

> Daniel Ari Friedman, Joel Dietz (2026). *A Living Meta-Analysis Architecture for Active Inference: Assertion Extraction, Nanopublications, and Hypothesis Scoring*. Active Inference Journal. DOI: 10.5281/zenodo.19461933. URL: https://doi.org/10.5281/zenodo.19461933.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
