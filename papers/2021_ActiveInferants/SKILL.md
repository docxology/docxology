---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "Active Inferants: An Active Inference Framework for Ant Colony Behavior"
description: "In this paper, we introduce an active inference model of ant colony foraging behavior, and implement the model in a series of in silico experiments. Active inference is a multiscale approach to behavi..."
tags: ["active-inference", "ant-foraging", "markov-decision-process", "stigmergy", "t-maze", "collective-behavior", "behavioral-modeling", "eco-evo-devo"]
domain: "Entomology"
citation: "Daniel Ari Friedman, Alec Tschantz, Maxwell J. D. Ramstead, Karl Friston, Axel Constant (2021). *Active Inferants: An Active Inference Framework for Ant Colony Behavior*. Frontiers in Behavioral Neuroscience."
doi: "10.3389/fnbeh.2021.647732"
---

# Active Inferants: An Active Inference Framework for Ant Colony Behavior

**Daniel Ari Friedman, Alec Tschantz, Maxwell J. D. Ramstead, Karl Friston, Axel Constant** (2021) · Entomology

## Context

This work addresses topics in **Entomology**: active inference, ant foraging, Markov decision process, stigmergy.

## Methods

Primary methods and techniques applied in this work:

- **Per-forager MDP formulation of active inference** — Each simulated ant forager runs its own Markov decision process with A (likelihood), B (transition), and C (pheromone preference) components; the colony is not modelled as one agent.
- **In silico alternating T-maze foraging paradigm** — Simulated colonies search a T-maze in which the food patch switches arm every 500 of 2,000 time steps, with a decaying attractant trail pheromone.
- **Inbound-only trail pheromone deposition rule** — Foragers lay attractant pheromone only after finding food and returning to the nest, a strategy modelled on Formica red wood ants.
- **Simulations of colony sizes 10, 30, 50, and 70 foragers** — Ran 2,000-step simulations at four colony sizes and tracked round trips and a mean Euclidean inter-ant distance coefficient as colony-level phenotypes.

## Key Findings

Core contributions and results:

- Colonies of foragers with no internal map of the T-maze foraged successfully using local pheromone-following and return-trip deposition rules.
- Colony size influenced per-nestmate round trips, apparently non-linearly, though the authors draw no generalization because key parameters were not varied.
- Each colony size quickly converged onto a characteristic range of the inter-ant distance metric.
- The model recovered basic colony phenomena such as trail formation after food discovery in the T-maze paradigm.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2016_AntGenetics](../2016_AntGenetics/)
- [2016_ForagingGene](../2016_ForagingGene/)
- [2017_MutAnts](../2017_MutAnts/)

## Validation

Verification points for this work:

- Canonical DOI: 10.3389/fnbeh.2021.647732
- PDF SHA-256: See zenodo_record
- Pairing confidence: unknown
- Last checked: 2026-07-01T20:50:01Z

## Prerequisites

- Familiarity with active inference, ant foraging, Markov decision process
- Background in Entomology fundamentals
- Access to source repository: N/A

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.3389/fnbeh.2021.647732`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
