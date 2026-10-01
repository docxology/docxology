---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "Symergetics: Symbolic Synergetics for Rational Arithmetic"
description: "Symergetics (Symbolic Synergetics) provides a framework for rational arithmetic, geometric pattern discovery, and all-integer accounting based on Buckminster Fuller's Synergetics. The package implemen..."
tags: ["symergetics", "synergetics", "buckminster-fuller", "rational-arithmetic", "quadray-coordinates", "ivm-lattice", "symbolic-computation", "computational-geometry"]
domain: "Art & Synergetics"
citation: "Daniel Friedman (2025). *Symergetics: Symbolic Synergetics for Rational Arithmetic*. Zenodo."
doi: "10.5281/zenodo.17114389"
---

# Symergetics: Symbolic Synergetics for Rational Arithmetic

**Daniel Friedman** (2025) · Art & Synergetics

## Context

This work addresses topics in **Art & Synergetics**: Symergetics, Synergetics, Buckminster Fuller, rational arithmetic.

## Methods

Primary methods and techniques applied in this work:

- **SymergeticsNumber exact-rational wrapper over Python fractions.Fraction** — Arithmetic is done with a Fraction-based class that keeps exact fractional representations and auto-simplifies via GCD.
- **Quadray (four-axis tetrahedral) coordinates in the IVM lattice** — Points are represented as (a, b, c, d) along four tetrahedral axes, normalized by subtracting the minimum coordinate.
- **IVM-unit volume calculation for Platonic solids** — The package computes polyhedron volumes in IVM units with the tetrahedron as the unit volume.
- **Pattern analysis of Scheherazade numbers (1001^n), primorials, palindromes** — Exact-arithmetic routines analyze powers of 1001, primorial sequences, and multi-base palindromes.
- **Test suite of 953 test functions across 32 files** — Validation is via a pytest suite covering arithmetic, coordinate transforms, geometry and integration cases.

## Key Findings

Core contributions and results:

- The package reports 100% precision preservation across 953 test cases.
- Exact arithmetic returns 11/12 for 3/4 + 1/6 rather than the float 0.9166666666666666, with no approximation errors detected in any test case.
- The paper reports that its Platonic-solid volume relationships in IVM units were independently verified, confirming Fuller's original Synergetics calculations.
- Quadray-to-Cartesian conversions are reported to round-trip exactly.
- Primorials are computed exactly, e.g. 10# = 6,469,693,230.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2018_PPPiP](../2018_PPPiP/)
- [2022_MirrorTest](../2022_MirrorTest/)
- [2023_BlakeFuller](../2023_BlakeFuller/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.17114389
- PDF SHA-256: See zenodo_record
- Pairing confidence: unknown
- Last checked: 2026-06-30T23:25:58Z

## Prerequisites

- Familiarity with Symergetics, Synergetics, Buckminster Fuller
- Background in Art & Synergetics fundamentals
- Access to source repository: N/A

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.17114389`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
