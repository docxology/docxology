<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 Policy Entanglement in Active Inference

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20418904-blue)](https://doi.org/10.5281/zenodo.20418904)

---

## Abstract

> Active inference models often need to choose among several policy streams at once, for example streams tied to different effectors, sensory channels, agents, agents within a group, or planning horizons. Standard discrete active-inference implementations keep this manageable by treating those streams as independent, but that simplification removes the dependencies that make coordinated action...

## Keywords

`active inference` · `free energy principle` · `policy inference` · `mean-field` · `total correlation` · `information geometry` · `Schmidt rank` · `tensor networks` · `sophisticated inference` · `Lean theorem proving` · `machine-checked free-energy identity`

## Methods

- **Coupling-parameter deformation of the independent policy posterior** — Multi-stream policy posteriors are deformed away from the mean-field product by a scalar coupling strength plus compatibility and preference potentials.
- **Lean 4 formalization: Mathlib proof of the central identity plus stock-Lean boundary** — MathlibProofs machine-checks the S01 free-energy identity with an axiom audit and negative controls; a stock-Lean fragment exposes a 21-row theorem surface as typed contracts.
- **pymdp/NumPy POMDP simulations of coupled policy ensembles** — Simulations sweep coupled ensembles, run short and long rollouts, check the projection identity, and produce free-energy, entropy, total-correlation, robustness, and adversarial sidecars.
- **Interval brackets on Float residuals for the K=2 decomposition sweep** — Conservative interval brackets check that Float-pipeline residuals fall within a widened high-precision envelope, without counting this as a proof.
- **Claim-strength ledger separating exact, parametric, numerical, and analogical claims** — Connections to prior frameworks are tagged as exact recoveries, parameterized embeddings, numerical witnesses, or structural analogies.

## Key Findings

- The central result is a free-energy decomposition into per-stream free energy, coupling preference terms, the coupling normalizer, and the information cost of leaving independence.
- The decomposition makes multi-information the explicit surcharge paid by a non-factorized policy posterior.
- Mean-field active inference is recovered as the exact independent case, with other frameworks linked through stated posterior-factorization maps.
- A verified Float-to-real error bridge for the numerical layer remains an explicitly open interface rather than an implied proof.
- The author states the manuscript does not claim a neural, clinical, biological, or quantum implementation; Markov-blanket and tensor-network language is a scoped analogy.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [ActiveInferenceInstitute/policy_entanglement](https://github.com/ActiveInferenceInstitute/policy_entanglement)
- GitHub release: [v1.0.0](https://github.com/ActiveInferenceInstitute/policy_entanglement/releases/tag/v1.0.0)
- DOI: [10.5281/zenodo.20418904](https://doi.org/10.5281/zenodo.20418904)
- Zenodo record: [https://zenodo.org/records/20418904](https://zenodo.org/records/20418904)
- PDF: [Friedman_2026_Policy_ae7cdd62.pdf](Friedman_2026_Policy_ae7cdd62.pdf)
- PDF SHA-256: ae7cdd62929324101ead3eba8177199141b0089a9baf35558107149331666fde

## Citation

> Daniel Ari Friedman (2026). *Policy Entanglement in Active Inference*. Zenodo. DOI: 10.5281/zenodo.20418904. URL: https://doi.org/10.5281/zenodo.20418904.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
