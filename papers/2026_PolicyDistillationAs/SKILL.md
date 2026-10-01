---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "On-Policy Distillation as Active Inference in Finite Variational Models"
description: "This paper formulates on-policy distillation as active inference in finite variational models, with exact claims only for declared objects and interpretive claims explicitly bounded outside them. In the construction, the intractable teacher policy pl..."
tags: ["on-policy-distillation", "active-inference", "self-distillation", "privileged-information", "free-energy-principle", "reverse-kl-divergence", "pymdp", "sophisticated-inference"]
domain: "Active Inference"
citation: "Daniel Ari Friedman (2026). *On-Policy Distillation as Active Inference in Finite Variational Models*. Zenodo."
doi: "10.5281/zenodo.20747834"
artifact_doi: "10.5281/zenodo.20749817"
---

# On-Policy Distillation as Active Inference in Finite Variational Models

**Daniel Ari Friedman** (2026) · Active Inference

## Context

This work addresses topics in **Active Inference**: on-policy distillation, active inference, self-distillation, privileged information.

## Methods

Primary methods and techniques applied in this work:

- **Formal mapping of OPD roles onto active-inference variational objects** — Teacher policy is read as the generative model, student policy as the approximate posterior, and per-token reverse-KL loss as variational free energy.
- **Bernoulli-Ising oracle with closed-form and recomputed mutual-information sweeps** — A binary toy couples a teacher's privileged variable to the answer through a coupling parameter; MI and the free-energy gap are computed analytically.
- **pymdp T-maze rollout with sophisticated-inference planning** — A pymdp agent samples its own observations under a privileged cue, serving as the on-policy student process witness.
- **Two-agent classroom: privileged teacher vs on-policy student** — A teacher with cue validity 0.98 and a student with cue validity 0.5 are compared on belief entropy and reverse-KL distillation signal.
- **Lean theorem inventory and fail-closed manuscript validation gates** — Lean theorem statements are extracted and checked against an inventory, with gates failing on sorry, axiom or native_decide.

## Key Findings

Core contributions and results:

- The closed-form and independently recomputed mutual-information sweeps agree to machine precision (RMSE 2.1e-16 nats).
- In the classroom toy, teacher belief entropy was 0.247 nats versus 0.347 nats for the student, with a mean reverse-KL distillation signal of 6.28 nats.
- In a four-state/two-action witness, teacher-forced train loss (0.333 nats) underestimated student-induced test loss (0.409 nats); on-policy correction reduced it to 0.096 nats.
- All reported numbers are hydrated from generated artifacts, and 16 of 16 invariant checks pass before rendering.
- The author states these are toy, generated findings rather than production-LLM measurements; external OPD results are context, not reproduced.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2018_WoodliceAndMen](../2018_WoodliceAndMen/)
- [2020_BehaviorEngineering](../2020_BehaviorEngineering/)
- [2021_ModelingConflict](../2021_ModelingConflict/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.20747834
- PDF SHA-256: c6b5ec494915e6e046f24cf723f8dbbf93a5b168544daed3cca14c089d4087aa
- Pairing confidence: strong
- Last checked: 2026-09-24T18:29:56Z
- Artifact DOI: 10.5281/zenodo.20749817

## Prerequisites

- Familiarity with on-policy distillation, active inference, self-distillation
- Background in Active Inference fundamentals
- Access to source repository: ActiveInferenceInstitute/on_policy_distillation

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.20747834`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
