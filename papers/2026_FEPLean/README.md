<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 🧠 Towards Lean 4 Formalization of the Free Energy Principle: AI-Driven Theorem Sketching and Verification for Active Inference and Bayesian Mechanics

**Daniel Ari Friedman** (2026) · *Active Inference Journal*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.19699233-blue)](https://doi.org/10.5281/zenodo.19699233)

---

## Abstract

> FEP_Lean v1.1.0 is a source-bound, machine-checked catalogue of 155 topics across 20 reviewed families and five areas: the Free Energy Principle, Active Inference, Bayesian Mechanics, Information Geometry, and non-equilibrium Thermodynamics. Every catalogue row carries a reviewed invariant, explicit assumptions and boundaries, a namespaced Lean 4 theorem body, and deterministic manuscript metadata.
>
> The release is pinned to Lean 4.33.1 and Mathlib 4.33.1 (locked Mathlib revision 0df444a360eaa60ab8c11dca51a86af692955474). Its native receipt verifies 155/155 topic closures with zero errors, warnings, or sorry. The schema-4 formalism audit covers all 823 required formal-resource declarations, including 699 evidence declarations, and reports no sorryAx or untrusted project axioms. The canonical Python acceptance run collected 1,203 tests: 1,080 passed, 123 skipped, zero failed or errored, with 89.81% line coverage (8,808/9,807 statements). The schema-4 Chrome 151 browser receipt replays six source-bound screenshots covering 155 topics, 20 families, 133 relations, 48 satisfied capabilities, and 15 typed numerical witnesses.
>
> These checks establish the exact shipped formal statements and reproducible software evidence; they do not prove the Free Energy Principle as a physical theory. Provider-backed Hermes commentary is optional and unavailable for this release cut, and no historical provider report is promoted to current full-mode evidence.
>
> Source and release: github.com/ActiveInferenceInstitute/fep_lean (https://github.com/ActiveInferenceInstitute/fep_lean) and GitHub release v1.1.0 (https://github.com/ActiveInferenceInstitute/fep_lean/releases/tag/v1.1.0). The exact deterministic 232-member evidence bundle has SHA-256 0009447598ecd3bbf68548eab360704a2539480379791eb0128186fa230884ea and binds release commit d7b6f8b15ea9dc451b191e3674a1fd72b5e586b4.

## Keywords

`free energy principle` · `active inference` · `bayesian mechanics` · `information geometry` · `non-equilibrium thermodynamics` · `Lean 4` · `Mathlib` · `interactive theorem proving` · `formal verification` · `theorem proving` · `measure theory` · `reproducible research`

## Methods

- **Curated catalog of 50 FEP topics as namespaced Lean 4 sketches against Mathlib4** — Compiled 50 topics across five pillars (FEP, Active Inference, Bayesian Mechanics, Information Geometry, Thermodynamics) as Lean 4 sketches from a single source of truth.
- **Native lake env lean verification on a pinned Lean/Mathlib v4.29.0 stack** — Verified every reported compilation result with a real lake env lean invocation against the pinned toolchain, with no mocked compilers or synthetic success signals.
- **LLM-assisted commentary pipeline (Hermes/OpenGauss, kimi-k2.6 via OpenRouter)** — Layered LLM drafting and commentary over the catalog, cached by Lean source hash, with the Lean kernel kept as sole ground truth for compilation claims.
- **Zero-mock test suite with coverage gate and SQLite run persistence** — Ran 347 tests that each exercise real files, a real SQLite store, live compiler calls or actual HTTP calls, holding coverage above an 89% CI gate.
- **Three-level sorry-aware maturity taxonomy (real / partial / aspirational)** — Introduced a classification intended to make incomplete formalization explicit; all current rows are tagged real.

## Key Findings

- On the pinned Lean 4 / Mathlib4 v4.29.0 stack, the shipped catalog compiles 50/50 sorry-free.
- The Hermes-assisted Gauss run run_20260424_064334 achieved 50/50 clean compiles with 0 sorry and 0 errors.
- Constructions that already typecheck in today's Mathlib4 include finite-set probability, Bayesian updating, finite-space KL divergence and variational free-energy bounds.
- The author cautions that the catalog covers definitional lemmas and structural identities rather than end-to-end FEP theorems, and many rows stop short of what the informal text proves.
- Formal verification here establishes formal adequacy only; it provides no empirical confirmation that brains minimize variational free energy.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [ActiveInferenceInstitute/fep_formal](https://github.com/ActiveInferenceInstitute/fep_formal)
- GitHub release: [v1.1.0](https://github.com/ActiveInferenceInstitute/fep_formal/releases/tag/v1.1.0)
- DOI: [10.5281/zenodo.19699233](https://doi.org/10.5281/zenodo.19699233)
- Artifact DOI: [10.5281/zenodo.22072956](https://doi.org/10.5281/zenodo.22072956)
- Zenodo record: [https://zenodo.org/records/19699233](https://zenodo.org/records/19699233)
- PDF: [fep-lean-manuscript-1.1.0.pdf](fep-lean-manuscript-1.1.0.pdf)
- PDF: [fep_lean_v1_04-24-2026.pdf](fep_lean_v1_04-24-2026.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/19699233)

## Citation

> Daniel Ari Friedman (2026). *Towards Lean 4 Formalization of the Free Energy Principle: AI-Driven Theorem Sketching and Verification for Active Inference and Bayesian Mechanics*. Active Inference Journal. DOI: 10.5281/zenodo.19699233. URL: https://doi.org/10.5281/zenodo.19699233.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
