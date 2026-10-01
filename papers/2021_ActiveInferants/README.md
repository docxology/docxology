<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 🐜 Active Inferants: An Active Inference Framework for Ant Colony Behavior

**Daniel Ari Friedman, Alec Tschantz, Maxwell J. D. Ramstead, Karl Friston, Axel Constant** (2021) · *Frontiers in Behavioral Neuroscience*

[![DOI](https://img.shields.io/badge/DOI-10.3389%2Ffnbeh.2021.647732-blue)](https://doi.org/10.3389/fnbeh.2021.647732)

---

## Abstract

> In this paper, we introduce an active inference model of ant colony foraging behavior, and implement the model in a series of in silico experiments. Active inference is a multiscale approach to behavioral modeling that is being applied across settings in theoretical biology and ethology. The ant colony is a classic case system in the function of distributed systems in terms of stigmergic...

## Keywords

`active inference` · `ant foraging` · `Markov decision process` · `stigmergy` · `T-maze` · `collective behavior` · `behavioral modeling` · `eco-evo-devo`

## Methods

- **Per-forager MDP formulation of active inference** — Each simulated ant forager runs its own Markov decision process with A (likelihood), B (transition), and C (pheromone preference) components; the colony is not modelled as one agent.
- **In silico alternating T-maze foraging paradigm** — Simulated colonies search a T-maze in which the food patch switches arm every 500 of 2,000 time steps, with a decaying attractant trail pheromone.
- **Inbound-only trail pheromone deposition rule** — Foragers lay attractant pheromone only after finding food and returning to the nest, a strategy modelled on Formica red wood ants.
- **Simulations of colony sizes 10, 30, 50, and 70 foragers** — Ran 2,000-step simulations at four colony sizes and tracked round trips and a mean Euclidean inter-ant distance coefficient as colony-level phenotypes.

## Key Findings

- Colonies of foragers with no internal map of the T-maze foraged successfully using local pheromone-following and return-trip deposition rules.
- Colony size influenced per-nestmate round trips, apparently non-linearly, though the authors draw no generalization because key parameters were not varied.
- Each colony size quickly converged onto a characteristic range of the inter-ant distance metric.
- The model recovered basic colony phenomena such as trail formation after food discovery in the T-maze paradigm.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.3389/fnbeh.2021.647732](https://doi.org/10.3389/fnbeh.2021.647732)
- PDF: [2021_ActiveInferants.pdf](2021_ActiveInferants.pdf)
- PDF SHA-256: Not recorded

## Citation

> Daniel Ari Friedman, Alec Tschantz, Maxwell J. D. Ramstead, Karl Friston, Axel Constant (2021). *Active Inferants: An Active Inference Framework for Ant Colony Behavior*. Frontiers in Behavioral Neuroscience. DOI: 10.3389/fnbeh.2021.647732. URL: https://doi.org/10.3389/fnbeh.2021.647732.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
