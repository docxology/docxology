<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 🎨 Symergetics: Symbolic Synergetics for Rational Arithmetic

**Daniel Friedman** (2025) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.17114389-blue)](https://doi.org/10.5281/zenodo.17114389)

---

## Abstract

> Floating-point arithmetic introduces systematic approximation errors that obscure fundamental mathematical relationships in geometric calculations, producing results like 2.999999999999999 instead of the exact integer 3. These compounding and confounding precision losses stymie a full-featured implementation of Buckminster Fuller's Synergetics framework, which requires symbolic operations on...

## Keywords

`Symergetics` · `Synergetics` · `Buckminster Fuller` · `rational arithmetic` · `Quadray coordinates` · `IVM lattice` · `symbolic computation` · `computational geometry`

## Methods

- **SymergeticsNumber exact-rational wrapper over Python fractions.Fraction** — Arithmetic is done with a Fraction-based class that keeps exact fractional representations and auto-simplifies via GCD.
- **Quadray (four-axis tetrahedral) coordinates in the IVM lattice** — Points are represented as (a, b, c, d) along four tetrahedral axes, normalized by subtracting the minimum coordinate.
- **IVM-unit volume calculation for Platonic solids** — The package computes polyhedron volumes in IVM units with the tetrahedron as the unit volume.
- **Pattern analysis of Scheherazade numbers (1001^n), primorials, palindromes** — Exact-arithmetic routines analyze powers of 1001, primorial sequences, and multi-base palindromes.
- **Test suite of 953 test functions across 32 files** — Validation is via a pytest suite covering arithmetic, coordinate transforms, geometry and integration cases.

## Key Findings

- The package reports 100% precision preservation across 953 test cases.
- Exact arithmetic returns 11/12 for 3/4 + 1/6 rather than the float 0.9166666666666666, with no approximation errors detected in any test case.
- The paper reports that its Platonic-solid volume relationships in IVM units were independently verified, confirming Fuller's original Synergetics calculations.
- Quadray-to-Cartesian conversions are reported to round-trip exactly.
- Primorials are computed exactly, e.g. 10# = 6,469,693,230.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.5281/zenodo.17114389](https://doi.org/10.5281/zenodo.17114389)
- Zenodo record: [https://zenodo.org/records/17114389](https://zenodo.org/records/17114389)
- PDF: [2025_Symergetics.pdf](2025_Symergetics.pdf)
- PDF download: [Symergetics_v1_DAF_9-13-2025.pdf](https://zenodo.org/api/records/17114390/files/Symergetics_v1_DAF_9-13-2025.pdf/content)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/17114389)

## Citation

> Daniel Friedman (2025). *Symergetics: Symbolic Synergetics for Rational Arithmetic*. Zenodo. DOI: 10.5281/zenodo.17114389. URL: https://doi.org/10.5281/zenodo.17114389.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
