---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "Cognitive Diagrams: Reviewing Categorical Accounts of Linguistic Case"
description: "Linguistic case offers a setting in which to examine how diagrams connect relational structure, compositional syntax, and uncertainty. This article reviews categorical approaches and supplies an executable collection of deliberately small examples. T..."
tags: ["cognitivecasediagrams"]
domain: "Active Inference"
citation: "Daniel Ari Friedman (2026). *Cognitive Diagrams: Reviewing Categorical Accounts of Linguistic Case*. Active Inference Journal."
doi: "10.5281/zenodo.19695259"
---

# Cognitive Diagrams: Reviewing Categorical Accounts of Linguistic Case

**Daniel Ari Friedman** (2026) · Active Inference

## Context

This work addresses topics in **Active Inference**: CognitiveCaseDiagrams.

## Methods

Primary methods and techniques applied in this work:

- **Case systems formalized as categories with alignment types as functors** — Reviews case systems as categories whose objects are case roles and morphisms are grammatical relations, treating each alignment type as a structure-preserving functor.
- **Case-typed DisCoCat/DisCoCirc string diagrams for sentence and discourse** — Extends DisCoCat with case-typed noun spaces and alignment-sensitive meaning functors, and uses DisCoCirc for discourse-level composition.
- **[0,1]-enriched case categories and categorical magnitude** — Equips case categories with [0,1]-valued hom-objects and uses categorical magnitude as an invariant for comparing case systems.
- **Integration with Distributional Active Inference to derive ERP predictions** — Embeds the case framework in a Distributional Active Inference model to state falsifiable predictions for P600, N400 and garden-path reanalysis.
- **Open-source Python implementation with automated tests and generated figures** — Implements the formal structures in a src/ package with a no-mocks test suite and programmatically generated figures.

## Key Findings

Core contributions and results:

- The review captures nominative-accusative, ergative-absolutive, active-stative, tripartite and fluid-S alignment within one algebraic framework linked by alignment functors.
- Within case-typed string diagrams, passivization reduces to a type permutation (a Swap in the pregroup category).
- When multi-turn agent interactions are modeled as a fixed category of licensed morphisms, prompt injection can be analyzed as ill-typed role promotion (a functorial type violation): a specification target, not a guarantee on current LLM APIs.
- The topos-theoretic equivalence chain across typological, type-logical, distributional and enriched case theories is presented as a research program, not a finished theorem.
- The accompanying code has 1197 tests across 64 files at 95.96% line-and-branch coverage on src/, plus 30 programmatically generated figures.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2018_WoodliceAndMen](../2018_WoodliceAndMen/)
- [2020_BehaviorEngineering](../2020_BehaviorEngineering/)
- [2021_ModelingConflict](../2021_ModelingConflict/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.19695259
- PDF SHA-256: See zenodo_record
- Pairing confidence: strong
- Last checked: 2026-09-24T18:29:54Z

## Prerequisites

- Familiarity with CognitiveCaseDiagrams
- Background in Active Inference fundamentals
- Access to source repository: docxology/cognitive_case_diagrams

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.19695259`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
