# Data Descriptor Template: Schema, Provenance, and Release Readiness

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21298884.svg)](https://doi.org/10.5281/zenodo.21298884)

---

## Abstract

This exemplar demonstrates a data descriptor workflow in which the schema, file inventory, provenance chain, license boundary, and validation gate are treated as first-class research artifacts rather than afterthoughts. It ships a small, public, synthetic demonstration dataset (two CSV files under data/fixtures/) and a machine-readable descriptor (data/example_descriptor.json) that declares each file's media type, sha256 checksum, and row count alongside a six-field data dictionary with typed constraints. A tested validation library (src/data_descriptor/) checks the descriptor's shape, safety, and completeness; recomputes each declared checksum and row count against the bytes on disk; and emits a deterministic, metadata-only release manifest suitable for pre-publication review. Every figure and quantitative claim in this manuscript is produced by that library and regenerated on demand, so the prose describes structure and provenance rather than transcribing values that would drift. This is a template with a demonstration dataset: it makes no scientific claim about the data, only about how to describe and release a dataset responsibly.

## Keywords

data descriptor · FAIR data · provenance · schema validation

## Artifacts

| Field | Value |
|------|-------|
| **DOI** | [10.5281/zenodo.21298884](https://doi.org/10.5281/zenodo.21298884) |
| **Published** | 2026-07-09 |
| **Version** | 0.1.0 |
| **Zenodo record** | https://zenodo.org/records/21298883 |

## Files

- `Friedman_2026_Data_a542f49d.pdf` - Zenodo PDF

## Citation

> Daniel Ari Friedman (2026). *Data Descriptor Template: Schema, Provenance, and Release Readiness*. Zenodo. DOI: 10.5281/zenodo.21298884. URL: https://doi.org/10.5281/zenodo.21298884.

## Related

- Zenodo record: https://zenodo.org/records/21298883
- [Full Bibliography](../../pages/BIBLIOGRAPHY.md) · [All Papers](../README.md)
