---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "iTrace: verification-first webcam eye-movement analysis"
description: "iTrace is an MIT-licensed Python toolkit for webcam-derived gaze, saccade, pupil, and quality diagnostics. Version 0.4.1 is a diagnostic v1 release: the pure NumPy/SciPy core is algorithmically verified against synthetic and closed-loop oracles, the ..."
tags: ["eye-tracking", "webcam", "gaze", "saccades", "pupillometry", "open-source", "diagnostic-pilot"]
domain: "Computational"
citation: "Daniel Ari Friedman (2026). *iTrace: verification-first webcam eye-movement analysis*. Zenodo."
doi: "10.5281/zenodo.20614908"
artifact_doi: "10.5281/zenodo.20614909"
---

# iTrace: verification-first webcam eye-movement analysis

**Daniel Ari Friedman** (2026) · Computational

## Context

This work addresses topics in **Computational**: eye-tracking, webcam, gaze, saccades.

## Methods

Primary methods and techniques applied in this work:

- **Hardware-decoupled pure NumPy/SciPy analysis core with optional capture shell** — Gaze geometry, I-VT/I-DT, Engbert-Kliegl microsaccade, main-sequence and pupil algorithms run headlessly, separate from an optional webcam/MediaPipe shell.
- **Verification against synthetic traces with ground truth held out by construction** — Every detector is tested on generated signals whose events are known, e.g. a 250 Hz fixation-saccade-fixation trace and an embedded 0.5 deg microsaccade.
- **3-D eyeball forward model closed loop through a pinhole camera** — Known gaze is projected to landmarks and back through the estimator on an animated 120 Hz scene to check geometric internal consistency.
- **Seeded Monte-Carlo landmark-noise sweep (sigma 0-0.016, 25 trials/level)** — Independent landmark noise is injected into the synthetic scene to rank fragility of gaze, saccade and pupil recovery, with bootstrap confidence intervals.
- **N=1 single-participant, single-device webcam pilot sessions** — One local webcam workflow recorded fixed-gaze, reading and target trials as derived records to give order-of-magnitude session diagnostics.

## Key Findings

Core contributions and results:

- On synthetic traces the I-VT detector recovered a 10 deg saccade's amplitude within 5% and peak velocity within 10%.
- The 3-D closed loop recovered gaze with 0.16 deg RMS residual (max 0.23 deg); the author states this is internal consistency, not device validation.
- In the idealised noise sweep, saccade detection was most fragile (F1 < 0.8 at sigma about 0.0014), while gaze crossed the 2 deg bound near sigma 0.005.
- The pupil noise robustness is reported only as a conditional illustration because it follows from the assumed pupil noise model.
- The headline limitation is an unclosed device validation gap: correctness rests on constructed ground truth, not reference measurements of real eyes.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2023_NSFReporting](../2023_NSFReporting/)
- [2023_NaturalAIBased](../2023_NaturalAIBased/)
- [2025_AuBI](../2025_AuBI/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.20614908
- PDF SHA-256: See zenodo_record
- Pairing confidence: needs_review
- Last checked: 2026-06-09T18:22:02Z
- Artifact DOI: 10.5281/zenodo.20614909

## Prerequisites

- Familiarity with eye-tracking, webcam, gaze
- Background in Computational fundamentals
- Access to source repository: docxology/itrace

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.20614908`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
