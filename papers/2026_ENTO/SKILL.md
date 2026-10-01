---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "ENTO: an ENcrypted, Typed, Omnitrack container format for multimodal research data"
description: "<p><strong>ENTO</strong> (ENcrypted, Typed, Omnitrack) is a flat ZIP container format and reference implementation for bundling heterogeneous research artifacts &mdash; time series, genomics slices, spectrograms, provenance proofs &mdash; into a sing..."
tags: ["research-data-formats", "authenticated-encryption", "aes-256-gcm", "reproducible-research", "multimodal-containers"]
domain: "Computational"
citation: "Daniel Ari Friedman (2026). *ENTO: an ENcrypted, Typed, Omnitrack container format for multimodal research data*. Zenodo."
doi: "10.5281/zenodo.20396328"
---

# ENTO: an ENcrypted, Typed, Omnitrack container format for multimodal research data

**Daniel Ari Friedman** (2026) · Computational

## Context

This work addresses topics in **Computational**: research data formats, authenticated encryption, AES-256-GCM, reproducible research.

## Methods

Primary methods and techniques applied in this work:

- **Flat ZIP layout: manifest.json, one encrypted member per track, optional proof** — Defines the container as a ZIP archive with a typed manifest, per-track .ento members and an optional hash-chain proof file.
- **Per-track AES-256-GCM envelopes with HKDF-derived keys** — Each track is sealed with authenticated encryption under a fixed nonce||tag||ciphertext header, specified in a Kaitai Struct file.
- **Four graded observability levels for export-time manifest redaction** — Observability levels 0–3 control which manifest metadata a recipient sees, without re-encrypting the track payloads.
- **Associated-data binding and PADMÉ length padding in the default profile** — The 0.4.0 default binds associated data and pads ciphertext members to PADMÉ buckets to coarsen the length channel.
- **Scripted benchmark: 150 repetitions over observability levels on fixture tracks** — Benchmarks on committed EEG, VCF and spectrogram fixtures plus a synthetic throughput track measure throughput, latency, expansion and tamper detection.

## Key Findings

Core contributions and results:

- Tamper detection succeeded on all 2400 benchmark rows (rate 1.0).
- Mean pack throughput was 78.9296 MiB/s on the medium-track condition at observability level 3 (n = 150, CV 15.3%); the paper makes no superiority claim.
- Ciphertext expansion on fixture tracks was an exact, zero-variance 1.7113.
- Length is not hidden exactly: non-sealed levels disclose byte_length in the manifest, and sealed export still reveals the PADMÉ bucket.
- Concludes that a flat ZIP container can carry typed multimodal tracks, authenticated encryption, graded observability and proof export without becoming a repository or hosted service.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2023_NSFReporting](../2023_NSFReporting/)
- [2023_NaturalAIBased](../2023_NaturalAIBased/)
- [2025_AuBI](../2025_AuBI/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.20396328
- PDF SHA-256: See zenodo_record
- Pairing confidence: strong
- Last checked: 2026-09-24T18:29:54Z

## Prerequisites

- Familiarity with research data formats, authenticated encryption, AES-256-GCM
- Background in Computational fundamentals
- Access to source repository: docxology/entofile

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.20396328`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
