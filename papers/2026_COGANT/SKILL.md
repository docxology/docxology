---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "COGANT: Deterministic Codebase-to-GNN Translation"
description: "COGANT (Codebase-to-GNN Translation) deterministically converts software repositories into structured Active Inference artifacts expressed in the Active Inference Institute's Generalized Notation Notation (GNN). It is an evidence compiler: it propaga..."
tags: ["program-analysis", "generalized-notation-notation", "gnn", "intermediate-representation", "code-property-graph", "active-inference", "reproducible-research", "codebase-to-model-translation", "cognitive-ecosystem-modeling"]
domain: "Computational"
citation: "Daniel Ari Friedman (2026). *COGANT: Deterministic Codebase-to-GNN Translation*. Zenodo."
doi: "10.5281/zenodo.20705350"
artifact_doi: "10.5281/zenodo.20705351"
---

# COGANT: Deterministic Codebase-to-GNN Translation

**Daniel Ari Friedman** (2026) · Computational

## Context

This work addresses topics in **Computational**: program analysis, Generalized Notation Notation, GNN, intermediate representation.

## Methods

Primary methods and techniques applied in this work:

- **Program-graph IR with confidence and provenance on nodes and edges** — Repositories are parsed (primarily via Python's standard-library ast) into a program graph IR whose nodes and edges carry confidence and provenance.
- **Fixpoint translation engine with 22 declarative rules in five families** — Rules (structural, semantic, control, behavioural, resilience) map nodes to 7 Active Inference mapping kinds, with priority-and-score conflict resolution.
- **A/B/C/D matrix derivation and GNN (Generalized Notation Notation) export** — Derives likelihood, transition, preference and prior matrices from the compiled state space and program-graph edges, normalized for the upstream GNN validator.
- **Forward-reverse-forward roundtrip over a 25-target regression corpus** — A reverse synthesizer rebuilds a Python package from each GNN bundle; role_preservation_score and strict isomorphism are recorded per target.
- **Rule-family and fixpoint-iteration ablations on packaged fixtures** — Removes each rule family and varies the iteration cap K in {1, 2, 5, 10}, recording changes in SemanticMapping counts on the shipped fixtures.

## Key Findings

Core contributions and results:

- On the v0.6.0 roundtrip ledger, all 25 targets are role-preserved, but only 1 of 25 meets strict structural isomorphism.
- The author cautions that fixtures are in-sample, with no held-out split or confidence intervals, so scores upper-bound rather than estimate out-of-sample performance.
- The fixpoint ablation shows a single pass suffices on every shipped fixture, with the K=10 cap serving as a safety valve.
- Rule-family ablation indicates structural rules drive HIDDEN_STATE while semantic rules drive OBSERVATION/ACTION/POLICY/PREFERENCE roles.
- The author states the passing test suite, coverage and type-check gates support reliability and reproducibility but do not by themselves establish semantic adequacy.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2023_NSFReporting](../2023_NSFReporting/)
- [2023_NaturalAIBased](../2023_NaturalAIBased/)
- [2025_AuBI](../2025_AuBI/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.20705350
- PDF SHA-256: See zenodo_record
- Pairing confidence: strong
- Last checked: 2026-09-24T18:29:55Z
- Artifact DOI: 10.5281/zenodo.20705351

## Prerequisites

- Familiarity with program analysis, Generalized Notation Notation, GNN
- Background in Computational fundamentals
- Access to source repository: ActiveInferenceInstitute/COGANT

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.20705350`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
