---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "Sortition Upstream of NTQR"
description: "How should you choose the judges, jurors, or reviewers who form a panel — and does that upstream choice change how well you can evaluate them without an answer key? A panel can be selected many ways — by competence, by a representative lottery (sorti..."
tags: ["sortition", "ntqr", "unlabeled-evaluation", "expert-panels", "peer-review", "error-independence", "statistical-power", "panel-formation", "synthetic-evaluation", "llm-reviewers"]
domain: "Computational"
citation: "Daniel Ari Friedman (2026). *Sortition Upstream of NTQR*. Zenodo."
doi: "10.5281/zenodo.21083779"
---

# Sortition Upstream of NTQR

**Daniel Ari Friedman** (2026) · Computational

## Context

This work addresses topics in **Computational**: sortition, NTQR, unlabeled evaluation, expert panels.

## Methods

Primary methods and techniques applied in this work:

- **Seeded synthetic panel instrument scored against a known oracle** — Generates synthetic expert populations and corpora, forms panels, runs the ntqr evaluator without labels, and scores its estimate against the supervised oracle.
- **Four panel-formation strategies compared** — Compares representative sortition, uniform random selection, single-bloc ideological selection, and competence-first expertise thresholding.
- **ntqr error-independent (EIE) evaluator over judge trios** — Uses the ntqr package's exact three-judge EIE solver for no-answer-key evaluation, treating larger panels as ensembles of trios; recovery error is an L1-style distance to the oracle.
- **Gaussian-copula composition-coupled error confound** — Injects shared latent shocks among same-group judges via a Gaussian copula on probit-thresholded competence, preserving marginal accuracy while tuning cross-judge error correlation.
- **Live gemma3:4b reviewer-panel companion and five pre-stated hypotheses** — Tests transfer (H5) with one local Ollama gemma3:4b model prompted as postdoctoral reviewers on fictitious applications; H1-H4 tested on the synthetic track.

## Key Findings

Core contributions and results:

- Formation rule, not panel size, was the dominant lever: competence-first selection had the lowest recovery error (0.037), while the other three strategies clustered around 0.147-0.148.
- With a composition-coupled error confound, single-bloc error exceeded representative error in 180/205 matched regimes, the gap widening from 0.000 to 0.112 as coupling rose.
- Recovery error tracks the panel's Herfindahl concentration over the axis the shared error rides on; re-keying the confound to an unbalanced axis erased the protection (0.147 to 0.229).
- Increasing panel size from three to six seats produced at most tiny increases in error (largest +0.015), so size was essentially neutral.
- H5 was rejected: with the live gemma3:4b panel, the synthetically best expertise-threshold rule was the worst (0.347), which the author frames as a hypothesis to test beyond one model.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2023_NSFReporting](../2023_NSFReporting/)
- [2023_NaturalAIBased](../2023_NaturalAIBased/)
- [2025_AuBI](../2025_AuBI/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.21083779
- PDF SHA-256: See zenodo_record
- Pairing confidence: strong
- Last checked: 2026-09-24T18:29:57Z

## Prerequisites

- Familiarity with sortition, NTQR, unlabeled evaluation
- Background in Computational fundamentals
- Access to source repository: docxology/ntqr_allotment

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.21083779`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
