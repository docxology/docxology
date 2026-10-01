---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "AlphaCOGANT: Recursive Corporate Self-Improvement as Active Inference"
description: "The AlphaFund whitepaper reframes recursive self-improvement (RSI) as a portfolio optimization problem: a corporation recursively improves when realized economic gains finance the next cycle of better prediction and deployment, and the firm's standin..."
tags: ["active-inference", "expected-free-energy", "recursive-self-improvement", "generalized-notation-notation", "economic-world-model", "portfolio-optimization", "epistemic-value", "reproducible-research"]
domain: "Computational"
citation: "Daniel Ari Friedman, Tucker Cahill Chambers (2026). *AlphaCOGANT: Recursive Corporate Self-Improvement as Active Inference*. Zenodo."
doi: "10.5281/zenodo.20976824"
---

# AlphaCOGANT: Recursive Corporate Self-Improvement as Active Inference

**Daniel Ari Friedman, Tucker Cahill Chambers** (2026) · Computational

## Context

This work addresses topics in **Computational**: active inference, expected free energy, recursive self-improvement, Generalized Notation Notation.

## Methods

Primary methods and techniques applied in this work:

- **Construct-by-construct AlphaFund-to-Active Inference dictionary** — Mapped each AlphaFund whitepaper construct (corporation tuple, EWM, filtration, action vector, t-RSI, etc.) to an Active Inference object.
- **GNN model file of the five-channel firm produced via the COGANT pattern** — Wrote AlphaFund's Economic World Model as a Generalized Notation Notation file with channel factors, A/B matrices, log-preferences and an EFE objective, using COGANT's codebase-to-GNN step.
- **Deterministic tested NumPy Active Inference engine (src/alphacogant/)** — Implemented state inference over channels, the epistemic/pragmatic EFE split, the marginal-return vector, and t-RSI certificate evaluation.
- **Engine-gated manuscript numbers and figure-provenance registry** — Generated every cited numeric from one function and cross-checked it by test, and registered each figure with its producer script and hashed manifest.
- **Bootstrap of create/decay posteriors with Dirichlet concentration sensitivity** — Bootstrapped belief uncertainty to compute standardized t-RSI and reported its sensitivity to the Dirichlet concentration parameter alpha.

## Key Findings

Core contributions and results:

- The paper argues AlphaFund's recursive-self-improvement-as-portfolio-optimization has an Active Inference representation that is expressible in GNN and producible by the COGANT pattern.
- t-RSI is recovered as the standardized distance between create-rate and decay-rate posteriors, i.e. a thresholded EFE-improvement certificate gating self-improvement commits.
- At point-estimate level the comparator discriminates: create exceeds decay (admit) at the self-improving point and falls below it (reject) at the coasting point.
- Caveat: with bootstrapped uncertainty the reduced two-level model's headline t-RSI is negative (-13.2552) at the self-improving point, so it does not robustly certify net improvement.
- The authors state AlphaCOGANT is a modeling and integrity instrument, not a trading system or financial advice, and does not reproduce AlphaFund's proprietary surfaces or track record.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2026_COGANT](../2026_COGANT/)
- [2025_CEREBRUM](../2025_CEREBRUM/)
- [2026_FEPLean](../2026_FEPLean/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.20976824
- PDF SHA-256: See zenodo_record
- Pairing confidence: strong
- Last checked: 2026-09-24T18:29:57Z

## Prerequisites

- Familiarity with active inference, expected free energy, recursive self-improvement
- Background in Computational fundamentals
- Access to source repository: docxology/alphacogant

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.20976824`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
