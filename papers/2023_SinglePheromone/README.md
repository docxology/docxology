<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 🐜 A single-pheromone model accounts for empirical patterns of ant colony foraging

**Eric Saund, Daniel Ari Friedman** (2023) · *Cognitive Systems Research*

[![DOI](https://img.shields.io/badge/DOI-10.1016%2Fj.cogsys.2023.02.005-blue)](https://doi.org/10.1016/j.cogsys.2023.02.005)

---

## Abstract

> We present a computational model showing that a single pheromone accounts for empirical patterns of ant colony foraging previously modeled using two pheromones. Our model demonstrates that the dynamics of pheromone deposition, evaporation, and ant behavioral responses to concentration gradients can produce the full range of observed foraging patterns with a simpler single-pheromone mechanism.

## Keywords

`pheromone` · `ant foraging` · `computational model` · `collective behavior` · `stigmergy` · `trail formation` · `parsimony`

## Methods

- **Reanalysis of Dussutour et al. (2009) Pheidole megacephala Y-maze data** — Uses the published Y-maze branch-choice results (Experiments 1, 2 and 4) of Dussutour et al. as the empirical target; no new ant experiments were run.
- **One-pheromone model with exponential decay and power-law amplification** — Models a single attractant pheromone that decays exponentially and is perceived through a concave power-law sensory amplification minus a noise level.
- **Branch preference as a product of two sigmoid functions** — Choice probability is modeled as a product of logistic terms for the difference between branches and the overall signal robustness.
- **Manual fitting and L-BFGS-B optimization in Python/SciPy** — Parameters were set by manual adjustment, then optimized with SciPy's bounded L-BFGS-B minimizing squared error against values read from the original figures.
- **Simulation of the dynamic-environment food-switching experiment** — Simulated Experiment 4 with differing per-ant deposit rates on food vs no-food branches and total traffic around 50 ants per minute.

## Key Findings

- The main reported observations of Dussutour et al. can be explained by a one-pheromone model.
- A one-pheromone model accounts for equal initial E+F preference across conditions followed by divergence after about 15 minutes.
- The one-pheromone model also accounts for preference flipping in the dynamic-environment experiment, and one optimized parameter set fits both figures reasonably.
- The authors conclude that two pheromones are plausible but unnecessary, so the original study is not dispositive evidence for a two-pheromone model.
- The model predicts that with food on both branches traffic equalizes without the oscillation predicted by the two-pheromone model.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.1016/j.cogsys.2023.02.005](https://doi.org/10.1016/j.cogsys.2023.02.005)
- PDF: [2023_SinglePheromone.pdf](2023_SinglePheromone.pdf)
- PDF SHA-256: Not recorded

## Citation

> Eric Saund, Daniel Ari Friedman (2023). *A single-pheromone model accounts for empirical patterns of ant colony foraging*. Cognitive Systems Research. DOI: 10.1016/j.cogsys.2023.02.005. URL: https://doi.org/10.1016/j.cogsys.2023.02.005.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
