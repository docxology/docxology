<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 📄 Forensic Audit of the MillenniumLean Clay-Proof Package (AIX Global)

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.22243472-blue)](https://doi.org/10.5281/zenodo.22243472)

---

## Abstract

> Statement-level forensic audit of the MillenniumLean package (AIX Global, Zenodo 10.5281/zenodo.22226553), which claims kernel-checked Lean 4 proofs of the six remaining Clay Millennium Problems. The audit independently reproduces every kernel-hygiene claim (clean build, zero sorry, zero project axioms) under the pinned toolchain, then audits what the theorem types actually say. Verdict: none of the six problems is resolved.

## Keywords

`lean-4` · `formal-verification` · `millennium-prize-problems` · `claim-audit` · `adversarial-review` · `evidence-first`

## Methods

- **Independent kernel reproduction under the pinned Lean 4/mathlib toolchain** — Rebuilt the MillenniumLean package with the exact pinned Lean toolchain and mathlib revision and re-ran its axiom report to check its kernel-hygiene claims.
- **Statement-level binder parsing compared against official Clay statements** — Parsed each claimed final theorem with a binder extractor and classified it against the official Clay problem statements as conditional, definition-only, or off-topic.
- **Script-checked, line-anchored quotation of the package source** — Verified all line-anchored quotations in the fourteen finding reports against the extracted package bytes by script, and disclosed an earlier failed draft.
- **Test suite asserting audit facts on real package bytes** — Used fifteen test files that assert audit facts against the actual package bytes without mocks.

## Key Findings

- The package's kernel claims hold and reproduce exactly: clean build, zero live sorry, zero project axioms, and only standard axiom footprints.
- The claimed final theorems are evidentially void: conditional implications with unproved premises, definitions of the open statements, or true theorems about unrelated simple objects.
- The 'universalization tower' certifying Hodge, BSD and Navier-Stokes proves only that 0 < n + 1 for all naturals.
- Verdict: none of the six Clay problems is resolved; the audit disputes no kernel output, only what those outputs are claimed to demonstrate.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [docxology/millennium_audit](https://github.com/docxology/millennium_audit)
- DOI: [10.5281/zenodo.22243472](https://doi.org/10.5281/zenodo.22243472)
- Artifact DOI: [10.5281/zenodo.22243473](https://doi.org/10.5281/zenodo.22243473)
- Zenodo record: [https://zenodo.org/records/22243473](https://zenodo.org/records/22243473)
- PDF: [Friedman_2026_MillenniumAudit.pdf](Friedman_2026_MillenniumAudit.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/22243473)

## Citation

> Daniel Ari Friedman (2026). *Forensic Audit of the MillenniumLean Clay-Proof Package (AIX Global)*. Zenodo. DOI: 10.5281/zenodo.22243472. URL: https://doi.org/10.5281/zenodo.22243472.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
