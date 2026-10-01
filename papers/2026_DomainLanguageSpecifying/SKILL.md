---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "A Domain Language for Specifying Controlled Methods"
description: "This paper describes a small, tested domain language for specifying controlled methods — the methods-paper exemplar of the Research Project Template (https://github.com/docxology/template). Unlike a results paper, this manuscript's subject is the met..."
tags: ["methods-paper", "domain-specific-language", "controlled-methods", "deterministic-compilation", "staged-validation", "dimensional-analysis"]
domain: "Computational"
citation: "Daniel Ari Friedman (2026). *A Domain Language for Specifying Controlled Methods*. Zenodo."
doi: "10.5281/zenodo.21086548"
---

# A Domain Language for Specifying Controlled Methods

**Daniel Ari Friedman** (2026) · Computational

## Context

This work addresses topics in **Computational**: methods paper, domain-specific language, controlled methods, deterministic compilation.

## Methods

Primary methods and techniques applied in this work:

- **Controlled vocabulary of 9 step intents and 3 execution targets** — Steps name one of nine intents (TRANSFER, ADD, MIX, etc.) and run on HUMAN, AUTOMATED or SIMULATION targets, generalizing BPL's protocol verbs.
- **Dimensional-safety unit system (Quantity/Dimension)** — Each quantity resolves to a controlled unit table and combining quantities of different dimensions raises an error at construction rather than at the bench.
- **Four staged validation gates with short-circuit** — Structural, semantic, plan (acyclicity) and target-compatibility gates run in fixed order, returning early if the first two fail.
- **Deterministic compilation via Kahn's algorithm and SHA-256 plan hash** — Validated steps are topologically scheduled with an explicit ascending step_id tie-break and the canonical JSON plan is hashed with SHA-256.
- **Two worked example methods and zero-mock test suite** — Demonstrates the DSL on a wet-lab PBS preparation and an automated sensor-calibration sweep, tested without mocks under a 90% coverage gate.

## Key Findings

Core contributions and results:

- Across the two worked example methods, 8 of 8 staged-gate evaluations passed.
- Live recompilation of each example method produced identical plan hashes, and a 3-record demonstration provenance hash-chain verified.
- The author concludes that a controlled vocabulary expressed as typed, validated dataclasses rather than a parsed grammar suffices to reproduce BPL's core safety properties at template-exemplar scope.
- Stable scheduling depends on the explicit tie-break: Kahn's algorithm alone does not guarantee a reproducible plan hash.
- The calibration example reused every step kind and target of the wet-lab example, with nothing added to support the second domain.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2023_NSFReporting](../2023_NSFReporting/)
- [2023_NaturalAIBased](../2023_NaturalAIBased/)
- [2025_AuBI](../2025_AuBI/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.21086548
- PDF SHA-256: ecd8519fc2a9a674bd8a4cf89f96122af76529c913e32bf880a7c842da08771a
- Pairing confidence: strong
- Last checked: 2026-09-24T18:29:57Z

## Prerequisites

- Familiarity with methods paper, domain-specific language, controlled methods
- Background in Computational fundamentals
- Access to source repository: docxology/template_methods_paper

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.21086548`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
