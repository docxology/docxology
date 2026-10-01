<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 🛡️ Active FractalRabbit: A Synthetic Benchmark for Belief Filtering Under Sparse Waypoint Observations

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21330636-blue)](https://doi.org/10.5281/zenodo.21330636)

---

## Abstract

> Sparse waypoint analysis is privacy-sensitive: it must separate movement from irregular reporting, missingness, spatial coarsening, and corruption while preserving uncertainty about hidden location. Active FractalRabbit provides a controlled, artifact-bound benchmark whose headline lane uses a deterministic project-local synthetic FractalRabbit-format fixture; a separately retained lane exercises...

## Keywords

`ActiveFractalRabbit`

## Methods

- **Synthetic waypoint benchmark: FractalRabbit fixture plus NSA simulator lane** — The headline lane uses a deterministic synthetic FractalRabbit-format fixture; a separate lane runs the pinned open-source NSA FractalRabbit software.
- **Discrete POMDP generative model over grid cells with four categorical modalities** — Waypoints are discretised into a 4x4 grid of hidden cells with location, time-of-day, speed and reporting-burst observation tensors.
- **Matched-information comparison of 14 predictors incl. HMM, particle, pymdp** — Temporal, Markov, sequence, state-space, neural, latent-state and active inference predictors are scored on held-out next-cell log-loss under matched information sets.
- **Soft-vs-hard marginalization protocol under a K-ary symmetric noisy emission** — Soft belief, hard MAP and observed-Markov predictors share transition, emission and priors, differing only in marginalize-versus-commit, across emission flip probabilities.
- **Traveller-clustered bootstrap with Holm and Benjamini-Hochberg correction** — Paired loss differences use traveller-clustered bootstrap intervals (B = 2000) with Holm-Bonferroni primary and BH secondary correction.

## Key Findings

- On the synthetic fixture, soft Bayesian marginalization beats a hard point estimate as emissions degrade: 0 nats at a clean channel to 0.739 nats at flip probability 0.400 on the primary draw, with a mean of 0.495 nats.
- Under noisy emission, active inference ranks 1 of 14 but leads the strongest non-AIF belief filter by only 0.005 nats, a statistical tie.
- No directional comparison in the clustered-bootstrap family survives multiplicity correction.
- Withholding location collapses the filter's mean mass on the true cell from 0.995 to 0.069.
- The pymdp lane matches the exact Bayes posterior (max abs. difference 3.99e-07) and contributes interpretability rather than predictive leadership on the default surface.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [ActiveInferenceInstitute/active_fractal_rabbit](https://github.com/ActiveInferenceInstitute/active_fractal_rabbit)
- GitHub release: [v0.2.0](https://github.com/ActiveInferenceInstitute/active_fractal_rabbit/releases/tag/v0.2.0)
- DOI: [10.5281/zenodo.21330636](https://doi.org/10.5281/zenodo.21330636)
- Zenodo record: [https://zenodo.org/records/21330636](https://zenodo.org/records/21330636)
- PDF: [Friedman_2026_Active_d676159d.pdf](Friedman_2026_Active_d676159d.pdf)
- PDF SHA-256: d676159d149a12a1e990457329ad4cf52d2d8ab4ffcf09f55b42bad8e0c3c052

## Citation

> Daniel Ari Friedman (2026). *Active FractalRabbit: A Synthetic Benchmark for Belief Filtering Under Sparse Waypoint Observations*. Zenodo. DOI: 10.5281/zenodo.21330636. URL: https://doi.org/10.5281/zenodo.21330636.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
