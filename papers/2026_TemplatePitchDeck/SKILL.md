---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "template_pitch_deck: Reproducible, Validated Pitch-Deck Generation"
description: "Research groups routinely need to pitch their work — to funders, partners, or collaborators — yet pitch decks are almost never treated as reproducible research artifacts: they are hand-assembled in proprietary slide tools, contain unverifiable claims..."
tags: ["pitch-deck", "slide-generation", "reproducible-research-communication", "meta-science-infrastructure", "science-integrity", "token-validation", "pptx", "pdf-rendering"]
domain: "Computational"
citation: "Daniel Ari Friedman (2026). *template_pitch_deck: Reproducible, Validated Pitch-Deck Generation*. Zenodo."
doi: "10.5281/zenodo.21281509"
---

# template_pitch_deck: Reproducible, Validated Pitch-Deck Generation

**Daniel Ari Friedman** (2026) · Computational

## Context

This work addresses topics in **Computational**: pitch deck, slide generation, reproducible research communication, meta-science infrastructure.

## Methods

Primary methods and techniques applied in this work:

- **Shared format-agnostic DeckContent/Slide content model with slide budgets** — Defines Slide, DeckContent and SlideBudget (short <=10, medium <=22, long <=45 slides) consumed by both renderers, with a pure function truncating decks to a budget.
- **Dual PDF (ReportLab) and PPTX (python-pptx) renderers with a parity test** — Renders the same resolved content via ReportLab canvas onto 16:9 pages and via python-pptx, with a test asserting PDF page count equals PPTX slide count.
- **{{TOKEN}} resolution against deck_tokens.yaml with fail-loud checks** — Resolves {{TOKEN}} placeholders from a token file of facts read live from the pitched project, raising on any unresolved token and checking output for leftover braces.
- **Word-boundary cliché denylist lint over every resolved slide** — Runs a denylist of pitch-deck stock phrases (e.g. synergy, disrupt, 10x) across all slides at all three lengths before rendering, as part of an audit script.
- **Negative-control fixtures proving validation gates fire** — Uses deliberately broken token and cliché-laden fixtures to show each audit failure mode triggers before trusting that the real content passes.

## Key Findings

Core contributions and results:

- The tool generates six artifacts (short, medium and long decks, each as PDF and PPTX) from one token-resolved content source.
- PDF and PPTX decks built from identical content carry identical slide counts and text, verified by reading back both file formats rather than by inspection.
- Rendering is deterministic: given the same repository state, two consecutive runs produce byte-identical PDF and PPTX output, with generation time kept only in deck metadata.
- No LLM/Ollama stage is required, since deck content is authored and token-resolved rather than model-generated at render time, keeping artifacts deterministic.
- The flagship deck pitches template_template to a meta-science and science-integrity audience using problem, solution, proof (currently measured facts) and ask arc.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

See [BIBLIOGRAPHY.md](../../pages/BIBLIOGRAPHY.md) for related publications.

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.21281509
- PDF SHA-256: See zenodo_record
- Pairing confidence: strong
- Last checked: 2026-09-24T18:29:57Z

## Prerequisites

- Familiarity with pitch deck, slide generation, reproducible research communication
- Background in Computational fundamentals
- Access to source repository: docxology/template-pitch-deck

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.21281509`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
