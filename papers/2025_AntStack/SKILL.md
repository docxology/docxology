---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "The Ant Stack"
description: "AntStack presents a multilevel framework for modeling ant colony organization, from molecular and neural processes at the individual scale through interaction networks to colony-level behavioral patte..."
tags: ["antstack", "multilevel-modeling", "ant-colonies", "social-insects", "multiscale-biology", "colony-organization"]
domain: "Entomology"
citation: "Daniel Ari Friedman (2025). *The Ant Stack*. Zenodo."
doi: "10.5281/zenodo.16782756"
---

# The Ant Stack

**Daniel Ari Friedman** (2025) · Entomology

## Context

This work addresses topics in **Entomology**: AntStack, multilevel modeling, ant colonies, social insects.

## Methods

Primary methods and techniques applied in this work:

- **AntBody: FlyBody MuJoCo simulator adapted to ant morphology** — The body layer adapts the FlyBody MuJoCo simulator to ant leg kinematics, exoskeleton and antennae/mandible actuation, portable to PyBullet.
- **Explicit Body–Brain I/O contract with fixed rates and SI units** — Specifies observations and actions at 100 Hz over a 1 ms physics step, with a latency budget and clock-drift bound.
- **AntBrain AL→MB→CX pipeline templated from fly/bee brains** — A functional neural abstraction templated from Drosophila/Apis via Virtual Fly Brain, with sparse Kenyon-cell coding, local plasticity and a ring-attractor CX.
- **AntMind minimal active-inference generative model** — A single-agent generative model over pose, heading, hunger and pheromone expectation, with variational free energy updates and short-horizon policy selection.
- **Diffusion–decay pheromone field for stigmergy** — Colony coordination via a grid pheromone field with decay λ, diffusion D and reward-linked deposits, which agents follow along the gradient.

## Key Findings

Core contributions and results:

- The paper presents the Ant Stack, a compact modular framework (AntBody, AntBrain, AntMind) intended to emulate an ant from physics to cognition.
- Stated contributions include an executable I/O contract between layers, a compact neural pipeline with local plasticity, and a minimal active-inference agent composing via stigmergy.
- The work specifies (rather than reports results from) evaluation suites for navigation, trail following, task allocation and robustness under noise/adversaries.
- The author states that no high-fidelity ant brain emulation yet closes the loop with a realistic body at interactive rates.
- Stated limitations: no ant connectome (fly/bee templates used), simulation-first scope with embedded real-time operation as future work, and field validation still needed.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2016_AntGenetics](../2016_AntGenetics/)
- [2016_ForagingGene](../2016_ForagingGene/)
- [2017_MutAnts](../2017_MutAnts/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.16782756
- PDF SHA-256: See zenodo_record
- Pairing confidence: unknown
- Last checked: 2026-07-01T20:50:01Z

## Prerequisites

- Familiarity with AntStack, multilevel modeling, ant colonies
- Background in Entomology fundamentals
- Access to source repository: N/A

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.16782756`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
