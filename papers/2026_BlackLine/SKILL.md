---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "Black Line: Strong Work in Public"
description: "A positive practice instrument for concise, inspectable, revisable work. It reads self-declared tags and evidence labels against a versioned practice registry and returns one of four statuses over declaration coverage. It measures whether the evidenc..."
tags: ["research-practice", "declaration-coverage", "evidence-discipline", "scientific-integrity", "reproducibility", "open-science", "engineering-practice"]
domain: "Cognitive Security"
citation: "Daniel Ari Friedman (2026). *Black Line: Strong Work in Public*. Zenodo."
doi: "10.5281/zenodo.21754235"
---

# Black Line: Strong Work in Public

**Daniel Ari Friedman** (2026) · Cognitive Security

## Context

This work addresses topics in **Cognitive Security**: research practice, declaration coverage, evidence discipline, scientific integrity.

## Methods

Primary methods and techniques applied in this work:

- **Versioned registry of eleven practices with coarse evidence labels** — Encodes practices such as question-first framing, source traceability, and clean reruns as 'wires', each with reviewed tags and required evidence labels.
- **Staged evaluate_work evaluator returning four statuses** — Validates configuration and registry, then runs intake normalization, freshness partition, tag matching, and scoring to return ALIGNED, NEEDS_EVIDENCE, NEEDS_REWORK, or OUTSIDE_SCOPE.
- **Structural invariants tested against planted-bad registries** — Seven invariants check the registry's own shape, each demonstrated firing on a deliberately broken registry rather than only passing on the real one.
- **Executed adversarial declarations against the real evaluator** — Runs label-stuffing, tag-minimization, and refresh-date laundering attacks to show how self-declared inputs can game the status.
- **Three claim classes with distinct evidentiary burdens** — Separates implementation, methodological, and world/authority claims so that tests or citations do not silently change the type of claim made.

## Key Findings

Core contributions and results:

- An ALIGNED status only means every required label for each applicable practice was declared fresh, never that a source is real or a claim true.
- Label-stuffing works: a research-tagged attempt declaring all 22 vocabulary labels with no artifacts returns ALIGNED.
- Coverage is asymmetric: 27 of the 55 tag-practice cells are applicable, computed directly from the registry.
- Seeded permutation sweeps confirm that once a declaration is non-empty the status never regresses, with the empty declaration as the intentional exception.
- The author makes a design and implementation claim only; no user study or outcome comparison was run.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

See [BIBLIOGRAPHY.md](../../pages/BIBLIOGRAPHY.md) for related publications.

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.21754235
- PDF SHA-256: See zenodo_record
- Pairing confidence: unknown
- Last checked: 2026-08-02T15:12:58Z

## Prerequisites

- Familiarity with research practice, declaration coverage, evidence discipline
- Background in Cognitive Security fundamentals
- Access to source repository: N/A

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.21754235`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
