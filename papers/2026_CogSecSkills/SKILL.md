---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "CogSecSkills: Multiharness Agentic Skills for Cognitive Security"
description: "A defensive, educational, harness-neutral library of 100 agentic tool-use skills for Cognitive Security and analytic tradecraft (Structured Analytic Techniques, source verification, deception detection, critical review), with configured structural ad..."
tags: ["cognitive-security", "structured-analytic-techniques", "agentic-ai", "intelligence-analysis", "osint", "counterintelligence", "multiharness-skills"]
domain: "Cognitive Security"
citation: "Daniel Ari Friedman (2026). *CogSecSkills: Multiharness Agentic Skills for Cognitive Security*. Zenodo."
doi: "10.5281/zenodo.21513316"
---

# CogSecSkills: Multiharness Agentic Skills for Cognitive Security

**Daniel Ari Friedman** (2026) · Cognitive Security

## Context

This work addresses topics in **Cognitive Security**: cognitive security, structured analytic techniques, agentic AI, intelligence analysis.

## Methods

Primary methods and techniques applied in this work:

- **Plan/Build/Teach architecture: registry, definitions, skills tree, AGEINT** — Separates a catalogue registry, canonical per-skill definitions, a harness-facing skills tree, and the AGEINT educational upstream.
- **Harness-neutral skill contract over a closed set of eight tool verbs** — Each skill may use only neutral verbs (read, search, write, exec, reason, web, delegate, ask), bound per harness through adapters.
- **Deterministic rendering into Claude, Codex, and Hermes adapters** — Renders each canonical definition into a spec, skill description, workflow, and one adapter per configured harness.
- **Automated anti-boilerplate per-skill quality audit** — Requires a skill-specific quality bundle and rejects generic or reused negative controls, rubrics, evidence and privacy entries.
- **Evidence ladder: 28 scenario fixtures and per-skill worked examples** — Checks curated safe and unsafe scenarios against the local router and verifies one reviewed worked example per skill.

## Key Findings

Core contributions and results:

- The generated catalogue reports one hundred implemented skills across seven taxonomy groups, from Structured Analytic Techniques to Research and Synthesis Methods.
- The author describes a local quality gate, explicitly 'not a safety proof', that can show all 100 skills include group-aware defensive boundaries and skill-specific governance entries in the current repository state.
- The worked-example gate verifies exact 100-skill coverage; the examples are expected-answer shapes, not live model transcripts.
- The author states the evidence is local conformance only and does not establish operational effectiveness, adversary coverage, user outcomes, or superiority over other libraries.
- The deterministic gates do not show that a live runtime will select the same skill, use tools correctly, or answer well in the field.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2023_NSFReporting](../2023_NSFReporting/)
- [2023_NaturalAIBased](../2023_NaturalAIBased/)
- [2025_AuBI](../2025_AuBI/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.21513316
- PDF SHA-256: See zenodo_record
- Pairing confidence: strong
- Last checked: 2026-10-12T18:48:29Z

## Prerequisites

- Familiarity with cognitive security, structured analytic techniques, agentic AI
- Background in Cognitive Security fundamentals
- Access to source repository: docxology/CogSecSkills

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.21513316`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
