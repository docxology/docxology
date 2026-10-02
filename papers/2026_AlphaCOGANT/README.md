<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 AlphaCOGANT: Recursive Corporate Self-Improvement as Active Inference

**Daniel Ari Friedman, Tucker Cahill Chambers** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20976824-blue)](https://doi.org/10.5281/zenodo.20976824)

---

## Abstract

> The AlphaFund whitepaper reframes recursive self-improvement (RSI) as a portfolio optimization problem: a corporation recursively improves when realized economic gains finance the next cycle of better prediction and deployment, and the firm's standing is summarized by t-RSI, a standardized gap between alpha-creation and alpha-decay rates. AlphaCOGANT observes that this construction is, term for term, an Active Inference agent — and makes the correspondence executable. We render AlphaFund's Economic World Model (EWM) as a generative model written in Generalized Notation Notation (GNN), produced by the COGANT codebase-to-GNN translation pattern. The firm's five capital channels — Investments, Sensors, Actuators, Parameters, and R&D — become the hidden-state factors of a partially-observed model; capital allocation becomes the control vector; and the portfolio optimizer's marginal-return objective becomes Expected Free Energy (EFE) minimization. The EFE decomposition supplies a principled reading of AlphaFund's own categories: its pragmatic value is expected log-equity growth (the alpha-creation rate, read off the broker ledger), and its epistemic value is the information gain about the EWM that Sensors and R&D purchase (the data-scaling and forecast-sharpening laws). t-RSI is recovered as the standardized distance between the create-rate and decay-rate posteriors — the thresholded EFE-improvement certificate that admits a self-improvement commit only when creation confidently exceeds decay. We give the technical and computational realization: a GNN model file for the five-channel firm, a tested NumPy Active Inference engine that performs state inference, computes the epistemic/pragmatic EFE split and the marginal-return vector, and evaluates the t-RSI certificate. We argue that GNN-via-COGANT brings two things AlphaFund's program needs and Active Inference already enforces: filtration integrity (the model may condition only on information available at decision time — the same "no-peeking" discipline that separates an EWM from a language model) and auditable capital allocation (every admissible funding move has a negative-EFE score under a single, legible objective). This is not financial advice; it is a demonstration that this reduced recursive-corporate-self-improvement model has a direct Active Inference representation supported by source-owning methods and artifact checks .

## Keywords

`active inference` · `expected free energy` · `recursive self-improvement` · `Generalized Notation Notation` · `economic world model` · `portfolio optimization` · `epistemic value` · `reproducible research`

## Methods

- **Construct-by-construct AlphaFund-to-Active Inference dictionary** — Mapped each AlphaFund whitepaper construct (corporation tuple, EWM, filtration, action vector, t-RSI, etc.) to an Active Inference object.
- **GNN model file of the five-channel firm produced via the COGANT pattern** — Wrote AlphaFund's Economic World Model as a Generalized Notation Notation file with channel factors, A/B matrices, log-preferences and an EFE objective, using COGANT's codebase-to-GNN step.
- **Deterministic tested NumPy Active Inference engine (src/alphacogant/)** — Implemented state inference over channels, the epistemic/pragmatic EFE split, the marginal-return vector, and t-RSI certificate evaluation.
- **Engine-gated manuscript numbers and figure-provenance registry** — Generated every cited numeric from one function and cross-checked it by test, and registered each figure with its producer script and hashed manifest.
- **Bootstrap of create/decay posteriors with Dirichlet concentration sensitivity** — Bootstrapped belief uncertainty to compute standardized t-RSI and reported its sensitivity to the Dirichlet concentration parameter alpha.

## Key Findings

- The paper argues AlphaFund's recursive-self-improvement-as-portfolio-optimization has an Active Inference representation that is expressible in GNN and producible by the COGANT pattern.
- t-RSI is recovered as the standardized distance between create-rate and decay-rate posteriors, i.e. a thresholded EFE-improvement certificate gating self-improvement commits.
- At point-estimate level the comparator discriminates: create exceeds decay (admit) at the self-improving point and falls below it (reject) at the coasting point.
- Caveat: with bootstrapped uncertainty the reduced two-level model's headline t-RSI is negative (-13.2552) at the self-improving point, so it does not robustly certify net improvement.
- The authors state AlphaCOGANT is a modeling and integrity instrument, not a trading system or financial advice, and does not reproduce AlphaFund's proprietary surfaces or track record.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [docxology/alphacogant](https://github.com/docxology/alphacogant)
- GitHub release: [v1.0.1](https://github.com/docxology/alphacogant/releases/tag/v1.0.1)
- DOI: [10.5281/zenodo.20976824](https://doi.org/10.5281/zenodo.20976824)
- Zenodo record: [https://zenodo.org/records/20976824](https://zenodo.org/records/20976824)
- PDF: [Friedman_2026_Alphacogant_41efa7a8.pdf](Friedman_2026_Alphacogant_41efa7a8.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/20976824)

## Citation

> Daniel Ari Friedman, Tucker Cahill Chambers (2026). *AlphaCOGANT: Recursive Corporate Self-Improvement as Active Inference*. Zenodo. DOI: 10.5281/zenodo.20976824. URL: https://doi.org/10.5281/zenodo.20976824.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
