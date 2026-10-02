<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 DemoCreate: Declarative Audio-Visual Demo Generation for Software

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20693216-blue)](https://doi.org/10.5281/zenodo.20693216)

---

## Abstract

> DemoCreate generates audio-visual demos of software — codebase tours, website walkthroughs, and terminal/CLI demos — from a single declarative, deterministic spine. A Demo is an ordered action stream plus narration chunks, merging CodeVideo's event-sourced virtual-IDE model with VSpeak's chunk/trigger model. Every heavy backend (TTS via Kokoro/Chatterbox, transcription via Whisper, capture via mss/Playwright, animation via Manim, assembly via MoviePy/ffmpeg) sits behind an abstract interface with a pure-Python deterministic default, so the package produces a real demo with only light dependencies and upgrades when extras are installed. On-screen actions are anchored to spoken trigger words via TTS→STT synchronization: narration audio is generated, transcribed back to word-level timestamps, and used to align the action stream with the narration.

## Keywords

`demo-generation` · `screencast` · `text-to-speech` · `code-walkthrough` · `video` · `narration` · `whisper` · `manim` · `playwright` · `reproducible` · `deterministic` · `tts-stt-synchronization`

## Methods

- **Declarative Demo schema of typed Actions and narration Chunks (JSON/YAML)** — Represents a demo as a validated value of scenes, narration chunks and typed actions that round-trips losslessly through JSON and YAML; rendering is a pure function of it.
- **Abstract backend interfaces with pure-Python deterministic defaults** — TTS, transcription, capture, assembly and PDF ingestion each sit behind an abstract interface whose 'auto' factory resolves to a light default; heavy backends are guarded.
- **TTS-to-STT round-trip with fuzzy trigger-word anchoring** — Narration is synthesized, transcribed back to word-level timestamps, and each action's trigger_word is fuzzy-matched to get an absolute millisecond timestamp.
- **Poppler-CLI paper subsystem for research-paper demos** — Reads a PDF with poppler utilities to extract title, abstract (skipping the TOC), captions, sections, figures and pages, and composes them into a narrated demo.
- **Real-filesystem test suite, content verifier and benchmark file** — Evaluates the package with a coverage-gated test suite, a verifier that checks rendered video has non-silent, non-black streams, and a reproducible benchmark file.

## Key Findings

- Across 51 source modules in 7 subsystems, 625 tests pass (3 skipped) under a ≥90% coverage gate, achieving roughly 95%.
- The recorded benchmark reports a 25.8 ms median build and 256.7 ms of render compute per second of output, with complete, monotonic sync timestamps.
- DemoCreate produced two content-verified 1080p H.264 videos: a 128.4 s self-explaining package demo and a 188.0 s demo of a 170-page paper.
- The author states DemoCreate is narrower than agentic generators and less specialized than asciinema for terminals, but uniquely combines declarative, deterministic, narrated, paper-capable demos.
- The steganographic provenance payload survives only in lossless PNG sidecars; H.264 encoding destroys it, so the MP4 carries provenance via container tags and on-screen bars.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [docxology/democreate](https://github.com/docxology/democreate)
- GitHub release: [v0.6.2](https://github.com/docxology/democreate/releases/tag/v0.6.2)
- DOI: [10.5281/zenodo.20693216](https://doi.org/10.5281/zenodo.20693216)
- Zenodo record: [https://zenodo.org/records/20693216](https://zenodo.org/records/20693216)
- PDF: [democreate-0.6.2-manuscript.pdf](democreate-0.6.2-manuscript.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/20693216)

## Citation

> Daniel Ari Friedman (2026). *DemoCreate: Declarative Audio-Visual Demo Generation for Software*. Zenodo. DOI: 10.5281/zenodo.20693216. URL: https://doi.org/10.5281/zenodo.20693216.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
