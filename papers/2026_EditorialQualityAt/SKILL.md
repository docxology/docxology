---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "Editorial Quality at Scale: A Reproducible Prose-Review Pipeline"
description: "This paper documents template_prose_project, the prose-focused exemplar of the Research Project Template (https://github.com/docxology/template). It pairs the template's two-layer architecture with the prose analysis infrastructure (https://github.co..."
tags: ["prose-analysis", "readability", "editorial-review", "reproducible-research", "manuscript-quality"]
domain: "Computational"
citation: "Daniel Ari Friedman (2026). *Editorial Quality at Scale: A Reproducible Prose-Review Pipeline*. Zenodo."
doi: "10.5281/zenodo.20417104"
---

# Editorial Quality at Scale: A Reproducible Prose-Review Pipeline

**Daniel Ari Friedman** (2026) · Computational

## Context

This work addresses topics in **Computational**: prose analysis, readability, editorial review, reproducible research.

## Methods

Primary methods and techniques applied in this work:

- **Five-stage pure-function pipeline: read, analyse, cross-check, evaluate, render** — template_prose_project implements editorial review as five pure-function stages in src/, with scripts limited to argument parsing and I/O.
- **Readability metrics: Flesch Reading Ease, Flesch-Kincaid grade, Gunning Fog** — Per-file metrics are computed with textbook readability formulae over a vowel-group syllable heuristic.
- **Heuristic quality flags: passive voice, hedge density, citation density** — A quality analyser flags passive-voice candidates, hedge words, Pandoc [@key] citation density, and long sentences.
- **Citation-key cross-check against references.bib with configurable policy** — Every cited key is matched against the BibTeX file, with fail_on_missing / fail_on_unused settings in config.yaml.
- **Run-twice diff test for byte-identical JSON output** — Reproducibility is checked locally by running the pipeline twice and diffing manuscript_report.json.

## Key Findings

Core contributions and results:

- The paper reports that editorial review can be expressed as a configurable, deterministic pipeline with no novel domain algorithm of its own.
- On the bundled manuscript, the run analysed 8 files totalling 1731 words, with average Flesch-Kincaid grade 15.87 and Gunning Fog 16.67.
- Because no external service is consulted, a second run on the same inputs produces byte-identical JSON (modulo timestamp metadata).
- The stated contribution is architectural: a reusable prose-quality module any template project can opt into, plus a minimal configurable exemplar.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2023_NSFReporting](../2023_NSFReporting/)
- [2023_NaturalAIBased](../2023_NaturalAIBased/)
- [2025_AuBI](../2025_AuBI/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.20417104
- PDF SHA-256: 290d21b10bd588b978d6a3200cdf0e3c2441ca86fcdc777ab41975fa910a260e
- Pairing confidence: strong
- Last checked: 2026-09-24T18:29:54Z

## Prerequisites

- Familiarity with prose analysis, readability, editorial review
- Background in Computational fundamentals
- Access to source repository: docxology/template_prose_project

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.20417104`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
