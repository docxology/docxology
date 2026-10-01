---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "Gene expression variation in the brains of harvester ant foragers is associated with collective behavior"
description: "Gene expression differences among workers performing different tasks are a key mechanism underlying division of labor in social insects. Here we characterize transcriptomic profiles of foragers compar..."
tags: ["gene-expression", "foragers", "rna-seq", "division-of-labor", "transcriptomics", "harvester-ants", "behavioral-castes", "pogonomyrmex-barbatus"]
domain: "Entomology"
citation: "Daniel Ari Friedman, Ryan Alexander York, Austin Travis Hilliard, Deborah M. Gordon (2020). *Gene expression variation in the brains of harvester ant foragers is associated with collective behavior*. Communications Biology."
doi: "10.1038/s42003-020-0813-8"
---

# Gene expression variation in the brains of harvester ant foragers is associated with collective behavior

**Daniel Ari Friedman, Ryan Alexander York, Austin Travis Hilliard, Deborah M. Gordon** (2020) · Entomology

## Context

This work addresses topics in **Entomology**: gene expression, foragers, RNA-Seq, division of labor.

## Methods

Primary methods and techniques applied in this work:

- **Single-forager brain RNA-seq from nine field colonies of P. barbatus** — Foragers collected on one morning near Rodeo, New Mexico had single brains sequenced on Illumina HiSeq 4000, yielding 85 transcriptomes from 9 colonies.
- **Expression-trait correlations with humidity sensitivity and brain DA:5HT** — Gene expression was correlated with colony sensitivity of foraging to humidity and forager brain dopamine-to-serotonin ratio, at colony-mean and per-sample levels.
- **PCA and linear discriminant analysis of transcriptomes by colony** — PCA on TPM expression, with 30 components retained for LDA stratified by colony, tested whether forager transcriptomes carry a colony signature.
- **WGCNA signed coexpression network with iterative module-density filtering** — Coexpression modules were built in the R WGCNA library and iteratively filtered to retain densely interconnected modules, leaving 7085 genes.
- **dN/dS against honey bee and five ant species, modeled with a GLM** — Coding-sequence constraint was estimated with orthologr and related to coexpression centrality and trait correlation in a generalized linear model.

## Key Findings

Core contributions and results:

- Forager brain gene expression patterns were more similar among nestmates than non-nestmates, with substantial variability within colonies as well.
- A fraction of colony expression differences were associated with humidity sensitivity of foraging and forager brain DA:5HT ratio.
- Neurotransmitter receptors as a category were significantly correlated in expression with colony sensitivity of foraging activity to humidity.
- Gene coexpression analysis identified 11 modules of loci with coordinated expression patterns across colonies.
- Genes more central to coexpression modules were more correlated with colony traits and evolving under increased coding-sequence constraint.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2016_AntGenetics](../2016_AntGenetics/)
- [2016_ForagingGene](../2016_ForagingGene/)
- [2017_MutAnts](../2017_MutAnts/)

## Validation

Verification points for this work:

- Canonical DOI: 10.1038/s42003-020-0813-8
- PDF SHA-256: See zenodo_record
- Pairing confidence: unknown
- Last checked: 2026-07-01T20:50:01Z

## Prerequisites

- Familiarity with gene expression, foragers, RNA-Seq
- Background in Entomology fundamentals
- Access to source repository: N/A

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.1038/s42003-020-0813-8`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
