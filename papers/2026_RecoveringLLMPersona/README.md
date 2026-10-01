<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 Recovering LLM-Persona Accuracies from Unlabeled Votes

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20498699-blue)](https://doi.org/10.5281/zenodo.20498699)

---

## Abstract

> Algebraic (NTQR) evaluation infers how accurate a group of noisy classifiers was on a finite test using only their responses — no answer key. We test this end to end on real large language models. Three trader "personas" (optimistic, neutral, pessimistic), instantiated as system prompts, each make a binary bullish/bearish call on the same 64 market scenarios; we run the identical trio through six...

## Keywords

`algebraic evaluation` · `NTQR` · `unsupervised evaluation` · `evaluation on unlabeled data` · `LLM-as-judge` · `error-independent evaluation` · `ensemble evaluability` · `constant classifier` · `AI safety warning light` · `reproducible research` · `answer-key-free recovery` · `local large language models`

## Methods

- **Three system-prompted trader personas as binary judges** — Optimist, neutral and pessimist personas each make a bullish/bearish call on the same 64 authored market scenarios, run through six local models via Ollama.
- **Unsupervised NTQR ErrorIndependentEvaluation on vote counts** — Recovers per-persona, per-label accuracy from unlabeled vote patterns only; authored truth is held out and used afterward to score recovery error.
- **Deliberately unbalanced 40/24 scenario deck** — The answer key is set to prevalence 0.625 to avoid the evaluator's removable singularity at prevalence exactly 1/2.
- **Schema-constrained JSON vote collection** — Uses Ollama structured output with a JSON Schema so parsing is a measured interface check before the binary vote matrix is analysed.
- **Scenario bootstrap and deterministic synthetic-ensemble study** — Bootstraps over scenarios for a CI on recovery MAE, and runs synthetic ensembles with known truth to test error scaling, correlated errors and tie-break failure.

## Key Findings

- For mistral:latest, unsupervised recovery matched authored-truth accuracies to a mean absolute error of 0.012, within the 0.102 sampling-noise floor.
- The algebra recovered a poor judge's accuracy without labels: the pessimist's true bullish accuracy of 0.57 was recovered as 0.59.
- Inter-judge disagreement did not imply evaluability; what gated evaluation was whether every individual judge varied, not ensemble-level disagreement.
- A label-free per-judge diagnostic (modal-vote fraction reaching 1.0) predicted exactly which models would be evaluable, before any solve.
- Synthetic studies show the failure alarm catches anti-correlated judges but can miss positively-correlated errors, and the tie-break inverts near chance-level judges.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [docxology/ntqr_llm](https://github.com/docxology/ntqr_llm)
- GitHub release: [v1.0.0](https://github.com/docxology/ntqr_llm/releases/tag/v1.0.0)
- DOI: [10.5281/zenodo.20498699](https://doi.org/10.5281/zenodo.20498699)
- Zenodo record: [https://zenodo.org/records/20498699](https://zenodo.org/records/20498699)
- PDF: [Friedman_2026_Recovering_e1196698.pdf](Friedman_2026_Recovering_e1196698.pdf)
- PDF SHA-256: e1196698427f9fe04d1f3071705adb6e5459983649c78d7f5d074756e989148b

## Citation

> Daniel Ari Friedman (2026). *Recovering LLM-Persona Accuracies from Unlabeled Votes*. Zenodo. DOI: 10.5281/zenodo.20498699. URL: https://doi.org/10.5281/zenodo.20498699.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
