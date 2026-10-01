<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 The Line Set: Holding Instruments Apart

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21754243-blue)](https://doi.org/10.5281/zenodo.21754243)

---

## Abstract

> A thin reader that declares what a set of small evaluative instruments is, reads whichever sibling packages are installed, and checks one narrow property: that no two of them have given the same spelling to different things. It adds no instrument of its own and computes no aggregate; a legible reading says only that the declared vocabularies did not overlap. Subtitle: A Declaration, a Reader, and...

## Keywords

`modularity` · `information hiding` · `separation of concerns` · `boundary objects` · `namespace collision` · `declarative registry` · `reproducible review` · `open science`

## Methods

- **Declarative set registry: four LineEntry records plus one shared token** — Declares the set (Red, Black, Golden, White Line) as data, each entry naming its question, job, and what it must not become.
- **Five-stage reader with fixed-precedence set statuses** — Reads installed sibling packages through resolve, bind, collide, declare and status stages, returning one of four SET_-prefixed readings.
- **Enum-member name collision check across sibling package roots** — Collects enum member names each line publishes at its package root and flags any name carried by more than one line, unless declared and disambiguated.
- **Seven offline structural checks plus a self-application check** — Runs seven declaration-only checks and an eighth that applies the package's own collision check to a declaration including itself.
- **Executed extensibility example appending a fifth colour at runtime** — Appends a hypothetical green_line entry without editing the package and runs the battery and reader on the extended declaration.

## Key Findings

- On the review date the four packages yielded 81 line-and-name pairs spanning 80 distinct names, and the only shared name was the already-declared, disambiguated one.
- The single shared name was OUTSIDE_SCOPE, carried by red_line and black_line.
- Appending a fifth line whose package is not installed yielded SET_PARTIAL, which the author argues is the correct answer rather than a shortfall.
- The author stresses that disjoint vocabularies are a necessary, not sufficient, condition: the check cannot detect conceptual overlap between instruments.
- The paper states the set digest is a comparison handle only, not tamper evidence or a record of who changed what.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.5281/zenodo.21754243](https://doi.org/10.5281/zenodo.21754243)
- Zenodo record: [https://zenodo.org/records/21754243](https://zenodo.org/records/21754243)
- PDF: [line_set_combined.pdf](line_set_combined.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/21754243)

## Citation

> Daniel Ari Friedman (2026). *The Line Set: Holding Instruments Apart*. Zenodo. DOI: 10.5281/zenodo.21754243. URL: https://doi.org/10.5281/zenodo.21754243.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
