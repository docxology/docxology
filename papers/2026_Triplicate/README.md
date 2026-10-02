<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 The Triplicate: A Data-Driven Large-Format Newspaper Layout Engine

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20533675-blue)](https://doi.org/10.5281/zenodo.20533675)

---

## Abstract

> We present template_newspaper, a pure-Python engine that renders a complete twelve-page, large-format newspaper to a print-ready PDF from structured YAML content. The exemplar edition is The Triplicate, a homage to the historic newspaper of Crescent City, California (founded 1879). The engine demonstrates designed multi-column page layout — nameplate and ears, spanning headlines, flowing column frames with an optional rail, drop caps, pull quotes, ruled modular boxes, data tables, halftone "engraving" figures and running folios — while keeping a strict separation between content (data) and engine (code): a new title is a data edit, never a code change. The layout strategy is a hybrid in which fixed furniture is drawn directly on the canvas to establish where the column grid begins, after which body copy flows through ReportLab frames that split paragraphs across columns automatically. The project obeys the research-template monorepo contract and is discovered and executed by the same orchestration pipeline as its code- and prose-focused siblings.

## Keywords

`newspaper layout` · `typography` · `reportlab` · `reproducible publishing` · `document engineering`

## Methods

- **Pure-Python engine rendering YAML content to a print-ready PDF** — template_newspaper reads a masthead manifest and per-page YAML files and renders a twelve-page large-format newspaper to PDF.
- **Hybrid drawn-furniture / ReportLab-flowed-body layout strategy** — Fixed furniture is drawn on the canvas first, then body copy flows through ReportLab frames via Frame.addFromList, splitting paragraphs across columns.
- **Nine single-responsibility modules with a deterministic four-step pipeline** — Editions are produced by Load, Measure, Compose and Emit steps across modules such as geometry, content, typography, figures, layout and engine.
- **Procedural Pillow halftone scenes and monochrome Matplotlib charts** — Photographic elements are procedural grayscale Pillow scenes with a 45-degree halftone screen; data graphics are black-and-gray Matplotlib charts.
- **pytest end-to-end render tests, mypy type checking, ruff linting** — A pytest suite tests the pure logic and renders the edition end-to-end, asserting a valid twelve-page PDF at correct trim with no over-set page.

## Key Findings

- The engine keeps content and code strictly separate, so producing a new newspaper title is a data edit rather than a code change.
- Drawing furniture first and starting column frames below it lets spanning headlines, standing boxes and automatic text flow coexist on one page.
- Rendering is deterministic: the same edition manifest always yields a byte-identical paper.
- The bold weight in a .ttc font collection sits at a face-specific subfont index; an early render produced italic Didot headlines from assuming the wrong index.
- The test suite reports roughly ninety-five percent line coverage.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [docxology/template_newspaper](https://github.com/docxology/template_newspaper)
- GitHub release: [v1.0.2](https://github.com/docxology/template_newspaper/releases/tag/v1.0.2)
- DOI: [10.5281/zenodo.20533675](https://doi.org/10.5281/zenodo.20533675)
- Zenodo record: [https://zenodo.org/records/20533675](https://zenodo.org/records/20533675)
- PDF: [Friedman_2026_Triplicate_5c991b5c.pdf](Friedman_2026_Triplicate_5c991b5c.pdf)
- PDF: [Friedman_2026_Triplicate_6c693dbd.pdf](Friedman_2026_Triplicate_6c693dbd.pdf)
- PDF: [Friedman_2026_Triplicate_851f9973.pdf](Friedman_2026_Triplicate_851f9973.pdf)
- PDF SHA-256: 6c693dbd80a4234d30d99f6a890191ff47faf197a0636753fa9785588c550a77

## Citation

> Daniel Ari Friedman (2026). *The Triplicate: A Data-Driven Large-Format Newspaper Layout Engine*. Zenodo. DOI: 10.5281/zenodo.20533675. URL: https://doi.org/10.5281/zenodo.20533675.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
