<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 Active Inference Multi-Track Exemplar

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20417021-blue)](https://doi.org/10.5281/zenodo.20417021)

---

## Abstract

> We study a minimal Active Inference stack on toy models: a Bernoulli–Ising analytical oracle, a pymdp T-maze rollout, and a sheaf-indexed compose contract that binds 34 fragment tracks into 12 flat IMRAD sections. The methodological contribution is a discipline rather than a domain finding: every reported number is hydrated from a generated artifact and every cross-track claim is machine-checked before rendering, so no figure or statistic can drift from the artifact that produced it — 6 sheaf axioms are verified before composition and 25 negative controls keep each failure path live. Claims are limited to those models and their generated artifacts. reports a 17-row coverage matrix (5 IMRAD group headers) regenerated from the live manifest at compose time. documents the T-maze harness aligned with pymdp sophisticated_inference examples (https://github.com/infer-actively/pymdp/tree/main/examples/experimental/sophisticated_inference). records 12 / 12 invariant checks passed. SI planning horizon: 2 steps. Sweep RMSE 0 nats bounds analytical–empirical agreement on the coupling grid.

## Keywords

`active inference` · `pymdp` · `sophisticated inference` · `generalized notation notation` · `lean`

## Methods

- **Bernoulli–Ising analytical oracle (K=2)** — Closed-form mutual information and free-energy decomposition on a symmetric Bernoulli–Ising toy, cross-checked by an independent exact recomputation via total correlation.
- **Deterministic pymdp T-maze rollout** — A minimal T-maze following pymdp sophisticated_inference examples, defaulting to state_inference with planning horizon policy_len = 2 and logged beliefs and actions.
- **Sheaf-indexed manuscript compose contract** — Binds 34 composable fragment types to manifest rows under an IMRAD outline, verifying sheaf axioms and negative controls before rendering.
- **Lean boundary-witness formalization** — Lean modules checked by lake build state small finite T-maze and graph-world witnesses, with axioms audited via #print axioms; explicitly not a broad formalization.
- **Artifact-hydrated reporting with validation gates** — Every reported number is hydrated from generated artifacts and cross-track claims are machine-checked by pipeline gates before the PDF is built.

## Key Findings

- The paper frames its result as a methodological discipline rather than a domain claim: 6 sheaf axioms are machine-checked and 25 negative controls keep failure paths live.
- It reports 12/12 invariant checks passed and a sweep RMSE of 0 nats between analytical and empirical values on the coupling grid.
- The measured state_inference T-maze rollout reports mean belief entropy 0.3251 nats over 2 steps, with goal reached and action diversity 2.
- A coverage audit reports 95 present, 95 bound, and 0 missing cells on the IMRAD matrix.
- The author states the models are pedagogical and validate consistency and artifact wiring, not empirical claims about biological agents.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [docxology/template_active_inference](https://github.com/docxology/template_active_inference)
- GitHub release: [v0.3.2](https://github.com/docxology/template_active_inference/releases/tag/v0.3.2)
- DOI: [10.5281/zenodo.20417021](https://doi.org/10.5281/zenodo.20417021)
- Zenodo record: [https://zenodo.org/records/20417021](https://zenodo.org/records/20417021)
- PDF: [Friedman_2026_Active_158b2fe2.pdf](Friedman_2026_Active_158b2fe2.pdf)
- PDF: [Friedman_2026_Active_713452dd.pdf](Friedman_2026_Active_713452dd.pdf)
- PDF: [Friedman_2026_Active_f191b48f.pdf](Friedman_2026_Active_f191b48f.pdf)
- PDF SHA-256: f191b48f94394cab17069fd04502c59fc1c287e7893eb078e05ba4be04d4a04c

## Citation

> Daniel Ari Friedman (2026). *Active Inference Multi-Track Exemplar*. Zenodo. DOI: 10.5281/zenodo.20417021. URL: https://doi.org/10.5281/zenodo.20417021.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
