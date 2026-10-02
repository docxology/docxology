<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 🧠 Active Skillference: A Validated Prerequisite Graph, Computational Claim Registry, and SkillTree Delivery Contract

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21865643-blue)](https://doi.org/10.5281/zenodo.21865643)

---

## Abstract

> Active Inference and the Free Energy Principle (FEP) provide model-based accounts of belief updating, learning, and action under uncertainty. We present Active Skillference, a provenance-bound curriculum-generation and SkillTree-export system for teaching those formal ideas. The paper evaluates structural validity, quantitative provenance, citation-role coverage, and artifact reproducibility; it does not evaluate learner outcomes, establish a new theory of Active Inference, or present an intelligent tutoring system. The curriculum is expressed as code: a typed, validated directed acyclic graph of 630 skills across 111 subjects spanning all 8 strata (mathematics -> probability -> information theory -> variational methods -> the FEP -> active inference -> computation -> applications), connected by 1199 prerequisite edges with a maximum dependency depth of 75 (of which the substantive concept chain accounts for 33; the remaining depth is per-stratum review and mastery sequencing rather than conceptual prerequisite, as the methodology details). Its defining feature is content-provenance binding: every quantitative value shown to a learner is produced by a tested computational kernel and inserted through a typed claim token, never hand-typed, and the build refuses to export if a claim is unbacked or if a bare result number appears in learner prose, manuscript prose, or correct numeric quiz answers. The contribution is therefore a systems and curriculum-infrastructure artifact: it makes a formal subject inspectable and deliverable, but does not claim that the resulting path is optimal for every learner. The validated graph exports directly into SkillTree’s data model (Project -> Subjects -> Skills with learning-path dependencies and quiz-gated completion), includes a scripted REST seeding path for a configured instance, and is mirrored by a local dashboard that exposes generated artifacts, figures, claim ledgers, scholarship audits, and graph diagnostics without taking ownership of learner progress or scoring from SkillTree. The result is a curriculum with a validator-backed artifact chain: re-running the kernels regenerates the claim ledger, figures, manuscript variables, SkillTree export, and learner-facing numbers, so the platform’s teaching claims remain bounded by what the code, citations, validators, and documented limitations actually support.

## Keywords

`active inference` · `free energy principle` · `variational inference` · `Bayesian inference` · `information theory` · `curriculum` · `prerequisite graph` · `SkillTree` · `computational provenance` · `micro-learning` · `reproducible research`

## Methods

- **Typed, validated DAG curriculum of skills across 8 Active Inference strata** — Encodes the curriculum as code from mathematics through FEP and active inference to applications, with prerequisite edges validated as a DAG.
- **Content-provenance binding via tested kernels and typed claim tokens** — Learner-facing numbers come only from tested computational kernels via claim tokens; the build refuses export on unbacked claims.
- **Export to SkillTree's Project-Subject-Skill model with REST seeding** — Exports the validated graph into SkillTree with learning-path dependencies and quiz-gated completion, plus a scripted REST seeding path.
- **Deterministic artifact evaluation of structure, provenance, citations, reproducibility** — Evaluates structural validity, quantitative provenance, citation-role coverage and artifact reproducibility, explicitly not learner outcomes.
- **Kernel-backed VFE/EFE teaching examples on small discrete models** — Supplement derives model-bounded examples such as noisy-sensor posteriors, EFE policy comparison, sum-product inference and Dirichlet learning.

## Key Findings

- The graph connects 630 skills in 111 subjects by 1199 prerequisite edges with maximum dependency depth 75, of which the substantive concept chain accounts for 33.
- Reports a bounded engineering result: a contested formal subject can be represented as an inspectable prerequisite graph whose contracts are checked separately.
- States these are properties of the build, not evidence that the chosen order is optimal for learners or that the framework is empirically confirmed.
- Positions the release as a candidate foundation for a later adaptive study, not an adaptive system, with SkillTree owning progress and scoring.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.5281/zenodo.21865643](https://doi.org/10.5281/zenodo.21865643)
- Zenodo record: [https://zenodo.org/records/21865643](https://zenodo.org/records/21865643)
- PDF: [Active_Skillference_v1.0.0_DOI-10.5281-zenodo.21865644.pdf](Active_Skillference_v1.0.0_DOI-10.5281-zenodo.21865644.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/21865643)

## Citation

> Daniel Ari Friedman (2026). *Active Skillference: A Validated Prerequisite Graph, Computational Claim Registry, and SkillTree Delivery Contract*. Zenodo. DOI: 10.5281/zenodo.21865643. URL: https://doi.org/10.5281/zenodo.21865643.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
