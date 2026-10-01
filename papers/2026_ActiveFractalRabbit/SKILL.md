---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "Active FractalRabbit: A Synthetic Benchmark for Belief Filtering Under Sparse Waypoint Observations"
description: "Sparse waypoint analysis is privacy-sensitive: it must separate movement from irregular reporting, missingness, spatial coarsening, and corruption while preserving uncertainty about hidden location. Active FractalRabbit provides a controlled, artifac..."
tags: ["activefractalrabbit"]
domain: "Cognitive Security"
citation: "Daniel Ari Friedman (2026). *Active FractalRabbit: A Synthetic Benchmark for Belief Filtering Under Sparse Waypoint Observations*. Zenodo."
doi: "10.5281/zenodo.21330636"
---

# Active FractalRabbit: A Synthetic Benchmark for Belief Filtering Under Sparse Waypoint Observations

**Daniel Ari Friedman** (2026) · Cognitive Security

## Context

This work addresses topics in **Cognitive Security**: ActiveFractalRabbit.

## Methods

Primary methods and techniques applied in this work:

- **Synthetic waypoint benchmark: FractalRabbit fixture plus NSA simulator lane** — The headline lane uses a deterministic synthetic FractalRabbit-format fixture; a separate lane runs the pinned open-source NSA FractalRabbit software.
- **Discrete POMDP generative model over grid cells with four categorical modalities** — Waypoints are discretised into a 4x4 grid of hidden cells with location, time-of-day, speed and reporting-burst observation tensors.
- **Matched-information comparison of 14 predictors incl. HMM, particle, pymdp** — Temporal, Markov, sequence, state-space, neural, latent-state and active inference predictors are scored on held-out next-cell log-loss under matched information sets.
- **Soft-vs-hard marginalization protocol under a K-ary symmetric noisy emission** — Soft belief, hard MAP and observed-Markov predictors share transition, emission and priors, differing only in marginalize-versus-commit, across emission flip probabilities.
- **Traveller-clustered bootstrap with Holm and Benjamini-Hochberg correction** — Paired loss differences use traveller-clustered bootstrap intervals (B = 2000) with Holm-Bonferroni primary and BH secondary correction.

## Key Findings

Core contributions and results:

- Soft belief marginalization beats a point estimate as emissions degrade: 0 nats at a clean channel to 0.739 nats at flip probability 0.400, with a cross-draw mean of 0.495 nats.
- Under noisy emission, active inference ranks 1 of 14 but leads the strongest non-AIF belief filter by only 0.005 nats, a statistical tie.
- No directional comparison in the clustered-bootstrap family survives multiplicity correction.
- Withholding location collapses the filter's mean mass on the true cell from 0.995 to 0.069.
- The pymdp lane matches the exact Bayes posterior (max abs. difference 3.99e-07) and contributes interpretability rather than predictive leadership on the default surface.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

See [BIBLIOGRAPHY.md](../../pages/BIBLIOGRAPHY.md) for related publications.

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.21330636
- PDF SHA-256: d676159d149a12a1e990457329ad4cf52d2d8ab4ffcf09f55b42bad8e0c3c052
- Pairing confidence: strong
- Last checked: 2026-09-24T18:29:57Z

## Prerequisites

- Familiarity with ActiveFractalRabbit
- Background in Cognitive Security fundamentals
- Access to source repository: ActiveInferenceInstitute/active_fractal_rabbit

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.21330636`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
