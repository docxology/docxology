---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "A variational synthesis of evolutionary and developmental dynamics"
description: "This paper introduces a variational formulation of natural selection, using the Bayesian mechanics of particular partitions to understand how slow phylogenetic processes constrain fast phenotypic processes. The main result is a formulation of adaptiv..."
tags: ["variational-synthesis", "natural-selection", "free-energy-principle", "bayesian-mechanics", "path-integral", "evo-devo", "adaptive-fitness", "particular-partition"]
domain: "Active Inference"
citation: "Karl Friston, Daniel A. Friedman, Axel Constant, V. Bleu Knight, Chris Fields, Thomas Parr, John O. Campbell (2023). *A variational synthesis of evolutionary and developmental dynamics*. Entropy."
doi: "10.3390/e25070964"
---

# A variational synthesis of evolutionary and developmental dynamics

**Karl Friston, Daniel A. Friedman, Axel Constant, V. Bleu Knight, Chris Fields, Thomas Parr, John O. Campbell** (2023) · Active Inference

## Context

This work addresses topics in **Active Inference**: variational synthesis, natural selection, Free Energy Principle, Bayesian mechanics.

## Methods

Primary methods and techniques applied in this work:

- **Bayesian mechanics of particular partitions (free energy principle)** — Particular partitions are used to analyze how slow phylogenetic processes constrain and are constrained by fast phenotypic processes.
- **Two coupled random dynamical systems linked by a renormalisation group** — Phylogenetic and phenotypic processes are modelled as two random dynamical systems coupled via renormalisation-group reduction and grouping operators.
- **Variational recipe: Bayesian filtering plus stochastic gradient descent on action** — A four-step protocol samples particles, finds least-action paths by generalised Bayesian filtering, scores the free-energy path integral, and updates parameters.
- **Numerical simulation of synaptic selection in a single neuron** — A single dendrite with 20 synapses over five segments was simulated over 64 cycles, with synapses eliminated via Bayesian model reduction on synaptic precision.

## Key Findings

Core contributions and results:

- The main result is a formulation of adaptive fitness as a path integral of phenotypic fitness, with least-action paths read as inference (phenotypic) and learning (phylogenetic).
- The synthesis implies that a population of conspecifics cannot be modelled per se; one must consider populations of distinct natural kinds that influence each other.
- Genotype and phenotype fitness are both selected through minimisation of the same free energy functional (Bayesian model evidence).
- In the synaptic-selection simulation, free energy progressively decreased at the slow timescale as synapses enabling the cell to predict its inputs were selected.
- The authors caution that the account is limited to mathematical apparatus, is not a process theory, and did not examine when the variational fitness lemma holds.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2018_WoodliceAndMen](../2018_WoodliceAndMen/)
- [2020_BehaviorEngineering](../2020_BehaviorEngineering/)
- [2021_ModelingConflict](../2021_ModelingConflict/)

## Validation

Verification points for this work:

- Canonical DOI: 10.3390/e25070964
- PDF SHA-256: See zenodo_record
- Pairing confidence: unknown
- Last checked: 2026-07-01T20:50:01Z

## Prerequisites

- Familiarity with variational synthesis, natural selection, Free Energy Principle
- Background in Active Inference fundamentals
- Access to source repository: N/A

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.3390/e25070964`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
