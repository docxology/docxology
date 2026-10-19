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

The PDF uses the native `PDFRenderer.render_combined` API from the committed
docxology/template revision pinned in `config.yaml`. Pandoc 3.12.1 and
pandoc-crossref 0.3.26 (built against that Pandoc) serve all formats; the native
PDF additionally requires XeTeX 3.141592653-2.6-0.999998 and BibTeX 0.99e.
Provide a local template Git repository containing that commit and a qualified
Python interpreter with its dependencies. The command exports committed source
and does not import or modify the template working tree or install packages.

```bash
uv run python3 code/orchestrators/render_manuscript.py \
  --template-root /path/to/template \
  --template-python /path/to/template-environment/bin/python \
  --output-dir /path/to/new-review --json
```

The external parent must exist without symlink ancestors; existing review
directories are never overwritten. The renderer validates structure, freezes
source bytes, rejects raw body markup and undeclared images, binds repository
links to HEAD, and parses the bibliography with Pandoc. A declared deterministic
vector producer writes the native cover under staged `docs/output/figures/`.
The cover illustrates source authority, shared policy, generated views, and
release evidence without asserting quantitative results. The reviewed
`preamble.md` is an executed, hash-bound PDF input.

The native worker runs with isolated Python imports, an environment allowlist,
and a bounded process group lifetime. Trusted template code and TeX still
execute; these controls are not a network or OS sandbox. Required tools and
unresolved bibliography/reference diagnostics fail closed. The receipt binds
template source/dependency metadata, the actual external runtime, staged
transformations, source/tool/cover/output hashes, and pending human/editorial
review. The declared body-diagram registry is integrated; arbitrary images and Mermaid require a separate reviewed producer.

HTML, EPUB3, and PowerPoint retain the Pandoc/citeproc renderer. All four formats
are manual review artifacts, excluded from normal site regeneration. Manuscript
text and original figures use CC BY 4.0; archived papers, software, artwork, and
linked third-party material retain their own rights.

Run the real integration explicitly with the same template inputs:

```bash
DOCXOLOGY_TEST_RENDER=1 DOCXOLOGY_TEMPLATE_ROOT=/path/to/template \
DOCXOLOGY_TEMPLATE_PYTHON=/path/to/template-environment/bin/python \
  uv run python3 -m pytest code/tests/test_manuscript_rendering.py -q
```

Ordinary tests skip the native integration. Successful rendering and assistant
layout inspection do not establish scientific validity, human approval, or
publication readiness. Inspect each requested format before external release.


## Body diagrams

The declared `repository-method-diagrams-v1` producer renders four explanatory
diagrams: architecture, progressive loading, evidence boundaries, and the release
path. The registry in `code/src/manuscript_figures.py` is the sole authority for
their virtual `../output/figures/*.png` source targets. Structural validation
recognizes only that exact registry/configuration; it does not claim asset creation.
Explicit rendering creates vector PDFs and offline PNG companions outside the
checkout. The native PDF uses vectors; HTML, EPUB and slides use PNG companions.
The receipt binds producer code, runtime versions and every asset hash. Unknown,
remote or arbitrary image inputs remain unsupported. Install the `pdf-extraction`
extra for the PNG rasterizer. These diagrams explain implementation contracts and
are not measurements or scientific results.
