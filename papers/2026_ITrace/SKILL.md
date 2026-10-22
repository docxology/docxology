---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "iTrace: verification-first webcam eye-movement analysis (corrected manuscript)"
description: "Archive note: The extracted image thumbnails are retained from itrace-0.4.1-manuscript.pdf and are not figures from the corrected 2026-10-16 manuscript. Use itrace-manuscript-2026-10-16.pdf or its pinned source archive for current figures. # iTrace m..."
tags: ["eye-tracking", "webcam", "gaze", "saccades", "pupillometry", "open-source", "diagnostic-pilot"]
domain: "Computational"
citation: "Daniel Ari Friedman (2026). *iTrace: verification-first webcam eye-movement analysis (corrected manuscript)*. Zenodo."
doi: "10.5281/zenodo.20614908"
artifact_doi: "10.5281/zenodo.23419306"
---

# iTrace: verification-first webcam eye-movement analysis (corrected manuscript)

**Daniel Ari Friedman** (2026) · Computational

## Context

This work addresses topics in **Computational**: eye-tracking, webcam, gaze, saccades.

## Methods

Primary methods and techniques applied in this work:

- **Hardware-decoupled analysis core** — The optional capture shell emits typed records consumed by a headless scientific-analysis core.
- **Constructed-ground-truth verification** — Headless tests exercise the algorithms on synthetic signals whose truth is supplied by construction.
- **Explicit caller-supplied benchmark truth** — Benchmark outputs report their truth boundary and distinguish comparator agreement from reference measurement.

## Key Findings

Core contributions and results:

- In the specified synthetic landmark-noise sweep, gaze remains below 2 deg RMS to sigma approximately 0.0048, about 3 pixels at 640-pixel width.
- One-to-one overlap-based saccade recovery falls below F1 = 0.8 near sigma 0.0014, about 0.92 pixels, in that synthetic sweep.
- The overlap result measures event recovery and does not establish timing accuracy.
- Pupil noise-sweep robustness is conditional on the assumed pupil-noise injection model.
- These results verify specified algorithms and internal geometry; they do not validate webcams as eye trackers.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2023_NSFReporting](../2023_NSFReporting/)
- [2023_NaturalAIBased](../2023_NaturalAIBased/)
- [2025_AuBI](../2025_AuBI/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.20614908
- PDF SHA-256: See zenodo_record
- Pairing confidence: manually_reviewed
- Last checked: 2026-10-16T21:46:48Z
- Artifact DOI: 10.5281/zenodo.23419306

## Prerequisites

- Familiarity with eye-tracking, webcam, gaze
- Background in Computational fundamentals
- Access to source repository: docxology/itrace

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.20614908`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
