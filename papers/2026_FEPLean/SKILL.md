---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "Towards Lean 4 Formalization of the Free Energy Principle: AI-Driven Theorem Sketching and Verification for Active Inference and Bayesian Mechanics"
description: "<p><strong>FEP_Lean v1.1.0</strong> is a source-bound, machine-checked catalogue of 155 topics across 20 reviewed families and five areas: the Free Energy Principle, Active Inference, Bayesian Mechanics, Information Geometry, and non-equilibrium Ther..."
tags: ["free-energy-principle", "active-inference", "bayesian-mechanics", "information-geometry", "non-equilibrium-thermodynamics", "lean-4", "mathlib", "interactive-theorem-proving", "formal-verification", "theorem-proving"]
domain: "Active Inference"
citation: "Daniel Ari Friedman (2026). *Towards Lean 4 Formalization of the Free Energy Principle: AI-Driven Theorem Sketching and Verification for Active Inference and Bayesian Mechanics*. Active Inference Journal."
doi: "10.5281/zenodo.19699233"
artifact_doi: "10.5281/zenodo.22072956"
---

# Towards Lean 4 Formalization of the Free Energy Principle: AI-Driven Theorem Sketching and Verification for Active Inference and Bayesian Mechanics

**Daniel Ari Friedman** (2026) · Active Inference

## Context

This work addresses topics in **Active Inference**: free energy principle, active inference, bayesian mechanics, information geometry.

## Methods

Primary methods and techniques applied in this work:

- **Curated catalog of 50 FEP topics as namespaced Lean 4 sketches against Mathlib4** — Compiled 50 topics across five pillars (FEP, Active Inference, Bayesian Mechanics, Information Geometry, Thermodynamics) as Lean 4 sketches from a single source of truth.
- **Native lake env lean verification on a pinned Lean/Mathlib v4.29.0 stack** — Verified every reported compilation result with a real lake env lean invocation against the pinned toolchain, with no mocked compilers or synthetic success signals.
- **LLM-assisted commentary pipeline (Hermes/OpenGauss, kimi-k2.6 via OpenRouter)** — Layered LLM drafting and commentary over the catalog, cached by Lean source hash, with the Lean kernel kept as sole ground truth for compilation claims.
- **Zero-mock test suite with coverage gate and SQLite run persistence** — Ran 347 tests that each exercise real files, a real SQLite store, live compiler calls or actual HTTP calls, holding coverage above an 89% CI gate.
- **Three-level sorry-aware maturity taxonomy (real / partial / aspirational)** — Introduced a classification intended to make incomplete formalization explicit; all current rows are tagged real.

## Key Findings

Core contributions and results:

- On the pinned Lean 4 / Mathlib4 v4.29.0 stack, the shipped catalog compiles 50/50 sorry-free.
- The Hermes-assisted Gauss run run_20260424_064334 achieved 50/50 clean compiles with 0 sorry and 0 errors.
- Constructions that already typecheck in today's Mathlib4 include finite-set probability, Bayesian updating, finite-space KL divergence and variational free-energy bounds.
- The author cautions that the catalog covers definitional lemmas and structural identities rather than end-to-end FEP theorems, and many rows stop short of what the informal text proves.
- Formal verification here establishes formal adequacy only; it provides no empirical confirmation that brains minimize variational free energy.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2018_WoodliceAndMen](../2018_WoodliceAndMen/)
- [2020_BehaviorEngineering](../2020_BehaviorEngineering/)
- [2021_ModelingConflict](../2021_ModelingConflict/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.19699233
- PDF SHA-256: See zenodo_record
- Pairing confidence: strong
- Last checked: 2026-09-24T18:29:54Z
- Artifact DOI: 10.5281/zenodo.22072956

## Prerequisites

- Familiarity with free energy principle, active inference, bayesian mechanics
- Background in Active Inference fundamentals
- Access to source repository: ActiveInferenceInstitute/fep_formal

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.19699233`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
