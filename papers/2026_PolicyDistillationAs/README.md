<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 🧠 On-Policy Distillation as Active Inference in Finite Variational Models

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20747834-blue)](https://doi.org/10.5281/zenodo.20747834)

---

## Abstract

> This paper formulates on-policy distillation as active inference in finite variational models, with exact claims only for declared objects and interpretive claims explicitly bounded outside them. In the construction, the intractable teacher policy plays the role of the generative model $p(o,s)$, the tractable student policy is the approximate posterior $q(s)$, and the per-token reverse-KL...

## Keywords

`on-policy distillation` · `active inference` · `self-distillation` · `privileged information` · `free energy principle` · `reverse KL divergence` · `pymdp` · `sophisticated inference`

## Methods

- **Formal mapping of OPD roles onto active-inference variational objects** — Teacher policy is read as the generative model, student policy as the approximate posterior, and per-token reverse-KL loss as variational free energy.
- **Bernoulli-Ising oracle with closed-form and recomputed mutual-information sweeps** — A binary toy couples a teacher's privileged variable to the answer through a coupling parameter; MI and the free-energy gap are computed analytically.
- **pymdp T-maze rollout with sophisticated-inference planning** — A pymdp agent samples its own observations under a privileged cue, serving as the on-policy student process witness.
- **Two-agent classroom: privileged teacher vs on-policy student** — A teacher with cue validity 0.98 and a student with cue validity 0.5 are compared on belief entropy and reverse-KL distillation signal.
- **Lean theorem inventory and fail-closed manuscript validation gates** — Lean theorem statements are extracted and checked against an inventory, with gates failing on sorry, axiom or native_decide.

## Key Findings

- The closed-form and independently recomputed mutual-information sweeps agree to machine precision (RMSE 2.1e-16 nats).
- In the classroom toy, teacher belief entropy was 0.247 nats versus 0.347 nats for the student, with a mean reverse-KL distillation signal of 6.28 nats.
- In a four-state/two-action witness, teacher-forced train loss (0.333 nats) underestimated student-induced test loss (0.409 nats); on-policy correction reduced it to 0.096 nats.
- All reported numbers are hydrated from generated artifacts, and 16 of 16 invariant checks pass before rendering.
- The author states these are toy, generated findings rather than production-LLM measurements; external OPD results are context, not reproduced.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [ActiveInferenceInstitute/on_policy_distillation](https://github.com/ActiveInferenceInstitute/on_policy_distillation)
- GitHub release: [v1.0.2](https://github.com/ActiveInferenceInstitute/on_policy_distillation/releases/tag/v1.0.2)
- DOI: [10.5281/zenodo.20747834](https://doi.org/10.5281/zenodo.20747834)
- Artifact DOI: [10.5281/zenodo.20749817](https://doi.org/10.5281/zenodo.20749817)
- Zenodo record: [https://zenodo.org/records/20747834](https://zenodo.org/records/20747834)
- PDF: [Friedman_2026_Onpolicy_c6b5ec49.pdf](Friedman_2026_Onpolicy_c6b5ec49.pdf)
- PDF SHA-256: c6b5ec494915e6e046f24cf723f8dbbf93a5b168544daed3cca14c089d4087aa

## Citation

> Daniel Ari Friedman (2026). *On-Policy Distillation as Active Inference in Finite Variational Models*. Zenodo. DOI: 10.5281/zenodo.20747834. URL: https://doi.org/10.5281/zenodo.20747834.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
