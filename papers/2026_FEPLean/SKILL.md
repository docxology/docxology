---
name: "FEPLean"
description: "Lean 4 and Mathlib4 formalization of the Free Energy Principle: 50-topic sorry-free catalog, Hermes/OpenGauss LLM drafting with native compiler verification, zero-mock testing, and bridges from variational/Active Inference/Bayesian mechanics to machine-checked statements."
tags:
  - active-inference
  - free-energy-principle
  - lean-4
  - mathlib4
  - interactive-theorem-proving
  - formal-verification
  - bayesian-mechanics
  - information-geometry
  - variational-inference
  - measure-theory
  - llm-itp
  - reproducible-research
---

# Towards Lean 4 Formalization of the Free Energy Principle

**Daniel Ari Friedman** (2026) · Active Inference Institute · formal methods · FEP

## Instructions

Use this skill when the task involves **Lean 4**, **Mathlib4**, **formalization of the FEP** or **Active Inference**, **variational / ELBO** statements, **LLM–ITP workflows** (draft vs. verify), **catalog-driven theorem libraries**, or **reproducible compiler-backed verification** as described in the fep_lean manuscript.

When applying this skill:

1. Treat **native Lean compilation** (and the paper’s **sorry-free** standard where relevant) as the **authority** for formal claims; treat LLM output as **proposals** unless backed by a checked proof.
2. Organize work by the manuscript’s **pillar/topic** structure: FEP, Active Inference, Bayesian mechanics, information geometry, thermodynamics—each with **namespace isolation** and explicit **Mathlib** dependencies.
3. Separate **delivered sorry-free topics** on the pinned stack from **open or aspirational** targets (e.g. certain SDE or full information-geometry formalizations) to avoid over-claiming.
4. For engineering on the open repo, respect the described **zero-mock** test policy: exercise real files, real stores, the **live compiler**, and real HTTP when testing integrated paths.

## Key Concepts

- **Verification gap** — Prose and informal equations vs. the measure-theoretic and type-theoretic obligations Lean exposes.
- **50-topic catalog** — Namespaced sketches with statements, imports, maturity metadata, and deterministic regeneration from source.
- **Axiomatization vs. problem solving** — Building a **shared, auditable** formal layer rather than only solving isolated benchmark problems.
- **Hermes / OpenGauss** — LLM pipeline for commentary and draft proofs; **cache keyed to Lean sources**; **Gauss** session protocol.
- **ELBO and variational free energy** — Bridge examples from informal bounds to **typed Mathlib** statements (see manuscript primer and KL/ELBO examples).
- **Zero-mock discipline** — Tests must hit real artifacts; no stubbed “compilation” in place of the actual prover in verification paths.

## Methods & Techniques

- **Lake** builds; **leanprover/lean4** and **Mathlib4** version pinning as shipping constraints.
- **Import-pattern strategy** for probability and analysis lemmas referenced by the catalog.
- **Maturity levels** and migration from `sorry` to fully checked proofs where the project policy allows work in progress in development but enforces a **shipping gate** (as documented).
- **Parallelism and caching** (e.g. Mathlib build cache) for practical CI and local verification loops.

## Key Findings

- A **reproducible, machine-checkable** anchor for a large slice of FEP-adjacent mathematics, with **explicit** labeling of what remains at aspirational or partial maturity.
- **Complementary** LLM and ITP roles: language models for **drafting and explanation**; **Lean** for **ground-truth** proof obligation checking.
- **Ecosystem view**: Mathlib4 already supports substantial fragments (e.g. finite-set probability, KL on finite spaces, key variational bound shapes) while deep continuous-time and geometric extensions remain frontier work.

## Prerequisites

- Basic **type theory** intuition (propositions as types, tactics at a high level).
- **Active Inference** / **FEP** vocabulary: variational free energy, generative models, perception–action loops (conceptual).
- **Probability and measure theory** at least at the level of **integrals**, **dominated convergence** awareness, and **Kullback–Leibler** on finite or simple spaces—per manuscript’s primer sections.

## Consulting & Tutoring

[Daniel Ari Friedman, PhD](https://docxology.github.io/docxology/) is available for AI research consulting and tutoring related to this skill.

## Related Skills

See [BIBLIOGRAPHY.md](../../pages/BIBLIOGRAPHY.md) for the complete publication catalog.

**Code and archive**: [https://github.com/ActiveInferenceInstitute/fep_lean](https://github.com/ActiveInferenceInstitute/fep_lean) · [https://doi.org/10.5281/zenodo.19699234](https://doi.org/10.5281/zenodo.19699234)
