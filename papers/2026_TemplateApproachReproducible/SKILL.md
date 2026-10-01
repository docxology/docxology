---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "A template/ approach to Reproducible Generative Research"
description: "The reproducibility crisis in computational research is fundamentally structural: research artifacts are scattered across disconnected tools—LaTeX editors, Jupyter notebooks, ad-hoc shell scripts—with no enforced mechanism to keep code, data, and man..."
tags: ["reproducible-research", "infrastructure-as-code", "steganography", "cryptographic-provenance", "latex-rendering", "modular-infrastructure", "publication-integrity", "zero-mock-testing", "thin-orchestrator", "two-layer-architecture"]
domain: "Computational"
citation: "Daniel Ari Friedman (2026). *A template/ approach to Reproducible Generative Research*. Zenodo."
doi: "10.5281/zenodo.20419007"
---

# A template/ approach to Reproducible Generative Research

**Daniel Ari Friedman** (2026) · Computational

## Context

This work addresses topics in **Computational**: reproducible research, infrastructure-as-code, steganography, cryptographic provenance.

## Methods

Primary methods and techniques applied in this work:

- **Two-Layer Architecture separating shared infrastructure from project workspaces** — Describes a repository design where N independent research projects share infrastructure packages without coupling to each other.
- **YAML-declared 12-stage build DAG from tests through Pandoc/XeLaTeX rendering** — Specifies the pipeline in pipeline.yaml; default full runs use 10 stages and --core-only runs 8.
- **Zero-Mock testing policy with 90% project and 60% infrastructure coverage gates** — Tests use real filesystem operations and subprocess calls rather than mocks, with coverage thresholds enforced by the pipeline.
- **Feature comparison against nine peer tools across fourteen dimensions** — Compares template/ with workflow managers, literate-programming systems, DVC, Overleaf and OpenAI Prism on enforcement features.
- **Multi-project pipeline runs measuring coverage, timing, integrity and watermarking** — Exemplar projects were run through the core pipeline on an Apple Silicon workstation, recording tests passed, durations and steganography timings.

## Key Findings

Core contributions and results:

- Reports 100% pipeline completion for the sampled multi-project runs, with timings described as illustrative.
- The manuscript was itself produced by the pipeline it describes, with metrics injected from repository introspection.
- The comparative analysis positions template/ as integrating fourteen distinctive enforcement capabilities in one repository.
- States that the provenance layer offers SHA-256 tamper detection but not cryptographic non-repudiation, since it lacks private-key signatures.
- Acknowledges the pipeline is single-machine, without native distributed execution, where Snakemake, Nextflow and CWL are superior.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2023_NSFReporting](../2023_NSFReporting/)
- [2023_NaturalAIBased](../2023_NaturalAIBased/)
- [2025_AuBI](../2025_AuBI/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.20419007
- PDF SHA-256: 535bd80943d0ae9fd504a926efb41c6b39c3a812a94ea4d51bc974029bca563c
- Pairing confidence: strong
- Last checked: 2026-09-24T18:29:54Z

## Prerequisites

- Familiarity with reproducible research, infrastructure-as-code, steganography
- Background in Computational fundamentals
- Access to source repository: docxology/template_template

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.20419007`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
