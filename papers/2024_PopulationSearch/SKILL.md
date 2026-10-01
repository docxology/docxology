---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "Enhancing Population-based Search with Active Inference"
description: "We propose integrating Active Inference into population-based metaheuristics to enhance performance through anticipatory environmental adaptation. Demonstrated with Ant Colony Optimization (ACO) on the Travelling Salesman Problem (TSP), experimental ..."
tags: ["population-search", "active-inference", "ant-colony-optimization", "tsp", "metaheuristics", "anticipatory-adaptation", "computational-optimization"]
domain: "Active Inference"
citation: "Nassim Dehouche, Daniel Friedman (2024). *Enhancing Population-based Search with Active Inference*. ArXiv."
doi: "10.48550/arXiv.2408.09548"
---

# Enhancing Population-based Search with Active Inference

**Nassim Dehouche, Daniel Friedman** (2024) · Active Inference

## Context

This work addresses topics in **Active Inference**: population search, Active Inference, Ant Colony Optimization, TSP.

## Methods

Primary methods and techniques applied in this work:

- **Active Inference-augmented Ant Colony Optimization for the TSP** — ACO is extended with a belief-update mechanism and a free-energy calculation so ant node selection adapts to current tour quality.
- **Belief-weighted node selection and free-energy tour scoring** — Belief is set from current versus best path length, scales pheromone/distance selection probabilities, and enters a free energy of path length plus entropy.
- **Benchmark against basic ACO and Nearest Neighbor on random symmetric graphs** — The AI-enhanced ACO was compared to basic ACO and a Nearest Neighbor heuristic on randomly generated symmetric graphs of several sizes.
- **Paired t-test, Wilcoxon signed-rank, and Mann-Whitney U tests** — Tour length and computation time differences between basic and AI-enhanced ACO were assessed with paired and non-parametric tests.
- **Python implementation released with appendix code and GitHub repo** — Python implementations of all methods are given in the appendix, with extended ANOVA results in the haailabs/ActiveACO repository.

## Key Findings

Core contributions and results:

- The Active Inference-enhanced ACO gave mean tour-length improvements over basic ACO at every graph size tested, peaking at 8.81% for 100-node graphs.
- Relative computational overhead fell with graph size, from 9.46% at 25 nodes to 1.97% at 500 nodes.
- Tour-length improvements were significant by paired t-test and Wilcoxon test, but the Mann-Whitney U test found no significant difference in overall distributions.
- The computation-time difference was not statistically significant at the 0.05 level.
- The authors note high variability in tour lengths for both algorithms, with performance gains varying considerably across graph types.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2018_WoodliceAndMen](../2018_WoodliceAndMen/)
- [2020_BehaviorEngineering](../2020_BehaviorEngineering/)
- [2021_ModelingConflict](../2021_ModelingConflict/)

## Validation

Verification points for this work:

- Canonical DOI: 10.48550/arXiv.2408.09548
- PDF SHA-256: See zenodo_record
- Pairing confidence: unknown
- Last checked: 2026-07-01T20:50:01Z

## Prerequisites

- Familiarity with population search, Active Inference, Ant Colony Optimization
- Background in Active Inference fundamentals
- Access to source repository: N/A

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.48550/arXiv.2408.09548`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
