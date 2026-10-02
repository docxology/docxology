<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 🧠 Federated inference and belief sharing

**Karl J. Friston, Thomas Parr, Conor Heins, Axel Constant, Daniel Friedman, Takuya Isomura, Chris Fields, Tim Verbelen, Maxwell Ramstead, John Clippinger, Christopher D. Frith** (2024) · *Neuroscience & Biobehavioral Reviews*

[![DOI](https://img.shields.io/badge/DOI-10.1016%2Fj.neubiorev.2023.105500-blue)](https://doi.org/10.1016/j.neubiorev.2023.105500)

---

## Abstract

> This paper concerns the distributed intelligence or federated inference that emerges under belief-sharing among agents who share a common world—and world model. Imagine, for example, several animals keeping a lookout for predators. Their collective surveillance rests upon being able to communicate their beliefs—about what they see—among themselves. But, how is this possible? Here, we show how all the necessary components arise from minimising free energy. We use numerical studies to simulate the generation, acquisition and emergence of language in synthetic agents. Specifically, we consider inference, learning and selection as minimising the variational free energy of posterior (i.e., Bayesian) beliefs about the states, parameters and structure of generative models, respectively. The common theme—that attends these optimisation processes—is the selection of actions that minimise expected free energy, leading to active inference, learning and model selection (a.k.a., structure learning). We first illustrate the role of communication in resolving uncertainty about the latent states of a partially observed world, on which agents have complementary perspectives. We then consider the acquisition of the requisite language—entailed by a likelihood mapping from an agent’s beliefs to their overt expression (e.g., speech)—showing that language can be transmitted across generations by active learning. Finally, we show that language is an emergent property of free energy minimisation, when agents operate within the same econiche. We conclude with a discussion of various perspectives on these phenomena; ranging from cultural niche construction, through federated learning, to the emergence of complexity in ensembles of self-organising systems.

## Keywords

`federated inference` · `belief sharing` · `Active Inference` · `distributed intelligence` · `multi-agent systems` · `message passing` · `collective cognition` · `privacy-preserving inference`

## Methods

- **Numerical simulations of language generation, acquisition and emergence** — Synthetic agents are simulated to study belief-sharing, with inference, learning and selection cast as minimising variational free energy over states, parameters and structure.
- **Discrete-state generative model of three sentinels observing a subject** — Three agents with complementary views share a model with location, proximity, pose and gaze factors, four visual, one proprioceptive and three auditory modalities.
- **With/without-communication comparison via zero-precision auditory mappings** — Communication is ablated by reducing auditory likelihood precision so agents can neither generate nor recognise auditory cues.
- **Active learning of Dirichlet counts and structure learning via Bayesian model reduction** — Language acquisition uses accumulation of Dirichlet counts; emergence uses structure learning updating priors over Dirichlet counts with Bayesian model reduction.
- **SPM Matlab routines (spm_MDP_VB_XXX.m) for belief updating** — Generic belief updates were implemented with standard SPM academic software routines.

## Key Findings

- With communication, the third agent resolved uncertainty about the subject's location by the third epoch, versus only after seeing it at the fifth epoch without communication.
- In the generational simulation, children's learned auditory mappings were almost identical to their parents' after four generations, acquired solely through active learning.
- Three language-naive agents exposed to 512 episodes converged on shared mappings in which nearly every hidden state became associated with a unique shared 'word'.
- A novice lacking precise visual mappings learned, from hearing supervisors, a visual mapping making her inferences indistinguishable from theirs by about 64 exposures.
- The authors state two technical contributions: belief-sharing among agents with different vantage points, and a belief-updating procedure for learning and model selection.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.1016/j.neubiorev.2023.105500](https://doi.org/10.1016/j.neubiorev.2023.105500)
- PDF: [2024_FederatedInference.pdf](2024_FederatedInference.pdf)
- PDF SHA-256: Not recorded

## Citation

> Karl J. Friston, Thomas Parr, Conor Heins, Axel Constant, Daniel Friedman, Takuya Isomura, Chris Fields, Tim Verbelen, Maxwell Ramstead, John Clippinger, Christopher D. Frith (2024). *Federated inference and belief sharing*. Neuroscience & Biobehavioral Reviews. DOI: 10.1016/j.neubiorev.2023.105500. URL: https://doi.org/10.1016/j.neubiorev.2023.105500.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
