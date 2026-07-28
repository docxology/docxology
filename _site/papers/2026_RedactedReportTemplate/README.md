# Redacted Report Template: Disclosure Control and Release Audit

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21298890.svg)](https://doi.org/10.5281/zenodo.21298890)

---

## Abstract

This exemplar demonstrates a complete disclosure-control pipeline for sanitized public release reports. The methodology combines classification-ceiling enforcement, source-protection validation, mosaic-risk scoring, and TPM-backed sealed sidecars across a sixteen-variant visual proof matrix. Four redaction styles—blackout, whiteout, grayout, and blur—are rendered across four PDF backgrounds—white, gray, black, and blur—yielding sixteen base proof PDFs. Each receives nine steganographic security methods including SHA-256/SHA-512 hash manifests, diagonal watermark overlays, footer provenance stamps, invisible text, QR and Code128 barcodes, PDF Info and XMP metadata, and embedded manifest attachments. Optional Kmyth TPM sealing wraps each hash manifest and steganography PDF in a .ski sidecar sealed against the TPM2-TSS storage hierarchy, bound to PCR selections and policy or-values. The release gate requires three reviewer roles—originator, classification reviewer, and release authority—each providing a non-empty rationale. A source-safe redaction ledger records SHA-256 hashes of each redacted span without exposing source text, and a segment hash manifest compares source and public SHA-256 digests for reproducible audit. The comprehensive release packet combines sanitized text, audit findings, ledger, hashes, review gate status, and paragraph-level audit tables into a single JSON-ready export. This exemplar confirms that visual presentation choices remain orthogonal to the release gate: the same source-safe decisions drive every output variant.

## Keywords

redaction · disclosure control · release audit · source protection

## Artifacts

| Field | Value |
|------|-------|
| **DOI** | [10.5281/zenodo.21298890](https://doi.org/10.5281/zenodo.21298890) |
| **Published** | 2026-07-10 |
| **Version** | 0.1.0 |
| **Zenodo record** | https://zenodo.org/records/21298890 |

## Files

- `Friedman_2026_Redacted_103642b6.pdf` - Zenodo PDF

## Citation

> Daniel Ari Friedman (2026). *Redacted Report Template: Disclosure Control and Release Audit*. Zenodo. DOI: 10.5281/zenodo.21298890. URL: https://doi.org/10.5281/zenodo.21298890.

## Related

- Zenodo record: https://zenodo.org/records/21298890
- [Full Bibliography](../../pages/BIBLIOGRAPHY.md) · [All Papers](../README.md)
