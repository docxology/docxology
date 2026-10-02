<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 MDKV: A Multitrack Markdown Container for Structured, Portable Documents

**Daniel Friedman** (2025) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.16790554-blue)](https://doi.org/10.5281/zenodo.16790554)

---

## Abstract

> Digital knowledge work increasingly demands documents that are simultaneously multilingual, multi‑audience, and multi‑channel. Traditional single‑file Markdown struggles when the same canonical content must coexist with translations, commentary, references, code exemplars, and revision notes – each with distinct lifecycles and audiences. This paper introduces MDKV, a simple but rigorous multitrack Markdown container that packages a document’s canonical content and auxiliary tracks into a single, portable `.mdkv` file. An `.mdkv` is a ZIP archive with a YAML `manifest.yaml` and a `tracks/` directory of UTF‑8 Markdown files. MDKV provides a principled data model, validation, search, and export services, a CLI, and a small GUI for selective preview and live editing. We formalize the MDKV model, present its software architecture, explain round‑trip export semantics, and evaluate design trade‑offs against adjacent technologies. The MDKV initial specification is open source under the Apache‑2.0 license and maintained at the project repository https://github.com/docxology/mdkv . We also situate MDKV with respect to Matroska (MKV) as background on containerization: although the two are orthogonal in domain (text vs. multimedia), they share conceptual lineage in extensible container design. We conclude with use cases, implications for governance and reproducibility, and future work such as richer validation rules and alternative exporters. This paper is itself a Markdown file that renders into a valid MDKV. The built artifact is available at paper/paper.mdkv ; combined exports are under paper/_bundle .

## Keywords

`MDKV` · `Markdown` · `multitrack documents` · `ZIP container` · `YAML manifest` · `round-trip export`

## Methods

- **ZIP container with YAML manifest and tracks/ directory of Markdown files** — MDKV defines an .mdkv file as a ZIP archive holding a manifest.yaml index plus one UTF-8 Markdown file per track.
- **Seven-type track taxonomy (primary, translation, commentary, code, etc.)** — Document layers are separated into typed tracks that are composed into views only at export time.
- **Python reference implementation split into core, storage, services, and CLI** — The software follows a thin-orchestrator design with separate modules for data model and validation, persistence, search/export, and command-line entry points.
- **Round-trip export via HTML-comment track headers** — Combined Markdown exports prefix each track with a comment encoding its id, type, and language so attribution can be reconstructed.
- **Normative MUST/SHOULD conformance requirements and minimal validator** — The paper specifies conformance rules and a base validator checking title, authors, a primary track, track paths, types, and unique ids.

## Key Findings

- The paper lists four contributions: a precise model and container format, a modular architecture exposed via CLI and GUI, detailed use cases, and guidance on cryptographic provenance and conformance.
- Export is designed to be deterministic: order follows the manifest, and identical inputs produce identical outputs.
- The author lists format limitations, including no built-in encryption or signing and code tracks that are listings rather than runnable notebooks.
- The paper notes that the reference validator currently checks for a track with id 'primary' rather than the type-level requirement.
- The paper is itself authored as a Markdown file that renders into a valid MDKV.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.5281/zenodo.16790554](https://doi.org/10.5281/zenodo.16790554)
- Zenodo record: [https://zenodo.org/records/16790554](https://zenodo.org/records/16790554)
- PDF: [2025_MDKV.pdf](2025_MDKV.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/16790554)

## Citation

> Daniel Friedman (2025). *MDKV: A Multitrack Markdown Container for Structured, Portable Documents*. Zenodo. DOI: 10.5281/zenodo.16790554. URL: https://doi.org/10.5281/zenodo.16790554.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
