<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 Redacted Report Template: Disclosure Control and Release Audit

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21298890-blue)](https://doi.org/10.5281/zenodo.21298890)

---

## Abstract

> This exemplar demonstrates a complete disclosure-control pipeline for sanitized public release reports. The methodology combines classification-ceiling enforcement, source-protection validation, mosaic-risk scoring, and TPM-backed sealed sidecars across a sixteen-variant visual proof matrix. Four redaction styles—blackout, whiteout, grayout, and blur—are rendered across four PDF...

## Keywords

`redaction` · `disclosure control` · `release audit` · `source protection`

## Methods

- **Invented fixture data with synthetic classified segments and reviewers** — The pipeline is exercised only on synthetic segments (UNCLASSIFIED to TOP_SECRET//SCI), synthetic redaction decisions and synthetic reviewer records.
- **Text-level release-audit engine with mosaic-risk scoring** — Segments are audited against a public classification ceiling, redaction spans checked for overlap, orphan decisions flagged, source-control coverage enforced, and residual markers scored.
- **4x4 visual redaction proof matrix plus nine steganographic methods** — Four redaction styles are rendered on four PDF backgrounds (16 PDFs), each post-processed with hash manifests, watermarks, barcodes, metadata and embedded manifests.
- **Kmyth TPM sealing via swtpm and an mssim-to-swtpm proxy on macOS** — Hash manifests and steganography PDFs are sealed into .ski sidecars; on macOS a software TPM and protocol proxy were used, and kmyth-seal was patched to flush contexts.
- **Source-safe SHA-256 redaction ledger and three-role review gate** — Redacted spans are recorded only as SHA-256 hashes, and release requires originator, classification reviewer and release authority approvals with rationales.

## Key Findings

- On the fixture packet (fourteen segments), the audit reported the packet releasable with redaction coverage 1.0, plus warning-level residual-marker findings.
- In the verified run, all sixteen variants produced both TPM sidecars, giving thirty-two .ski files.
- Without the FlushContext patch, the second kmyth-seal invocation fails with an out-of-memory-for-object-contexts error on swtpm.
- The author reports that visual presentation choices are orthogonal to the release gate: all four redaction treatments yield equivalent source-safe outputs.
- Stated limitations: fixture data is invented, swtpm lacks hardware tamper resistance, and batch sealing of 32 sidecars takes about thirty seconds via the proxy.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.5281/zenodo.21298890](https://doi.org/10.5281/zenodo.21298890)
- Zenodo record: [https://zenodo.org/records/21298890](https://zenodo.org/records/21298890)
- PDF: [Friedman_2026_Redacted_103642b6.pdf](Friedman_2026_Redacted_103642b6.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/21298890)

## Citation

> Daniel Ari Friedman (2026). *Redacted Report Template: Disclosure Control and Release Audit*. Zenodo. DOI: 10.5281/zenodo.21298890. URL: https://doi.org/10.5281/zenodo.21298890.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
