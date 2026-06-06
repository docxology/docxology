# A Deterministic Testbed for Self-Organizing Agent-Team Coordination

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20533670.svg)](https://doi.org/10.5281/zenodo.20533670)

---

## Abstract

Abstract

Recent work on AutoScientists  coordinates self-organizing teams of language-model agents through a small set of shared mechanisms: a champion-and-experiment-log shared state, a registry of retired dead-end directions, effect-size ranking of candidate directions, noise-band confirmation of claimed improvements, and stagnation-driven reorganization of teams. This exemplar provides a deterministic, standalone reference implementation of those mechanisms and studies them honestly as a testbed rather than as a performance claim.

We make the comparison fair by holding the total number of objective evaluations fixed: coordinated teams partition a single sequential experiment budget rather than adding parallel compute. Under that matched budget, coordination cannot — and in our results does not — beat a single-thread baseline on the final champion metric; we report the actual numbers and claim no speedup. What the testbed does demonstrate are two distinct, independently measurable benefits. First, noise-robustness: because the objective is stochastic, a single observed gain can be a draw of evaluation noise, so we separate the reported champion metric from the clean noise-free ground truth and show that noise-band confirmation shrinks the gap between them by roughly an order of magnitude — with confirmation on, the final champion's reported metric sits $0.0012$ above its clean value, against $0.0156$ with confirmation removed, while every configuration reaches the same clean optimum. Second, search hygiene: the dead-end registry, consulted by the proposer, cuts redundant re-probes of retired directions from $36$ to $0$ and halts at $36$ of the $60$ experiments — the same clean answer, reached with less waste. A per-mechanism ablation isolates each component's contribution, and the language-model proposer is a clean plug-in seam: a deterministic rule-based agent drives the reproducible figures, and a live Hermes agent (served by Ollama) can be swapped in without touching the coordination loop.

---
Associated artifacts
GitHub release: v1.0.0 (https://github.com/docxology/template_autoscientists/releases/tag/v1.0.0)
PDF SHA-256: a7f202bb1aa3c13803508e033c7561e6afe8b74148b60e9a3f91341ebfc21e65

## Keywords

agent coordination · scientific discovery · noise-band confirmation · ablation study · reproducible research · language-model agents

## Publication Details

| Field | Value |
|------|-------|
| **DOI** | [10.5281/zenodo.20533670](https://doi.org/10.5281/zenodo.20533670) |
| **Published** | 2026 |
| **Version** | 1.0.0 |
| **Zenodo record** | https://zenodo.org/records/20533670 |
| **GitHub release** | https://github.com/docxology/template_autoscientists/releases/tag/v1.0.0 |
| **Source repository** | https://github.com/docxology/template_autoscientists |

## Files

- `Friedman_2026_Deterministic_a7f202bb.pdf` - Zenodo PDF

## Citation

> Friedman, D. A. (2026). *A Deterministic Testbed for Self-Organizing Agent-Team Coordination*. Zenodo. https://doi.org/10.5281/zenodo.20533670

## Related

- Zenodo record: https://zenodo.org/records/20533670
- GitHub release: https://github.com/docxology/template_autoscientists/releases/tag/v1.0.0
- Source repository: https://github.com/docxology/template_autoscientists
- [Full Bibliography](../../pages/BIBLIOGRAPHY.md) · [All Papers](../README.md)
