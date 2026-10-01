<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 🐜 A snapshot and pipeline for tissue-specific gene expression meta-analysis in honey bees

**Daniel Ari Friedman, Chao Tong, Timothy A. Linksvayer, Matthias Freund, Nicole Weronika Keough, Brian Johnson** (2023) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.10400744-blue)](https://doi.org/10.5281/zenodo.10400744)

---

## Abstract

> The honey bee ( Apis mellifera ) is a pivotal species in both ecological and research contexts, serving as a model organism for studying complex social behavior and physiological processes. A critical aspect of understanding these complexities is the analysis of tissue-specific gene expression (TSGE), a challenging task due to the need to handle large bioinformatics data and manual tissue...

## Keywords

`honey bees` · `Apis mellifera` · `gene expression` · `RNA-Seq` · `novel traits` · `taxonomically restricted genes` · `coding sequence evolution`

## Methods

- **Entrez/NCBI SRA query for Apis mellifera Illumina RNA-seq samples** — Public RNA-seq samples were gathered via an Entrez search filtered to A. mellifera, Illumina platforms, rnaseq type and SRA biosample.
- **Six-script MetaInformAnt pipeline built on AMALGKIT** — A versioned, openly available pipeline of six scripts covered environment setup, genome and metadata download, SRA download, quantification and curation.
- **Metadata tissue-name harmonization script** — A 2.5_update_metadata.py script corrected inconsistent tissue labels so equivalent samples (e.g. variants of 'whole body') were grouped together.
- **fastp QC, kallisto pseudoalignment, amalgkit curation** — Raw reads were QC'd with fastp, quantified with kallisto against Amel_HAv3.1, and merged/normalized into one dataset with amalgkit.
- **PCA, clustering and differential expression descriptives** — Post-processing scripts ran principal component, clustering and differential expression analyses on the curated expression data.

## Key Findings

- From 4349 samples and 12,398 loci, AMALGKIT processing retained 731 samples and 177 loci, released as a public July 2023 TSGE snapshot.
- Curation reduced 133 uniquely named tissues to 54 groups; whole adult body, brain and mushroom body made up 62.3% of samples.
- Optional metadata fields were largely blank (e.g. 99.1% genotype, 67.5% sex, 77.8% age), limiting their use as surrogate variables in harmonization.
- Average library size increased over time, but publication date explained only a small fraction of variance in total bases (R2=0.061).
- The authors suggest several possible reasons for the heavy winnowing: heterogeneous experiments, asymmetric tissue coverage with single-tissue designs, and incomplete metadata that may have underpowered surrogate variable analysis.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.5281/zenodo.10400744](https://doi.org/10.5281/zenodo.10400744)
- Artifact DOI: [10.5281/zenodo.10400745](https://doi.org/10.5281/zenodo.10400745)
- Zenodo record: [https://zenodo.org/records/10400745](https://zenodo.org/records/10400745)
- PDF: [2023_HoneyBeeGeneExpression.pdf](2023_HoneyBeeGeneExpression.pdf)
- PDF download: [Apis-seq_v1_12_18_2023.pdf](https://zenodo.org/api/records/10400745/files/Apis-seq_v1_12_18_2023.pdf/content)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/10400745)

## Citation

> Daniel Ari Friedman, Chao Tong, Timothy A. Linksvayer, Matthias Freund, Nicole Weronika Keough, Brian Johnson (2023). *A snapshot and pipeline for tissue-specific gene expression meta-analysis in honey bees*. Zenodo. DOI: 10.5281/zenodo.10400744. URL: https://doi.org/10.5281/zenodo.10400744.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
