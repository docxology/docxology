# Manuscript - docxology

This directory contains a source-backed technical draft for:

**docxology: Research, Software, and Citation Index**

A public profile repository indexing bibliography, software, generated GitHub inventory, and research documentation across entomology, active inference, cognitive security, and art/synergetics. The draft describes this repository system; archived publications remain under [`papers/`](../../papers/).

Read [`MANUSCRIPT_STATUS.md`](MANUSCRIPT_STATUS.md) for the evidence and rendering boundary. The architecture and configuration map is in [`development.md`](../operations/development.md).

## File Inventory

- `config.yaml`
- `preamble.md`
- `references.bib`
- `00_abstract.md`
- `01_introduction.md`
- `02_system_context.md`
- `03_methods.md`
- `04_artifacts_and_evidence.md`
- `05_reproducibility.md`
- `06_limitations_and_next_steps.md`
- `S01_source_surface.md`
- `98_symbols_glossary.md`
- `99_references.md`
- `AGENTS.md`
- `README.md`
- `SYNTAX.md`
- `MANUSCRIPT_STATUS.md`

## Source Surfaces

| Surface | Role |
|---|---|
| [`pages/`](../../pages/) | Curated bibliography, software catalog, profile, and discovery documentation |
| [`papers/`](../../papers/) | Archived source documents, extracted text, and per-paper documentation |
| [`code/`](../../code/) | Executable generation, validation, intake, and browser tests |
| [`reports/`](../../reports/) | Dated source observations and scoped QA evidence |
| [`resume/`](../../resume/) | Structured CV authority and generated exports |
| [`works/`](../../works/) | Generated permanent work landing pages |
| [`data/`](../../data/) | Identity reservations, cached observations, structured exports, and release controls |

## Verification

From this repository root:

```bash
uv run python3 code/orchestrators/validate_manuscript.py
uv run python3 code/orchestrators/validate_manuscript.py --json
```

The read-only validator checks root-relative configuration, section labels, citation-key resolution, unresolved tokens, cross-references, and local references, including reference-style links/images. It checks bounded BibTeX entry delimiters and key inventory, rejecting unclosed entries, stray text, duplicate keys, and unresolved citations. It rejects duplicate YAML keys and non-boolean gate/render settings. It does not validate complete BibTeX field grammar, citation style, TeX rendering, external sources, or publication readiness. `--root PATH` supports disposable repository fixtures; JSON goes to stdout without creating a receipt.

The declared formats in `config.yaml` are requested rendering targets. This repository does not currently declare a manuscript rendering command. A future rendering integration must specify its pinned runtime, output location, cross-reference support, figure handling, and inspected artifact before a rendered-publication claim is added.
