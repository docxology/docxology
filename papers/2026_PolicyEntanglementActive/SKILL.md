---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "Policy Entanglement in Active Inference"
description: "Active inference models often need to choose among several policy streams at once, for example streams tied to different effectors, sensory channels, agents, agents within a group, or planning horizons. Standard discrete active-inference implementati..."
tags: ["active-inference", "free-energy-principle", "policy-inference", "mean-field", "total-correlation", "information-geometry", "schmidt-rank", "tensor-networks", "sophisticated-inference", "lean-theorem-proving"]
domain: "Computational"
citation: "Daniel Ari Friedman (2026). *Policy Entanglement in Active Inference*. Zenodo."
doi: "10.5281/zenodo.20418904"
---

# Policy Entanglement in Active Inference

**Daniel Ari Friedman** (2026) · Computational

## Context

This work addresses topics in **Computational**: active inference, free energy principle, policy inference, mean-field.

## Methods

Primary methods and techniques applied in this work:

- **Coupling-parameter deformation of the independent policy posterior** — Multi-stream policy posteriors are deformed away from the mean-field product by a scalar coupling strength plus compatibility and preference potentials.
- **Lean 4 formalization: Mathlib proof of the central identity plus stock-Lean boundary** — MathlibProofs machine-checks the S01 free-energy identity with an axiom audit and negative controls; a stock-Lean fragment exposes a 21-row theorem surface as typed contracts.
- **pymdp/NumPy POMDP simulations of coupled policy ensembles** — Simulations sweep coupled ensembles, run short and long rollouts, check the projection identity, and produce free-energy, entropy, total-correlation, robustness, and adversarial sidecars.
- **Interval brackets on Float residuals for the K=2 decomposition sweep** — Conservative interval brackets check that Float-pipeline residuals fall within a widened high-precision envelope, without counting this as a proof.
- **Claim-strength ledger separating exact, parametric, numerical, and analogical claims** — Connections to prior frameworks are tagged as exact recoveries, parameterized embeddings, numerical witnesses, or structural analogies.

## Key Findings

Core contributions and results:

- The central result is a free-energy decomposition into per-stream free energy, coupling preference terms, the coupling normalizer, and the information cost of leaving independence.
- The decomposition makes multi-information the explicit surcharge paid by a non-factorized policy posterior.
- Mean-field active inference is recovered as the exact independent case, with other frameworks linked through stated posterior-factorization maps.
- A verified Float-to-real error bridge for the numerical layer remains an explicitly open interface rather than an implied proof.
- The author states the manuscript does not claim a neural, clinical, biological, or quantum implementation; Markov-blanket and tensor-network language is a scoped analogy.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2023_NSFReporting](../2023_NSFReporting/)
- [2023_NaturalAIBased](../2023_NaturalAIBased/)
- [2025_AuBI](../2025_AuBI/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.20418904
- PDF SHA-256: ae7cdd62929324101ead3eba8177199141b0089a9baf35558107149331666fde
- Pairing confidence: strong
- Last checked: 2026-09-24T18:29:54Z

## Prerequisites

- Familiarity with active inference, free energy principle, policy inference
- Background in Computational fundamentals
- Access to source repository: ActiveInferenceInstitute/policy_entanglement

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.20418904`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
