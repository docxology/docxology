<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 The Witness Register: Co-Registration Without Aggregation

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21754245-blue)](https://doi.org/10.5281/zenodo.21754245)

---

## Abstract

> A shared register that co-registers independent instruments' report envelopes without aggregating them. It stores each report's envelope verbatim, records cross-instrument relations as separate describing records, keeps history append-only and sealed, and — only when asked, for one declared next use — emits a bounded posture that always points back at the state that earned it. It never parses...

## Keywords

`co-registration` · `append-only log` · `provenance` · `non-compensatory decision rules` · `boundary objects` · `research infrastructure` · `open science`

## Methods

- **witness_register Python package with shape-check intake of envelopes** — A small Python package with no line-package imports accepts line.report-envelope/1.0 JSON envelopes by value after a schema shape check, storing native_status verbatim.
- **SHA-256 sealed, prior_ref-chained append-only witness states** — Each state is sealed by SHA-256 over canonical JSON and chained to its predecessor; the prior seal is re-derived before extension so tampering fails closed.
- **Non-compensatory -1/0/+1 projection with fixed precedence rules** — For a declared next use, a bounded posture is computed from relation records only: unresolved block forces -1, empty state is -1, any hold caps at 0.
- **Formal definitions and propositions bound to named tests** — Definitions and propositions (append-only, non-compensatory, determinism, etc.) are each bound to a named test in the package's test suite.
- **3x3 canonical witness battery with falsification pass; real envelopes** — Nine constructed cases (positive, negative, adversarial) are run against the projection, with planted errors to confirm checks can fail; worked examples use real envelopes from four lines.

## Key Findings

- On four real envelopes describing different subjects, chain verification was clean, return recoverability and relation fidelity were 1.0, and the posture was held at 0.
- In the same-subject example, meeting the return contract lifted only the return_due hold, and the posture stayed at 0 because one open question entered as an unresolved dependency.
- A non-compensatory block forced -1 both alone and under fifty AGREES relations; an empty register was -1.
- Every battery check passed on the real register, and every case raised BatteryError when its observed behaviour was deliberately falsified.
- The author states limits: the chain tip is unbound without an external anchor, intake is a shape check not a truth check, and examples cover one date and nine constructed states.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.5281/zenodo.21754245](https://doi.org/10.5281/zenodo.21754245)
- Zenodo record: [https://zenodo.org/records/21754245](https://zenodo.org/records/21754245)
- PDF: [witness_register_combined.pdf](witness_register_combined.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/21754245)

## Citation

> Daniel Ari Friedman (2026). *The Witness Register: Co-Registration Without Aggregation*. Zenodo. DOI: 10.5281/zenodo.21754245. URL: https://doi.org/10.5281/zenodo.21754245.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
