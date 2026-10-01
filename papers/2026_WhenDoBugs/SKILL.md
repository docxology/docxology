---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "When do bugs see (infra)red?"
description: "Objective: To review the plausibility of insect detection of infrared (IR) cues that covary with semiochemical vibrational signatures, and to produce falsifiable predictions through the integration of comparative entomology, spectroscopy, neural timi..."
tags: ["insect-olfaction", "infrared-detection", "vibrational-theory-of-olfaction", "semiochemicals", "sensilla-morphology", "electromagnetic-sensing", "active-inference", "reproducible-research"]
domain: "Computational"
citation: "Tucker Chambers, Daniel A. Friedman (2026). *When do bugs see (infra)red?*. Zenodo."
doi: "10.5281/zenodo.20450880"
---

# When do bugs see (infra)red?

**Tucker Chambers, Daniel A. Friedman** (2026) · Computational

## Context

This work addresses topics in **Computational**: insect olfaction, infrared detection, vibrational theory of olfaction, semiochemicals.

## Methods

Primary methods and techniques applied in this work:

- **Integration of literature morphometrics, ATR-FTIR evidence, ORN timing, and EM models** — Combines published sensilla ranges, FTIR insect-chemistry evidence, olfactory neuron timing constraints, and deterministic electromagnetic models.
- **Coarse atmospheric IR transmission window model with sensitivity terms** — A baseline window model plus humidity, temperature, scattering, and path-length terms, explicitly framed as a scenario generator.
- **Quarter-/half-wave resonance estimates for sensilla as dielectric antennas** — Representative sensilla classes, anchored to published Thripidae measurements, are compared against IR wavelengths via resonance and waveguide calculations.
- **Unit-tested deterministic code (CohereAnts) with fixed seeds and coverage gate** — All models are implemented in tested src/ modules with seed 42 and a 90% coverage gate, with seven appendix case studies.
- **Preregistered IR-only assay protocols with thermal-matched controls** — Specifies single-sensillum electrophysiology, behavioral IR-only assays, and SEM morphometrics with QCL/LED bands and N>=50 per condition.

## Key Findings

Core contributions and results:

- The computed figures show where sensillum dimensions, CHC-associated mid-IR bands, and atmospheric windows overlap, but do not by themselves establish biological IR olfaction.
- The framework yields five preregistered falsifiers, including spectral nulls under matched thermal load and geometric mismatch between sensilla and predicted resonances.
- Published insect ORN timing is fast enough that any IR stage would need to be experimentally separated from already-rapid molecular responses.
- Beetle, kissing-bug, ant, cycad, and mosquito examples establish radiant IR sensing precedents but not direct semiochemical IR olfaction.
- On a CHC spectrum fixture, the paper's automated peak detection identifies CHC-associated bands that published ATR-FTIR work links to species discrimination; perceptual use of those bands remains to be tested.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2023_NSFReporting](../2023_NSFReporting/)
- [2023_NaturalAIBased](../2023_NaturalAIBased/)
- [2025_AuBI](../2025_AuBI/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.20450880
- PDF SHA-256: See zenodo_record
- Pairing confidence: strong
- Last checked: 2026-09-24T18:29:54Z

## Prerequisites

- Familiarity with insect olfaction, infrared detection, vibrational theory of olfaction
- Background in Computational fundamentals
- Access to source repository: docxology/cohereants

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.20450880`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
