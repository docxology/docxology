<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 Policy Entanglement in Active Inference

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20418904-blue)](https://doi.org/10.5281/zenodo.20418904)

---

## Abstract

> Active inference models often need to choose among several policy streams at once, for example streams tied to different effectors, sensory channels, agents, agents within a group, or planning horizons. Standard discrete active-inference implementations keep this manageable by treating those streams as independent, but that simplification removes the dependencies that make coordinated action possible. This manuscript introduces policy entanglement: a controlled deformation of the usual independent policy posterior by a scalar coupling strength and explicit compatibility and preference potentials. The construction preserves the finite active inference setting while making cross-stream dependence a first-class modeling object rather than an implicit artifact of the chosen factorization. The framework keeps a claim-strength ledger that distinguishes exact recoveries, parameterized embeddings, numerical witnesses, and structural analogies. Mean-field active inference is the exact independent case. Products of experts, copula variational inference, options, hierarchical and sophisticated inference, branching-time active inference, renormalization-style compression, and Markov-blanket multi-agent views are connected as special cases through their stated posterior-factorization maps. The central result is a free-energy decomposition that separates ordinary per-stream free energy, coupling preference terms, the coupling normalizer, and the information cost of leaving independence. The decomposition makes multi-information the explicit surcharge paid by a non-factorized policy posterior and shows how coupling strength, compatibility structure, and off-diagonal preference costs enter the same accounting identity. This result supplies the organizing principle for the rest of the paper. It supports an information-geometric reading of the coupled policy family as a path away from the mean-field submanifold, a projection identity that returns the coupled posterior to its independent marginals, a spectral and tensor-train view of dominant coordinated policy modes, a heterogeneous-ensemble coupling-tax bound, and a phase vocabulary for under-coupled, mixed, and highly concentrated policy posteriors. These interpretations are intentionally limited: the manuscript does not claim a neural, clinical, biological, or quantum implementation, and Markov-blanket and tensor-network language is used as scoped modeling analogy unless a specific theorem row or generated artifact supports a stronger statement. The main decomposition analytic identity is machine-checked in ℝ in the Mathlib-backed Lean layer with an axiom audit and negative controls. A separate stock-Lean boundary fragment remains Mathlib-free and exposes the theorem surface as typed contracts for the Python simulation layer and the manuscript registry, including witness-consuming rows where analytic payloads are deliberately supplied at the boundary. The executable numerical layer remains a Float pipeline, so a verified Float↔ℝ error bridge is still an explicitly open interface rather than an implied proof; conservative interval brackets on the K=2 decomposition sweep certify Float residuals within a widened high-precision envelope (output/reports/float_real_residual.json) without promoting the registry row to proved. The empirical companion uses pymdp and NumPy to sweep coupled policy ensembles, run short and long rollouts, check the projection identity to round-off precision, produce free-energy, entropy, total-correlation, action-distribution, robustness, and adversarial sidecars, and render figures from those artifacts. The manuscript, figures, theorem map, citation registry, notation glossary (§S6), bibliography, and PDF are regenerated from the same source-owned pipeline, so prose claims are tied to Lean sources, Python witnesses, output metadata, and validation gates rather than maintained by hand. All manuscript methods, tests, and documentation are available as open-source software at https://github.com/ActiveInferenceInstitute/policy_entanglement (DOI: https://doi.org/10.5281/zenodo.20419536).

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
