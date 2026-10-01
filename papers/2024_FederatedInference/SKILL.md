---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "Federated inference and belief sharing"
description: "This paper concerns the distributed intelligence or federated inference that emerges under belief-sharing among agents who share a common world—and world model. Imagine, for example, several animals keeping a lookout for predators. Their collective s..."
tags: ["federated-inference", "belief-sharing", "active-inference", "distributed-intelligence", "multi-agent-systems", "message-passing", "collective-cognition", "privacy-preserving-inference"]
domain: "Active Inference"
citation: "Karl J. Friston, Thomas Parr, Conor Heins, Axel Constant, Daniel Friedman, Takuya Isomura, Chris Fields, Tim Verbelen, Maxwell Ramstead, John Clippinger, Christopher D. Frith (2024). *Federated inference and belief sharing*. Neuroscience & Biobehavioral Reviews."
doi: "10.1016/j.neubiorev.2023.105500"
---

# Federated inference and belief sharing

**Karl J. Friston, Thomas Parr, Conor Heins, Axel Constant, Daniel Friedman, Takuya Isomura, Chris Fields, Tim Verbelen, Maxwell Ramstead, John Clippinger, Christopher D. Frith** (2024) · Active Inference

## Context

This work addresses topics in **Active Inference**: federated inference, belief sharing, Active Inference, distributed intelligence.

## Methods

Primary methods and techniques applied in this work:

- **Numerical simulations of language generation, acquisition and emergence** — Synthetic agents are simulated to study belief-sharing, with inference, learning and selection cast as minimising variational free energy over states, parameters and structure.
- **Discrete-state generative model of three sentinels observing a subject** — Three agents with complementary views share a model with location, proximity, pose and gaze factors, four visual, one proprioceptive and three auditory modalities.
- **With/without-communication comparison via zero-precision auditory mappings** — Communication is ablated by reducing auditory likelihood precision so agents can neither generate nor recognise auditory cues.
- **Active learning of Dirichlet counts and structure learning via Bayesian model reduction** — Language acquisition uses accumulation of Dirichlet counts; emergence uses structure learning updating priors over Dirichlet counts with Bayesian model reduction.
- **SPM Matlab routines (spm_MDP_VB_XXX.m) for belief updating** — Generic belief updates were implemented with standard SPM academic software routines.

## Key Findings

Core contributions and results:

- With communication, the third agent resolved uncertainty about the subject's location by the third epoch, versus only after seeing it at the fifth epoch without communication.
- In the generational simulation, children's learned auditory mappings were almost identical to their parents' after four generations, acquired solely through active learning.
- Three language-naive agents exposed to 512 episodes converged on shared mappings in which nearly every hidden state became associated with a unique shared 'word'.
- A novice lacking precise visual mappings learned, from hearing supervisors, a visual mapping making her inferences indistinguishable from theirs by about 64 exposures.
- The authors state two technical contributions: belief-sharing among agents with different vantage points, and a belief-updating procedure for learning and model selection.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2018_WoodliceAndMen](../2018_WoodliceAndMen/)
- [2020_BehaviorEngineering](../2020_BehaviorEngineering/)
- [2021_ModelingConflict](../2021_ModelingConflict/)

## Validation

Verification points for this work:

- Canonical DOI: 10.1016/j.neubiorev.2023.105500
- PDF SHA-256: See zenodo_record
- Pairing confidence: unknown
- Last checked: 2026-07-01T20:50:01Z

## Prerequisites

- Familiarity with federated inference, belief sharing, Active Inference
- Background in Active Inference fundamentals
- Access to source repository: N/A

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.1016/j.neubiorev.2023.105500`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
