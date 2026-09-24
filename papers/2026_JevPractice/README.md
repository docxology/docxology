# Jev in Practice: A Composable Python Toolkit for TypeSafe's System One Decision Model

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22816187.svg)](https://doi.org/10.5281/zenodo.22816187)

---

## Abstract

Jev is TypeSafe's flagship System One decision model: instead of generating text, it answers typed questions (Choice, Score, Noul) about a state with calibrated probabilities that software can branch on directly. This work presents daf-jev , an open, modular, composable Python toolkit for the Jev API, together with a live-API characterization of the model. The package layers ergonomic question builders, a decision-composition library (confidence gates, tiered routing, composite scoring), a concurrent corpus evaluator, a calibration module, a CLI, an agent skill, and a Model Context Protocol (MCP) server over a thin typed client. Live benchmarks show that batching questions into one call is faster and cheaper than sequential calls (up to ~18x speedup and ~4x fewer tokens), that decision pipelines complete within the model's millisecond envelope, and that reported confidence is self-consistent across repeated evaluations. All numbers in the accompanying manuscript are generated from benchmark artifacts; the full provenance chain (hashed documentation snapshot, figure registry, validation receipts) is machine-checked.

## Keywords

paired GitHub and Zenodo publication

## Artifacts

| Field | Value |
|------|-------|
| **DOI** | [10.5281/zenodo.22816187](https://doi.org/10.5281/zenodo.22816187) |
| **Published** | 2026-09-23 |
| **Version** | 0.6.0 |
| **Zenodo record** | https://zenodo.org/records/22816187 |
| **GitHub release** | https://github.com/docxology/daf-jev/releases/tag/v0.4.0 |
| **Source repository** | https://github.com/docxology/daf-jev |

## Files

- `daf-jev_combined.pdf` - Zenodo PDF

## Citation

> Friedman, D. A. (2026). *Jev in Practice: A Composable Python Toolkit for TypeSafe's System One Decision Model*. Zenodo. DOI: 10.5281/zenodo.22816187. URL: https://doi.org/10.5281/zenodo.22816187.

## Related

- GitHub release: https://github.com/docxology/daf-jev/releases/tag/v0.6.0

- GitHub release: https://github.com/docxology/daf-jev/releases/tag/v0.5.0

- GitHub release: https://github.com/docxology/daf-jev/releases/tag/v0.4.1

- Zenodo record: https://zenodo.org/records/22816187
- GitHub release: https://github.com/docxology/daf-jev/releases/tag/v0.4.0
- Source repository: https://github.com/docxology/daf-jev
- [Full Bibliography](../../pages/BIBLIOGRAPHY.md) · [All Papers](../README.md)
