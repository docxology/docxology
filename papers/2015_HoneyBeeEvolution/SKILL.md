---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "Large-Scale Coding Sequence Change Underlies the Evolution of Postdevelopmental Novelty in Honey Bees"
description: "A key question in evolutionary biology concerns how novel traits arise at the molecular level. Honey bees (Apis mellifera) have evolved numerous postdevelopmental novel traits, including royal jelly..."
tags: ["honey-bees", "apis-mellifera", "rna-seq", "taxonomically-restricted-genes", "novel-traits", "gene-expression", "evolutionary-biology", "royal-jelly", "beeswax", "venom"]
domain: "Genetics & Biomedical"
citation: "William Cameron Jasper, Timothy A. Linksvayer, Joel Atallah, Daniel Friedman, Joanna C. Chiu, Brian R. Johnson (2015). *Large-Scale Coding Sequence Change Underlies the Evolution of Postdevelopmental Novelty in Honey Bees*. Molecular Biology & Evolution."
doi: "10.1093/molbev/msu292"
---

# Large-Scale Coding Sequence Change Underlies the Evolution of Postdevelopmental Novelty in Honey Bees

**William Cameron Jasper, Timothy A. Linksvayer, Joel Atallah, Daniel Friedman, Joanna C. Chiu, Brian R. Johnson** (2015) · Genetics & Biomedical

## Context

This work addresses topics in **Genetics & Biomedical**: honey bees, Apis mellifera, RNA-Seq, taxonomically restricted genes.

## Methods

Primary methods and techniques applied in this work:

- **Ten RNA-Seq experiments across novel and conserved honey bee tissues** — Tissues from nurse and forager bees (three colonies, three biological replicates per tissue and caste) were sequenced to compare novel and conserved tissues.
- **Illumina HiSeq 2000 sequencing with Tophat/bowtie2, HTSeq, and EdgeR** — Reads were aligned to Apis mellifera genome build 4.5, counted per gene with HTSeq, and differentially expressed genes called with EdgeR at FDR < 0.05.
- **BLASTx against 71 genomes to classify taxonomically restricted genes** — Each honey bee transcript was blasted against proteins from 71 published genomes to assign genes to TRG classes (Orphans, bee-specific, Hymenoptera, etc.) or conserved.
- **Positive selection calls from published MK-test selection coefficients** — Genes were labelled positively selected or not using a population genomic study's MK-test estimates comparing A. mellifera and A. cerana.
- **WGCNA gene coexpression network connectivity** — Weighted Gene Coexpression Network Analysis in R was used to estimate within-module and total connectivity for each gene.

## Key Findings

Core contributions and results:

- For novel adult physiological functions, positively selected tissue-specific genes of high expression underlie novelty by conferring specialized cellular functions.
- Positively selected genes, whether TRGs or conserved genes, are the least connected genes within gene expression networks.
- TRGs are strongly associated with novel functions and tissues, and much less with conserved tissues and functions.
- Genes expressed in fewer tissues had a higher probability of being positively selected in 8 of 10 tissues.
- The authors conclude that in adults, low-connectedness genes underlie novel phenotypes through rapid coding sequence change, suggesting the evo-devo paradigm is limited postdevelopment.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2015_CryptoJews](../2015_CryptoJews/)
- [2015_EhrlichialInfection](../2015_EhrlichialInfection/)
- [2016_NuclearStructure](../2016_NuclearStructure/)

## Validation

Verification points for this work:

- Canonical DOI: 10.1093/molbev/msu292
- PDF SHA-256: See zenodo_record
- Pairing confidence: unknown
- Last checked: 2026-07-01T20:50:01Z

## Prerequisites

- Familiarity with honey bees, Apis mellifera, RNA-Seq
- Background in Genetics & Biomedical fundamentals
- Access to source repository: N/A

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.1093/molbev/msu292`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
