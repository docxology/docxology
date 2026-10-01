<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 Template Madlib: Deterministic Token Injection for Conditional IMRAD Manuscripts

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20786638-blue)](https://doi.org/10.5281/zenodo.20786638)

---

## Abstract

> This exemplar asks whether a reviewable pipeline can hydrate a complete IMRAD manuscript from configuration-owned lexical data while preserving an audit trail that remains readable before and after rendering. The project deliberately keeps playful Mad Lib mechanics inside a serious reproducibility contract: the manuscript shell names large placeholders, the config declares allowable language, and...

## Keywords

`madlib generation` · `token injection` · `conditional manuscripts` · `reproducible research` · `IMRAD`

## Methods

- **Seeded SHA-256 digest selection of lexicon tokens per slot** — Each slot hashes the seed, slot name, category, ordinal and full category list; the digest indexes the configured lexicon category.
- **YAML config-owned lexicon, slots, and section conditions** — Lexicon categories, slots, section switches, method rows and claims are declared in YAML; source code turns them into manuscript bodies.
- **Staged pipeline from config validation to hydrated Markdown** — Validates the madlib block, builds a TokenPlan and section bodies, writes artifact JSON and a figure registry, then hydrates Markdown.
- **Explicit vs. loader-default config field-origin inventory** — Classifies configuration paths as explicitly set in YAML or inherited from loader defaults and reports them as method evidence.
- **Project tests and shared output validator** — Tests check determinism, seed and category sensitivity, malformed configs, section disablement and unresolved tokens; a validator checks rendered outputs.

## Key Findings

- With seed 431, the schema expands 22 slot rules into 40 token choices across 10 lexicon categories.
- The generated plan enabled all 11 manuscript sections and filled 40 token choices, each traced to its variable, category, section and config pointer.
- Re-running generation with seed 431 and the same lexicon produces the same token plan.
- The author frames the main result as traceability surviving a complete render path, not any particular word choice.
- The paper explicitly does not claim lexical replacement creates scholarship; it shows a conditional text generator can be made accountable to config, tests and validation.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [docxology/template_madlib](https://github.com/docxology/template_madlib)
- GitHub release: [v0.1.1](https://github.com/docxology/template_madlib/releases/tag/v0.1.1)
- DOI: [10.5281/zenodo.20786638](https://doi.org/10.5281/zenodo.20786638)
- Artifact DOI: [10.5281/zenodo.20932025](https://doi.org/10.5281/zenodo.20932025)
- Zenodo record: [https://zenodo.org/records/20786638](https://zenodo.org/records/20786638)
- PDF: [Friedman_2026_Template_a593c1fe.pdf](Friedman_2026_Template_a593c1fe.pdf)
- PDF: [Friedman_2026_Template_d9248f4f.pdf](Friedman_2026_Template_d9248f4f.pdf)
- PDF SHA-256: d9248f4f372fc3baf21cbf5cc5cdb7daffe0e22e62ac6fa2e3a697a26f3308b6

## Citation

> Daniel Ari Friedman (2026). *Template Madlib: Deterministic Token Injection for Conditional IMRAD Manuscripts*. Zenodo. DOI: 10.5281/zenodo.20786638. URL: https://doi.org/10.5281/zenodo.20786638.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
