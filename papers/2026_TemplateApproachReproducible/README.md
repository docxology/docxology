<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 A template/ approach to Reproducible Generative Research

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20419007-blue)](https://doi.org/10.5281/zenodo.20419007)

---

## Abstract

> The reproducibility crisis in computational research is fundamentally structural: research artifacts are scattered across disconnected tools—LaTeX editors, Jupyter notebooks, ad-hoc shell scripts—with no enforced mechanism to keep code, data, and manuscript synchronized. Studies have shown that most published findings are false positives, replication rates in psychology hover around 36%, and only...

## Keywords

`reproducible research` · `infrastructure-as-code` · `steganography` · `cryptographic provenance` · `LaTeX rendering` · `modular infrastructure` · `publication integrity` · `zero-mock testing` · `thin orchestrator` · `two-layer architecture` · `FAIR4RS` · `research software engineering`

## Methods

- **Two-Layer Architecture separating shared infrastructure from project workspaces** — Describes a repository design where N independent research projects share infrastructure packages without coupling to each other.
- **YAML-declared 12-stage build DAG from tests through Pandoc/XeLaTeX rendering** — Specifies the pipeline in pipeline.yaml; default full runs use 10 stages and --core-only runs 8.
- **Zero-Mock testing policy with 90% project and 60% infrastructure coverage gates** — Tests use real filesystem operations and subprocess calls rather than mocks, with coverage thresholds enforced by the pipeline.
- **Feature comparison against nine peer tools across fourteen dimensions** — Compares template/ with workflow managers, literate-programming systems, DVC, Overleaf and OpenAI Prism on enforcement features.
- **Multi-project pipeline runs measuring coverage, timing, integrity and watermarking** — Exemplar projects were run through the core pipeline on an Apple Silicon workstation, recording tests passed, durations and steganography timings.

## Key Findings

- Reports 100% pipeline completion for the sampled multi-project runs, with timings described as illustrative.
- The manuscript was itself produced by the pipeline it describes, with metrics injected from repository introspection.
- The comparative analysis positions template/ as integrating fourteen distinctive enforcement capabilities in one repository.
- States that the provenance layer offers SHA-256 tamper detection but not cryptographic non-repudiation, since it lacks private-key signatures.
- Acknowledges the pipeline is single-machine, without native distributed execution, where Snakemake, Nextflow and CWL are superior.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [docxology/template_template](https://github.com/docxology/template_template)
- GitHub release: [v1.0.9](https://github.com/docxology/template_template/releases/tag/v1.0.9)
- DOI: [10.5281/zenodo.20419007](https://doi.org/10.5281/zenodo.20419007)
- Zenodo record: [https://zenodo.org/records/20419007](https://zenodo.org/records/20419007)
- PDF: [Friedman_2026_Template_535bd809.pdf](Friedman_2026_Template_535bd809.pdf)
- PDF: [Friedman_2026_Template_57199c03.pdf](Friedman_2026_Template_57199c03.pdf)
- PDF: [Friedman_2026_Template_b9bc5cf3.pdf](Friedman_2026_Template_b9bc5cf3.pdf)
- PDF SHA-256: 535bd80943d0ae9fd504a926efb41c6b39c3a812a94ea4d51bc974029bca563c

## Citation

> Daniel Ari Friedman (2026). *A template/ approach to Reproducible Generative Research*. Zenodo. DOI: 10.5281/zenodo.20419007. URL: https://doi.org/10.5281/zenodo.20419007.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
