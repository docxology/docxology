---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "The Free Energy Principle & Active Inference: a Systematic Literature Analysis"
description: "Here we perform a literature analysis of publications in scientific literature using the term “Free Energy Principle” or “Active Inference”, with an emphasis on works written by Karl J Friston. For a subset of papers with accessible full texts, we pe..."
tags: ["systematic-literature-analysis", "free-energy-principle", "active-inference", "karl-friston", "history-of-science", "bibliometrics", "ontology"]
domain: "Active Inference"
citation: "Virginia Bleu Knight, RJ Cordes, Daniel Friedman (2022). *The Free Energy Principle & Active Inference: a Systematic Literature Analysis*. Zenodo."
doi: "10.5281/zenodo.7449367"
---

# The Free Energy Principle & Active Inference: a Systematic Literature Analysis

**Virginia Bleu Knight, RJ Cordes, Daniel Friedman** (2022) · Active Inference

## Context

This work addresses topics in **Active Inference**: systematic literature analysis, Free Energy Principle, Active Inference, Karl Friston.

## Methods

Primary methods and techniques applied in this work:

- **Publish or Perish / Google Scholar search for FEP, ActInf and Friston papers** — Citations from 1990–2021 matching the two terms or authored by Karl Friston were collected and de-duplicated manually by title.
- **BioPython query of open-access PubMed papers for full-text subset** — The BioPython API was used to restrict analysis to open-source PubMed papers with the terms in title/abstract.
- **PyPDF2 term-frequency extraction using Active Inference Ontology terms** — A custom PyPDF2 script counted 74 core, 250 supplement and 74 entailed ontology terms in each abstract and PDF.
- **Manual annotation of figures, equations, tables, boxes, supplements** — Each analyzed paper was hand-annotated for structural/mathematical features and estimated citations per year.
- **ResearchRabbit citation network; Coda tables; Orange clustering** — ResearchRabbit built a citation network of the focal papers; Coda merged data into reflexive tables; Orange clustered term usage.

## Key Findings

Core contributions and results:

- From the larger FEP/ActInf citation corpus, the analysis focused on an initial set of 237 open-access papers obtained via PubMed.
- The most highly cited papers in the open-source dataset were from 2013 and all included Karl J. Friston as an author.
- By citations per year, Friston is not in the top five first authors; Sterzer (109.3) and Carhart-Harris (108.5) lead, and top papers by this metric date from 2018–2020.
- All core Active Inference Ontology terms increased in use frequency over time.
- Term frequencies tracked specific publications, e.g. 'Information Geometry' rose after Parr et al. 2019 and 'Cognitivism' after Friston & Allen 2018.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2018_WoodliceAndMen](../2018_WoodliceAndMen/)
- [2020_BehaviorEngineering](../2020_BehaviorEngineering/)
- [2021_ModelingConflict](../2021_ModelingConflict/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.7449367
- PDF SHA-256: See zenodo_record
- Pairing confidence: unknown
- Last checked: 2026-06-30T23:24:59Z

## Prerequisites

- Familiarity with systematic literature analysis, Free Energy Principle, Active Inference
- Background in Active Inference fundamentals
- Access to source repository: N/A

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.7449367`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
