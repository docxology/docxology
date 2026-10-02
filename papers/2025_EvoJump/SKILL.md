---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "EvoJump: A Unified Framework for Stochastic Modeling of Evolutionary Ontogenetic Trajectories"
description: "Biological development unfolds as a stochastic process characterized by continuous variation and discrete transitions, yet traditional analytical methods fail to capture this complexity, and we present EvoJump, a unified computational framework that ..."
tags: ["evojump", "stochastic-modeling", "ontogenetic-trajectories", "jump-diffusion", "fractional-brownian-motion"]
domain: "Active Inference"
citation: "Daniel Friedman (2025). *EvoJump: A Unified Framework for Stochastic Modeling of Evolutionary Ontogenetic Trajectories*. Zenodo."
doi: "10.5281/zenodo.17229924"
---

# EvoJump: A Unified Framework for Stochastic Modeling of Evolutionary Ontogenetic Trajectories

**Daniel Friedman** (2025) · Active Inference

## Context

This work addresses topics in **Active Inference**: EvoJump, stochastic modeling, ontogenetic trajectories, jump-diffusion.

## Methods

Primary methods and techniques applied in this work:

- **Cross-sectional 'laser plane' view of ontogeny as a stochastic process** — Development is conceptualised as stochastic trajectories examined through phenotype distributions at successive timepoints.
- **Python package unifying OU-jump, fBM, Cox-Ingersoll-Ross and Lévy process models** — EvoJump implements several stochastic process models for developmental trajectories behind consistent interfaces.
- **Wavelet, copula, extreme value and regime-switching analyses of trajectories** — Statistical modules apply wavelets for multi-scale patterns, copulas for dependence, EVT for rare events and regime-switching for phase detection.
- **Validation via synthetic data, analytical solutions and integration tests** — Each process model and statistical method is checked with synthetic data of known parameters, analytical solutions where available, and end-to-end tests.
- **Simulated 100-generation Drosophila selective sweep case study** — A logistic-selection SDE with drift models a red-eye allele sweep and a correlated eye-size trait, based on a published classroom study.

## Key Findings

Core contributions and results:

- Validation tests confirmed expected properties, e.g. fBM recovered standard Brownian motion at H = 0.5 and distinguished persistence regimes.
- The author reports that all tests in the testing framework pass.
- On synthetic data, copula analysis showed significant positive dependence between early and late developmental phenotypes (Kendall's τ = 0.45).
- The Drosophila simulation captured a near-fixation selective sweep, correlated eye-size evolution, hitchhiking, and selection-drift balance.
- Stated limitations include time-homogeneous parameters, separate analysis of traits, and treating observations as exact without measurement error.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2018_WoodliceAndMen](../2018_WoodliceAndMen/)
- [2020_BehaviorEngineering](../2020_BehaviorEngineering/)
- [2021_ModelingConflict](../2021_ModelingConflict/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.17229924
- PDF SHA-256: See zenodo_record
- Pairing confidence: unknown
- Last checked: 2026-06-30T23:25:48Z

## Prerequisites

- Familiarity with EvoJump, stochastic modeling, ontogenetic trajectories
- Background in Active Inference fundamentals
- Access to source repository: N/A

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.17229924`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
