# Editorial Quality at Scale: A Reproducible Prose-Review Pipeline

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20417104.svg)](https://doi.org/10.5281/zenodo.20417104)

---

## Abstract

Abstract

This paper documents template_prose_project, the prose-focused exemplar of the Research Project Template (https://github.com/docxology/template). It pairs the template's two-layer architecture with the prose analysis infrastructure (https://github.com/docxology/template/tree/main/infrastructure/prose) (readability metrics, structural outline, editorial quality flags) and the reference validation infrastructure (https://github.com/docxology/template/tree/main/infrastructure/reference) (BibTeX validation), demonstrating that rigorous editorial review can be expressed as a configurable, deterministic pipeline with no novel domain algorithm of its own.

A single manuscript/config.yaml defines target grade-level bands, citation-density floors, structural rules (every section has an H1, no heading levels skipped), and bibliography-consistency policy. The pipeline reads the manuscript, runs the prose analysers, cross-checks every  citation against manuscript/references.bib, evaluates the configured checks, and writes a deterministic markdown review report alongside three figures (per-file word counts, readability metrics, citation density) and a JSON manuscript_report.json suitable for CI artefacts.

Run snapshot. The current configuration analyses 8 file(s) totalling 1822 words across 86 sentence(s) and 63 paragraph(s). Average Flesch-Kincaid grade level is 16.79; average Gunning Fog index is 17.84; the manuscript references 6 unique citation key(s); the longest section is 413 words and the shortest is 17. These numbers are auto-substituted by scripts/z_generate_manuscript_variables.py after every run, so the abstract tracks the JSON outputs in output/.

The contribution is methodological and architectural: a generic, reusable prose-quality module (infrastructure/prose/) that any project in the template can opt into, plus a minimal, configurable exemplar (projects/template_prose_project/) that wires it to the bibliography and the manuscript pipeline. Together with template_code_project (numerical research), template_autoresearch_project (deterministic plan/evidence/readiness loops), and the optional projects_archive/template_search_project add-on (literature discovery), it covers the dominant shapes of academic research projects in the template.

Keywords: prose analysis, readability, editorial review, reproducible manuscript review, scientific infrastructure

---
Associated artifacts
GitHub release: v0.4.0 (https://github.com/docxology/template_prose_project/releases/tag/v0.4.0)
DOI: https://doi.org/10.5281/zenodo.20417104
Zenodo: https://zenodo.org/records/20417104
PDF SHA-256: cbe5adae0be78b58c77637042257e9faa61a21b6c5101da52600cf8e2e80c0e2

## Keywords

prose analysis · readability · editorial review · reproducible research · manuscript quality

## Publication Details

| Field | Value |
|------|-------|
| **DOI** | [10.5281/zenodo.20417104](https://doi.org/10.5281/zenodo.20417104) |
| **Published** | 2026 |
| **Version** | 0.4.0 |
| **Zenodo record** | https://zenodo.org/records/20420342 |
| **GitHub release** | https://github.com/docxology/template_prose_project/releases/tag/v0.4.0 |
| **Source repository** | https://github.com/docxology/template_prose_project |

## Files

- `Friedman_2026_Editorial_cbe5adae.pdf` - Zenodo PDF

## Citation

> Friedman, D. A. (2026). *Editorial Quality at Scale: A Reproducible Prose-Review Pipeline*. Zenodo. https://doi.org/10.5281/zenodo.20417104

## Related

- Zenodo record: https://zenodo.org/records/20420342
- GitHub release: https://github.com/docxology/template_prose_project/releases/tag/v0.4.0
- Source repository: https://github.com/docxology/template_prose_project
- [Full Bibliography](../../pages/BIBLIOGRAPHY.md) · [All Papers](../README.md)
