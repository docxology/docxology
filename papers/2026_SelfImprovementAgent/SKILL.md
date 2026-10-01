---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "Self-Improvement Agent Harness: A Deterministic SIA Exemplar"
description: "This exemplar documents template_sia, a deterministic implementation of the Self-Improvement Agent (SIA) harness contract described in the Self-Improvement Agents specification (Hexo AI, 2026, arXiv:2605.27276). The default pipeline replays fixture-b..."
tags: ["self-improvement-agents", "benchmark-harness", "reproducible-research", "agent-evaluation"]
domain: "Computational"
citation: "Daniel Ari Friedman (2026). *Self-Improvement Agent Harness: A Deterministic SIA Exemplar*. Zenodo."
doi: "10.5281/zenodo.20453879"
---

# Self-Improvement Agent Harness: A Deterministic SIA Exemplar

**Daniel Ari Friedman** (2026) · Computational

## Context

This work addresses topics in **Computational**: self-improvement agents, benchmark harness, reproducible research, agent evaluation.

## Methods

Primary methods and techniques applied in this work:

- **Meta -> Target -> Feedback three-agent SIA loop** — The harness cycles a meta agent that seeds a target agent, the target run on public data, and a feedback agent that reads private metrics to propose the next generation.
- **Public/private task split with deterministic reference baseline** — Each task separates agent-visible data and instructions from held-out evaluation labels, plus a deterministic reference target agent.
- **Fixture-replay determinism contract with opt-in live mode** — By default generations replay recorded fixtures so CI never runs generated code or calls LLM APIs; a flag enables bounded subprocess execution with optional Ollama feedback.
- **mini_classify single-feature threshold classifier task** — The bundled exemplar task is a threshold classifier on one feature column, evaluated over 3 generations on 6 held-out samples.

## Key Findings

Core contributions and results:

- In the bundled fixture-replay run, final accuracy on mini_classify was 0.8333 over 6 held-out samples after 3 generations.
- Accuracy rose from the first to the final generation by a metric delta of 0.3333 in the fixture replay.
- template_sia shows the SIA harness contract can be embedded in the Research Project Template without vendoring upstream orchestration code, split into an infrastructure layer and a project layer.
- The author states the fixture-replay metrics validate wiring only and are not evidence of state-of-the-art self-improvement.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2023_NSFReporting](../2023_NSFReporting/)
- [2023_NaturalAIBased](../2023_NaturalAIBased/)
- [2025_AuBI](../2025_AuBI/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.20453879
- PDF SHA-256: 6e6d19d04182628bb825471cf8094b5c32d2c491d2c646652ec7e2439ba80773
- Pairing confidence: strong
- Last checked: 2026-09-24T18:29:54Z

## Prerequisites

- Familiarity with self-improvement agents, benchmark harness, reproducible research
- Background in Computational fundamentals
- Access to source repository: docxology/template_sia

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.20453879`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
