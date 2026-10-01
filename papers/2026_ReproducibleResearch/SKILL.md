---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "A template/ approach to Reproducible Generative Research: Architecture and Ergonomics from Configuration through Publication"
description: "Infrastructure-as-code research lifecycle: Two-Layer Architecture, eight-stage build pipeline, Zero-Mock testing, and Documentation Duality (README + AGENTS + SKILL)."
tags: ["reproducible-research", "infrastructure-as-code", "build-pipeline", "open-science", "model-context-protocol"]
domain: "Computational"
citation: "Daniel Ari Friedman (2026). *A template/ approach to Reproducible Generative Research: Architecture and Ergonomics from Configuration through Publication*. Zenodo."
doi: "10.5281/zenodo.16903351"
---

# A template/ approach to Reproducible Generative Research: Architecture and Ergonomics from Configuration through Publication

**Daniel Ari Friedman** (2026) · Computational

## Context

This work addresses topics in **Computational**: reproducible research, infrastructure as code, build pipeline, open science.

## Methods

Primary methods and techniques applied in this work:

- **Two-Layer Architecture: 12 shared infrastructure subpackages + standalone projects** — template/ separates a reusable infrastructure/ layer (~150 Python modules) from self-contained projects/ workspaces that consume it.
- **Eight-stage build pipeline from environment setup to LLM review** — Stages run sequentially: setup, tests with coverage, analysis scripts, Pandoc/XeLaTeX rendering, hashing/watermarking, PDF validation, LLM review.
- **Zero-Mock testing policy with 90%/60% coverage gates** — Tests use real filesystem operations and subprocesses instead of mocks, with coverage thresholds of 90% for projects and 60% for infrastructure.
- **SHA-256 hashing with steganographic watermarking for provenance** — Rendered PDFs carry SHA-256 hashes in metadata plus alpha-channel overlays and QR codes for tamper detection.
- **Multi-project evaluation and feature comparison with peer tools** — Three exemplar projects were run through the full pipeline, and template/ was compared with peer tools (e.g. Snakemake, Quarto, DVC) on fourteen dimensions.

## Key Findings

Core contributions and results:

- All three exemplar projects (39, 505 and 65 tests) completed the pipeline, a reported 100% success rate with zero mock violations.
- Total pipeline duration across the three projects was ~125s on Apple M-series hardware, ~42s per project on average.
- The infrastructure suite of ~3,083 tests reached 83%+ coverage against a 60% threshold, with zero mock violations.
- The comparative feature analysis is reported to show template/ uniquely combining eleven distinctive capabilities in one enforced pipeline.
- Among stated limitations, the provenance layer offers SHA-256 tamper detection but not cryptographic non-repudiation, since it lacks private-key signatures.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2023_NSFReporting](../2023_NSFReporting/)
- [2023_NaturalAIBased](../2023_NaturalAIBased/)
- [2025_AuBI](../2025_AuBI/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.16903351
- PDF SHA-256: See zenodo_record
- Pairing confidence: unknown
- Last checked: 2026-06-30T23:26:12Z

## Prerequisites

- Familiarity with reproducible research, infrastructure as code, build pipeline
- Background in Computational fundamentals
- Access to source repository: N/A

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.16903351`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
