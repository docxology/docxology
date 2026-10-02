<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 Refinement of Gold: A Metallurgical Analogy for Scientific Manuscript Composition

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20931955-blue)](https://doi.org/10.5281/zenodo.20931955)

---

## Abstract

> This paper presents a metallurgical analogy for scientific manuscript composition, mapping gold-refining stages onto the template infrastructure pipeline. The refinery processes manuscript ore through 5 stages — from raw draft (9K, ~37.5% purity) through smelting, assaying, and cupellation — to nine-nines certification (99.9999999%), the ultra-high-purity standard of electronics-grade gold. The analogy is load-bearing, not merely rhetorical: each metallurgical stage corresponds to a real template-infrastructure operation. Smelting removes dross (filler, unsupported claims); assaying tests claims against evidence; cupellation resolves cross-references; certification validates the full pipeline. The mega-madlib token engine selects 8 domain tokens deterministically via seeded SHA-256 digest over category inventories, ensuring every prose element is traceable and reproducible. Results: The refinery achieves final purity of 99.9999999% (nine-nines) (24K (nine-nines certified)) with a total purity gain of 90.00% across all stages. Nine-nines certification: Yes. The purity progression is shown in , and the karat grading scale in . Keywords: gold refining, manuscript composition, mega-madlib, token injection, scientific purity, assaying, karat grading

## Keywords

`gold refining` · `manuscript composition` · `mega-madlib` · `token injection` · `scientific purity` · `assaying` · `karat grading`

## Methods

- **Five-stage gold-refining analogy mapped to manuscript operations** — Maps ore, smelting, assaying, cupellation, and certification onto manuscript template-infrastructure operations such as claim removal, evidence checks, and cross-reference resolution.
- **Seeded SHA-256 mega-madlib token selection from a config-owned lexicon** — Selects domain vocabulary tokens deterministically from lexicon categories declared in config.yaml so every prose token is traceable to its config key.
- **Monotone-purity constraint enforced in code and tests** — Stage purity values must strictly increase, enforced by assert_monotone_increase in src/refinery.py and covered by the test suite.
- **Karat grading of stage purities via karat_for_purity()** — Maps each stage's purity fraction to a standard gold fineness grade (9K to 24K and nine-nines) in src/purity.py.
- **Deterministic seeded regeneration of all outputs** — The pipeline regenerates figures, data, and reports from the same config and source code; the reported run used seed 431.

## Key Findings

- The paper argues the analogy is load-bearing rather than only rhetorical, since each metallurgical stage corresponds to a real template-infrastructure operation.
- The exemplar pipeline reports a monotone purity sequence over 5 stages ending at the nine-nines certification stage.
- The token engine generated 8 tokens from seed 431 across 4 lexicon categories, each traceable in a provenance table.
- The paper explicitly does not claim empirical validation of manuscript quality metrics or generalizability of its purity fractions.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [docxology/template_gold_refinement](https://github.com/docxology/template_gold_refinement)
- GitHub release: [v0.1.0](https://github.com/docxology/template_gold_refinement/releases/tag/v0.1.0)
- DOI: [10.5281/zenodo.20931955](https://doi.org/10.5281/zenodo.20931955)
- Zenodo record: [https://zenodo.org/records/20931955](https://zenodo.org/records/20931955)
- PDF: [Friedman_2026_Refinement_36431789.pdf](Friedman_2026_Refinement_36431789.pdf)
- PDF SHA-256: 3643178951b267632e607606b6daaba21ea75d8f7590899948b5999d1854198b

## Citation

> Daniel Ari Friedman (2026). *Refinement of Gold: A Metallurgical Analogy for Scientific Manuscript Composition*. Zenodo. DOI: 10.5281/zenodo.20931955. URL: https://doi.org/10.5281/zenodo.20931955.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
