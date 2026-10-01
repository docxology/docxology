<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 🧠 EvoJump: Stochastic Modeling of Evolutionary Ontogenetic Trajectories

**Daniel Friedman** (2025) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.17229924-blue)](https://doi.org/10.5281/zenodo.17229924)

---

## Abstract

> Biological development unfolds as a stochastic process characterized by continuous variation and discrete transitions, yet traditional analytical methods fail to capture this complexity, and we present EvoJump, a unified computational framework that models developmental trajectories as stochastic processes analyzed through cross-sectional laser plane views of phenotypic distributions. EvoJump...

## Keywords

`evolutionary transitions` · `EvoJump` · `Active Inference` · `major transitions` · `phenotypic complexity` · `Free Energy Principle`

## Methods

- **Cross-sectional 'laser plane' view of ontogeny as a stochastic process** — Development is conceptualised as stochastic trajectories examined through phenotype distributions at successive timepoints.
- **Python package unifying OU-jump, fBM, Cox-Ingersoll-Ross and Lévy process models** — EvoJump implements several stochastic process models for developmental trajectories behind consistent interfaces.
- **Wavelet, copula, extreme value and regime-switching analyses of trajectories** — Statistical modules apply wavelets for multi-scale patterns, copulas for dependence, EVT for rare events and regime-switching for phase detection.
- **Validation via synthetic data, analytical solutions and integration tests** — Each process model and statistical method is checked with synthetic data of known parameters, analytical solutions where available, and end-to-end tests.
- **Simulated 100-generation Drosophila selective sweep case study** — A logistic-selection SDE with drift models a red-eye allele sweep and a correlated eye-size trait, based on a published classroom study.

## Key Findings

- Validation tests confirmed expected properties, e.g. fBM recovered standard Brownian motion at H = 0.5 and distinguished persistence regimes.
- The author reports that all tests in the testing framework pass.
- On synthetic data, copula analysis showed significant positive dependence between early and late developmental phenotypes (Kendall's τ = 0.45).
- The Drosophila simulation captured a near-fixation selective sweep, correlated eye-size evolution, hitchhiking, and selection-drift balance.
- Stated limitations include time-homogeneous parameters, separate analysis of traits, and treating observations as exact without measurement error.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.5281/zenodo.17229924](https://doi.org/10.5281/zenodo.17229924)
- Zenodo record: [https://zenodo.org/records/17229924](https://zenodo.org/records/17229924)
- PDF: [2025_EvoJump.pdf](2025_EvoJump.pdf)
- PDF download: [EvoJump_DAF_9-30-2025.pdf](https://zenodo.org/api/records/17229925/files/EvoJump_DAF_9-30-2025.pdf/content)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/17229924)

## Citation

> Daniel Friedman (2025). *EvoJump: Stochastic Modeling of Evolutionary Ontogenetic Trajectories*. Zenodo. DOI: 10.5281/zenodo.17229924. URL: https://doi.org/10.5281/zenodo.17229924.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
