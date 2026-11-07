<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 🛡️ Black Line: Strong Work in Public

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21754235-blue)](https://doi.org/10.5281/zenodo.21754235)

---

## Abstract

> Black Line describes an operating discipline implemented through eleven practices in six families and a staged evaluator of declared evidence labels. The selected manuscript states that ALIGNED concerns fresh declarations, not source truth, safety, accreditation or permission. It includes structural checks and adversarial self-declaration examples while explicitly reporting no user-study or outcome comparison. This catalog refresh checks source quotations without rerunning those software experiments.

## Keywords

`research practice` · `declaration coverage` · `evidence discipline` · `scientific integrity` · `reproducibility` · `open science` · `engineering practice`

## Methods

- **Versioned registry of eleven practices with coarse evidence labels** — Encodes practices such as question-first framing, source traceability, and clean reruns as 'wires', each with reviewed tags and required evidence labels.
- **Staged evaluate_work evaluator returning four statuses** — Validates configuration and registry, then runs intake normalization, freshness partition, tag matching, and scoring to return ALIGNED, NEEDS_EVIDENCE, NEEDS_REWORK, or OUTSIDE_SCOPE.
- **Structural invariants tested against planted-bad registries** — Seven invariants check the registry's own shape, each demonstrated firing on a deliberately broken registry rather than only passing on the real one.
- **Executed adversarial declarations against the real evaluator** — Runs label-stuffing, tag-minimization, and refresh-date laundering attacks to show how self-declared inputs can game the status.
- **Three claim classes with distinct evidentiary burdens** — Separates implementation, methodological, and world/authority claims so that tests or citations do not silently change the type of claim made.

## Key Findings

- An ALIGNED status only means every required label for each applicable practice was declared fresh, never that a source is real or a claim true.
- Label-stuffing works: a research-tagged attempt declaring all 22 vocabulary labels with no artifacts returns ALIGNED.
- Coverage is asymmetric: 27 of the 55 tag-practice cells are applicable, computed directly from the registry.
- Seeded permutation sweeps confirm that once a declaration is non-empty the status never regresses, with the empty declaration as the intentional exception.
- The author makes a design and implementation claim only; no user study or outcome comparison was run.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.5281/zenodo.21754235](https://doi.org/10.5281/zenodo.21754235)
- Artifact DOI: [10.5281/zenodo.22833503](https://doi.org/10.5281/zenodo.22833503)
- Zenodo record: [https://zenodo.org/records/22833503](https://zenodo.org/records/22833503)
- Historical local PDF: [black_line_combined.pdf](black_line_combined.pdf)
- Current PDF (Zenodo, version 0.4.1): [black_line_combined.pdf](https://zenodo.org/api/records/22833503/files/black_line_combined.pdf/content)
- Local PDFs remain preserved historical archives.
- Extracted text retains its own source provenance; a matching filename does not establish edition identity.
- PDF SHA-256: e0c5bf331a5b77a1d1436cbe288ea5e2a2183de81627203dc20ac96e04071c04

## Citation

> Daniel Ari Friedman (2026). *Black Line: Strong Work in Public*. Zenodo. DOI: 10.5281/zenodo.21754235. URL: https://doi.org/10.5281/zenodo.21754235.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
