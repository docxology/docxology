<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 iTrace: verification-first webcam eye-movement analysis

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20614908-blue)](https://doi.org/10.5281/zenodo.20614908)

---

## Abstract

> iTrace is an MIT-licensed Python toolkit for webcam-derived gaze, saccade, pupil, and quality diagnostics. Version 0.4.1 is a diagnostic v1 release: the pure NumPy/SciPy core is algorithmically verified against synthetic and closed-loop oracles, the optional webcam shell exports derived records, and the empirical ledger covers a single-participant, single-device, five-session diagnostic pilot. This release does not claim reference-device accuracy, cross-device generality, population generality, or webcam-accuracy validation.

## Keywords

`eye-tracking` · `webcam` · `gaze` · `saccades` · `pupillometry` · `open-source` · `diagnostic-pilot`

## Methods

- **Hardware-decoupled pure NumPy/SciPy analysis core with optional capture shell** — Gaze geometry, I-VT/I-DT, Engbert-Kliegl microsaccade, main-sequence and pupil algorithms run headlessly, separate from an optional webcam/MediaPipe shell.
- **Verification against synthetic traces with ground truth held out by construction** — Every detector is tested on generated signals whose events are known, e.g. a 250 Hz fixation-saccade-fixation trace and an embedded 0.5 deg microsaccade.
- **3-D eyeball forward model closed loop through a pinhole camera** — Known gaze is projected to landmarks and back through the estimator on an animated 120 Hz scene to check geometric internal consistency.
- **Seeded Monte-Carlo landmark-noise sweep (sigma 0-0.016, 25 trials/level)** — Independent landmark noise is injected into the synthetic scene to rank fragility of gaze, saccade and pupil recovery, with bootstrap confidence intervals.
- **N=1 single-participant, single-device webcam pilot sessions** — One local webcam workflow recorded fixed-gaze, reading and target trials as derived records to give order-of-magnitude session diagnostics.

## Key Findings

- On synthetic traces the I-VT detector recovered a 10 deg saccade's amplitude within 5% and peak velocity within 10%.
- On the synthetic 3-D closed loop, gaze was recovered with 0.16 deg RMS residual (max 0.23 deg) for gaze within ±15 deg; the author states this is internal consistency, not device validation.
- In the idealised noise sweep, saccade detection was most fragile (F1 < 0.8 at sigma about 0.0014), while gaze crossed the 2 deg bound near sigma 0.005.
- The pupil noise robustness is reported only as a conditional illustration because it follows from the assumed pupil noise model.
- The headline limitation is an unclosed device validation gap: correctness rests on constructed ground truth, not reference measurements of real eyes.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [docxology/itrace](https://github.com/docxology/itrace)
- GitHub release: [v0.4.1](https://github.com/docxology/itrace/releases/tag/v0.4.1)
- DOI: [10.5281/zenodo.20614908](https://doi.org/10.5281/zenodo.20614908)
- Artifact DOI: [10.5281/zenodo.20614909](https://doi.org/10.5281/zenodo.20614909)
- Zenodo record: [https://zenodo.org/records/20614909](https://zenodo.org/records/20614909)
- PDF: [itrace-0.4.1-manuscript.pdf](itrace-0.4.1-manuscript.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/20614909)

## Citation

> Daniel Ari Friedman (2026). *iTrace: verification-first webcam eye-movement analysis*. Zenodo. DOI: 10.5281/zenodo.20614908. URL: https://doi.org/10.5281/zenodo.20614908.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
