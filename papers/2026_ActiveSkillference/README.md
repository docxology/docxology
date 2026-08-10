# Active Skillference: A Validated Prerequisite Graph, Computational Claim Registry, and SkillTree Delivery Contract

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21865643.svg)](https://doi.org/10.5281/zenodo.21865643)

---

## Abstract

Active Inference and the Free Energy Principle (FEP) provide model-based accounts of belief updating, learning, and action under uncertainty. We present Active Skillference, a provenance-bound curriculum-generation and SkillTree-export system for teaching those formal ideas. The paper evaluates structural validity, quantitative provenance, citation-role coverage, and artifact reproducibility; it does not evaluate learner outcomes, establish a new theory of Active Inference, or present an intelligent tutoring system. The curriculum is expressed as code: a typed, validated directed acyclic graph of 630 skills across 111 subjects spanning all 8 strata (mathematics -> probability -> information theory -> variational methods -> the FEP -> active inference -> computation -> applications), connected by 1199 prerequisite edges with a maximum dependency depth of 75 (of which the substantive concept chain accounts for 33; the remaining depth is per-stratum review and mastery sequencing rather than conceptual prerequisite, as the methodology details). Its defining feature is content-provenance binding: every quantitative value shown to a learner is produced by a tested computational kernel and inserted through a typed claim token, never hand-typed, and the build refuses to export if a claim is unbacked or if a bare result number appears in learner prose, manuscript prose, or correct numeric quiz answers. The contribution is therefore a systems and curriculum-infrastructure artifact: it makes a formal subject inspectable and deliverable, but does not claim that the resulting path is optimal for every learner. The validated graph exports directly into SkillTree’s data model (Project -> Subjects -> Skills with learning-path dependencies and quiz-gated completion), includes a scripted REST seeding path for a configured instance, and is mirrored by a local dashboard that exposes generated artifacts, figures, claim ledgers, scholarship audits, and graph diagnostics without taking ownership of learner progress or scoring from SkillTree. The result is a curriculum with a validator-backed artifact chain: re-running the kernels regenerates the claim ledger, figures, manuscript variables, SkillTree export, and learner-facing numbers, so the platform’s teaching claims remain bounded by what the code, citations, validators, and documented limitations actually support.

## Keywords

active inference · free energy principle · variational inference · Bayesian inference · information theory · curriculum · prerequisite graph · SkillTree · computational provenance · micro-learning · reproducible research

## Artifacts

| Field | Value |
|------|-------|
| **DOI** | [10.5281/zenodo.21865643](https://doi.org/10.5281/zenodo.21865643) |
| **Published** | 2026-08-10 |
| **Version** | 1.0.0 |
| **Zenodo record** | https://zenodo.org/records/21865643 |

## Files

- `Active_Skillference_v1.0.0_DOI-10.5281-zenodo.21865644.pdf` - Zenodo PDF

## Citation

> Daniel Ari Friedman (2026). *Active Skillference: A Validated Prerequisite Graph, Computational Claim Registry, and SkillTree Delivery Contract*. Zenodo. DOI: 10.5281/zenodo.21865643. URL: https://doi.org/10.5281/zenodo.21865643.

## Related

- Zenodo record: https://zenodo.org/records/21865643
- [Full Bibliography](../../pages/BIBLIOGRAPHY.md) · [All Papers](../README.md)
