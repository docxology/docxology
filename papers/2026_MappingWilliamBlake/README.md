<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 Mapping William Blake's Works: Evidence ledgers, source provenance, text-image diagnostics, and rights-bounded release controls

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21047573-blue)](https://doi.org/10.5281/zenodo.21047573)

---

## Abstract

> William Blake's works survive across editions, copy records, image archives, museum catalogues, transcriptions, and finding aids. Computational coverage is difficult to assess without explicit units, source authority, and evidence boundaries. We present *blake*, a 7-phase pipeline that connects a 104-entry work-level target ledger with retained source records, local analysis, provenance, recoverability checks, and generated publication artifacts.
>
> The saved offline run analyzes 727 local source/copy records. Its 6109 image associations reference 5975 distinct files. It represents 69 ledger targets (66.3%) and fully satisfies the declared evidence profile for 45 targets (43.3%). The text-bearing subset has 540 records and 682407 tokenizer-defined words. These exploratory text results include retained transcriptions with unverified authorship; they are not a Blake-authored language census. The top-level analysis ledger records 727/727 records analyzed and 0 top-level errors. Nested sub-analysis limitations are counted separately.
>
> Local recovery preserves 8481 inventoried files and 5975/6003 discovered image identifiers, leaving 28 unresolved. Checksums and a corruption-detection restore drill establish recoverability of the captured inventory, not completeness of Blake's oeuvre. Quantitative prose, tables, and figures derive from saved artifacts. Public releases contain project-authored software, manuscript sources, aggregate evidence, and checksums; provider texts, XML, images, private indexes, backups, and source-image mosaics remain local. The contribution is an auditable corpus-governance and preservation method with explicit scholarly and distribution limits.
>
> The implementation separates corpus custody from application policy. Portable source snapshots and explicit schema conversion preserve source identities and roles, while distinct retrieval profiles expose normalized-token, literal-casefold and regex contracts. Shared counting, hierarchy and evidence-admission methods support application papers without embedding their vocabularies or interpretations. Current source-derived diagrams identify those interfaces separately from the historical analytical producer.
>
> This deposit pairs the 94-page manuscript edition 0.5.0 with Blake software release 0.7.0. Generic half-open interval methods preserve occupied support, multiplicity and overlapping record pairs while applications retain source grouping and domain judgments. Entomology and Federalism are independent applications, linked as related research objects rather than runtime dependencies.

## Keywords

`William Blake` · `digital humanities` · `corpus acquisition` · `source provenance` · `rights-bounded release`

## Methods

- **Target-ledgered provenance pipeline** — Connect the 104-entry work-level ledger to source/copy evidence, analysis, recoverability and publication controls through seven phases.
- **Separated custody and retrieval policy** — Retain source identities and roles while exposing distinct normalized-token, literal-casefold and regex retrieval contracts.
- **Inventory-bounded recoverability** — Use checksums and a restore drill to assess the captured inventory rather than completeness of the oeuvre.

## Key Findings

- The saved run contains 727 local source/copy records and represents 69 of 104 work-level targets (66.3%); 45 targets (43.3%) fully meet the declared evidence profile.
- The text subset contains 540 records and 682407 tokenizer-defined words, including retained transcriptions with unverified authorship.
- Recovery preserves 8481 inventoried files and 5975 of 6003 discovered image identifiers, with 28 unresolved.
- The text counts include unverified authorship and do not establish a census of Blake-authored language.
- Image association counts do not establish an independent-image census or museum-wide completeness.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [docxology/blake](https://github.com/docxology/blake)
- GitHub release: [v0.7.0](https://github.com/docxology/blake/releases/tag/v0.7.0)
- DOI: [10.5281/zenodo.21047573](https://doi.org/10.5281/zenodo.21047573)
- Artifact DOI: [10.5281/zenodo.23921364](https://doi.org/10.5281/zenodo.23921364)
- Zenodo record: [https://zenodo.org/records/21047573](https://zenodo.org/records/21047573)
- Historical local PDF: [blake_working_paper.pdf](blake_working_paper.pdf)
- Current PDF (Zenodo, version 0.5.0): [Blake.pdf](https://zenodo.org/api/records/23921364/files/Blake.pdf/content)
- Local PDFs remain preserved historical archives.
- Extracted text retains its own source provenance; a matching filename does not establish edition identity.
- PDF SHA-256: 812e53237b40f808b4502e3dd358cbee5cda7d587e493ba95e41f02c11ad03eb

## Citation

> Daniel Ari Friedman (2026). *Mapping William Blake's Works: Evidence ledgers, source provenance, text-image diagnostics, and rights-bounded release controls*. Zenodo. DOI: 10.5281/zenodo.21047573. URL: https://doi.org/10.5281/zenodo.21047573.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
