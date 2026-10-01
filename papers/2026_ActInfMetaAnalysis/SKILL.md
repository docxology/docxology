---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "A Living Meta-Analysis Architecture for Active Inference: Assertion Extraction, Nanopublications, and Hypothesis Scoring"
description: "Computational living meta-analysis of the Active Inference and Free Energy Principle literature: multi-source retrieval, nanopublication extraction, and hypothesis scoring architecture."
tags: ["active-inference", "meta-analysis", "nanopublications", "assertion-extraction", "citation-weighted-scoring", "literature-review", "free-energy-principle", "computational-bibliography", "open-science"]
domain: "Active Inference"
citation: "Daniel Ari Friedman, Joel Dietz (2026). *A Living Meta-Analysis Architecture for Active Inference: Assertion Extraction, Nanopublications, and Hypothesis Scoring*. Active Inference Journal."
doi: "10.5281/zenodo.19461933"
---

# A Living Meta-Analysis Architecture for Active Inference: Assertion Extraction, Nanopublications, and Hypothesis Scoring

**Daniel Ari Friedman, Joel Dietz** (2026) · Active Inference

## Context

This work addresses topics in **Active Inference**: Active Inference, meta-analysis, nanopublications, assertion extraction.

## Methods

Primary methods and techniques applied in this work:

- **Multi-source retrieval (arXiv, Semantic Scholar, OpenAlex) with ID-hierarchy dedup** — Literature was retrieved from three databases and deduplicated to 819 papers using a DOI > arXiv > Semantic Scholar > OpenAlex identifier hierarchy.
- **Keyword-based A/B/C domain taxonomy (200+ indicators, 8 categories)** — Papers were classified into Core Theory, Tools & Translation and Application Domains by keyword matching rather than expert annotation.
- **Abstract-only LLM assertion extraction with gemma3:4b on local Ollama** — Each abstract was assessed against eight hypotheses via a JSON-schema prompt returning direction, confidence and reasoning.
- **Nanopublication knowledge graph with citation-weighted hypothesis scoring** — Extracted assertions became structured nanopublications in an RDF-compatible knowledge graph scored by a citation-weighted evidence function.
- **NMF topic modelling and intra-corpus citation network analysis** — Non-negative matrix factorization was used to find latent topics, and citation edges among corpus papers were analyzed for network topology.

## Key Findings

Core contributions and results:

- Application domains dominated the corpus (Domain C 64.0%), with tools (B) at 20.8% and core theory (A) at 15.2%.
- The citation network was sparse: 2,176 intra-corpus edges out of 29,323 outgoing references (7.4% resolution), anchored by hub papers.
- Hypothesis scores clustered into tiers, with H1 FEP Universality in a diffuse tier (about +0.48) dominated by neutral assessments.
- The authors caution that all assertions are automatically generated and not manually validated, so hypothesis scores are preliminary.
- Preliminary experiments indicated about 15-20% over-extraction, and error rates for the 819-paper run were not quantified.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2018_WoodliceAndMen](../2018_WoodliceAndMen/)
- [2020_BehaviorEngineering](../2020_BehaviorEngineering/)
- [2021_ModelingConflict](../2021_ModelingConflict/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.19461933
- PDF SHA-256: See zenodo_record
- Pairing confidence: unknown
- Last checked: 2026-06-30T23:26:01Z

## Prerequisites

- Familiarity with Active Inference, meta-analysis, nanopublications
- Background in Active Inference fundamentals
- Access to source repository: N/A

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.19461933`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
