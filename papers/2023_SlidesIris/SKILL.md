---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "Slides for Iris"
description: "Some initial slides from today. For context see:&nbsp;@speakerjohnash"
tags: ["slidesiris"]
domain: "Active Inference"
citation: "Daniel Ari Friedman (2023). *Slides for Iris*. Zenodo."
doi: "10.5281/zenodo.7838652"
artifact_doi: "10.5281/zenodo.7838653"
---

# Slides for Iris

**Daniel Ari Friedman** (2023) · Active Inference

## Context

This work addresses topics in **Active Inference**: SlidesIris.

## Methods

Primary methods and techniques applied in this work:

- **Active Inference generative model drawn as a Bayesian graph** — The slides open with a labelled graph of the A, B, C, D, E, G and policy terms of an Active Inference generative model as the reference frame.
- **Mapping GPT onto a minimal prior/state/observation model** — A reduced D-s-o model is used to describe what GPT does: prior as training set and parameters, latent semantic state, and word strings as observations.
- **Perceptual-inference extension with a transition matrix B** — Temporal dynamics are added via the perceptual inference part of Active Inference, with hidden states changing over time and no action selection.
- **Renormalization-group model of nested attention (Friston et al. 2023)** — A figure from Friston, Friedman et al. 2023 is reused to sketch how speakers, groups and sets of groups could be modelled as nested attention.

## Key Findings

Core contributions and results:

- The slides identify that in the GPT framing the latent semantic state is not separated by speaker, so speakers are admixed and cannot be weighted or attended to differentially.
- Reusing a renormalization-group figure from Friston, Friedman et al. 2023, the slides sketch speaker attention as a portfolio (regime) of nested attentions at all levels.
- Listed next steps are adding visualizations/dashboards, specifying the model in GNN toward implementation, and adding an action component.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2018_WoodliceAndMen](../2018_WoodliceAndMen/)
- [2020_BehaviorEngineering](../2020_BehaviorEngineering/)
- [2021_ModelingConflict](../2021_ModelingConflict/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.7838652
- PDF SHA-256: See zenodo_record
- Pairing confidence: unknown
- Last checked: 2026-05-30T18:56:22Z
- Artifact DOI: 10.5281/zenodo.7838653

## Prerequisites

- Familiarity with SlidesIris
- Background in Active Inference fundamentals
- Access to source repository: N/A

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.7838652`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
