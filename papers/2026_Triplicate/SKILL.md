---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "The Triplicate: A Data-Driven Large-Format Newspaper Layout Engine"
description: "We present template_newspaper, a pure-Python engine that renders a complete twelve-page, large-format newspaper to a print-ready PDF from structured YAML content. The exemplar edition is The Triplicate, a homage to the historic newspaper of Crescent ..."
tags: ["newspaper-layout", "typography", "reportlab", "reproducible-publishing", "document-engineering"]
domain: "Computational"
citation: "Daniel Ari Friedman (2026). *The Triplicate: A Data-Driven Large-Format Newspaper Layout Engine*. Zenodo."
doi: "10.5281/zenodo.20533675"
---

# The Triplicate: A Data-Driven Large-Format Newspaper Layout Engine

**Daniel Ari Friedman** (2026) · Computational

## Context

This work addresses topics in **Computational**: newspaper layout, typography, reportlab, reproducible publishing.

## Methods

Primary methods and techniques applied in this work:

- **Pure-Python engine rendering YAML content to a print-ready PDF** — template_newspaper reads a masthead manifest and per-page YAML files and renders a twelve-page large-format newspaper to PDF.
- **Hybrid drawn-furniture / ReportLab-flowed-body layout strategy** — Fixed furniture is drawn on the canvas first, then body copy flows through ReportLab frames via Frame.addFromList, splitting paragraphs across columns.
- **Nine single-responsibility modules with a deterministic four-step pipeline** — Editions are produced by Load, Measure, Compose and Emit steps across modules such as geometry, content, typography, figures, layout and engine.
- **Procedural Pillow halftone scenes and monochrome Matplotlib charts** — Photographic elements are procedural grayscale Pillow scenes with a 45-degree halftone screen; data graphics are black-and-gray Matplotlib charts.
- **pytest end-to-end render tests, mypy type checking, ruff linting** — A pytest suite tests the pure logic and renders the edition end-to-end, asserting a valid twelve-page PDF at correct trim with no over-set page.

## Key Findings

Core contributions and results:

- The engine keeps content and code strictly separate, so producing a new newspaper title is a data edit rather than a code change.
- Drawing furniture first and starting column frames below it lets spanning headlines, standing boxes and automatic text flow coexist on one page.
- Rendering is deterministic: the same edition manifest always yields a byte-identical paper.
- The bold weight in a .ttc font collection sits at a face-specific subfont index; an early render produced italic Didot headlines from assuming the wrong index.
- The test suite reports roughly ninety-five percent line coverage.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2023_NSFReporting](../2023_NSFReporting/)
- [2023_NaturalAIBased](../2023_NaturalAIBased/)
- [2025_AuBI](../2025_AuBI/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.20533675
- PDF SHA-256: 6c693dbd80a4234d30d99f6a890191ff47faf197a0636753fa9785588c550a77
- Pairing confidence: strong
- Last checked: 2026-09-24T18:29:55Z

## Prerequisites

- Familiarity with newspaper layout, typography, reportlab
- Background in Computational fundamentals
- Access to source repository: docxology/template_newspaper

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.20533675`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
