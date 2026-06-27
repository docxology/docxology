# AlphaCOGANT: Recursive Corporate Self-Improvement as Active Inference

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20976824.svg)](https://doi.org/10.5281/zenodo.20976824)

---

## Abstract

The AlphaFund whitepaper reframes recursive self-improvement (RSI) as a portfolio
optimization problem:  a corporation recursively improves when realized economic
gains finance the next cycle of better prediction and deployment, and the firm's
standing is summarized by t-RSI, a standardized gap between alpha-creation and
alpha-decay rates. AlphaCOGANT observes that this construction is, term for
term, an Active Inference agent  — and makes the correspondence executable.

We render AlphaFund's Economic World Model (EWM) as a generative model written
in Generalized Notation Notation (GNN), produced by the COGANT
codebase-to-GNN translation pattern. The firm's five capital channels —
Investments, Sensors, Actuators, Parameters, and R&amp;D — become the hidden-state
factors of a partially-observed model; capital allocation becomes the control
vector; and the portfolio optimizer's marginal-return objective becomes
Expected Free Energy (EFE) minimization. The EFE decomposition supplies a
principled reading of AlphaFund's own categories: its pragmatic value is
expected log-equity growth (the alpha-creation rate, read off the broker ledger),
and its epistemic value is the information gain about the EWM that Sensors and
R&amp;D purchase (the data-scaling and forecast-sharpening laws). t-RSI is recovered
as the standardized distance between the create-rate and decay-rate posteriors —
the thresholded EFE-improvement certificate that admits a self-improvement commit
only when creation confidently exceeds decay.

We give the technical and computational realization: a GNN model file for the
five-channel firm, a tested NumPy Active Inference engine that performs state
inference, computes the epistemic/pragmatic EFE split and the marginal-return
vector, and evaluates the t-RSI certificate. We argue that GNN-via-COGANT brings
two things AlphaFund's program needs and Active Inference already enforces:
filtration integrity (the model may condition only on information available
at decision time — the same "no-peeking" discipline that separates an EWM from a
language model) and auditable capital allocation (every admissible funding
move has a negative-EFE score under a single, legible objective). This is not
financial advice; it is a demonstration that this reduced
recursive-corporate-self-improvement model has a direct Active Inference
representation supported by source-owning methods and artifact checks .

---
Associated artifacts
GitHub release: v1.0.1 (https://github.com/docxology/alphacogant/releases/tag/v1.0.1)
DOI: https://doi.org/10.5281/zenodo.20976824
Zenodo: https://zenodo.org/records/20976824
PDF SHA-256: 41efa7a8a98e6a67cece68377b8f0c5f19304e85c664ec9516353ee24eb0421f

## Keywords

active inference · expected free energy · recursive self-improvement · Generalized Notation Notation · economic world model · portfolio optimization · epistemic value · reproducible research

## Publication Details

| Field | Value |
|------|-------|
| **DOI** | [10.5281/zenodo.20976824](https://doi.org/10.5281/zenodo.20976824) |
| **Published** | 2026 |
| **Version** | 1.0.1 |
| **Zenodo record** | https://zenodo.org/records/20977774 |
| **GitHub release** | https://github.com/docxology/alphacogant/releases/tag/v1.0.1 |
| **Source repository** | https://github.com/docxology/alphacogant |

## Files

- `Friedman_2026_Alphacogant_41efa7a8.pdf` - Zenodo PDF

## Citation

> Friedman, D. A. (2026). *AlphaCOGANT: Recursive Corporate Self-Improvement as Active Inference*. Zenodo. https://doi.org/10.5281/zenodo.20976824

## Related

- GitHub release: https://github.com/docxology/alphacogant/releases/tag/v1.0.0

- Zenodo record: https://zenodo.org/records/20977774
- GitHub release: https://github.com/docxology/alphacogant/releases/tag/v1.0.1
- Source repository: https://github.com/docxology/alphacogant
- [Full Bibliography](../../pages/BIBLIOGRAPHY.md) · [All Papers](../README.md)
