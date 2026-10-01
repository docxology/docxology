<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 🐜 Illegal States, Mostly Unrepresentable

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21298885-blue)](https://doi.org/10.5281/zenodo.21298885)

---

## Abstract

> This paper presents a strongly-typed, decentralized multiagent simulation — an ant-robot colony — as the computational exemplar of the Research Project Template (https://github.com/docxology/template). Each colony member is an Agent that owns exactly one real, on-disk SQLite database and one in-process, fault-injectable protocol endpoint; no agent ever touches another agent's storage or network...

## Keywords

`strongly typed programming` · `session types` · `algebraic data types` · `category theory` · `active inference` · `multiagent systems` · `affine types` · `illegal state unrepresentable`

## Methods

- **Simulated ant-robot colony: agents with own SQLite DB and protocol endpoint** — Each simulated colony member owns one on-disk SQLite database and one fault-injectable protocol endpoint, with no shared storage or network state.
- **mypy --strict as oracle on six known-bad and three known-good fixtures** — Runs mypy --strict as a subprocess on negative-control fixtures (expect errors), positive-control fixtures, and the src tree (expect zero exit).
- **Seeded fault injection (drop/reorder/duplicate/corrupt) over an in-process bus** — Drives real handshakes through an in-process bus with each fault mode enabled, checking typed error results and seed determinism.
- **Pre-registered seeded experiments with Wilson CIs, Fisher and Cochran–Armitage tests** — Tests colony convergence over independently seeded trials at a calibrated baseline (8 agents, 2 locations, 30 ticks) using Wilson intervals, Fisher and trend tests.
- **Design lenses: schema as functor; decision as expected-free-energy minimizer** — Frames per-agent storage as a functor Schema→Set and decisions via expected free energy, explicitly as design lenses rather than proofs.

## Key Findings

- The stigmergic mechanism's convergence beat a random-choice null model: its Wilson lower bound (0.8816) clears the null model's upper bound (0.0368).
- Disabling only pheromone deposit collapsed convergence to chance level, attributing the mechanism's advantage to the stigmergic channel in this configuration.
- Convergence versus decay showed a threshold rather than a monotonic slope, with 0/60 trials converging at decay 0.10 and 0.30.
- Convergence decreased strictly as preference heterogeneity widened (1.0000 > 0.9333 > 0.2500 > 0.0333).
- An audit found a defect the src-only mypy gate missed (a Protocol a frozen dataclass could not satisfy), fixed with read-only properties and a good-fixture regression guard.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.5281/zenodo.21298885](https://doi.org/10.5281/zenodo.21298885)
- Zenodo record: [https://zenodo.org/records/21298885](https://zenodo.org/records/21298885)
- PDF: [Friedman_2026_Illegal_5bda439c.pdf](Friedman_2026_Illegal_5bda439c.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/21298885)

## Citation

> Daniel Ari Friedman (2026). *Illegal States, Mostly Unrepresentable*. Zenodo. DOI: 10.5281/zenodo.21298885. URL: https://doi.org/10.5281/zenodo.21298885.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
