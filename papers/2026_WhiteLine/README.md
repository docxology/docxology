<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 White Line: A Typed Ledger for the Edge of the Claim

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21754241-blue)](https://doi.org/10.5281/zenodo.21754241)

---

## Abstract

> A typed ledger for absence: epistemic gaps, ethical restraint, and contemplative negative space. It records what is missing, withheld, or unresolved under a total caution order, decays stale namings past their review horizons, and refuses to infer why anything is absent. Withholding is recorded as a boundary, never mined as missing evidence. Subtitle: Keeping missing evidence, ethical boundaries...

## Keywords

`absence` · `epistemic gaps` · `missing evidence` · `withheld material` · `uncertainty` · `negative results` · `research ethics` · `open science`

## Methods

- **Pure-data Python package: 11-record registry + assess_absence evaluator** — The instrument is a small Python package holding a versioned registry of eleven absence records and a staged evaluator, presented as a tested prototype.
- **Typology of three absence kinds and four ledger states** — Records are typed EPISTEMIC, ETHICAL or CONTEMPLATIVE, and observations assign NAMED, UNRESOLVED, WITHHELD or ledger-reserved NOT_RECORDED.
- **Staged intake/matching/scoring with caution order and staleness decay** — Intake screens inputs with typed events, conflicting observers resolve to the more cautious state, and dated NAMED entries decay past their review horizon.
- **Formal definitions/propositions each bound to a named test** — The evaluator is restated as definitions and propositions, and a table maps each to the test that exercises it, checked by tests/test_formalism.py.
- **Planted-defect battery for six structural invariants** — For each of six registry invariants, a registry carrying exactly that defect is constructed to show the check rejects it while passing the real registry.

## Key Findings

- Under the stated contract, no input can make an absence appear more settled than its most cautious observer reported (caution monotonicity).
- In a worked seven-input example with careless and adversarial inputs, intake logged five typed events and the tally was NAMED 0, UNRESOLVED 1, WITHHELD 1, NOT_RECORDED 9.
- A positive-control battery shows every intake code can fire, so zero rows in a tally mean untriggered rather than unreachable; it shows reachability only.
- The defect battery establishes detection of the planted defects only, not the absence of every possible structural fault.
- The author stresses the registry's finiteness: absences outside its eleven categories are not tracked, and extending it requires human judgment.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.5281/zenodo.21754241](https://doi.org/10.5281/zenodo.21754241)
- Zenodo record: [https://zenodo.org/records/21754241](https://zenodo.org/records/21754241)
- PDF: [white_line_combined.pdf](white_line_combined.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/21754241)

## Citation

> Daniel Ari Friedman (2026). *White Line: A Typed Ledger for the Edge of the Claim*. Zenodo. DOI: 10.5281/zenodo.21754241. URL: https://doi.org/10.5281/zenodo.21754241.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
