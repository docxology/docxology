<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 Golden Line: Toward What Matters

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21754237-blue)](https://doi.org/10.5281/zenodo.21754237)

---

## Abstract

> A directional instrument for recording long-horizon aspirations and observable movement toward them. It returns one of four directional readings per aspiration against a versioned registry and deliberately computes no aggregate: there is no virtue score, and NOT_OBSERVED means no valid entry was admitted rather than that nobody looked. Subtitle: An Aspirational Thread for Long-Horizon Work Code...

## Keywords

`aspiration` · `long-horizon work` · `directional assessment` · `values in practice` · `research ethics` · `open science` · `non-compensatory reading`

## Methods

- **Python package with a versioned nine-entry aspiration registry** — Each aspiration pairs a thread and horizon with lists of Markers (signs of movement toward) and Counter-signals (signs of movement away).
- **Staged progress_report evaluator (intake, matching, decision)** — Horizon entries are screened and normalized, matched against declared markers/counter-signals, and mapped to TOWARD, INQUIRY, DRIFTING, or NOT_OBSERVED without numeric scores.
- **Formal definitions and propositions bound to named tests** — The evaluator's decision rule is restated as definitions and propositions matching the code, each tied to a test, plus seven structural invariants with planted-bad detection tests.
- **Descriptive analysis helpers and code-derived figures** — Pure read-only helpers (signal_inventory, horizon_distribution, temporal_currentness_sweep, report_overview) generate figures, several replaying the evaluator on synthetic entries.
- **Scholarship lineage for the founding aspirations** — Situates the four founding aspirations in a lineage from practical wisdom and practice-internal goods through capabilities, repair, commons governance, and metric hazards.

## Key Findings

- Counter-signal precedence: any recorded declared counter-signal yields DRIFTING regardless of how many markers were observed or staleness.
- TOWARD requires every declared marker and no counter-signal; there is no partial credit, so all-but-one marker reads the same as none.
- Stale or date-unauditable fully-marked observations yield INQUIRY rather than DRIFTING; the currentness sweep shows an exclusive boundary (current at 90, stale at 91 days).
- The shipped registry declares 18 markers and 9 counter-signals, all distinct; the paper stresses this counts vocabulary, not fulfilment.
- The author acknowledges the instrument does not handle the adversarial case: an observer can file the tokens that produce a TOWARD.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.5281/zenodo.21754237](https://doi.org/10.5281/zenodo.21754237)
- Zenodo record: [https://zenodo.org/records/21754237](https://zenodo.org/records/21754237)
- PDF: [golden_line_combined.pdf](golden_line_combined.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/21754237)

## Citation

> Daniel Ari Friedman (2026). *Golden Line: Toward What Matters*. Zenodo. DOI: 10.5281/zenodo.21754237. URL: https://doi.org/10.5281/zenodo.21754237.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
