<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 COGANT: Deterministic Codebase-to-GNN Translation

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20705350-blue)](https://doi.org/10.5281/zenodo.20705350)

---

## Abstract

> COGANT (Codebase-to-GNN Translation) deterministically converts software repositories into structured Active Inference artifacts expressed in the Active Inference Institute's Generalized Notation Notation (GNN). It is an evidence compiler: it propagates reviewable program facts through a finite fixpoint rule pipeline and emits graph, matrix, provenance, visualization, and round-trip artifacts...

## Keywords

`program analysis` · `Generalized Notation Notation` · `GNN` · `intermediate representation` · `code property graph` · `active inference` · `reproducible research` · `codebase-to-model translation` · `cognitive ecosystem modeling`

## Methods

- **Program-graph IR with confidence and provenance on nodes and edges** — Repositories are parsed (primarily via Python's standard-library ast) into a program graph IR whose nodes and edges carry confidence and provenance.
- **Fixpoint translation engine with 22 declarative rules in five families** — Rules (structural, semantic, control, behavioural, resilience) map nodes to 7 Active Inference mapping kinds, with priority-and-score conflict resolution.
- **A/B/C/D matrix derivation and GNN (Generalized Notation Notation) export** — Derives likelihood, transition, preference and prior matrices from the compiled state space and program-graph edges, normalized for the upstream GNN validator.
- **Forward-reverse-forward roundtrip over a 25-target regression corpus** — A reverse synthesizer rebuilds a Python package from each GNN bundle; role_preservation_score and strict isomorphism are recorded per target.
- **Rule-family and fixpoint-iteration ablations on packaged fixtures** — Removes each rule family and varies the iteration cap K in {1, 2, 5, 10}, recording changes in SemanticMapping counts on the shipped fixtures.

## Key Findings

- On the v0.6.0 roundtrip ledger, all 25 targets are role-preserved, but only 1 of 25 meets strict structural isomorphism.
- The author cautions that fixtures are in-sample, with no held-out split or confidence intervals, so scores upper-bound rather than estimate out-of-sample performance.
- The fixpoint ablation shows a single pass suffices on every shipped fixture, with the K=10 cap serving as a safety valve.
- Rule-family ablation indicates structural rules drive HIDDEN_STATE while semantic rules drive OBSERVATION/ACTION/POLICY/PREFERENCE roles.
- The author states the passing test suite, coverage and type-check gates support reliability and reproducibility but do not by themselves establish semantic adequacy.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [ActiveInferenceInstitute/COGANT](https://github.com/ActiveInferenceInstitute/COGANT)
- GitHub release: [v0.6.0](https://github.com/ActiveInferenceInstitute/COGANT/releases/tag/v0.6.0)
- DOI: [10.5281/zenodo.20705350](https://doi.org/10.5281/zenodo.20705350)
- Artifact DOI: [10.5281/zenodo.20705351](https://doi.org/10.5281/zenodo.20705351)
- Zenodo record: [https://zenodo.org/records/20705350](https://zenodo.org/records/20705350)
- PDF: [COGANT-0.6.0.pdf](COGANT-0.6.0.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/20705350)

## Citation

> Daniel Ari Friedman (2026). *COGANT: Deterministic Codebase-to-GNN Translation*. Zenodo. DOI: 10.5281/zenodo.20705350. URL: https://doi.org/10.5281/zenodo.20705350.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
