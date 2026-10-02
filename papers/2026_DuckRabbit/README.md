<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 DuckRabbit: Typed Multimodal Illusion Generator

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21419693-blue)](https://doi.org/10.5281/zenodo.21419693)

---

## Abstract

> DuckRabbit is typed, deterministic research software by Daniel Ari Friedman (Active Inference Institute) for constructing reproducible visual, auditory, temporal, and audiovisual stimulus families. The intended public release will be available at the following repository: https://github.com/docxology/DuckRabbit DuckRabbit is released under the MIT License. Its basic unit is an immutable request containing an illusion identifier, validated parameters, a seed, and an encoding specification. The request yields a canonical artifact, objective media measurements, and a versioned provenance manifest before any delivery codec is selected. This separation makes the stimulus a testable computational object while reserving claims about perception for controlled observer protocols. The release situates its engineering choices within a deliberately broad historical foundation spanning Greek, Arabic/Islamicate, Chinese, and early-modern work on optics, visual inference, and cross-sensory knowledge, alongside later psychophysics and illusion research. These traditions motivate questions about construction, observation, and evidence; they are contextual precedents, not evidence that a generated file reproduces an ancient, early-modern, or clinical observation. Version 0.5.0 contains 17 implemented generators and 18 catalog entries, supported by 36 source records and 18 evidence records in a checked-in audit snapshot. The package generates 15 publication figures and 10 machine-derived tables from the live registry. It also provides a typed observer-study harness and a transparent synthetic diagnostic: a hand-specified feature observer with serialized weights, temperature, analytic calibration, and human_data=false. No participant data are bundled; synthetic model output is explicitly nonhuman. DuckRabbit verifies physical stimulus properties, media round trips, hashes, timing, and declared provenance. It does not infer a universal percept, effect size, or cross-device perceptual equivalence from a generated artifact. Its contribution is a reproducibility and epistemic boundary: source-backed family descriptions, deterministic media facts, and future observer hypotheses remain different typed records rather than being collapsed into one claim. DuckRabbit is software for reproducible stimulus construction and audit, not a claim that a generated file alone produces a universal perceptual effect.

## Keywords

`perceptual illusions` · `cognitive taxonomy` · `audio-visual stimuli` · `deterministic generation` · `typed parameters` · `research software` · `reproducible research` · `psychophysics`

## Methods

- **Typed immutable stimulus request (identifier, parameters, seed, encoding)** — Each stimulus is generated from an immutable request whose value objects validate finite parameter ranges, yielding a canonical image, audio, video or audiovisual artifact.
- **Canonical little-endian float32 serialization with SHA digests and v2 manifests** — Canonical arrays plus shape, clock and units are hashed independently of PNG/WAV/GIF/MP4/NPZ delivery, and a v2 manifest records parameters, metrics and verification status.
- **Encode-decode verification with format-specific tolerances** — Delivered files are decoded and checked against canonical facts; PNG, GIF, WAV and NPZ use local adapters while MP4 uses an optional ffmpeg backend.
- **Objective media metrics (luminance, RMS, spectral centroid, frame deltas, sync offsets)** — Computes physical or decoded-media metrics with units and computation versions, explicitly kept separate from observer responses.
- **Hand-specified synthetic feature observer (logistic, human_data=false)** — A serialized feature observer with fixed weights and temperature exercises analysis orchestration across parameter sweeps; it is not trained or calibrated on humans.

## Key Findings

- Version 0.5.0 contains 17 implemented generators and 18 catalog entries, supported by 36 source records and 18 evidence records.
- The publication workflow generates 15 publication figures and 10 machine-derived tables from the live registry.
- The package is framed around falsifiable engineering hypotheses, including that identical typed requests yield identical canonical arrays and digests.
- The author states the validation suite establishes software repeatability, not replicability of an observer effect under new displays, populations or tasks.
- No participant data are bundled; the synthetic observer output is explicitly nonhuman and does not estimate human thresholds or effect sizes.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [docxology/DuckRabbit](https://github.com/docxology/DuckRabbit)
- GitHub release: [v0.5.0](https://github.com/docxology/DuckRabbit/releases/tag/v0.5.0)
- DOI: [10.5281/zenodo.21419693](https://doi.org/10.5281/zenodo.21419693)
- Zenodo record: [https://zenodo.org/records/21419693](https://zenodo.org/records/21419693)
- PDF: [Friedman_2026_Duckrabbit_3afefaee.pdf](Friedman_2026_Duckrabbit_3afefaee.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/21419693)

## Citation

> Daniel Ari Friedman (2026). *DuckRabbit: Typed Multimodal Illusion Generator*. Zenodo. DOI: 10.5281/zenodo.21419693. URL: https://doi.org/10.5281/zenodo.21419693.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
