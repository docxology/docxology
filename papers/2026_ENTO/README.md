# ENTO: an ENcrypted, Typed, Omnitrack container format for multimodal research data

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20647443.svg)](https://doi.org/10.5281/zenodo.20647443)

---

## Abstract

ENTO (ENcrypted, Typed, Omnitrack) is a flat ZIP container format and reference implementation for bundling heterogeneous research artifacts &mdash; time series, genomics slices, spectrograms, provenance proofs &mdash; into a single verifiable file. Each track is sealed under per-track AES-256-GCM authenticated encryption with format+track associated-data binding and PADM&Eacute; length padding. The default wire format is 0.4.0; formats 0.2.0, 0.3.0, and 0.3.1 remain read/write compatibility profiles. Graded observability levels control how much manifest metadata a recipient sees, and an optional hash-chained proof export provides tamper-evident lineage. Verification deliberately separates key-authenticated integrity from keyless corruption detection. This deposit is the 0.4 manuscript release candidate together with the MIT-licensed reference implementation source. Planned code home: https://github.com/docxology/entofile.

## Keywords

research data formats · authenticated encryption · AES-256-GCM · reproducible research · multimodal containers

## Publication Details

| Field | Value |
|------|-------|
| **DOI** | [10.5281/zenodo.20647443](https://doi.org/10.5281/zenodo.20647443) |
| **Published** | 2026-06-11 |
| **Version** | 0.4 |
| **Zenodo record** | https://zenodo.org/records/https://zenodo.org/records/20396328 |

## Files

- `entofile-0.4.pdf` - Zenodo PDF

## Citation

> Daniel Ari Friedman (2026). *ENTO: an ENcrypted, Typed, Omnitrack container format for multimodal research data*. Zenodo. https://doi.org/10.5281/zenodo.20647443

## Related

- GitHub release: https://github.com/docxology/entofile/releases/tag/v0.4

- Zenodo record: https://zenodo.org/records/20647443
- [Full Bibliography](../../pages/BIBLIOGRAPHY.md) · [All Papers](../README.md)
