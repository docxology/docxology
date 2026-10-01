---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "Refinement of Gold: A Metallurgical Analogy for Scientific Manuscript Composition"
description: "This paper presents a metallurgical analogy for scientific manuscript composition, mapping gold-refining stages onto the template infrastructure pipeline. The refinery processes manuscript ore through 5 stages — from raw draft (9K, ~37.5% purity) thr..."
tags: ["gold-refining", "manuscript-composition", "mega-madlib", "token-injection", "scientific-purity", "assaying", "karat-grading"]
domain: "Computational"
citation: "Daniel Ari Friedman (2026). *Refinement of Gold: A Metallurgical Analogy for Scientific Manuscript Composition*. Zenodo."
doi: "10.5281/zenodo.20931955"
---

# Refinement of Gold: A Metallurgical Analogy for Scientific Manuscript Composition

**Daniel Ari Friedman** (2026) · Computational

## Context

This work addresses topics in **Computational**: gold refining, manuscript composition, mega-madlib, token injection.

## Methods

Primary methods and techniques applied in this work:

- **Five-stage gold-refining analogy mapped to manuscript operations** — Maps ore, smelting, assaying, cupellation, and certification onto manuscript template-infrastructure operations such as claim removal, evidence checks, and cross-reference resolution.
- **Seeded SHA-256 mega-madlib token selection from a config-owned lexicon** — Selects domain vocabulary tokens deterministically from lexicon categories declared in config.yaml so every prose token is traceable to its config key.
- **Monotone-purity constraint enforced in code and tests** — Stage purity values must strictly increase, enforced by assert_monotone_increase in src/refinery.py and covered by the test suite.
- **Karat grading of stage purities via karat_for_purity()** — Maps each stage's purity fraction to a standard gold fineness grade (9K to 24K and nine-nines) in src/purity.py.
- **Deterministic seeded regeneration of all outputs** — The pipeline regenerates figures, data, and reports from the same config and source code; the reported run used seed 431.

## Key Findings

Core contributions and results:

- The paper argues the analogy is load-bearing rather than only rhetorical, since each metallurgical stage corresponds to a real template-infrastructure operation.
- The exemplar pipeline reports a monotone purity sequence over 5 stages ending at the nine-nines certification stage.
- The token engine generated 8 tokens from seed 431 across 4 lexicon categories, each traceable in a provenance table.
- The paper explicitly does not claim empirical validation of manuscript quality metrics or generalizability of its purity fractions.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2023_NSFReporting](../2023_NSFReporting/)
- [2023_NaturalAIBased](../2023_NaturalAIBased/)
- [2025_AuBI](../2025_AuBI/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.20931955
- PDF SHA-256: 3643178951b267632e607606b6daaba21ea75d8f7590899948b5999d1854198b
- Pairing confidence: strong
- Last checked: 2026-06-26T15:16:06Z

## Prerequisites

- Familiarity with gold refining, manuscript composition, mega-madlib
- Background in Computational fundamentals
- Access to source repository: docxology/template_gold_refinement

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.20931955`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
