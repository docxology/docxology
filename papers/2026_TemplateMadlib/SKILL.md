---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "Template Madlib: Deterministic Token Injection for Conditional IMRAD Manuscripts"
description: "This exemplar asks whether a reviewable pipeline can hydrate a complete IMRAD manuscript from configuration-owned lexical data while preserving an audit trail that remains readable before and after rendering. The project deliberately keeps playful Ma..."
tags: ["madlib-generation", "token-injection", "conditional-manuscripts", "reproducible-research", "imrad"]
domain: "Computational"
citation: "Daniel Ari Friedman (2026). *Template Madlib: Deterministic Token Injection for Conditional IMRAD Manuscripts*. Zenodo."
doi: "10.5281/zenodo.20786638"
artifact_doi: "10.5281/zenodo.20932025"
---

# Template Madlib: Deterministic Token Injection for Conditional IMRAD Manuscripts

**Daniel Ari Friedman** (2026) · Computational

## Context

This work addresses topics in **Computational**: madlib generation, token injection, conditional manuscripts, reproducible research.

## Methods

Primary methods and techniques applied in this work:

- **Seeded SHA-256 digest selection of lexicon tokens per slot** — Each slot hashes the seed, slot name, category, ordinal and full category list; the digest indexes the configured lexicon category.
- **YAML config-owned lexicon, slots, and section conditions** — Lexicon categories, slots, section switches, method rows and claims are declared in YAML; source code turns them into manuscript bodies.
- **Staged pipeline from config validation to hydrated Markdown** — Validates the madlib block, builds a TokenPlan and section bodies, writes artifact JSON and a figure registry, then hydrates Markdown.
- **Explicit vs. loader-default config field-origin inventory** — Classifies configuration paths as explicitly set in YAML or inherited from loader defaults and reports them as method evidence.
- **Project tests and shared output validator** — Tests check determinism, seed and category sensitivity, malformed configs, section disablement and unresolved tokens; a validator checks rendered outputs.

## Key Findings

Core contributions and results:

- With seed 431, the schema expands 22 slot rules into 40 token choices across 10 lexicon categories.
- The generated plan enabled all 11 manuscript sections and filled 40 token choices, each traced to its variable, category, section and config pointer.
- Re-running generation with seed 431 and the same lexicon produces the same token plan.
- The author frames the main result as traceability surviving a complete render path, not any particular word choice.
- The paper explicitly does not claim lexical replacement creates scholarship; it shows a conditional text generator can be made accountable to config, tests and validation.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2023_NSFReporting](../2023_NSFReporting/)
- [2023_NaturalAIBased](../2023_NaturalAIBased/)
- [2025_AuBI](../2025_AuBI/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.20786638
- PDF SHA-256: d9248f4f372fc3baf21cbf5cc5cdb7daffe0e22e62ac6fa2e3a697a26f3308b6
- Pairing confidence: strong
- Last checked: 2026-09-24T18:29:56Z
- Artifact DOI: 10.5281/zenodo.20932025

## Prerequisites

- Familiarity with madlib generation, token injection, conditional manuscripts
- Background in Computational fundamentals
- Access to source repository: docxology/template_madlib

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.20786638`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
