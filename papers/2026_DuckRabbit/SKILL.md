---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "DuckRabbit: Typed Multimodal Illusion Generator"
description: "DuckRabbit is typed, deterministic research software by Daniel Ari Friedman (Active Inference Institute) for constructing reproducible visual, auditory, temporal, and audiovisual stimulus families. The intended public release will be available at the..."
tags: ["perceptual-illusions", "cognitive-taxonomy", "audio-visual-stimuli", "deterministic-generation", "typed-parameters", "research-software", "reproducible-research", "psychophysics"]
domain: "Computational"
citation: "Daniel Ari Friedman (2026). *DuckRabbit: Typed Multimodal Illusion Generator*. Zenodo."
doi: "10.5281/zenodo.21419693"
---

# DuckRabbit: Typed Multimodal Illusion Generator

**Daniel Ari Friedman** (2026) · Computational

## Context

This work addresses topics in **Computational**: perceptual illusions, cognitive taxonomy, audio-visual stimuli, deterministic generation.

## Methods

Primary methods and techniques applied in this work:

- **Typed immutable stimulus request (identifier, parameters, seed, encoding)** — Each stimulus is generated from an immutable request whose value objects validate finite parameter ranges, yielding a canonical image, audio, video or audiovisual artifact.
- **Canonical little-endian float32 serialization with SHA digests and v2 manifests** — Canonical arrays plus shape, clock and units are hashed independently of PNG/WAV/GIF/MP4/NPZ delivery, and a v2 manifest records parameters, metrics and verification status.
- **Encode-decode verification with format-specific tolerances** — Delivered files are decoded and checked against canonical facts; PNG, GIF, WAV and NPZ use local adapters while MP4 uses an optional ffmpeg backend.
- **Objective media metrics (luminance, RMS, spectral centroid, frame deltas, sync offsets)** — Computes physical or decoded-media metrics with units and computation versions, explicitly kept separate from observer responses.
- **Hand-specified synthetic feature observer (logistic, human_data=false)** — A serialized feature observer with fixed weights and temperature exercises analysis orchestration across parameter sweeps; it is not trained or calibrated on humans.

## Key Findings

Core contributions and results:

- Version 0.5.0 contains 17 implemented generators and 18 catalog entries, supported by 36 source records and 18 evidence records.
- The publication workflow generates 15 publication figures and 10 machine-derived tables from the live registry.
- The package is framed around falsifiable engineering hypotheses, including that identical typed requests yield identical canonical arrays and digests.
- The author states the validation suite establishes software repeatability, not replicability of an observer effect under new displays, populations or tasks.
- No participant data are bundled; the synthetic observer output is explicitly nonhuman and does not estimate human thresholds or effect sizes.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

See [BIBLIOGRAPHY.md](../../pages/BIBLIOGRAPHY.md) for related publications.

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.21419693
- PDF SHA-256: See zenodo_record
- Pairing confidence: strong
- Last checked: 2026-09-24T18:29:58Z

## Prerequisites

- Familiarity with perceptual illusions, cognitive taxonomy, audio-visual stimuli
- Background in Computational fundamentals
- Access to source repository: docxology/DuckRabbit

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.21419693`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
