---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "Data Descriptor Template: Schema, Provenance, and Release Readiness"
description: "This exemplar demonstrates a data descriptor workflow in which the schema, file inventory, provenance chain, license boundary, and validation gate are treated as first-class research artifacts rather than afterthoughts. It ships a small, public, synt..."
tags: ["data-descriptor", "fair-data", "provenance", "schema-validation"]
domain: "Computational"
citation: "Daniel Ari Friedman (2026). *Data Descriptor Template: Schema, Provenance, and Release Readiness*. Zenodo."
doi: "10.5281/zenodo.21298883"
---

# Data Descriptor Template: Schema, Provenance, and Release Readiness

**Daniel Ari Friedman** (2026) · Computational

## Context

This work addresses topics in **Computational**: data descriptor, FAIR data, provenance, schema validation.

## Methods

Primary methods and techniques applied in this work:

- **Synthetic demo dataset: two CSV fixtures plus JSON descriptor** — Ships two small deterministic synthetic CSV files (measurements, subjects) described by a machine-readable descriptor with checksums and row counts.
- **Six-field data dictionary with typed constraints** — Declares six fields with types, nullability, units, regex patterns, closed enumerations and numeric bounds for the measurement table.
- **Order-independent sha256 schema fingerprint** — descriptor_fingerprint() hashes (name, type, nullable) triples so reordering fields does not change the schema fingerprint.
- **Validation gate with readiness score and perturbed negative control** — validate_descriptor() emits severity-tagged findings folded into a readiness score; a deliberately broken copy tests that the gate reacts.
- **Byte-level descriptor-to-file verification** — verify_descriptor_files() recomputes sha256 and row counts of present files and reports verified, mismatch, or absent status.

## Key Findings

Core contributions and results:

- The clean fixture descriptor produces zero validation findings, while the deliberately perturbed demo produces several errors and warnings.
- For the shipped fixture, both files verify: declared and actual row counts agree and each recomputed checksum matches, leaving the readiness score unpenalised.
- The paper reports that its zero-mock test suite exceeds the 90% project coverage gate.
- The work explicitly makes no scientific claim about the synthetic data; claims are limited to how to describe and release a dataset.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

See [BIBLIOGRAPHY.md](../../pages/BIBLIOGRAPHY.md) for related publications.

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.21298883
- PDF SHA-256: See zenodo_record
- Pairing confidence: unknown
- Last checked: 2026-07-10T19:31:29Z

## Prerequisites

- Familiarity with data descriptor, FAIR data, provenance
- Background in Computational fundamentals
- Access to source repository: N/A

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.21298883`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
