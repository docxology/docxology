<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 When do bugs see (infra)red?

**Tucker Chambers, Daniel A. Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20450880-blue)](https://doi.org/10.5281/zenodo.20450880)

---

## Abstract

> Objective: To review the plausibility of insect detection of infrared (IR) cues that covary with semiochemical vibrational signatures, and to produce falsifiable predictions through the integration of comparative entomology, spectroscopy, neural timing analysis, and computational electromagnetism. The vibrational theory remains contested, so the framework treats IR/vibrational sensing as a testable complement to molecular recognition rather than a replacement for receptor binding . Methods: We integrate: (i) literature-grounded morphometric ranges for antennal sensilla, (ii) ATR-FTIR evidence that insect body chemistry can support species discrimination, (iii) published olfactory receptor neuron timing constraints, and (iv) deterministic electromagnetic models that expose their assumptions and parameter sensitivity . Preregistered experimental protocols specify QCL/LED bands (2--25 µm), thermal matched controls, power density 0.1--2 mW/cm², and N≥50 per condition. All analyses use fixed random seeds (42) where stochastic routines are present. Results: The computational figures show where sensillum-scale dimensions, CHC-associated mid-IR bands, and atmospheric windows overlap, but they do not by themselves establish biological IR olfaction. The strongest empirical anchors are narrower: fast insect ORN first-spike timing, photomechanic IR organs in pyrophilous beetles, hematophagy IR cues in mosquitoes and kissing bugs, thermogenic pollination signals in cycads, thermosensitive coeloconic sensilla in ants, and passive cuticle IR optics . These sources motivate specific experiments while also constraining the manuscript's range and mechanism claims. Conclusions: The framework yields five preregistered falsifiers aligned with \Cref{sec:discussion}: (1) spectral nulls under matched thermal load, (2) geometric mismatch between sensilla dimensions and predicted resonances, (3) environmental misalignment of CHC peaks with transmission windows, (4) temporal indistinguishability of IR versus thermal ORN latencies, and (5) behavioral independence of IR-only orientation from chemical gradients. Protocols specify QCL/LED bands (2--25 µm), matched power deposition, and N≥50 per condition to separate electromagnetic detection from thermal artifacts. Implications: Applications of this work include biomimetic IR sensor design, better-controlled pest-monitoring experiments, and clearer tests of whether insect olfactory systems ever use wavelength-specific electromagnetic information. Keywords: insect olfaction, infrared detection, vibrational theory, electromagnetic sensing, sensilla morphology, cuticular hydrocarbons, atmospheric transmission, biomimetic sensors Reproducibility: Complete implementation with seven case studies in Appendices

## Keywords

`insect olfaction` · `infrared detection` · `vibrational theory of olfaction` · `semiochemicals` · `sensilla morphology` · `electromagnetic sensing` · `active inference` · `reproducible research`

## Methods

- **Integration of literature morphometrics, ATR-FTIR evidence, ORN timing, and EM models** — Combines published sensilla ranges, FTIR insect-chemistry evidence, olfactory neuron timing constraints, and deterministic electromagnetic models.
- **Coarse atmospheric IR transmission window model with sensitivity terms** — A baseline window model plus humidity, temperature, scattering, and path-length terms, explicitly framed as a scenario generator.
- **Quarter-/half-wave resonance estimates for sensilla as dielectric antennas** — Representative sensilla classes, anchored to published Thripidae measurements, are compared against IR wavelengths via resonance and waveguide calculations.
- **Unit-tested deterministic code (CohereAnts) with fixed seeds and coverage gate** — All models are implemented in tested src/ modules with seed 42 and a 90% coverage gate, with seven appendix case studies.
- **Preregistered IR-only assay protocols with thermal-matched controls** — Specifies single-sensillum electrophysiology, behavioral IR-only assays, and SEM morphometrics with QCL/LED bands and N>=50 per condition.

## Key Findings

- The computed figures show where sensillum dimensions, CHC-associated mid-IR bands, and atmospheric windows overlap, but do not by themselves establish biological IR olfaction.
- The framework yields five preregistered falsifiers, including spectral nulls under matched thermal load and geometric mismatch between sensilla and predicted resonances.
- Published insect ORN timing is fast enough that any IR stage would need to be experimentally separated from already-rapid molecular responses.
- Beetle, kissing-bug, ant, cycad, and mosquito examples establish radiant IR sensing precedents but not direct semiochemical IR olfaction.
- On a CHC spectrum fixture, the paper's automated peak detection identifies CHC-associated bands that published ATR-FTIR work links to species discrimination; perceptual use of those bands remains to be tested.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [docxology/cohereants](https://github.com/docxology/cohereants)
- GitHub release: [v1.0.0](https://github.com/docxology/cohereants/releases/tag/v1.0.0)
- DOI: [10.5281/zenodo.20450880](https://doi.org/10.5281/zenodo.20450880)
- Zenodo record: [https://zenodo.org/records/20450880](https://zenodo.org/records/20450880)
- PDF: [cohereants_combined.pdf](cohereants_combined.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/20450880)

## Citation

> Tucker Chambers, Daniel A. Friedman (2026). *When do bugs see (infra)red?*. Zenodo. DOI: 10.5281/zenodo.20450880. URL: https://doi.org/10.5281/zenodo.20450880.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
