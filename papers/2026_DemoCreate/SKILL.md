---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "DemoCreate: Declarative Audio-Visual Demo Generation for Software"
description: "<p>DemoCreate generates audio-visual demos of software &mdash; codebase tours, website walkthroughs, and terminal/CLI demos &mdash; from a single declarative, deterministic spine. A Demo is an ordered action stream plus narration chunks, merging Code..."
tags: ["demo-generation", "screencast", "text-to-speech", "code-walkthrough", "video", "narration", "whisper", "manim", "playwright", "reproducible"]
domain: "Computational"
citation: "Daniel Ari Friedman (2026). *DemoCreate: Declarative Audio-Visual Demo Generation for Software*. Zenodo."
doi: "10.5281/zenodo.20693216"
---

# DemoCreate: Declarative Audio-Visual Demo Generation for Software

**Daniel Ari Friedman** (2026) · Computational

## Context

This work addresses topics in **Computational**: demo-generation, screencast, text-to-speech, code-walkthrough.

## Methods

Primary methods and techniques applied in this work:

- **Declarative Demo schema of typed Actions and narration Chunks (JSON/YAML)** — Represents a demo as a validated value of scenes, narration chunks and typed actions that round-trips losslessly through JSON and YAML; rendering is a pure function of it.
- **Abstract backend interfaces with pure-Python deterministic defaults** — TTS, transcription, capture, assembly and PDF ingestion each sit behind an abstract interface whose 'auto' factory resolves to a light default; heavy backends are guarded.
- **TTS-to-STT round-trip with fuzzy trigger-word anchoring** — Narration is synthesized, transcribed back to word-level timestamps, and each action's trigger_word is fuzzy-matched to get an absolute millisecond timestamp.
- **Poppler-CLI paper subsystem for research-paper demos** — Reads a PDF with poppler utilities to extract title, abstract (skipping the TOC), captions, sections, figures and pages, and composes them into a narrated demo.
- **Real-filesystem test suite, content verifier and benchmark file** — Evaluates the package with a coverage-gated test suite, a verifier that checks rendered video has non-silent, non-black streams, and a reproducible benchmark file.

## Key Findings

Core contributions and results:

- Across 51 source modules in 7 subsystems, 625 tests pass (3 skipped) under a ≥90% coverage gate, achieving roughly 95%.
- The recorded benchmark reports a 25.8 ms median build and 256.7 ms of render compute per second of output, with complete, monotonic sync timestamps.
- DemoCreate produced two content-verified 1080p H.264 videos: a 128.4 s self-explaining package demo and a 188.0 s demo of a 170-page paper.
- The author states DemoCreate is narrower than agentic generators and less specialized than asciinema for terminals, but uniquely combines declarative, deterministic, narrated, paper-capable demos.
- The steganographic provenance payload survives only in lossless PNG sidecars; H.264 encoding destroys it, so the MP4 carries provenance via container tags and on-screen bars.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2023_NSFReporting](../2023_NSFReporting/)
- [2023_NaturalAIBased](../2023_NaturalAIBased/)
- [2025_AuBI](../2025_AuBI/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.20693216
- PDF SHA-256: See zenodo_record
- Pairing confidence: strong
- Last checked: 2026-09-24T18:29:55Z

## Prerequisites

- Familiarity with demo-generation, screencast, text-to-speech
- Background in Computational fundamentals
- Access to source repository: docxology/democreate

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.20693216`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
