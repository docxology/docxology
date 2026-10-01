---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "Computational Complexity and Energetics of the Ant Stack"
description: "We present a comprehensive computational complexity and energy analysis framework for the Ant Stack, an integrated biomimetic architecture for embodied artificial intelligence. Our investigation employs analytical models for contact dynamics physics,..."
tags: ["antstack", "complexity-science", "information-theory", "complex-adaptive-systems", "ant-colonies", "non-equilibrium-thermodynamics"]
domain: "Entomology"
citation: "Daniel Friedman (2025). *Computational Complexity and Energetics of the Ant Stack*. Zenodo."
doi: "10.5281/zenodo.17238736"
---

# Computational Complexity and Energetics of the Ant Stack

**Daniel Friedman** (2025) · Entomology

## Context

This work addresses topics in **Entomology**: AntStack, complexity science, information theory, complex adaptive systems.

## Methods

Primary methods and techniques applied in this work:

- **Closed-form per-module complexity for AntBody, AntBrain, and AntMind loops** — Derives time and space complexity for the body (contact dynamics), brain (sparse spiking network), and mind (active inference planning) loops of the Ant Stack.
- **Device-coefficient energy model for compute, memory, spikes, and actuation** — Converts workload counts to Joules per decision using assumed coefficients such as 1.0 pJ per FLOP, SRAM/DRAM per-byte costs, and 1.0 aJ per spike.
- **Manifest-driven experiments with seeding and bootstrap CIs** — Runs scaling sweeps from manifests with seed=123, reporting 1000-sample nonparametric bootstrap intervals and log-log regression fits.
- **Comparison against Landauer limit and biological cost of transport** — Benchmarks module energies against kT ln 2 per bit and compares the hexapod's cost of transport with values for biological ants.

## Key Findings

Core contributions and results:

- In the energy model, AntBody energy stayed constant despite morphological scaling, making sensor optimization and contact resolution the main efficiency targets rather than joint count.
- In the energy model, biological sparsity allowed 16× sensory scaling (64 to 1024 channels) with constant energy consumption.
- AntMind energy grew steeply with planning horizon, and real-time operation was reported infeasible beyond a horizon of 15.
- Modelled neural processing sits about 4.2 × 10^8 times above the Landauer minimum, which the author identifies as the largest optimization opportunity.
- The modelled locomotion cost of transport (≈1.93) falls within robotic platform ranges but is 2-6× higher than biological ants (0.1-0.3).

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2016_AntGenetics](../2016_AntGenetics/)
- [2016_ForagingGene](../2016_ForagingGene/)
- [2017_MutAnts](../2017_MutAnts/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.17238736
- PDF SHA-256: See zenodo_record
- Pairing confidence: unknown
- Last checked: 2026-06-30T23:25:43Z

## Prerequisites

- Familiarity with AntStack, complexity science, information theory
- Background in Entomology fundamentals
- Access to source repository: N/A

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.17238736`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
