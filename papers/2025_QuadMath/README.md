<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 🎨 QuadMath: An Analytical Review of 4D and Quadray Coordinates

**Daniel Friedman** (2025) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.16887799-blue)](https://doi.org/10.5281/zenodo.16887799)

---

## Abstract

> We review a unified analytical framework for four dimensional (4D) modeling and Quadray coordinates, synthesizing geometric foundations, optimization on tetrahedral lattices, and information geometry. Building on R. Buckminster Fuller’s Synergetics and the Quadray coordinate system, with extensive reference to Kirby Urner’s computational implementations across multiple programming languages (see...

## Keywords

`QuadMath` · `Quadray coordinates` · `4D geometry` · `Synergetics` · `Buckminster Fuller` · `IVM lattice` · `rational arithmetic` · `computational geometry`

## Methods

- **Three-namespace framing of '4D': Coxeter.4D, Einstein.4D, Fuller.4D** — Separated Euclidean E4, Minkowski spacetime, and synergetics/Quadray meanings of 4D with a dot-notation to avoid cross-domain confusion.
- **Nelder–Mead adapted to the integer Quadray lattice with volume tracking** — Ran Nelder–Mead simplex steps, snapping each proposal to the nearest integer Quadray point and monitoring integer tetravolume as a convergence diagnostic.
- **Fisher information and natural gradient in Quadray parameter space** — Defined Fisher information over Quadray parameters and analyzed optimization as geodesic motion on an information manifold.
- **Tested Python codebase with exact Bareiss determinants and cross-validation** — Accompanied the review with a fully tested Python codebase (100% coverage for src/), cross-validated against Kirby Urner's 4dsolutions reference implementations.
- **Bridging vs native tetravolume comparison (Cayley–Menger + S3 vs Ace 5x5)** — Compared IVM tetravolumes from edge-length Cayley–Menger determinants converted by S3 against Tom Ace's native 5x5 Quadray determinant on canonical cases.

## Key Findings

- The review describes how integer lattice constraints quantize tetrahedral simplex volumes into discrete 'energy levels' that regularize optimization.
- Bridging (Cayley–Menger + S3) and native (Ace 5x5) tetravolume computations agree at machine precision on the tested integer-Quadray examples.
- On a simple quadratic objective, the discrete Nelder–Mead converges with simplex volume showing discrete plateaus characteristic of integer-lattice optimization.
- In IVM units, common synergetic polyhedra have integer volumes, e.g. cube 3, octahedron 4, rhombic dodecahedron 6, cuboctahedron 20, relative to the unit tetrahedron.
- The author notes limitations: embedding choice for distances, possible need for hybrid continuous/lattice strategies, and that empirical benchmarking is still needed to quantify benefits.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.5281/zenodo.16887799](https://doi.org/10.5281/zenodo.16887799)
- Zenodo record: [https://zenodo.org/records/16887799](https://zenodo.org/records/16887799)
- PDF: [2025_QuadMath.pdf](2025_QuadMath.pdf)
- PDF download: [QuadMath_v1_DAF_08-16-2025.pdf](https://zenodo.org/api/records/16887800/files/QuadMath_v1_DAF_08-16-2025.pdf/content)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/16887799)

## Citation

> Daniel Friedman (2025). *QuadMath: An Analytical Review of 4D and Quadray Coordinates*. Zenodo. DOI: 10.5281/zenodo.16887799. URL: https://doi.org/10.5281/zenodo.16887799.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
