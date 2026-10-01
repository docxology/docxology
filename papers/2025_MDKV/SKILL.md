---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "MDKV: A Multitrack Markdown Container for Structured, Portable Documents"
description: "MDKV (Markdown Key-Value) is a lightweight, YAML-free key-value format for Markdown documents. Every key-value pair maps to a Markdown heading and its body text, enabling round-trip transformations be..."
tags: ["mdkv", "markdown", "key-value-format", "structured-data", "document-specification", "yaml-free", "round-trip-transformation"]
domain: "Computational"
citation: "Daniel Friedman (2025). *MDKV: A Multitrack Markdown Container for Structured, Portable Documents*. Zenodo."
doi: "10.5281/zenodo.16790554"
---

# MDKV: A Multitrack Markdown Container for Structured, Portable Documents

**Daniel Friedman** (2025) · Computational

## Context

This work addresses topics in **Computational**: MDKV, Markdown, key-value format, structured data.

## Methods

Primary methods and techniques applied in this work:

- **ZIP container with YAML manifest and tracks/ directory of Markdown files** — MDKV defines an .mdkv file as a ZIP archive holding a manifest.yaml index plus one UTF-8 Markdown file per track.
- **Seven-type track taxonomy (primary, translation, commentary, code, etc.)** — Document layers are separated into typed tracks that are composed into views only at export time.
- **Python reference implementation split into core, storage, services, and CLI** — The software follows a thin-orchestrator design with separate modules for data model and validation, persistence, search/export, and command-line entry points.
- **Round-trip export via HTML-comment track headers** — Combined Markdown exports prefix each track with a comment encoding its id, type, and language so attribution can be reconstructed.
- **Normative MUST/SHOULD conformance requirements and minimal validator** — The paper specifies conformance rules and a base validator checking title, authors, a primary track, track paths, types, and unique ids.

## Key Findings

Core contributions and results:

- The paper lists four contributions: a precise model and container format, a modular architecture exposed via CLI and GUI, detailed use cases, and guidance on cryptographic provenance and conformance.
- Export is designed to be deterministic: order follows the manifest, and identical inputs produce identical outputs.
- The author lists format limitations, including no built-in encryption or signing and code tracks that are listings rather than runnable notebooks.
- The paper notes that the reference validator currently checks for a track with id 'primary' rather than the type-level requirement.
- The paper is itself authored as a Markdown file that renders into a valid MDKV.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2023_NSFReporting](../2023_NSFReporting/)
- [2023_NaturalAIBased](../2023_NaturalAIBased/)
- [2025_AuBI](../2025_AuBI/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.16790554
- PDF SHA-256: See zenodo_record
- Pairing confidence: unknown
- Last checked: 2026-06-30T23:25:50Z

## Prerequisites

- Familiarity with MDKV, Markdown, key-value format
- Background in Computational fundamentals
- Access to source repository: N/A

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.16790554`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
