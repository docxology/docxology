---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "Bounded AutoResearch for a Tiny Reproducible Machine-Learning Task"
description: "This paper presents Deterministic bounded AutoResearch for a small MNIST neural-network task, a public template exemplar that turns an AutoResearch loop into ordinary reproducible research infrastructure. The case study is intentionally small but con..."
tags: ["autoresearch", "reproducible-research", "machine-learning-benchmark", "artifact-readiness", "human-review", "local-artifact-integrity"]
domain: "Computational"
citation: "Daniel Ari Friedman (2026). *Bounded AutoResearch for a Tiny Reproducible Machine-Learning Task*. Zenodo."
doi: "10.5281/zenodo.20417016"
---

# Bounded AutoResearch for a Tiny Reproducible Machine-Learning Task

**Daniel Ari Friedman** (2026) · Computational

## Context

This work addresses topics in **Computational**: autoresearch, reproducible research, machine learning benchmark, artifact readiness.

## Methods

Primary methods and techniques applied in this work:

- **Offline MNIST subset: 2000 train / 500 test images, seed 20260525** — Uses a committed, class-balanced local MNIST subset with recorded provenance hashes; no data are downloaded at runtime.
- **Bounded candidate search over MLP, softmax, nearest-centroid, patch-attention** — Evaluates at most 4 configured candidates against a nearest-centroid baseline, choosing by test accuracy with deterministic tie-breaks.
- **Seven-stage AutoResearch pipeline with file-backed ledgers** — Runs 7 configured stages, writing proposal, candidate, run, phase and review ledgers that hydrate manuscript variables.
- **Safety controls: proposal-only autonomy, no LLM calls, deferred review** — Defaults to proposal_only autonomy, records 0 LLM calls and no cost, never executes generated code, and leaves publication approval to a human.
- **Statistical diagnostics: Wilson intervals, bootstrap, McNemar, calibration** — Reports Wilson score intervals, deterministic bootstrap intervals, paired discordance tests, Brier score and negative log likelihood.

## Key Findings

Core contributions and results:

- The loop selected exp-mlp-tanh-64 after evaluating 4 of 5 proposed candidates, raising test accuracy from the 82.6% baseline to 89.4%.
- Diagnostics report macro F1 of 89.4%, a bootstrap accuracy interval of 86.4% to 92.0%, and top-2 accuracy of 95.6%.
- The selected candidate was top-ranked in 72.5% of deterministic bootstrap resamples, with exp-mlp-relu-32 as runner-up.
- The local security attestation passed with 0 checksum mismatches, and readiness passed with review gates deferred to a human.
- The paper states its contribution is not a new MNIST classifier but a template showing bounded AutoResearch run through a reproducible-paper lifecycle.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2023_NSFReporting](../2023_NSFReporting/)
- [2023_NaturalAIBased](../2023_NaturalAIBased/)
- [2025_AuBI](../2025_AuBI/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.20417016
- PDF SHA-256: e07b62850a1995935283d37a45c21d71fa7c4e69cdcc451c5a1ea8aee6d0c94a
- Pairing confidence: strong
- Last checked: 2026-09-24T18:29:54Z

## Prerequisites

- Familiarity with autoresearch, reproducible research, machine learning benchmark
- Background in Computational fundamentals
- Access to source repository: docxology/template_autoresearch_project

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.20417016`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
