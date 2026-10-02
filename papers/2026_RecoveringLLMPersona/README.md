<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 Recovering LLM-Persona Accuracies from Unlabeled Votes

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20498699-blue)](https://doi.org/10.5281/zenodo.20498699)

---

## Abstract

> Algebraic (NTQR) evaluation infers how accurate a group of noisy classifiers was on a finite test using only their responses — no answer key. We test this end to end on real large language models. Three trader "personas" (optimistic, neutral, pessimistic), instantiated as system prompts, each make a binary bullish/bearish call on the same 64 market scenarios; we run the identical trio through six locally-hosted models via Ollama. For each model we recover per-persona, per-label accuracy with ErrorIndependentEvaluation (unsupervised) and score it against the authored ground truth (supervised), which is used only as a check. On the five models whose three judges all varied (mistral:latest, gemma4:latest, gemma3:4b, gemma2:2b, granite4.1:3b), the unsupervised algebra recovered persona accuracies to a mean absolute error of 0.012, within the 0.102 sampling-noise floor across all six per-label accuracy terms, with no labels -- including a persona's genuinely poor bullish accuracy of 0.57, recovered as 0.59. The other model collapsed at least one persona into a constant classifier (a judge that voted one way on all 64 scenarios), which makes the error-independent algebra unsolvable. The central, non-obvious result: inter-judge disagreement does not imply evaluability. Aggregate disagreement separated this run only because the unevaluable model(s) collapsed to 0.00; the five evaluable models spanned 0.03–0.23. What gates evaluation is a per-judge condition — every judge must vary (and answer) — not an ensemble one. We formalize this as a label-free evaluability diagnostic (a judge whose modal-vote fraction reaches 1.0 is a constant classifier; an unparseable vote is an abstention) that predicted exactly which models would be evaluable, before any solve and without ground truth. This is a concrete instance of the safety property the NTQR logic promises: it warns you when an ensemble is not good enough to be evaluated. A scenario bootstrap puts a 95% CI of [0.000, 0.038] on the recovery MAE (well inside the 0.102 noise floor), and a deterministic synthetic study generalizes the recovery beyond the finite set of real evaluable models — error falls like 1/√Q (slope -0.58, stable across ensembles) — while mapping two honest limits: the built-in failure alarm catches anti-correlated judges with no false positives yet can miss positively-correlated (shared-training) errors, and the two-solution tie-break inverts once judges are no longer clearly better than random — exactly where simple majority-voting evaluation, though biased, is the more robust fallback.

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
