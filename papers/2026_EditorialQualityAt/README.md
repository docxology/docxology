<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 Editorial Quality at Scale: A Reproducible Prose-Review Pipeline

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20417104-blue)](https://doi.org/10.5281/zenodo.20417104)

---

## Abstract

> This paper documents template_prose_project, the prose-focused exemplar of the Research Project Template (https://github.com/docxology/template). It pairs the template's two-layer architecture with the prose analysis infrastructure (https://github.com/docxology/template/tree/main/infrastructure/prose) (readability metrics, structural outline, editorial quality flags) and the reference validation...

## Keywords

`prose analysis` · `readability` · `editorial review` · `reproducible research` · `manuscript quality`

## Methods

- **Five-stage pure-function pipeline: read, analyse, cross-check, evaluate, render** — template_prose_project implements editorial review as five pure-function stages in src/, with scripts limited to argument parsing and I/O.
- **Readability metrics: Flesch Reading Ease, Flesch-Kincaid grade, Gunning Fog** — Per-file metrics are computed with textbook readability formulae over a vowel-group syllable heuristic.
- **Heuristic quality flags: passive voice, hedge density, citation density** — A quality analyser flags passive-voice candidates, hedge words, Pandoc [@key] citation density, and long sentences.
- **Citation-key cross-check against references.bib with configurable policy** — Every cited key is matched against the BibTeX file, with fail_on_missing / fail_on_unused settings in config.yaml.
- **Run-twice diff test for byte-identical JSON output** — Reproducibility is checked locally by running the pipeline twice and diffing manuscript_report.json.

## Key Findings

- The paper reports that editorial review can be expressed as a configurable, deterministic pipeline with no novel domain algorithm of its own.
- On the bundled manuscript, the run analysed 8 files totalling 1731 words, with average Flesch-Kincaid grade 15.87 and Gunning Fog 16.67.
- Because no external service is consulted, a second run on the same inputs produces byte-identical JSON (modulo timestamp metadata).
- The stated contribution is architectural: a reusable prose-quality module any template project can opt into, plus a minimal configurable exemplar.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [docxology/template_prose_project](https://github.com/docxology/template_prose_project)
- GitHub release: [v0.4.2](https://github.com/docxology/template_prose_project/releases/tag/v0.4.2)
- DOI: [10.5281/zenodo.20417104](https://doi.org/10.5281/zenodo.20417104)
- Zenodo record: [https://zenodo.org/records/20417104](https://zenodo.org/records/20417104)
- PDF: [Friedman_2026_Editorial_290d21b1.pdf](Friedman_2026_Editorial_290d21b1.pdf)
- PDF: [Friedman_2026_Editorial_b59313ea.pdf](Friedman_2026_Editorial_b59313ea.pdf)
- PDF: [Friedman_2026_Editorial_cbe5adae.pdf](Friedman_2026_Editorial_cbe5adae.pdf)
- PDF SHA-256: 290d21b10bd588b978d6a3200cdf0e3c2441ca86fcdc777ab41975fa910a260e

## Citation

> Daniel Ari Friedman (2026). *Editorial Quality at Scale: A Reproducible Prose-Review Pipeline*. Zenodo. DOI: 10.5281/zenodo.20417104. URL: https://doi.org/10.5281/zenodo.20417104.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
