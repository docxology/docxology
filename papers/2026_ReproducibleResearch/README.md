<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 A template/ approach to Reproducible Generative Research: Architecture and Ergonomics from Configuration through Publication

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.16903351-blue)](https://doi.org/10.5281/zenodo.16903351)

---

## Abstract

> The reproducibility crisis in computational research is fundamentally structural: research artifacts are scattered across disconnected tools. template/ applies Infrastructure as Code to the research lifecycle, making the manuscript, test suite, and provenance chain version-controlled, deterministically buildable, and independently verifiable.

## Keywords

`reproducible research` · `infrastructure as code` · `build pipeline` · `open science` · `Model Context Protocol`

## Methods

- **Two-Layer Architecture: 12 shared infrastructure subpackages + standalone projects** — template/ separates a reusable infrastructure/ layer (~150 Python modules) from self-contained projects/ workspaces that consume it.
- **Eight-stage build pipeline from environment setup to LLM review** — Stages run sequentially: setup, tests with coverage, analysis scripts, Pandoc/XeLaTeX rendering, hashing/watermarking, PDF validation, LLM review.
- **Zero-Mock testing policy with 90%/60% coverage gates** — Tests use real filesystem operations and subprocesses instead of mocks, with coverage thresholds of 90% for projects and 60% for infrastructure.
- **SHA-256 hashing with steganographic watermarking for provenance** — Rendered PDFs carry SHA-256 hashes in metadata plus alpha-channel overlays and QR codes for tamper detection.
- **Multi-project evaluation and feature comparison with peer tools** — Three exemplar projects were run through the full pipeline, and template/ was compared with peer tools (e.g. Snakemake, Quarto, DVC) on fourteen dimensions.

## Key Findings

- All three exemplar projects (39, 505 and 65 tests) completed the pipeline, a reported 100% success rate with zero mock violations.
- Total pipeline duration across the three projects was ~125s on Apple M-series hardware, ~42s per project on average.
- The infrastructure suite of ~3,083 tests reached 83%+ coverage against a 60% threshold, with zero mock violations.
- The comparative feature analysis is reported to show template/ uniquely combining eleven distinctive capabilities in one enforced pipeline.
- Among stated limitations, the provenance layer offers SHA-256 tamper detection but not cryptographic non-repudiation, since it lacks private-key signatures.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.5281/zenodo.16903351](https://doi.org/10.5281/zenodo.16903351)
- Zenodo record: [https://zenodo.org/records/16903351](https://zenodo.org/records/16903351)
- PDF: [template_daf_v1_03202026.pdf](template_daf_v1_03202026.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/16903351)

## Citation

> Daniel Ari Friedman (2026). *A template/ approach to Reproducible Generative Research: Architecture and Ergonomics from Configuration through Publication*. Zenodo. DOI: 10.5281/zenodo.16903351. URL: https://doi.org/10.5281/zenodo.16903351.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
