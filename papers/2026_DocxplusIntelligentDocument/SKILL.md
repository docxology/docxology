---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "docxplus — the Intelligent Document Container"
description: "A standards-first reference implementation of a byte-valid OOXML .docx that also carries a modular, Ed25519-signed, AES-256-GCM-encrypted intelligence layer through spec-sanctioned side-channels, with an optional bridge to the docxology/steganographe..."
tags: ["ooxml", "docx", "open-packaging-conventions", "steganography", "document-security", "reproducible-research"]
domain: "Computational"
citation: "Daniel Ari Friedman (2026). *docxplus — the Intelligent Document Container*. Zenodo."
doi: "10.5281/zenodo.21983948"
---

# docxplus — the Intelligent Document Container

**Daniel Ari Friedman** (2026) · Computational

## Context

This work addresses topics in **Computational**: OOXML, DOCX, Open Packaging Conventions, steganography.

## Methods

Primary methods and techniques applied in this work:

- **Dual-contract design: OPC/ODF surface contract plus signed intelligence manifest** — A single archive is both a conforming .docx/.odt and a carrier of typed payload modules indexed by an Ed25519-signed manifest.
- **Per-module sealing (Argon2id/Scrypt + AES-256-GCM, X25519, Shamir k-of-n, decoys)** — Payloads are sealed individually rather than encrypting the whole package, with slot names bound as AES-GCM additional authenticated data.
- **Five spec-sanctioned transport channels incl. LSB steganography** — Implements custom XML parts, auxiliary package parts, custom document properties, MCE choice blocks, and LSB embedding in displayed images.
- **Merkle-tree provenance with composite surface digest and transparency log** — Signs a Merkle root over modules together with a digest of every part, content type and relationship; attestations go into a log anchored by a signed tree head.
- **Mock-free test harness, project round-trip, chi-squared steganalysis and red-team review** — Evaluated with 467 mock-free tests at a 90% coverage gate, an in-tree chi-squared LSB detector, a project round-trip harness, and 14 adversarial review cycles.

## Key Findings

Core contributions and results:

- In the reference dossier, all 5 modules across all 4 sealing lineages extracted and verified, and the container passed OPC conformance.
- Carrying a 14-file, 9-directory project tree into both .docx and .odt containers, all 18 of 18 round-trip invariants held, with byte-identical packed payloads between profiles.
- The round-trip harness found that packing followed symbolic links, embedding link targets such as an SSH key; symlinks are now refused by default.
- The chi-squared detector flags fully embedded sealed (ciphertext) carriers but does not detect unsealed low-entropy payloads at any fill rate.
- Fourteen adversarial review cycles closed 88 confirmed findings, and a sample-pair analysis estimator was withdrawn after proving mis-scaled by roughly an order of magnitude.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

See [BIBLIOGRAPHY.md](../../pages/BIBLIOGRAPHY.md) for related publications.

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.21983948
- PDF SHA-256: See zenodo_record
- Pairing confidence: strong
- Last checked: 2026-09-24T18:29:58Z

## Prerequisites

- Familiarity with OOXML, DOCX, Open Packaging Conventions
- Background in Computational fundamentals
- Access to source repository: docxology/docxplus

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.21983948`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
