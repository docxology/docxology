<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 Self-Improvement Agent Harness: A Deterministic SIA Exemplar

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20453879-blue)](https://doi.org/10.5281/zenodo.20453879)

---

## Abstract

> This exemplar documents template_sia, a deterministic implementation of the Self-Improvement Agent (SIA) harness contract described in the Self-Improvement Agents specification (Hexo AI, 2026, arXiv:2605.27276). The default pipeline replays fixture-backed generations for the mini_classify task; opt-in live mode runs bounded target subprocesses and optional Ollama-backed meta/feedback steps.
>
> Run snapshot. Task mini_classify, run 1, 3 generation(s), live=false. Final accuracy=0.8333 over 6 held-out samples. Values are injected by scripts/z_generate_manuscript_variables.py after analysis.
>
> Keywords: self-improvement agents, benchmark harness, reproducible evaluation, agent loops

## Keywords

`self-improvement agents` · `benchmark harness` · `reproducible research` · `agent evaluation`

## Methods

- **Meta -> Target -> Feedback three-agent SIA loop** — The harness cycles a meta agent that seeds a target agent, the target run on public data, and a feedback agent that reads private metrics to propose the next generation.
- **Public/private task split with deterministic reference baseline** — Each task separates agent-visible data and instructions from held-out evaluation labels, plus a deterministic reference target agent.
- **Fixture-replay determinism contract with opt-in live mode** — By default generations replay recorded fixtures so CI never runs generated code or calls LLM APIs; a flag enables bounded subprocess execution with optional Ollama feedback.
- **mini_classify single-feature threshold classifier task** — The bundled exemplar task is a threshold classifier on one feature column, evaluated over 3 generations on 6 held-out samples.

## Key Findings

- In the bundled fixture-replay run, final accuracy on mini_classify was 0.8333 over 6 held-out samples after 3 generations.
- Accuracy rose from the first to the final generation by a metric delta of 0.3333 in the fixture replay.
- template_sia shows the SIA harness contract can be embedded in the Research Project Template without vendoring upstream orchestration code, split into an infrastructure layer and a project layer.
- The author states the fixture-replay metrics validate wiring only and are not evidence of state-of-the-art self-improvement.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [docxology/template_sia](https://github.com/docxology/template_sia)
- GitHub release: [v0.1.2](https://github.com/docxology/template_sia/releases/tag/v0.1.2)
- DOI: [10.5281/zenodo.20453879](https://doi.org/10.5281/zenodo.20453879)
- Zenodo record: [https://zenodo.org/records/20453879](https://zenodo.org/records/20453879)
- PDF: [Friedman_2026_Selfimprovement_6e6d19d0.pdf](Friedman_2026_Selfimprovement_6e6d19d0.pdf)
- PDF: [Friedman_2026_Selfimprovement_7087b6d1.pdf](Friedman_2026_Selfimprovement_7087b6d1.pdf)
- PDF: [Friedman_2026_Selfimprovement_e350973a.pdf](Friedman_2026_Selfimprovement_e350973a.pdf)
- PDF SHA-256: 6e6d19d04182628bb825471cf8094b5c32d2c491d2c646652ec7e2439ba80773

## Citation

> Daniel Ari Friedman (2026). *Self-Improvement Agent Harness: A Deterministic SIA Exemplar*. Zenodo. DOI: 10.5281/zenodo.20453879. URL: https://doi.org/10.5281/zenodo.20453879.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
