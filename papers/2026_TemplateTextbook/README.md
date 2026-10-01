<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 The Template Textbook

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20533125-blue)](https://doi.org/10.5281/zenodo.20533125)

---

## Abstract

> A modular, fillable scaffold for book-length technical works: a data-driven manuscript (parts/chapters/labs/questions), a tested computational backbone, deterministic figures and Mermaid diagrams, and a content scaffold/validation engine.

## Keywords

`TemplateTextbook`

## Methods

- **Single config.yaml source of truth for book structure** — Parts, chapters, front matter, appendices, labs and question banks are declared in config.yaml, from which TOC, numbering and integrity tests read.
- **Tested Python backbone (textbook.models) and deterministic figures** — Worked equations are implemented as tested Python functions that chapter prose calls, and figures are generated deterministically from code.
- **Pandoc + pandoc-crossref rendering pipeline** — The manuscript is assembled from Markdown in declared order after analysis scripts produce figures, then rendered to PDF via Pandoc with pandoc-crossref.
- **Stub-marker counting audit and manuscript-integrity tests** — A quality audit counts STUB/TODO/TKTK markers and pytest checks the per-chapter content contract, unique labels, citations and glossary anchors.
- **Two filled worked-reference chapters (logistic growth; dose-response)** — First Principles derives the logistic growth law; Case Studies fits a linear dose-response trend to a small synthetic six-condition dataset.

## Key Findings

- The book is explicitly a scaffold rather than a finished work: every structural element is present and author-specific passages are marked stubs.
- It provides twelve chapter shells across four parts, each with a matching lab and question bank.
- Claims building the book reproduces byte-identical figures and numbers, since nothing in the prose is computed by hand.
- The worked case study's linear fit gives slope 1.375 and R2 = 0.999, while warning that three averaged points cannot support prediction or extrapolation.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [docxology/template_textbook](https://github.com/docxology/template_textbook)
- GitHub release: [v0.1.2](https://github.com/docxology/template_textbook/releases/tag/v0.1.2)
- DOI: [10.5281/zenodo.20533125](https://doi.org/10.5281/zenodo.20533125)
- Zenodo record: [https://zenodo.org/records/20533125](https://zenodo.org/records/20533125)
- PDF: [Friedman_2026_Template_7b67cb2d.pdf](Friedman_2026_Template_7b67cb2d.pdf)
- PDF: [Friedman_2026_Template_c6c97f24.pdf](Friedman_2026_Template_c6c97f24.pdf)
- PDF: [template_textbook_combined.pdf](template_textbook_combined.pdf)
- PDF SHA-256: 7b67cb2d9118f0a72001395f0a94c529313804d7e5cdf7f6ca2dc9f7ab57d168

## Citation

> Daniel Ari Friedman (2026). *The Template Textbook*. Zenodo. DOI: 10.5281/zenodo.20533125. URL: https://doi.org/10.5281/zenodo.20533125.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
