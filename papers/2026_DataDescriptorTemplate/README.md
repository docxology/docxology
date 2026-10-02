<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 Data Descriptor Template: Schema, Provenance, and Release Readiness

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21298883-blue)](https://doi.org/10.5281/zenodo.21298883)

---

## Abstract

> This exemplar demonstrates a data descriptor workflow in which the schema, file inventory, provenance chain, license boundary, and validation gate are treated as first-class research artifacts rather than afterthoughts. It ships a small, public, synthetic demonstration dataset (two CSV files under data/fixtures/) and a machine-readable descriptor (data/example_descriptor.json) that declares each file's media type, sha256 checksum, and row count alongside a six-field data dictionary with typed constraints. A tested validation library (src/data_descriptor/) checks the descriptor's shape, safety, and completeness; recomputes each declared checksum and row count against the bytes on disk; and emits a deterministic, metadata-only release manifest suitable for pre-publication review. Every figure and quantitative claim in this manuscript is produced by that library and regenerated on demand, so the prose describes structure and provenance rather than transcribing values that would drift. This is a template with a demonstration dataset: it makes no scientific claim about the data, only about how to describe and release a dataset responsibly.

## Keywords

`data descriptor` · `FAIR data` · `provenance` · `schema validation`

## Methods

- **Synthetic demo dataset: two CSV fixtures plus JSON descriptor** — Ships two small deterministic synthetic CSV files (measurements, subjects) described by a machine-readable descriptor with checksums and row counts.
- **Six-field data dictionary with typed constraints** — Declares six fields with types, nullability, units, regex patterns, closed enumerations and numeric bounds for the measurement table.
- **Order-independent sha256 schema fingerprint** — descriptor_fingerprint() hashes (name, type, nullable) triples so reordering fields does not change the schema fingerprint.
- **Validation gate with readiness score and perturbed negative control** — validate_descriptor() emits severity-tagged findings folded into a readiness score; a deliberately broken copy tests that the gate reacts.
- **Byte-level descriptor-to-file verification** — verify_descriptor_files() recomputes sha256 and row counts of present files and reports verified, mismatch, or absent status.

## Key Findings

- The clean fixture descriptor produces zero validation findings, while the deliberately perturbed demo produces several errors and warnings.
- For the shipped fixture, both files verify: declared and actual row counts agree and each recomputed checksum matches, leaving the readiness score unpenalised.
- The paper reports that its zero-mock test suite exceeds the 90% project coverage gate.
- The work explicitly makes no scientific claim about the synthetic data; claims are limited to how to describe and release a dataset.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.5281/zenodo.21298883](https://doi.org/10.5281/zenodo.21298883)
- Zenodo record: [https://zenodo.org/records/21298883](https://zenodo.org/records/21298883)
- PDF: [Friedman_2026_Data_a542f49d.pdf](Friedman_2026_Data_a542f49d.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/21298883)

## Citation

> Daniel Ari Friedman (2026). *Data Descriptor Template: Schema, Provenance, and Release Readiness*. Zenodo. DOI: 10.5281/zenodo.21298883. URL: https://doi.org/10.5281/zenodo.21298883.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
