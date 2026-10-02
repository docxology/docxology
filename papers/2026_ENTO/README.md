<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 ENTO: an ENcrypted, Typed, Omnitrack container format for multimodal research data

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20396328-blue)](https://doi.org/10.5281/zenodo.20396328)

---

## Abstract

> ENTO (ENcrypted, Typed, Omnitrack) is a flat ZIP container format and reference implementation for bundling heterogeneous research artifacts — time series, genomics slices, spectrograms, provenance proofs — into a single verifiable file. Each track is sealed under per-track AES-256-GCM authenticated encryption with format+track associated-data binding and PADMÉ length padding. The default wire format is 0.4.0; formats 0.2.0, 0.3.0, and 0.3.1 remain read/write compatibility profiles. Graded observability levels control how much manifest metadata a recipient sees, and an optional hash-chained proof export provides tamper-evident lineage. Verification deliberately separates key-authenticated integrity from keyless corruption detection.
>
> This deposit is the 0.4 manuscript release candidate together with the MIT-licensed reference implementation source. Planned code home: https://github.com/docxology/entofile.

## Keywords

`research data formats` · `authenticated encryption` · `AES-256-GCM` · `reproducible research` · `multimodal containers`

## Methods

- **Flat ZIP layout: manifest.json, one encrypted member per track, optional proof** — Defines the container as a ZIP archive with a typed manifest, per-track .ento members and an optional hash-chain proof file.
- **Per-track AES-256-GCM envelopes with HKDF-derived keys** — Each track is sealed with authenticated encryption under a fixed nonce||tag||ciphertext header, specified in a Kaitai Struct file.
- **Four graded observability levels for export-time manifest redaction** — Observability levels 0–3 control which manifest metadata a recipient sees, without re-encrypting the track payloads.
- **Associated-data binding and PADMÉ length padding in the default profile** — The 0.4.0 default binds associated data and pads ciphertext members to PADMÉ buckets to coarsen the length channel.
- **Scripted benchmark: 150 repetitions over observability levels on fixture tracks** — Benchmarks on committed EEG, VCF and spectrogram fixtures plus a synthetic throughput track measure throughput, latency, expansion and tamper detection.

## Key Findings

- Tamper detection succeeded on all 2400 benchmark rows (rate 1.0).
- Mean pack throughput was 78.9296 MiB/s on the medium-track condition at observability level 3 (n = 150, CV 15.3%); the paper makes no superiority claim.
- Ciphertext expansion on fixture tracks was an exact, zero-variance 1.7113.
- Length is not hidden exactly: non-sealed levels disclose byte_length in the manifest, and sealed export still reveals the PADMÉ bucket.
- Concludes that a flat ZIP container can carry typed multimodal tracks, authenticated encryption, graded observability and proof export without becoming a repository or hosted service.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [docxology/entofile](https://github.com/docxology/entofile)
- GitHub release: [v0.4](https://github.com/docxology/entofile/releases/tag/v0.4)
- DOI: [10.5281/zenodo.20396328](https://doi.org/10.5281/zenodo.20396328)
- Zenodo record: [https://zenodo.org/records/20396328](https://zenodo.org/records/20396328)
- PDF: [entofile-0.4.pdf](entofile-0.4.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/20396328)

## Citation

> Daniel Ari Friedman (2026). *ENTO: an ENcrypted, Typed, Omnitrack container format for multimodal research data*. Zenodo. DOI: 10.5281/zenodo.20396328. URL: https://doi.org/10.5281/zenodo.20396328.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
