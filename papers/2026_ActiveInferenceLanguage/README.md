# Active Inference Language Model: A Fully Explicit Discrete Language System and a Gate-Audit Method

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22409418.svg)](https://doi.org/10.5281/zenodo.22409418)

---

## Abstract

Language offers a testbed for cognitive models that connect uncertain perception, structured representations and goal-directed action. AILM (Active Inference Language Model) explores this connection through explicit discrete generative models implemented in pymdp. Its six linguistic levels represent letters, phonemes, words, case roles, sentence types and document position. Conditional probabilities, preferences, habits and policy precision have declared meanings and inspectable parameter sources. AILM provides a bounded alternative to learned embedding representations for studying specified linguistic mechanisms, and a potential complement to the broader predictive capabilities of large language models. Its generative core uses no transformer, neural network or learned embedding. Generalized Notation Notation (GNN) specifies the models; pymdp executes their inference and, only on the generation path, selects policies under expected free energy. A connected runtime exchanges conditional messages and supports next-word policy selection. This composition does not establish a globally exact posterior, and the letter generator's expected-free-energy rule reduces to a preference-weighted softmax over the habit. These explicit mechanisms are candidates for cognitive investigation, not evidence of human-like understanding. On a locally frozen Georgetown University Multilayer (GUM) corpus population, the connected comparison indicates lower integrated loss than disabling the named channels while retaining the same train-fitted observation encoder. This result concerns normalized letters and token spaces; full-stream closed-vocabulary word loss remains infinite because out-of-vocabulary tokens receive zero word probability. The comparison is local evidence for a fixed composition, not external replication or unrestricted language competence. Separate component and intervention studies show that linguistic messages can help or harm a receiver; different insertion sites constrain their attribution. The accompanying gate-audit method compares thresholds with trivial baselines, typed comparators and deliberately broken variants, and binds numerical results to recorded runs through a claims ledger. Historical gates were largely repaired after construction, and held-back findings retain their stated task and uncertainty limits. The contribution is an inspectable platform for testing linguistic inference mechanisms together with an audit method that makes their failures visible. External neural models serve as supplemental reference probes; integration with them remains a proposal.

## Keywords

active inference · Generalized Notation Notation · GNN · pymdp · discrete state space · language model · computational linguistics · hidden Markov model · gate audit · reproducibility

## Artifacts

| Field | Value |
|------|-------|
| **DOI** | [10.5281/zenodo.22409418](https://doi.org/10.5281/zenodo.22409418) |
| **Published** | 2026-10-30 |
| **Version** | 1.0.0 |
| **Zenodo record** | https://zenodo.org/records/22409418 |
| **GitHub release** | https://github.com/ActiveInferenceInstitute/active_inference_language_model/releases/tag/v1.0.0 |
| **Source repository** | https://github.com/ActiveInferenceInstitute/active_inference_language_model |

## Files

- `Active_Inference_Language_Model_1.0.0.pdf` - Zenodo PDF

## Citation

> Friedman, D. A. (2026). *Active Inference Language Model: A Fully Explicit Discrete Language System and a Gate-Audit Method*. Zenodo. DOI: 10.5281/zenodo.22409418. URL: https://doi.org/10.5281/zenodo.22409418.

## Related

- Zenodo record: https://zenodo.org/records/22409418
- GitHub release: https://github.com/ActiveInferenceInstitute/active_inference_language_model/releases/tag/v1.0.0
- Source repository: https://github.com/ActiveInferenceInstitute/active_inference_language_model
- [Full Bibliography](../../pages/BIBLIOGRAPHY.md) · [All Papers](../README.md)
