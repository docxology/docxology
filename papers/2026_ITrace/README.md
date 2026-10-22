<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 iTrace: verification-first webcam eye-movement analysis (corrected manuscript)

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20614908-blue)](https://doi.org/10.5281/zenodo.20614908)

---

## Abstract

> Archive note: The extracted image thumbnails are retained from itrace-0.4.1-manuscript.pdf and are not figures from the corrected 2026-10-16 manuscript. Use itrace-manuscript-2026-10-16.pdf or its pinned source archive for current figures.
>
> # iTrace manuscript revision, 2026-10-16 This deposit archives the corrected 30-page manuscript from reviewed commit `310be17ace8ae61621afe01329356427a3e6c861`. Exact source and figure artifacts are at https://github.com/docxology/itrace/tree/310be17ace8ae61621afe01329356427a3e6c861. It is a manuscript revision after the immutable v0.5.0 release, not a new package release. The package version in that source remains 0.5.0. The previous release remains at https://doi.org/10.5281/zenodo.23403300. References in the manuscript to that DOI identify the archived baseline. Changes correct overlap scoring, resampling and fit uncertainty, fitted-null diagnostics, uncertainty figures, scholarship, and scientific interpretation. The manuscript distinguishes synthetic verification from real-device validation. No new participant or reference-device data are claimed. Verification: 737 tests passed, 2 skipped, 91.05% combined statement-and-branch coverage; 44 final artifact tests passed, independent review approved the exact source commit, and all ten hosted CI jobs passed. The included figure manifest inventories 41 artifacts in the linked source tree. `provenance.json` binds this PDF to the Git commit; `SHA256SUMS` inventories every payload.

## Keywords

`eye-tracking` · `webcam` · `gaze` · `saccades` · `pupillometry` · `open-source` · `diagnostic-pilot`

## Methods

- **Hardware-decoupled analysis core** — The optional capture shell emits typed records consumed by a headless scientific-analysis core.
- **Constructed-ground-truth verification** — Headless tests exercise the algorithms on synthetic signals whose truth is supplied by construction.
- **Explicit caller-supplied benchmark truth** — Benchmark outputs report their truth boundary and distinguish comparator agreement from reference measurement.

## Key Findings

- In the specified synthetic landmark-noise sweep, gaze remains below 2 deg RMS to sigma approximately 0.0048, about 3 pixels at 640-pixel width.
- One-to-one overlap-based saccade recovery falls below F1 = 0.8 near sigma 0.0014, about 0.92 pixels, in that synthetic sweep.
- The overlap result measures event recovery and does not establish timing accuracy.
- Pupil noise-sweep robustness is conditional on the assumed pupil-noise injection model.
- These results verify specified algorithms and internal geometry; they do not validate webcams as eye trackers.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [docxology/itrace](https://github.com/docxology/itrace)
- GitHub release: [v0.5.0](https://github.com/docxology/itrace/releases/tag/v0.5.0)
- DOI: [10.5281/zenodo.20614908](https://doi.org/10.5281/zenodo.20614908)
- Artifact DOI: [10.5281/zenodo.23419306](https://doi.org/10.5281/zenodo.23419306)
- Zenodo record: [https://zenodo.org/records/20614908](https://zenodo.org/records/20614908)
- PDF: [itrace-0.4.1-manuscript.pdf](itrace-0.4.1-manuscript.pdf)
- PDF: [itrace-manuscript-2026-10-16.pdf](itrace-manuscript-2026-10-16.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/20614908)

## Citation

> Daniel Ari Friedman (2026). *iTrace: verification-first webcam eye-movement analysis (corrected manuscript)*. Zenodo. DOI: 10.5281/zenodo.20614908. URL: https://doi.org/10.5281/zenodo.20614908.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
