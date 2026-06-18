# On-Policy Distillation as Active Inference in Finite Variational Models

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20749817.svg)](https://doi.org/10.5281/zenodo.20749817)

---

## Abstract

Abstract

This paper formulates on-policy distillation as active inference in finite variational models, with exact claims only for declared objects and interpretive claims explicitly bounded outside them. In the construction, the intractable teacher policy plays the role of the generative model $p(o,s)$, the tractable student policy is the approximate posterior $q(s)$, and the per-token reverse-KL distillation loss is variational free energy up to the evidence constant, $F = D_{\mathrm{KL}}(q\,\|\,p(s\mid o)) - \log p(o)$, whose KL target is the teacher-induced posterior $p(s\mid o)\propto p(o,s)$ .

The title's "as" is therefore a scoped mathematical correspondence rather than the slogan OPD = Active Inference. Variational free energy names the realized-rollout distillation loss; expected free energy remains the planning-side objective by which the pymdp agent selects actions . On-policy student rollouts generate the observations on which the posterior is scored, connecting the construction to induced-distribution mismatch in imitation learning and exposure-bias analyses while preserving their different objectives, empirical regimes, and contested severity . Privileged traces and feedback play the role that train-time-only information plays in the LUPI/distillation lineage .

Four deterministic witnesses instantiate the correspondence. A Bernoulli-Ising oracle couples a teacher's privileged variable to the answer through $\lambda$, making $I(\lambda)$ the teacher-student mutual information and the finite free-energy gap the toy distillation objective; the closed-form and independently recomputed mutual-information sweeps agree to machine precision (RMSE 2.1e-16 nats). A pymdp T-maze rollout supplies the on-policy student that samples its own observations under a privileged cue . A two-agent classroom pits a privileged teacher (cue validity 0.98) against an on-policy student (cue validity 0.5), measuring teacher belief entropy 0.247 nats versus student 0.347 nats and a mean reverse-KL distillation signal of 6.28 nats. A four-state/two-action sequential-shift witness shows teacher-forced train loss 0.333 nats underestimating student-induced test loss 0.409 nats, with deterministic on-policy correction reducing it to 0.096 nats.

These are toy, generated findings, not production-LLM measurements. Recent privileged-context, context-distillation, adaptive-teacher, freshness-aware OPD, RLHF/instruction-tuning, self-generated reasoning, Qwen OPD-vs-RL, and Thinking Machines replication reports remain external context rather than reproduced results . The supplemental sheaf/provenance layer keeps that boundary operational: every reported number is hydrated from a generated artifact, every figure is source-bound, and 16 / 16 invariant checks pass before rendering.

---
Associated artifacts
GitHub release: v1.0.2 (https://github.com/ActiveInferenceInstitute/on_policy_distillation/releases/tag/v1.0.2)
DOI: https://doi.org/10.5281/zenodo.20749817
Zenodo: https://zenodo.org/records/20749817
PDF SHA-256: c6b5ec494915e6e046f24cf723f8dbbf93a5b168544daed3cca14c089d4087aa

## Keywords

on-policy distillation · active inference · self-distillation · privileged information · free energy principle · reverse KL divergence · pymdp · sophisticated inference

## Publication Details

| Field | Value |
|------|-------|
| **DOI** | [10.5281/zenodo.20749817](https://doi.org/10.5281/zenodo.20749817) |
| **Published** | 2026-06-18 |
| **Version** | 1.0.2 |
| **Zenodo record** | https://zenodo.org/records/20749817 |
| **GitHub release** | https://github.com/ActiveInferenceInstitute/on_policy_distillation/releases/tag/v1.0.2 |
| **Source repository** | https://github.com/ActiveInferenceInstitute/on_policy_distillation |

## Files

- `Friedman_2026_Onpolicy_c6b5ec49.pdf` - Zenodo PDF

## Citation

> Friedman, D. A. (2026). *On-Policy Distillation as Active Inference in Finite Variational Models*. Zenodo. https://doi.org/10.5281/zenodo.20749817

## Related

- Zenodo record: https://zenodo.org/records/20749817
- GitHub release: https://github.com/ActiveInferenceInstitute/on_policy_distillation/releases/tag/v1.0.2
- Source repository: https://github.com/ActiveInferenceInstitute/on_policy_distillation
- [Full Bibliography](../../pages/BIBLIOGRAPHY.md) · [All Papers](../README.md)
