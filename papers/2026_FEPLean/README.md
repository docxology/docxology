# Towards Lean 4 Formalization of the Free Energy Principle

**Daniel Ari Friedman** (2026) · *Active Inference Journal* · Version v1

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.19699234-blue)](https://doi.org/10.5281/zenodo.19699234)

---

<!-- Schema.org structured data for search engines -->
<!--
{"@context":"https://schema.org","@type":"ScholarlyArticle","headline":"Towards Lean 4 Formalization of the Free Energy Principle: AI-Driven Theorem Sketching and Verification for Active Inference and Bayesian Mechanics","abstract":"50-topic Lean 4 catalog against Mathlib4 spanning FEP, Active Inference, Bayesian mechanics, information geometry, and thermodynamics; sorry-free verification on pinned Lean/Mathlib, Hermes/OpenGauss LLM pipeline, zero-mock testing.","keywords":["Free Energy Principle","Active Inference","Lean 4","Mathlib4","interactive theorem proving","formal verification","Bayesian mechanics","information geometry","LLM-ITP","reproducible research"],"author":[{"@type":"Person","name":"Daniel Ari Friedman","url":"https://docxology.github.io/docxology/","affiliation":[{"@type":"Organization","name":"Active Inference Institute"}]}]}
-->

## Abstract

> The Free Energy Principle (FEP) unifies a broad class of system properties under a variational free-energy functional, but a **machine-checked** substrate for assessing related formal claims has been missing. Dependent-type provers require explicit measure spaces, domination, and integrability that prose often leaves implicit. This work introduces a **curated catalog of 50 topics** across five pillars—14 FEP, 11 Active Inference, 10 Bayesian Mechanics, 8 Information Geometry, and 7 non-equilibrium Thermodynamics—each as a **namespaced Lean 4 sketch** against **Mathlib4**, with natural-language statements, imports, ecosystem-maturity tags, and **sorry-free** theorem bodies maintained from a single source of truth. On the pinned stack **leanprover/lean4:v4.29.0** / **Mathlib4 v4.29.0**, the shipped catalog compiles **50/50** sorry-free under `lake env lean`. The manuscript describes an **LLM-assisted** drafting and commentary layer (**Hermes** / **OpenGauss**; primary model `moonshotai/kimi-k2.6` with cache keyed to Lean source hashes) while the **Lean 4 kernel** remains sole ground truth for compilation claims, plus a **zero-mock** test discipline. End-to-end reproduction, source, catalog, and figures are released with the open **fep_lean** repository.

## Keywords

`Free Energy Principle` · `Active Inference` · `Lean 4` · `Mathlib4` · `interactive theorem proving` · `formal verification` · `variational inference` · `Bayesian mechanics` · `information geometry` · `LLM-ITP integration` · `reproducible research` · `measure theory`

## Key Contributions

- A **50-topic formal catalog** of FEP-related mathematics with explicit Mathlib4-facing statements and a reproducible, version-pinned verification story.
- **Axiomatization vs. problem-solving**: positions LLM+ITP work as building shared formal structure, not just benchmark solving.
- **Hermes / OpenGauss** pipeline: LLM drafts and explains sketches while **native Lean** verifies; compilation remains the non-negotiable check.
- **Zero-mock testing policy** in the software stack (real files, real SQLite, live compiler, real HTTP) as stated in the manuscript.
- A **Lean primer** and **Mathlib4 / measure-theoretic probability** guidance aimed at Active Inference researchers entering formal methods.

## Methods & Artifacts

- Theoretical and systems paper: **YAML → manuscript → Lake** pipeline; per-topic modules with LaTeX-adjacent statement signatures.
- **Open-source**: [https://github.com/ActiveInferenceInstitute/fep_lean](https://github.com/ActiveInferenceInstitute/fep_lean) (manuscript build uses the [docxology template](https://github.com/docxology/template) approach for validated metadata injection).
- Archived manuscript (v1): [https://doi.org/10.5281/zenodo.19699234](https://doi.org/10.5281/zenodo.19699234) · Zenodo record [https://zenodo.org/records/19699234](https://zenodo.org/records/19699234)

## Consulting & Tutoring

**Available for AI Research Consulting and Tutoring.** [Contact Daniel Ari Friedman, PhD](https://docxology.github.io/docxology/) for collaboration on formal methods for Active Inference, Lean/Mathlib, and LLM–ITP workflows.

## Citation

```bibtex
@article{2026_FEPLean,
  author = {Daniel Ari Friedman},
  title = {{Towards Lean 4 Formalization of the Free Energy Principle: AI-Driven Theorem Sketching and Verification for Active Inference and Bayesian Mechanics}},
  journal = {Active Inference Journal},
  year = {2026},
  version = {v1},
  doi = {10.5281/zenodo.19699234},
  url = {https://doi.org/10.5281/zenodo.19699234},
  note = {Code: \url{https://github.com/ActiveInferenceInstitute/fep_lean}},
}
```

## File Inventory

- `AGENTS.md`
- `fep_lean_v1_04-24-2026.pdf`
- `README.md`
- `SKILL.md`
