<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 SynthOBS & FractiSynth: A Golden-Ratio OBS Broadcast Console and Native Transducer

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21418782-blue)](https://doi.org/10.5281/zenodo.21418782)

---

## Abstract

> A tested Python reference engine, native libobs plugin, and obspython bridge for a telemetry-driven broadcast console. Includes deterministic figures, a versioned live OBS evidence bundle, fail-closed telemetry contracts, and a research-grade technical design manuscript. 1217 tests passing, 96.09% coverage on src/synthobs. Source: https://github.com/docxology/SynthOBS/releases/tag/v1.618.0. This version replaces the PDF with one that carries its own DOI on the cover/citation page (the v1 PDF referenced the DOI only externally).

## Keywords

`OBS Studio` · `libobs` · `reproducible research software` · `space-weather telemetry` · `real-time digital signal processing` · `software provenance` · `software citation`

## Methods

- **Dependency-free Python reference engine (src/synthobs/)** — Geometry, telemetry gates, DSP, console shape, and command grammar are defined in Python with no OBS or third-party runtime imports, serving as the portable source of truth.
- **Native libobs C plugin (FractiSynth) with libcurl-backed telemetry** — A separate C implementation applies the engine's declared video and audio contracts at the OBS host boundary.
- **Golden-ratio constant for viewport splits, video scale, limiter knee, spiral** — phi = 1.618 is used as an engineering parameter for layout and DSP contracts; the author explicitly treats it as a design choice.
- **Two-plane telemetry model from NOAA space-weather products** — An amplitude plane uses F10.7 cm radio flux and active-region counts, while an independent phase plane maps solar-wind speed through the EGS gateway key.
- **Live OBS acceptance protocol via obs-websocket with six gates** — A real OBS process and websocket connection are used to fit the console to canvas, capture compositor pixels, compare silent vs. tone audio, and inspect HUD provenance.

## Key Findings

- All six required live-OBS gates passed in the versioned run 20260717T153649Z.
- The materials table reports a test collection of 1217 tests with 96.09% coverage.
- The author states that the golden-ratio choices are engineering decisions and the manuscript does not infer perceptual or broadcast-quality benefits from them.
- The stated design proposition is narrow: a single pinned constant, fail-closed state transitions, and versioned captures make a cross-language OBS instrument easier to reason about and re-run.
- The two telemetry planes are designed to be independent, so a solar-wind dropout does not overwrite the SWO vector and invalid telemetry does not create a new lock.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.5281/zenodo.21418782](https://doi.org/10.5281/zenodo.21418782)
- Zenodo record: [https://zenodo.org/records/21418782](https://zenodo.org/records/21418782)
- PDF: [SynthOBS_v1.618.0.pdf](SynthOBS_v1.618.0.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/21418782)

## Citation

> Daniel Ari Friedman (2026). *SynthOBS & FractiSynth: A Golden-Ratio OBS Broadcast Console and Native Transducer*. Zenodo. DOI: 10.5281/zenodo.21418782. URL: https://doi.org/10.5281/zenodo.21418782.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
