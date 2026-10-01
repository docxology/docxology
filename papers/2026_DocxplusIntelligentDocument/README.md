<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 docxplus — the Intelligent Document Container

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21983948-blue)](https://doi.org/10.5281/zenodo.21983948)

---

## Abstract

> A standards-first reference implementation of a byte-valid OOXML .docx that also carries a modular, Ed25519-signed, AES-256-GCM-encrypted intelligence layer through spec-sanctioned side-channels, with an optional bridge to the docxology/steganographer signed-packet backend.

## Keywords

`OOXML` · `DOCX` · `Open Packaging Conventions` · `steganography` · `document security` · `reproducible research`

## Methods

- **Dual-contract design: OPC/ODF surface contract plus signed intelligence manifest** — A single archive is both a conforming .docx/.odt and a carrier of typed payload modules indexed by an Ed25519-signed manifest.
- **Per-module sealing (Argon2id/Scrypt + AES-256-GCM, X25519, Shamir k-of-n, decoys)** — Payloads are sealed individually rather than encrypting the whole package, with slot names bound as AES-GCM additional authenticated data.
- **Five spec-sanctioned transport channels incl. LSB steganography** — Implements custom XML parts, auxiliary package parts, custom document properties, MCE choice blocks, and LSB embedding in displayed images.
- **Merkle-tree provenance with composite surface digest and transparency log** — Signs a Merkle root over modules together with a digest of every part, content type and relationship; attestations go into a log anchored by a signed tree head.
- **Mock-free test harness, project round-trip, chi-squared steganalysis and red-team review** — Evaluated with 467 mock-free tests at a 90% coverage gate, an in-tree chi-squared LSB detector, a project round-trip harness, and 14 adversarial review cycles.

## Key Findings

- In the reference dossier, all 5 modules across all 4 sealing lineages extracted and verified, and the container passed OPC conformance.
- Carrying a 14-file, 9-directory project tree into both .docx and .odt containers, all 18 of 18 round-trip invariants held, with byte-identical packed payloads between profiles.
- The round-trip harness found that packing followed symbolic links, embedding link targets such as an SSH key; symlinks are now refused by default.
- The chi-squared detector flags fully embedded sealed (ciphertext) carriers but does not detect unsealed low-entropy payloads at any fill rate.
- Fourteen adversarial review cycles closed 88 confirmed findings, and a sample-pair analysis estimator was withdrawn after proving mis-scaled by roughly an order of magnitude.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [docxology/docxplus](https://github.com/docxology/docxplus)
- GitHub release: [v1.0.1](https://github.com/docxology/docxplus/releases/tag/v1.0.1)
- DOI: [10.5281/zenodo.21983948](https://doi.org/10.5281/zenodo.21983948)
- Zenodo record: [https://zenodo.org/records/21983948](https://zenodo.org/records/21983948)
- PDF: [manuscript.pdf](manuscript.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/21983948)

## Citation

> Daniel Ari Friedman (2026). *docxplus — the Intelligent Document Container*. Zenodo. DOI: 10.5281/zenodo.21983948. URL: https://doi.org/10.5281/zenodo.21983948.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
