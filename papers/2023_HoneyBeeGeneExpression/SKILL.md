---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "A snapshot and pipeline for tissue-specific gene expression meta-analysis in honey bees"
description: "The genetic basis of phenotypic novelty is a major unresolved question in evolutionary biology. We investigate how large-scale coding sequence change underlies the evolution of postdevelopmental novel..."
tags: ["honey-bees", "apis-mellifera", "gene-expression", "rna-seq", "novel-traits", "taxonomically-restricted-genes", "coding-sequence-evolution"]
domain: "Entomology"
citation: "Daniel Ari Friedman, Chao Tong, Timothy A. Linksvayer, Matthias Freund, Nicole Weronika Keough, Brian Johnson (2023). *A snapshot and pipeline for tissue-specific gene expression meta-analysis in honey bees*. Zenodo."
doi: "10.5281/zenodo.10400744"
artifact_doi: "10.5281/zenodo.10400745"
---

# A snapshot and pipeline for tissue-specific gene expression meta-analysis in honey bees

**Daniel Ari Friedman, Chao Tong, Timothy A. Linksvayer, Matthias Freund, Nicole Weronika Keough, Brian Johnson** (2023) · Entomology

## Context

This work addresses topics in **Entomology**: honey bees, Apis mellifera, gene expression, RNA-Seq.

## Methods

Primary methods and techniques applied in this work:

- **Entrez/NCBI SRA query for Apis mellifera Illumina RNA-seq samples** — Public RNA-seq samples were gathered via an Entrez search filtered to A. mellifera, Illumina platforms, rnaseq type and SRA biosample.
- **Six-script MetaInformAnt pipeline built on AMALGKIT** — A versioned, openly available pipeline of six scripts covered environment setup, genome and metadata download, SRA download, quantification and curation.
- **Metadata tissue-name harmonization script** — A 2.5_update_metadata.py script corrected inconsistent tissue labels so equivalent samples (e.g. variants of 'whole body') were grouped together.
- **fastp QC, kallisto pseudoalignment, amalgkit curation** — Raw reads were QC'd with fastp, quantified with kallisto against Amel_HAv3.1, and merged/normalized into one dataset with amalgkit.
- **PCA, clustering and differential expression descriptives** — Post-processing scripts ran principal component, clustering and differential expression analyses on the curated expression data.

## Key Findings

Core contributions and results:

- From 4349 samples and 12,398 loci, AMALGKIT processing retained 731 samples and 177 loci, released as a public July 2023 TSGE snapshot.
- Curation reduced 133 uniquely named tissues to 54 groups; whole adult body, brain and mushroom body made up 62.3% of samples.
- Optional metadata fields were largely blank (e.g. 99.1% genotype, 67.5% sex, 77.8% age), limiting their use as surrogate variables in harmonization.
- Average library size increased over time, but publication date explained only a small fraction of variance in total bases (R2=0.061).
- The authors attribute the heavy winnowing to heterogeneous experiments, asymmetric tissue coverage with single-tissue designs, and incomplete metadata underpowering surrogate variable analysis.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2016_AntGenetics](../2016_AntGenetics/)
- [2016_ForagingGene](../2016_ForagingGene/)
- [2017_MutAnts](../2017_MutAnts/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.10400744
- PDF SHA-256: See zenodo_record
- Pairing confidence: unknown
- Last checked: 2026-08-22T20:30:00Z
- Artifact DOI: 10.5281/zenodo.10400745

## Prerequisites

- Familiarity with honey bees, Apis mellifera, gene expression
- Background in Entomology fundamentals
- Access to source repository: N/A

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.10400744`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
