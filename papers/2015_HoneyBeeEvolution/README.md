<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 🧬 Large-Scale Coding Sequence Change Underlies the Evolution of Postdevelopmental Novelty in Honey Bees

**William Cameron Jasper, Timothy A. Linksvayer, Joel Atallah, Daniel Friedman, Joanna C. Chiu, Brian R. Johnson** (2015) · *Molecular Biology & Evolution*

[![DOI](https://img.shields.io/badge/DOI-10.1093%2Fmolbev%2Fmsu292-blue)](https://doi.org/10.1093/molbev/msu292)

---

## Abstract

> Whether coding or regulatory sequence change is more important to the evolution of phenotypic novelty is one of biology’s major unresolved questions. The field of evo–devo has shown that in early development changes to regulatory regions are the dominant mode of genetic change, but whether this extends to the evolution of novel phenotypes in the adult organism is unclear. Here, we conduct ten RNA-Seq experiments across both novel and conserved tissues in the honey bee to determine to what extent postdevelopmental novelty is based on changes to the coding regions of genes. We make several discoveries. First, we show that with respect to novel physiological functions in the adult animal, positively selected tissue-specific genes of high expression underlie novelty by conferring specialized cellular functions. Such genes are often, but not always taxonomically restricted genes (TRGs). We further show that positively selected genes, whether TRGs or conserved genes, are the least connected genes within gene expression networks. Overall, this work suggests that the evo–devo paradigm is limited, and that the evolution of novelty, postdevelopment, follows additional rules. Specifically, evo–devo stresses that high network connectedness (repeated use of the same gene in many contexts) constrains coding sequence change as it would lead to negative pleiotropic effects. Here, we show that in the adult animal, the converse is true: Genes with low network connectedness (TRGs and tissue-specific conserved genes) underlie novel phenotypes by rapidly changing coding sequence to perform new-specialized functions.

## Keywords

`honey bees` · `Apis mellifera` · `RNA-Seq` · `taxonomically restricted genes` · `novel traits` · `gene expression` · `evolutionary biology` · `royal jelly` · `beeswax` · `venom`

## Methods

- **Ten RNA-Seq experiments across novel and conserved honey bee tissues** — Tissues from nurse and forager bees (three colonies, three biological replicates per tissue and caste) were sequenced to compare novel and conserved tissues.
- **Illumina HiSeq 2000 sequencing with Tophat/bowtie2, HTSeq, and EdgeR** — Reads were aligned to Apis mellifera genome build 4.5, counted per gene with HTSeq, and differentially expressed genes called with EdgeR at FDR < 0.05.
- **BLASTx against 71 genomes to classify taxonomically restricted genes** — Each honey bee transcript was blasted against proteins from 71 published genomes to assign genes to TRG classes (Orphans, bee-specific, Hymenoptera, etc.) or conserved.
- **Positive selection calls from published MK-test selection coefficients** — Genes were labelled positively selected or not using a population genomic study's MK-test estimates comparing A. mellifera and A. cerana.
- **WGCNA gene coexpression network connectivity** — Weighted Gene Coexpression Network Analysis in R was used to estimate within-module and total connectivity for each gene.

## Key Findings

- For novel adult physiological functions, positively selected tissue-specific genes of high expression underlie novelty by conferring specialized cellular functions.
- Positively selected genes, whether TRGs or conserved genes, are the least connected genes within gene expression networks.
- TRGs are strongly associated with novel functions and tissues, and much less with conserved tissues and functions.
- Genes expressed in fewer tissues had a higher probability of being positively selected in 8 of 10 tissues.
- The authors conclude that in adults, low-connectedness genes underlie novel phenotypes through rapid coding sequence change, suggesting the evo-devo paradigm is limited postdevelopment.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.1093/molbev/msu292](https://doi.org/10.1093/molbev/msu292)
- PDF: [2015_HoneyBeeEvolution.pdf](2015_HoneyBeeEvolution.pdf)
- PDF SHA-256: Not recorded

## Citation

> William Cameron Jasper, Timothy A. Linksvayer, Joel Atallah, Daniel Friedman, Joanna C. Chiu, Brian R. Johnson (2015). *Large-Scale Coding Sequence Change Underlies the Evolution of Postdevelopmental Novelty in Honey Bees*. Molecular Biology & Evolution. DOI: 10.1093/molbev/msu292. URL: https://doi.org/10.1093/molbev/msu292.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
