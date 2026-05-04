---
name: "ActInfMetaAnalysis"
description: "Expertise in the living meta-analysis architecture for Active Inference/FEP literature: multi-source retrieval and deduplication, three-tier taxonomy, LLM-to-nanopublication extraction over eight hypotheses, RDF-compatible graphs, citation-weighted scoring (Zenodo v2, 2026)."
tags:
  - active-inference
  - meta-analysis
  - nanopublications
  - llm-extraction
  - living-literature-review
  - citation-weighted-scoring
  - free-energy-principle
  - computational-bibliography
  - open-science
---

# A Living Meta-Analysis Architecture for Active Inference

**Daniel Ari Friedman** · **Joel Dietz** (2026) · Active Inference · computational meta-science

**DOI**: [10.5281/zenodo.19897664](https://doi.org/10.5281/zenodo.19897664) · **Zenodo**: [record v2](https://zenodo.org/records/19897664)

## Instructions

Use this skill for **living (continuously updatable) meta-analysis**, **LLM-mediated assertion extraction**, **nanopublications**, **hypothesis-level evidence maps**, or **computational surveys of Active Inference / FEP literature**.

When applying this skill:

1. Treat extractions as **automated hypotheses about text**, not human-validated facts, unless a validation study is cited.
2. Prefer the **three-part story**: ingest & dedupe → taxonomic / thematic structure → nanopublication graph + citation-weighted scores.
3. When interpreting scores, stress **relative** ordering and temporal drift; avoid over-interpreting absolute magnitudes (bias and wording effects are discussed in the paper).
4. Cite **[v2](https://doi.org/10.5281/zenodo.19897664)** for the current PDF; **[v1](https://doi.org/10.5281/zenodo.19461934)** remains version history.

## Key Concepts

- **Living meta-analysis** — pipelines designed to refresh as new papers enter arXiv / Semantic Scholar / OpenAlex-class sources.
- **Canonical deduplication** — DOI-led identifier hierarchy collapsing duplicate records (*N* = 819 illustrative corpus in v2).
- **Three-tier taxonomy** — tiers A/B/C covering core theory, tools & translation, and application domains (eight categories).
- **Eight core hypotheses** — abstract-level LLM judgments with directional support, confidence, and short rationales packaged as nanopublications.
- **Nanopublications** — small, attributable, machine-readable assertion units suited to RDF-compatible graphs.
- **Citation-weighted evidence** — aggregates support in the corpus citation structure; outputs tiered consensus / debate summaries.

## Methods & Techniques

- Multi-repository retrieval (arXiv, Semantic Scholar, OpenAlex) and hierarchical ID-based deduplication.
- Classification into A/B/C taxonomy; auxiliary topic modeling and citation-graph statistics.
- LLM prompting over abstracts mapped to eight hypotheses; structured nanopublication emission.
- Graph scoring and qualitative interpretation (application-heavy corpus shape, hub papers, hypothesis tiers).
- Reproduction: https://github.com/ActiveInferenceInstitute/act_inf_metaanalysis

## Key Findings

- Automated, queryable hypothesis-level landscapes are feasible without hand-labeling every paper—at the cost of validation labor and known LLM biases.
- Field-level statistics (tier mix, hypothesis tiers, citation sparsity *within* the induced corpus) are first-class outputs alongside point scores.
- The architecture transfers to other fast-growing literatures if domain hypotheses and ontology hooks are redesigned.

## Prerequisites

- Conceptual familiarity with Active Inference or the Free Energy Principle.
- Basic understanding of bibliographic APIs and duplicate handling.
- Awareness of limits of abstract-only LLM classification versus full-text semantics.

## 🎯 Consulting & Tutoring

[Daniel Ari Friedman, PhD](https://docxology.github.io/docxology/) is available for AI Research Consulting and Tutoring related to this skill.

## Related Skills

See [BIBLIOGRAPHY.md](../../pages/BIBLIOGRAPHY.md) for the publication catalog.

**Code and data**: https://github.com/ActiveInferenceInstitute/act_inf_metaanalysis
