<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 🧠 Enhancing Population-based Search with Active Inference

**Nassim Dehouche, Daniel Friedman** (2024) · *ArXiv*

[![DOI](https://img.shields.io/badge/DOI-10.48550%2FarXiv.2408.09548-blue)](https://doi.org/10.48550/arXiv.2408.09548)

---

## Abstract

> We propose integrating Active Inference into population-based metaheuristics to enhance performance through anticipatory environmental adaptation. Demonstrated with Ant Colony Optimization (ACO) on the Travelling Salesman Problem (TSP), experimental results indicate Active Inference yields improved solutions with marginal increase in computational cost, with performance patterns relating to graph topology.

## Keywords

`population search` · `Active Inference` · `Ant Colony Optimization` · `TSP` · `metaheuristics` · `anticipatory adaptation` · `computational optimization`

## Methods

- **Active Inference-augmented Ant Colony Optimization for the TSP** — ACO is extended with a belief-update mechanism and a free-energy calculation so ant node selection adapts to current tour quality.
- **Belief-weighted node selection and free-energy tour scoring** — Belief is set from current versus best path length, scales pheromone/distance selection probabilities, and enters a free energy of path length plus entropy.
- **Benchmark against basic ACO and Nearest Neighbor on random symmetric graphs** — The AI-enhanced ACO was compared to basic ACO and a Nearest Neighbor heuristic on randomly generated symmetric graphs of several sizes.
- **Paired t-test, Wilcoxon signed-rank, and Mann-Whitney U tests** — Tour length and computation time differences between basic and AI-enhanced ACO were assessed with paired and non-parametric tests.
- **Python implementation released with appendix code and GitHub repo** — Python implementations of all methods are given in the appendix, with extended ANOVA results in the haailabs/ActiveACO repository.

## Key Findings

- The Active Inference-enhanced ACO gave mean tour-length improvements over basic ACO at every graph size tested, peaking at 8.81% for 100-node graphs.
- Relative computational overhead fell with graph size, from 9.46% at 25 nodes to 1.97% at 500 nodes.
- Tour-length improvements were significant by paired t-test and Wilcoxon test, but the Mann-Whitney U test found no significant difference in overall distributions.
- The computation-time difference was not statistically significant at the 0.05 level.
- The authors note high variability in tour lengths for both algorithms, with performance gains varying considerably across graph types.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.48550/arXiv.2408.09548](https://doi.org/10.48550/arXiv.2408.09548)
- PDF: [2024_PopulationSearch.pdf](2024_PopulationSearch.pdf)
- PDF SHA-256: Not recorded

## Citation

> Nassim Dehouche, Daniel Friedman (2024). *Enhancing Population-based Search with Active Inference*. ArXiv. DOI: 10.48550/arXiv.2408.09548. URL: https://doi.org/10.48550/arXiv.2408.09548.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
