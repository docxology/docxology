# A Living Meta-Analysis Architecture for Active Inference: Assertion Extraction, Nanopublications, and Hypothesis Scoring

**Daniel Ari Friedman** · **Joel Dietz** (2026) · *Active Inference Journal*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.19897664-blue)](https://doi.org/10.5281/zenodo.19897664) · [Zenodo v2](https://zenodo.org/records/19897664)

---

<!-- Schema.org structured data for search engines -->
<!--
{"@context":"https://schema.org","@type":"ScholarlyArticle","headline":"A Living Meta-Analysis Architecture for Active Inference: Assertion Extraction, Nanopublications, and Hypothesis Scoring","abstract":"Automated living meta-analysis for Active Inference/FEP: multi-source literature retrieval and deduplication; three-tier taxonomy; LLM-driven nanopublications over eight hypotheses; RDF-compatible knowledge graph with citation-weighted scoring; corpus N=819 (v2).","keywords":["Active Inference","meta-analysis","nanopublications","living literature review","hypothesis scoring","LLM extraction","Free Energy Principle","OpenAlex","Semantic Scholar","arXiv"],"author":[{"@type":"Person","name":"Daniel Ari Friedman","url":"https://danielarifriedman.com/"},{"@type":"Person","name":"Joel Dietz"}]}
-->

*Computational meta-analysis of the Active Inference and FEP literature (v2, April 2026)*

## Abstract

> No prior automated system tracks hypothesis-level evidence across the full Active Inference and Free Energy Principle literature at scale. This work presents a **living meta-analysis** framework: literature is retrieved from arXiv, Semantic Scholar, and OpenAlex and deduplicated (*N* = 819 in v2) via a canonical identifier hierarchy (DOI > arXiv ID > Semantic Scholar ID > OpenAlex ID). Papers are classified into a three-tier taxonomy (A: core theory; B: tools and translation; C: application domains) across eight categories. An LLM-powered pipeline evaluates each abstract against eight core hypotheses, emitting structured **nanopublications** (directionality, confidence, reasoning) that populate an RDF-compatible knowledge graph scored by a citation-weighted evidence function. **All extractions are machine-generated and not fully manually validated; hypothesis scores are preliminary** and are most useful for relative ranking and trajectories, not as standalone point estimates. Open code and reproduction materials: [act_inf_metaanalysis](https://github.com/ActiveInferenceInstitute/act_inf_metaanalysis).

## Keywords

`Active Inference` · `Free Energy Principle` · `meta-analysis` · `living literature review` · `nanopublications` · `LLM extraction` · `hypothesis scoring` · `knowledge graph` · `OpenAlex` · `Semantic Scholar` · `arXiv`

## Key Contributions

- Multi-source retrieval, identifier-based deduplication, and a three-tier (A/B/C) taxonomy for mapping the field.
- LLM-driven assertion extraction into nanopublications wired for RDF-style graphs and queryable evidence landscapes.
- Citation-weighted scoring over eight hypotheses with explicit reporting of consensus vs. debate structure and automation caveats.
- Open pipeline suitable for **continuous** (living) updates as new papers appear.

## Methods

- Corpus construction from arXiv, Semantic Scholar, and OpenAlex; hierarchical deduplication of records.
- Taxonomic labeling (eight categories under A/B/C); complementary topic modeling (e.g., NMF) and citation-network views.
- LLM evaluation of abstracts against eight hypotheses; nanopublication records with directionality, confidence, and rationale.
- Graph-level citation-weighted aggregation; interpretive emphasis on relative tiers and biases (publication bias, linguistic asymmetry) per manuscript discussion.
- Reproducible implementation: https://github.com/ActiveInferenceInstitute/act_inf_metaanalysis

## Version note

Zenodo **[v2](https://zenodo.org/records/19897664)** (`10.5281/zenodo.19897664`, updated 2026-04-30) revises title, scope, and empirical details relative to **[v1](https://doi.org/10.5281/zenodo.19461934)**. Cite **v2** for the current manuscript PDF.

## 🎯 Consulting & Tutoring

**Available for AI Research Consulting and Tutoring.** [Contact Daniel Ari Friedman, PhD](https://danielarifriedman.com/) for collaboration on Active Inference, Bayesian modeling, and computational meta-science.

## Citation

```bibtex
@article{2026_ActInfMetaAnalysis,
  author = {Daniel Ari Friedman and Joel Dietz},
  title = {{A Living Meta-Analysis Architecture for Active Inference: Assertion Extraction, Nanopublications, and Hypothesis Scoring}},
  journal = {Active Inference Journal},
  year = {2026},
  doi = {10.5281/zenodo.19897664},
  url = {https://doi.org/10.5281/zenodo.19897664},
  note = {Zenodo v2},
}
```

## File Inventory

- `AGENTS.md`
- `act_inf_metaanalysis_v2_04-30-2026.pdf`
- `README.md`
- `SKILL.md`

Earlier Zenodo v1 used `act_inf_metaanalysis_v1_04-19-2026.pdf` (see [v1 DOI](https://doi.org/10.5281/zenodo.19461934)); not kept in this clone.
