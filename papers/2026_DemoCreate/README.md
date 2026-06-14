# DemoCreate: Declarative Audio-Visual Demo Generation for Software

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20693217.svg)](https://doi.org/10.5281/zenodo.20693217)

---

## Abstract

DemoCreate generates audio-visual demos of software &mdash; codebase tours, website walkthroughs, and terminal/CLI demos &mdash; from a single declarative, deterministic spine. A Demo is an ordered action stream plus narration chunks, merging CodeVideo's event-sourced virtual-IDE model with VSpeak's chunk/trigger model. Every heavy backend (TTS via Kokoro/Chatterbox, transcription via Whisper, capture via mss/Playwright, animation via Manim, assembly via MoviePy/ffmpeg) sits behind an abstract interface with a pure-Python deterministic default, so the package produces a real demo with only light dependencies and upgrades when extras are installed. On-screen actions are anchored to spoken trigger words via TTS&rarr;STT synchronization: narration audio is generated, transcribed back to word-level timestamps, and used to align the action stream with the narration.

## Keywords

demo-generation · screencast · text-to-speech · code-walkthrough · video · narration · whisper · manim · playwright · reproducible · deterministic · tts-stt-synchronization · virtual-ide

## Publication Details

| Field | Value |
|------|-------|
| **DOI** | [10.5281/zenodo.20693217](https://doi.org/10.5281/zenodo.20693217) |
| **Published** | 2026-06-04 |
| **Version** | 0.6.2 |
| **Zenodo record** | https://zenodo.org/records/20693217 |

## Files

- `democreate-0.6.2-manuscript.pdf` - Zenodo PDF

## Citation

> Daniel Ari Friedman (2026). *DemoCreate: Declarative Audio-Visual Demo Generation for Software*. Zenodo. https://doi.org/10.5281/zenodo.20693217

## Related

- Zenodo record: https://zenodo.org/records/20693217
- [Full Bibliography](../../pages/BIBLIOGRAPHY.md) · [All Papers](../README.md)
