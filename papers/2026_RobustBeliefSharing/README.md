<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 🧠 Robust Belief Sharing in Federated Active Inference: A Recovery-Tested Generalized-Variational Framework for Categorical Contamination-Aware Consensus

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21864003-blue)](https://doi.org/10.5281/zenodo.21864003)

---

## Abstract

> Multi-agent active inference gives a natural account of belief sharing: agents hold local posteriors over a shared latent state, communicate those beliefs, and pool them into a colony-level consensus. The same mechanism is fragile when a member is miscalibrated, corrupted, or strategically wrong. Because the standard pool multiplies the reports together, a single confident-but-wrong broadcast...

## Keywords

`active inference` · `federated learning` · `generalised variational inference` · `belief sharing` · `robustness` · `FedGVI`

## Methods

- **Discrete-categorical NumPy/SciPy reimplementation of FedGVI primitives** — FedGVI generalized-Bayes primitives (divergences, bounded losses, generalized posterior, cavity algebra, robust aggregation) were reimplemented for categorical beliefs.
- **Three-step federation protocol: local update, broadcast, server fusion** — Agents form generalized-Bayes posteriors against their cavity, broadcast them, and a server fuses them, with each agent's heard consensus excluding its own message.
- **Server rules: sharp reweighting heuristic and variational aggregate** — Two server aggregators are compared: a divergence-reweighting heuristic and an objective-backed variational_aggregate derived from an aggregation free energy.
- **Paired Wilcoxon tests with BH-FDR and bootstrap CIs over 960 trials** — Robust-vs-naive contrasts under contamination use matched-pairs Wilcoxon signed-rank tests deflated with Benjamini-Hochberg FDR and bootstrap confidence intervals.
- **Simulation study suite on a 7-agent, 9-location sentinel POMDP** — Studies run on a fixed ensemble of 7 agents sharing a 9-location factor (seed 0), plus acuity recovery, disjoint-observation and MLP-transfer extensions.

## Key Findings

- Recovery contract: KL/NLL client limits recover closed-form Bayes and the zero-robustness server branch recovers the log-linear pool, with maximum deviations of 5.55e-17 and 0.
- Across 960 paired trials at the verdict contamination rate, the headline robust method (RKL) reached accuracy 0.9867 versus 0.9021 for the naive pool.
- The server heuristic is regime-dependent: at the most severe swept rate the best robust mean reached 0.9880 versus 0.6928 for the standard pool, an operating-point contrast only.
- In a disjoint-observation extension, communicating agents (0.493) outperformed isolated agents (0.326) across 128 seeds, framed as evidence for that configuration only.
- The authors state the evidence does not establish universal Byzantine tolerance, truth recovery, calibration, or an optimal robustness parameter.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.5281/zenodo.21864003](https://doi.org/10.5281/zenodo.21864003)
- Artifact DOI: [10.5281/zenodo.21972644](https://doi.org/10.5281/zenodo.21972644)
- Zenodo record: [https://zenodo.org/records/21864003](https://zenodo.org/records/21864003)
- PDF: [active_fedference_combined.pdf](active_fedference_combined.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/21864003)

## Citation

> Daniel Ari Friedman (2026). *Robust Belief Sharing in Federated Active Inference: A Recovery-Tested Generalized-Variational Framework for Categorical Contamination-Aware Consensus*. Zenodo. DOI: 10.5281/zenodo.21864003. URL: https://doi.org/10.5281/zenodo.21864003.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
