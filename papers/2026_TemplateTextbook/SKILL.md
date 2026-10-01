---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "The Template Textbook"
description: "A modular, fillable scaffold for book-length technical works: a data-driven manuscript (parts/chapters/labs/questions), a tested computational backbone, deterministic figures and Mermaid diagrams, and a content scaffold/validation engine."
tags: ["templatetextbook"]
domain: "Computational"
citation: "Daniel Ari Friedman (2026). *The Template Textbook*. Zenodo."
doi: "10.5281/zenodo.20533125"
---

# The Template Textbook

**Daniel Ari Friedman** (2026) · Computational

## Context

This work addresses topics in **Computational**: TemplateTextbook.

## Methods

Primary methods and techniques applied in this work:

- **Single config.yaml source of truth for book structure** — Parts, chapters, front matter, appendices, labs and question banks are declared in config.yaml, from which TOC, numbering and integrity tests read.
- **Tested Python backbone (textbook.models) and deterministic figures** — Worked equations are implemented as tested Python functions that chapter prose calls, and figures are generated deterministically from code.
- **Pandoc + pandoc-crossref rendering pipeline** — The manuscript is assembled from Markdown in declared order after analysis scripts produce figures, then rendered to PDF via Pandoc with pandoc-crossref.
- **Stub-marker counting audit and manuscript-integrity tests** — A quality audit counts STUB/TODO/TKTK markers and pytest checks the per-chapter content contract, unique labels, citations and glossary anchors.
- **Two filled worked-reference chapters (logistic growth; dose-response)** — First Principles derives the logistic growth law; Case Studies applies a linear dose-response fit to a small dataset of replicate measurements across control, low and high conditions.

## Key Findings

Core contributions and results:

- The book is explicitly a scaffold rather than a finished work: every structural element is present and author-specific passages are marked stubs.
- It provides twelve chapter shells across four parts, each with a matching lab and question bank.
- Claims building the book reproduces byte-identical figures and numbers, since nothing in the prose is computed by hand.
- The worked case study's linear fit gives slope 1.375 and R2 = 0.999, while warning that three averaged points cannot support prediction or extrapolation.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2023_NSFReporting](../2023_NSFReporting/)
- [2023_NaturalAIBased](../2023_NaturalAIBased/)
- [2025_AuBI](../2025_AuBI/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.20533125
- PDF SHA-256: 7b67cb2d9118f0a72001395f0a94c529313804d7e5cdf7f6ca2dc9f7ab57d168
- Pairing confidence: strong
- Last checked: 2026-09-24T18:29:55Z

## Prerequisites

- Familiarity with TemplateTextbook
- Background in Computational fundamentals
- Access to source repository: docxology/template_textbook

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.20533125`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
