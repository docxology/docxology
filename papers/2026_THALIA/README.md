<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 THALIA: Typed Harness with Analytical Lexical-Integrated Architecture

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21763244-blue)](https://doi.org/10.5281/zenodo.21763244)

---

## Abstract

> THALIA is an executable research harness for long-context memory systems. It combines typed stage contracts, inspectable context selection, evidence-preserving episodic state, lexical-first retrieval, and bounded compiler search with source-bound evaluation and reproducible artifact checks. The deterministic results are finite diagnostic evidence; model-quality, integrity-advantage, and production-readiness claims remain separately gated.

## Keywords

`agentic systems` · `long-context memory` · `retrieval-augmented generation` · `reproducible research`

## Methods

- **Five-stage typed pipeline: Inspector, Retriever, Reasoner, Memory Gate, Compiler** — Implements a long-context memory harness where each stage has a typed input/output contract, runnable implementation, evidence trace and declared scope.
- **Offline lexical/hashing retrieval fused by weighted reciprocal-rank fusion** — The deterministic core uses BM25/grep, hashing-based retrieval, weighted RRF, real SQLite state and bounded MIPRO/GEPA-style configuration search without network calls.
- **Episodic-first memory: raw episodes appended before gated consolidation** — The Memory Gate appends each raw turn to state before evaluating a derived memory delta, preserving source material for auditing.
- **Tiered evaluation on LongMemEval-style, local, and LongMemEval_S slices** — Evaluates a fixed 6-example diagnostic set, a 24-example local comparison with gemma3:4b, an external LongMemEval_S transfer slice, and a 40-question bottleneck slice.
- **Injection and poisoning probes of cited excerpts** — Recorded injection probes test whether cited excerpts contain a supplied gold value and measure a poisoning effect, as negative controls.

## Key Findings

- On the fixed 6-example diagnostic set the default configuration reaches composite 0.621 (token-F1 0.477, citation-support proxy 0.830, efficiency 0.854).
- The 8-candidate compiler search ties on this easy set, so configuration improvement is unobserved; its main output is an auditable trace with a tie rule.
- Replacing the extractive Reasoner with gemma3:4b changed mean token-F1 from 0.587 to 0.540 in the 24-example comparison, with an interval spanning zero.
- In the 40-question bottleneck slice, ranking recall is 1.00 but Inspector recall is 0.60; an adaptive context policy raised neural token-F1 from 0.086 to 0.171.
- The author reports operational provenance as the clearest advantage, with equality on poisoning and no general answer-quality advantage.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.5281/zenodo.21763244](https://doi.org/10.5281/zenodo.21763244)
- Zenodo record: [https://zenodo.org/records/21763244](https://zenodo.org/records/21763244)
- PDF: [thalia-0.1.0.pdf](thalia-0.1.0.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/21763244)

## Citation

> Daniel Ari Friedman (2026). *THALIA: Typed Harness with Analytical Lexical-Integrated Architecture*. Zenodo. DOI: 10.5281/zenodo.21763244. URL: https://doi.org/10.5281/zenodo.21763244.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
