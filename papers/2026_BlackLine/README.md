<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 🛡️ Black Line: Strong Work in Public

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21754235-blue)](https://doi.org/10.5281/zenodo.21754235)

---

## Abstract

> A positive practice instrument for concise, inspectable, revisable work. It reads self-declared tags and evidence labels against a versioned practice registry and returns one of four statuses over declaration coverage. It measures whether the evidence a practice asks for was declared — never whether the work is true, good, or permitted; an ALIGNED reading authorizes nothing. Subtitle: A Positive...

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
- Zenodo record: [https://zenodo.org/records/21754235](https://zenodo.org/records/21754235)
- PDF: [black_line_combined.pdf](black_line_combined.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/21754235)

## Citation

> Daniel Ari Friedman (2026). *Black Line: Strong Work in Public*. Zenodo. DOI: 10.5281/zenodo.21754235. URL: https://doi.org/10.5281/zenodo.21754235.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
