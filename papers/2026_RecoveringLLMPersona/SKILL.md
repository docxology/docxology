---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "Recovering LLM-Persona Accuracies from Unlabeled Votes"
description: "Algebraic (NTQR) evaluation infers how accurate a group of noisy classifiers was on a finite test using only their responses — no answer key. We test this end to end on real large language models. Three trader \"personas\" (optimistic, neutral, pessimi..."
tags: ["algebraic-evaluation", "ntqr", "unsupervised-evaluation", "evaluation-on-unlabeled-data", "llm-as-judge", "error-independent-evaluation", "ensemble-evaluability", "constant-classifier", "ai-safety-warning-light", "reproducible-research"]
domain: "Computational"
citation: "Daniel Ari Friedman (2026). *Recovering LLM-Persona Accuracies from Unlabeled Votes*. Zenodo."
doi: "10.5281/zenodo.20498699"
---

# Recovering LLM-Persona Accuracies from Unlabeled Votes

**Daniel Ari Friedman** (2026) · Computational

## Context

This work addresses topics in **Computational**: algebraic evaluation, NTQR, unsupervised evaluation, evaluation on unlabeled data.

## Methods

Primary methods and techniques applied in this work:

- **Three system-prompted trader personas as binary judges** — Optimist, neutral and pessimist personas each make a bullish/bearish call on the same 64 authored market scenarios, run through six local models via Ollama.
- **Unsupervised NTQR ErrorIndependentEvaluation on vote counts** — Recovers per-persona, per-label accuracy from unlabeled vote patterns only; authored truth is held out and used afterward to score recovery error.
- **Deliberately unbalanced 40/24 scenario deck** — The answer key is set to prevalence 0.625 to avoid the evaluator's removable singularity at prevalence exactly 1/2.
- **Schema-constrained JSON vote collection** — Uses Ollama structured output with a JSON Schema so parsing is a measured interface check before the binary vote matrix is analysed.
- **Scenario bootstrap and deterministic synthetic-ensemble study** — Bootstraps over scenarios for a CI on recovery MAE, and runs synthetic ensembles with known truth to test error scaling, correlated errors and tie-break failure.

## Key Findings

Core contributions and results:

- For mistral:latest, unsupervised recovery matched authored-truth accuracies to a mean absolute error of 0.012, within the 0.102 sampling-noise floor.
- The algebra recovered a poor judge's accuracy without labels: the pessimist's true bullish accuracy of 0.57 was recovered as 0.59.
- Inter-judge disagreement did not imply evaluability; what gated evaluation was whether every individual judge varied, not ensemble-level disagreement.
- A label-free per-judge diagnostic (modal-vote fraction reaching 1.0) predicted exactly which models would be evaluable, before any solve.
- Synthetic studies show the failure alarm catches anti-correlated judges but can miss positively-correlated errors, and the tie-break inverts near chance-level judges.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2023_NSFReporting](../2023_NSFReporting/)
- [2023_NaturalAIBased](../2023_NaturalAIBased/)
- [2025_AuBI](../2025_AuBI/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.20498699
- PDF SHA-256: e1196698427f9fe04d1f3071705adb6e5459983649c78d7f5d074756e989148b
- Pairing confidence: strong
- Last checked: 2026-09-24T18:29:55Z

## Prerequisites

- Familiarity with algebraic evaluation, NTQR, unsupervised evaluation
- Background in Computational fundamentals
- Access to source repository: docxology/ntqr_llm

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.20498699`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
