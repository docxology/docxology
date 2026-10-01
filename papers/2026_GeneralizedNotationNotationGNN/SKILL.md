---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "GeneralizedNotationNotation (GNN)"
description: "Active Inference offers a unifying account of perception, learning, and action under the free energy principle, yet the generative models at its core are still communicated ad hoc: scattered across prose descriptions, bespoke notebooks, and framework..."
tags: ["active-inference", "generative-models", "cognitive-modeling", "notation-system", "reproducibility", "computational-neuroscience", "bayesian-inference", "standards", "gnn", "python"]
domain: "Active Inference"
citation: "Daniel Ari Friedman (2026). *GeneralizedNotationNotation (GNN)*. Zenodo."
doi: "10.5281/zenodo.7803313"
artifact_doi: "10.5281/zenodo.22985529"
---

# GeneralizedNotationNotation (GNN)

**Daniel Ari Friedman** (2026) · Active Inference

## Context

This work addresses topics in **Active Inference**: active inference, generative models, cognitive modeling, notation system.

## Methods

Primary methods and techniques applied in this work:

- **Parsing and structured export** — Parses plain-text model specifications into an internal representation and structured export formats, retaining declared model vocabulary.
- **Model-kind type checking and validation** — Checks state spaces, observation modalities, control factors, matrix dimensions, and kind-specific shape contracts before code generation.
- **Kind-aware model rendering** — Carries structurally determined model kinds into rendering and execution, recording which backends can handle each kind and which report it unsupported.
- **Semantic fidelity and cross-framework gates** — Provides reproducible commands for testing semantic preservation in round trips and comparing generated model structure across backend implementations.

## Key Findings

Core contributions and results:

- The manuscript presents the Triple Play as text, graphical, and executable views derived from a shared model specification.
- At the manuscript snapshot, the framework covers 32 exemplar specifications across nine model families and ten registered rendering backends.
- The manuscript reports profiled execution gaps for continuous and hierarchical models, and a deliberate render-only scope for structural models; it does not claim that every model executes on every backend.
- The manuscript specifies reproducible validation commands and explicitly avoids asserting a fixed passing-check count.
- The manuscript describes long-running orchestration contracts that generate, validate, and replay data without mutating live infrastructure.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2018_WoodliceAndMen](../2018_WoodliceAndMen/)
- [2020_BehaviorEngineering](../2020_BehaviorEngineering/)
- [2021_ModelingConflict](../2021_ModelingConflict/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.7803313
- PDF SHA-256: acb7749c561b26562064421ca2f7fbca68c8b0e8a955082e5d5a3e28b50bd784
- Pairing confidence: unknown
- Last checked: 2026-10-01
- Artifact DOI: 10.5281/zenodo.22985529

## Prerequisites

- Familiarity with active inference, generative models, cognitive modeling
- Background in Active Inference fundamentals
- Access to source repository: ActiveInferenceInstitute/Generalized_Notation_Notation

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.7803313`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
