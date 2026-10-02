<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 A Deterministic Testbed for Self-Organizing Agent-Team Coordination

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20533669-blue)](https://doi.org/10.5281/zenodo.20533669)

---

## Abstract

> Recent work on AutoScientists coordinates self-organizing teams of language-model agents through a small set of shared mechanisms: a champion-and-experiment-log shared state, a registry of retired dead-end directions, effect-size ranking of candidate directions, noise-band confirmation of claimed improvements, and stagnation-driven reorganization of teams. This exemplar provides a deterministic, standalone reference implementation of those mechanisms and studies them honestly as a testbed rather than as a performance claim.
>
> We make the comparison fair by holding the total number of objective evaluations fixed: coordinated teams partition a single sequential experiment budget rather than adding parallel compute. Under that matched budget, coordination cannot — and in our results does not — beat a single-thread baseline on the final champion metric; we report the actual numbers and claim no speedup. What the testbed does demonstrate are two distinct, independently measurable benefits. First, noise-robustness: because the objective is stochastic, a single observed gain can be a draw of evaluation noise, so we separate the reported champion metric from the clean noise-free ground truth and show that noise-band confirmation shrinks the gap between them by roughly an order of magnitude — with confirmation on, the final champion's reported metric sits $0.0012$ above its clean value, against $0.0156$ with confirmation removed, while every configuration reaches the same clean optimum. Second, search hygiene: the dead-end registry, consulted by the proposer, cuts redundant re-probes of retired directions from $36$ to $0$ and halts at $36$ of the $60$ experiments — the same clean answer, reached with less waste. A per-mechanism ablation isolates each component's contribution, and the language-model proposer is a clean plug-in seam: a deterministic rule-based agent drives the reproducible figures, and a live Hermes agent (served by Ollama) can be swapped in without touching the coordination loop.

## Keywords

`agent coordination` · `scientific discovery` · `noise-band confirmation` · `ablation study` · `reproducible research` · `language-model agents`

## Methods

- **Deterministic re-implementation of AutoScientists coordination mechanisms** — Re-implements AutoScientists' mechanisms (confirmation, dead-end registry, effect-size ranking, reorganization, team partitioning) as individually switchable modules.
- **Synthetic rippled quadratic objective with seeded noise (d=4)** — Optimizes a 4-D objective with a global peak at the origin, cosine ripples and seeded bounded noise, allowing reported vs clean metric comparison.
- **Matched 60-experiment sequential budget vs single-thread baseline** — Coordinated teams partition the same sequential budget as a single-thread baseline rather than adding parallel compute.
- **One-at-a-time per-mechanism ablation via SearchConfig** — Starts from the full coordinated configuration and switches off exactly one mechanism per ablation run.
- **Pluggable Proposer: deterministic rule-based vs Hermes LLM via Ollama** — Figures use a rule-based DeterministicProposer; a HermesProposer served by Ollama can be swapped in and is tested only by an opt-in test.

## Key Findings

- Under the matched budget, coordinated teams and the baseline reach the same clean optimum (advantage 0.0000); coordination was slightly slower to first reach it (16 vs 12 experiments).
- Noise-band confirmation reduced accepted noise roughly 13-fold (reported-vs-clean gap 0.01565 to 0.00121) on this objective.
- The dead-end registry cut redundant re-probes from 36 to 0 and let the search halt at 36 rather than 60 experiments, with the clean answer unchanged.
- Effect-size ranking and reorganization did not change any measured quantity on this objective.
- The author cautions that these magnitudes are properties of this synthetic objective, budget and deterministic proposer, not general constants.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [docxology/template_autoscientists](https://github.com/docxology/template_autoscientists)
- GitHub release: [v1.0.2](https://github.com/docxology/template_autoscientists/releases/tag/v1.0.2)
- DOI: [10.5281/zenodo.20533669](https://doi.org/10.5281/zenodo.20533669)
- Zenodo record: [https://zenodo.org/records/20533669](https://zenodo.org/records/20533669)
- PDF: [Friedman_2026_Deterministic_0af39137.pdf](Friedman_2026_Deterministic_0af39137.pdf)
- PDF: [Friedman_2026_Deterministic_972bc4e0.pdf](Friedman_2026_Deterministic_972bc4e0.pdf)
- PDF: [Friedman_2026_Deterministic_a7f202bb.pdf](Friedman_2026_Deterministic_a7f202bb.pdf)
- PDF SHA-256: 0af391375b14eb397812a8050657e2980fbc3a768e6fb108aa2f7eff46773e16

## Citation

> Daniel Ari Friedman (2026). *A Deterministic Testbed for Self-Organizing Agent-Team Coordination*. Zenodo. DOI: 10.5281/zenodo.20533669. URL: https://doi.org/10.5281/zenodo.20533669.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
