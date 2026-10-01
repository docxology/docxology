---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "A Deterministic Testbed for Self-Organizing Agent-Team Coordination"
description: "Recent work on AutoScientists coordinates self-organizing teams of language-model agents through a small set of shared mechanisms: a champion-and-experiment-log shared state, a registry of retired dead-end directions, effect-size ranking of candidate..."
tags: ["agent-coordination", "scientific-discovery", "noise-band-confirmation", "ablation-study", "reproducible-research", "language-model-agents"]
domain: "Computational"
citation: "Daniel Ari Friedman (2026). *A Deterministic Testbed for Self-Organizing Agent-Team Coordination*. Zenodo."
doi: "10.5281/zenodo.20533669"
---

# A Deterministic Testbed for Self-Organizing Agent-Team Coordination

**Daniel Ari Friedman** (2026) · Computational

## Context

This work addresses topics in **Computational**: agent coordination, scientific discovery, noise-band confirmation, ablation study.

## Methods

Primary methods and techniques applied in this work:

- **Deterministic re-implementation of AutoScientists coordination mechanisms** — Re-implements AutoScientists' mechanisms (confirmation, dead-end registry, effect-size ranking, reorganization, team partitioning) as individually switchable modules.
- **Synthetic rippled quadratic objective with seeded noise (d=4)** — Optimizes a 4-D objective with a global peak at the origin, cosine ripples and seeded bounded noise, allowing reported vs clean metric comparison.
- **Matched 60-experiment sequential budget vs single-thread baseline** — Coordinated teams partition the same sequential budget as a single-thread baseline rather than adding parallel compute.
- **One-at-a-time per-mechanism ablation via SearchConfig** — Starts from the full coordinated configuration and switches off exactly one mechanism per ablation run.
- **Pluggable Proposer: deterministic rule-based vs Hermes LLM via Ollama** — Figures use a rule-based DeterministicProposer; a HermesProposer served by Ollama can be swapped in and is tested only by an opt-in test.

## Key Findings

Core contributions and results:

- Under the matched budget, coordinated teams and the baseline reach the same clean optimum (advantage 0.0000); coordination was slightly slower to first reach it (16 vs 12 experiments).
- Noise-band confirmation reduced accepted noise roughly 13-fold (reported-vs-clean gap 0.01565 to 0.00121) on this objective.
- The dead-end registry cut redundant re-probes from 36 to 0 and let the search halt at 36 rather than 60 experiments, with the clean answer unchanged.
- Effect-size ranking and reorganization did not change any measured quantity on this objective.
- The author cautions that these magnitudes are properties of this synthetic objective, budget and deterministic proposer, not general constants.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2023_NSFReporting](../2023_NSFReporting/)
- [2023_NaturalAIBased](../2023_NaturalAIBased/)
- [2025_AuBI](../2025_AuBI/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.20533669
- PDF SHA-256: 0af391375b14eb397812a8050657e2980fbc3a768e6fb108aa2f7eff46773e16
- Pairing confidence: strong
- Last checked: 2026-09-24T18:29:55Z

## Prerequisites

- Familiarity with agent coordination, scientific discovery, noise-band confirmation
- Background in Computational fundamentals
- Access to source repository: docxology/template_autoscientists

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.20533669`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
