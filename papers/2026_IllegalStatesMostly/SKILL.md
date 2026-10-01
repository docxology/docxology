---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "Illegal States, Mostly Unrepresentable"
description: "This paper presents a strongly-typed, decentralized multiagent simulation — an ant-robot colony — as the computational exemplar of the Research Project Template (https://github.com/docxology/template). Each colony member is an Agent that owns exactly..."
tags: ["strongly-typed-programming", "session-types", "algebraic-data-types", "category-theory", "active-inference", "multiagent-systems", "affine-types", "illegal-state-unrepresentable"]
domain: "Entomology"
citation: "Daniel Ari Friedman (2026). *Illegal States, Mostly Unrepresentable*. Zenodo."
doi: "10.5281/zenodo.21298885"
---

# Illegal States, Mostly Unrepresentable

**Daniel Ari Friedman** (2026) · Entomology

## Context

This work addresses topics in **Entomology**: strongly typed programming, session types, algebraic data types, category theory.

## Methods

Primary methods and techniques applied in this work:

- **Simulated ant-robot colony: agents with own SQLite DB and protocol endpoint** — Each simulated colony member owns one on-disk SQLite database and one fault-injectable protocol endpoint, with no shared storage or network state.
- **mypy --strict as oracle on six known-bad and three known-good fixtures** — Runs mypy --strict as a subprocess on negative-control fixtures (expect errors), positive-control fixtures, and the src tree (expect zero exit).
- **Seeded fault injection (drop/reorder/duplicate/corrupt) over an in-process bus** — Drives real handshakes through an in-process bus with each fault mode enabled, checking typed error results and seed determinism.
- **Pre-registered seeded experiments with Wilson CIs, Fisher and Cochran–Armitage tests** — Tests colony convergence over independently seeded trials at a calibrated baseline (8 agents, 2 locations, 30 ticks) using Wilson intervals, Fisher and trend tests.
- **Design lenses: schema as functor; decision as expected-free-energy minimizer** — Frames per-agent storage as a functor Schema→Set and decisions via expected free energy, explicitly as design lenses rather than proofs.

## Key Findings

Core contributions and results:

- The stigmergic mechanism's convergence beat a random-choice null model: its Wilson lower bound (0.8816) clears the null model's upper bound (0.0368).
- Disabling only pheromone deposit collapsed convergence to chance level, attributing the mechanism's advantage to the stigmergic channel in this configuration.
- Convergence versus decay showed a threshold rather than a monotonic slope, with 0/60 trials converging at decay 0.10 and 0.30.
- Convergence decreased strictly as preference heterogeneity widened (1.0000 > 0.9333 > 0.2500 > 0.0333).
- An audit found a defect the src-only mypy gate missed (a Protocol a frozen dataclass could not satisfy), fixed with read-only properties and a good-fixture regression guard.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

See [BIBLIOGRAPHY.md](../../pages/BIBLIOGRAPHY.md) for related publications.

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.21298885
- PDF SHA-256: See zenodo_record
- Pairing confidence: unknown
- Last checked: 2026-07-10T19:31:26Z

## Prerequisites

- Familiarity with strongly typed programming, session types, algebraic data types
- Background in Entomology fundamentals
- Access to source repository: N/A

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.21298885`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
