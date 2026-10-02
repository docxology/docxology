<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 🧠 Robust Belief Sharing in Federated Active Inference: A Recovery-Tested Generalized-Variational Framework for Categorical Contamination-Aware Consensus

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21864003-blue)](https://doi.org/10.5281/zenodo.21864003)

---

## Abstract

> Multi-agent active inference gives a natural account of belief sharing: agents hold local posteriors over a shared latent state, communicate those beliefs, and pool them into a colony-level consensus. The same mechanism is fragile when a member is miscalibrated, corrupted, or strategically wrong. Because the standard pool multiplies the reports together, a single confident-but-wrong broadcast that puts near-zero mass on the true state can pull the whole consensus off it, outweighing many honest members. The colony therefore needs a way to preserve the useful structure of belief sharing while limiting the influence of contaminated beliefs. This paper presents Active Fedference, a discrete-categorical framework that connects robust federated generalized variational inference with active inference belief sharing. The main bridge is structural: standard belief sharing appears as the non-robust corner of a broader generalized-Bayes family, while robust losses, conservative server fusion, and explicit aggregation diagnostics describe how the system moves away from that corner under declared contamination mechanisms. The result is not a replacement for belief sharing, but a containment result: ordinary belief sharing is recovered when robustness is turned off. Bounded-loss theory applies on the client axis, while the variational-server axis supplies an objective-backed redescending weight update. The manuscript separates three robustness axes that are often conflated. First, client-side generalized-Bayes updates change how each agent absorbs evidence; this is the rigorous axis, carrying FedGVI’s bounded-influence result only under the source theorem’s loss, model, and contamination assumptions. Second, a sharp server-side reweighting heuristic suppresses beliefs that pull away from the emerging consensus, while carrying only its recovery-limit guarantee — no proven objective and no bounded-influence bound. Third, a variational aggregation rule supplies a more conservative objective-backed server alternative, with a raw effective-weight bound but not an estimator-level bounded-influence proof for the normalized consensus. Keeping these axes separate lets the paper state exactly which claims are proven, which are empirical, and which remain engineering extensions. The study suite then exercises the framework as an end-to-end research system: recovery checks anchor the standard-Bayes limit, belief-sharing studies verify the communication baseline, contamination experiments test robust consensus, and extension studies probe moving agents, hierarchical latent structure, sensitivity to acuity and colony size, parameter recovery, and single-host socket-backed federation traces. All reported quantities are generated from deterministic analysis artifacts and injected into the manuscript by token, so the paper, figures, release package, and validation reports remain tied to the same execution record. The open-source repository is ActiveInferenceInstitute/Active_Fedference . The production Zenodo release DOI is 10.5281/zenodo.21864004, and the repository and deposited PDF point to each other through this DOI and the repository URL.

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
