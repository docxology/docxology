# Skillarum: Conditionally Reproducible Website-to-Agent-Skill Compilation

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22663906.svg)](https://doi.org/10.5281/zenodo.22663906)

---

## Abstract

Skillarum turns selected public website pages into portable SKILL.md documents for agent harnesses such as Codex, Claude Code, and Hermes. Work is separated into five inspectable stages: acquire, prepare, process, parse, and render. The crawler restricts acquisition to configured HTTP(S) origins, honours robots.txt, validates redirects, and records provenance for every page. Source text is delimited as untrusted data for LLM generation; generated code is never executed. The deterministic backend is offline and source-extractive; optional OpenAI and Ollama backends provide provider generation with typed fallback traces. Rendered skills carry provenance manifests, and an evidence-gated research package aggregates run observations into descriptive statistics, figures, and a scholarly manuscript. This release pairs the software source snapshot with the companion manuscript PDF.

## Keywords

website extraction · agent skills · provenance · reproducibility · prompt injection · static compilation

## Artifacts

| Field | Value |
|------|-------|
| **DOI** | [10.5281/zenodo.22663906](https://doi.org/10.5281/zenodo.22663906) |
| **Published** | 2026-09-08 |
| **Version** | 0.2.0 |
| **Zenodo record** | https://zenodo.org/records/22663906 |
| **GitHub release** | https://github.com/docxology/Skillarum/releases/tag/v0.2.0 |
| **Source repository** | https://github.com/docxology/Skillarum |

## Files

- `Skillarum_combined.pdf` - Zenodo PDF

## Citation

> Friedman, D. A. (2026). *Skillarum: Conditionally Reproducible Website-to-Agent-Skill Compilation*. Zenodo. DOI: 10.5281/zenodo.22663906. URL: https://doi.org/10.5281/zenodo.22663906.

## Related

- Zenodo record: https://zenodo.org/records/22663906
- GitHub release: https://github.com/docxology/Skillarum/releases/tag/v0.2.0
- Source repository: https://github.com/docxology/Skillarum
- [Full Bibliography](../../pages/BIBLIOGRAPHY.md) · [All Papers](../README.md)
