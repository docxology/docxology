<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 A Domain Language for Specifying Controlled Methods

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21086548-blue)](https://doi.org/10.5281/zenodo.21086548)

---

## Abstract

> This paper describes a small, tested domain language for specifying
> controlled methods — the methods-paper exemplar of the
> Research Project Template (https://github.com/docxology/template). Unlike a
> results paper, this manuscript's subject is the methodology itself: a
> controlled vocabulary, a unit system with dimensional safety, four staged
> validation gates, and a deterministic compiler, implemented in
> projects/templates/template_methods_paper/src/methods_dsl/ and described
> section by section in . The domain language's vocabulary is
> informed by BPL (Biology Programming Language,
> ), an upstream reference that encodes laboratory protocols as
> programs with biology-native types, staged validation, and deterministic
> compilation; this exemplar generalizes BPL's intent vocabulary and pipeline
> shape from wet-lab protocols to any controlled procedure.
>
> A Method is a name, a set of typed parameters and resources, and an
> ordered, dependent set of steps — constructed directly as frozen Python
> dataclasses (src/methods_dsl/model.py) rather than parsed from new text
> syntax. Every Quantity carries a unit that resolves to one of
> 18 controlled units across six dimensions, and every step
> names one of 9 controlled-vocabulary intents
> (src/methods_dsl/vocabulary.py), executable on one of 3
> backends. 4 staged gates — structural, semantic, plan, and
> target — validate a method before compile_method
> (src/methods_dsl/compiler.py) deterministically schedules it with Kahn's
> algorithm and hashes the canonical plan with SHA-256.
>
> We demonstrate the language on 2 worked example
> methods spanning both domains BPL's design targets and the domains it
> generalizes to: a manual wet-lab preparation
> (PBSPreparation, 5 steps, target human,
> plan hash 313b9b17de98) and an automated instrument-calibration
> procedure (SensorCalibrationSweep, 4 steps,
> target automated, plan hash d89cced19be6).
> Live re-compilation determinism check: Yes. Across both
> methods, 8 of 8 staged-gate
> evaluations pass. A demonstration provenance hash-chain
> (src/methods_dsl/trust.py) of length 3 verifies as
> Yes.
>
> Contributions are methodological and architectural. On the methods
> side, we show that a controlled vocabulary expressed as typed dataclasses —
> not a parsed grammar — is sufficient to reproduce BPL's core safety
> properties (dimensional safety, staged validation, deterministic
> compilation) at a scope appropriate for a template exemplar. On the
> architecture side, the DSL is covered above the 90% project gate by a
> zero-mock test suite, generates 13 artifacts
> (1 figures, 6 data files,
> 6 reports) per pipeline run, and injects reproducibility
> metadata (configuration hash 23b5981d45bdc598, build timestamp
> 2026-06-30T23:02:10Z) into .
>
> Keywords: methods paper, domain-specific language, controlled methods, deterministic compilation, staged validation, dimensional analysis

## Keywords

`methods paper` · `domain-specific language` · `controlled methods` · `deterministic compilation` · `staged validation` · `dimensional analysis`

## Methods

- **Controlled vocabulary of 9 step intents and 3 execution targets** — Steps name one of nine intents (TRANSFER, ADD, MIX, etc.) and run on HUMAN, AUTOMATED or SIMULATION targets, generalizing BPL's protocol verbs.
- **Dimensional-safety unit system (Quantity/Dimension)** — Each quantity resolves to a controlled unit table and combining quantities of different dimensions raises an error at construction rather than at the bench.
- **Four staged validation gates with short-circuit** — Structural, semantic, plan (acyclicity) and target-compatibility gates run in fixed order, returning early if the first two fail.
- **Deterministic compilation via Kahn's algorithm and SHA-256 plan hash** — Validated steps are topologically scheduled with an explicit ascending step_id tie-break and the canonical JSON plan is hashed with SHA-256.
- **Two worked example methods and zero-mock test suite** — Demonstrates the DSL on a wet-lab PBS preparation and an automated sensor-calibration sweep, tested without mocks under a 90% coverage gate.

## Key Findings

- Across the two worked examples, which were built to pass, the analysis script recorded 8 of 8 staged-gate evaluations passing (2 methods x 4 gates).
- Live recompilation of each example method produced identical plan hashes, and a 3-record demonstration provenance hash-chain verified.
- The author concludes that a controlled vocabulary expressed as typed, validated dataclasses rather than a parsed grammar suffices to reproduce BPL's core safety properties at template-exemplar scope.
- Stable scheduling depends on the explicit tie-break: Kahn's algorithm alone does not guarantee a reproducible plan hash.
- The calibration example reused every step kind and target of the wet-lab example, with nothing added to support the second domain.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [docxology/template_methods_paper](https://github.com/docxology/template_methods_paper)
- GitHub release: [v1.0.0](https://github.com/docxology/template_methods_paper/releases/tag/v1.0.0)
- DOI: [10.5281/zenodo.21086548](https://doi.org/10.5281/zenodo.21086548)
- Zenodo record: [https://zenodo.org/records/21086548](https://zenodo.org/records/21086548)
- PDF: [Friedman_2026_Domain_ecd8519f.pdf](Friedman_2026_Domain_ecd8519f.pdf)
- PDF SHA-256: ecd8519fc2a9a674bd8a4cf89f96122af76529c913e32bf880a7c842da08771a

## Citation

> Daniel Ari Friedman (2026). *A Domain Language for Specifying Controlled Methods*. Zenodo. DOI: 10.5281/zenodo.21086548. URL: https://doi.org/10.5281/zenodo.21086548.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
