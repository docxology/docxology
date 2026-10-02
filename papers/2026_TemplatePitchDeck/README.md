<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 template_pitch_deck: Reproducible, Validated Pitch-Deck Generation

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21281509-blue)](https://doi.org/10.5281/zenodo.21281509)

---

## Abstract

> Research groups routinely need to pitch their work — to funders, partners, or collaborators — yet pitch decks are almost never treated as reproducible research artifacts: they are hand-assembled in proprietary slide tools, contain unverifiable claims, and cannot be regenerated when the underlying facts change. template_pitch_deck closes that gap. It generates six artifacts from one token-resolved content source — short, medium, and long decks, each in both PDF and PPTX — with every numeric claim traced back to a live introspection of the repository it describes, every {{TOKEN}} substitution verified to have actually landed, and every sentence checked against a denylist of pitch-deck clichés. The flagship content pitches template_template (../../template_template/), this monorepo's own autopoietic meta-project, to a meta-science and science-integrity audience — the kind of pitch an organization like the Active Inference Institute or COGSEC would actually hand to a funder. The rendering engine itself is new, reusable infrastructure: infrastructure/rendering/slide_deck.py (ReportLab, PDF) and infrastructure/rendering/pptx_deck.py (python-pptx) both consume the same DeckContent model, so a PDF and a PPTX built from identical content carry identical slide counts and identical text — verified by direct read-back of both file formats, not by inspection. Keywords: pitch deck, slide generation, reproducible research communication, meta-science infrastructure, token validation, PPTX, PDF rendering.

## Keywords

`pitch deck` · `slide generation` · `reproducible research communication` · `meta-science infrastructure` · `science integrity` · `token validation` · `PPTX` · `PDF rendering`

## Methods

- **Shared format-agnostic DeckContent/Slide content model with slide budgets** — Defines Slide, DeckContent and SlideBudget (short <=10, medium <=22, long <=45 slides) consumed by both renderers, with a pure function truncating decks to a budget.
- **Dual PDF (ReportLab) and PPTX (python-pptx) renderers with a parity test** — Renders the same resolved content via ReportLab canvas onto 16:9 pages and via python-pptx, with a test asserting PDF page count equals PPTX slide count.
- **{{TOKEN}} resolution against deck_tokens.yaml with fail-loud checks** — Resolves {{TOKEN}} placeholders from a token file of facts read live from the pitched project, raising on any unresolved token and checking output for leftover braces.
- **Word-boundary cliché denylist lint over every resolved slide** — Runs a denylist of pitch-deck stock phrases (e.g. synergy, disrupt, 10x) across all slides at all three lengths before rendering, as part of an audit script.
- **Negative-control fixtures proving validation gates fire** — Uses deliberately broken token and cliché-laden fixtures to show each audit failure mode triggers before trusting that the real content passes.

## Key Findings

- The tool generates six artifacts (short, medium and long decks, each as PDF and PPTX) from one token-resolved content source.
- PDF and PPTX decks built from identical content carry identical slide counts and text, verified by reading back both file formats rather than by inspection.
- Rendering is deterministic: given the same repository state, two consecutive runs produce byte-identical PDF and PPTX output, with generation time kept only in deck metadata.
- No LLM/Ollama stage is required, since deck content is authored and token-resolved rather than model-generated at render time, keeping artifacts deterministic.
- The flagship deck pitches template_template to a meta-science and science-integrity audience using problem, solution, proof (currently measured facts) and ask arc.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [docxology/template-pitch-deck](https://github.com/docxology/template-pitch-deck)
- GitHub release: [v1.0.2](https://github.com/docxology/template-pitch-deck/releases/tag/v1.0.2)
- DOI: [10.5281/zenodo.21281509](https://doi.org/10.5281/zenodo.21281509)
- Zenodo record: [https://zenodo.org/records/21281509](https://zenodo.org/records/21281509)
- PDF: [Friedman_2026_Templatepitchdeck_66941950.pdf](Friedman_2026_Templatepitchdeck_66941950.pdf)
- PDF: [template_template_pitch_long.pdf](template_template_pitch_long.pdf)
- PDF: [template_template_pitch_medium.pdf](template_template_pitch_medium.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/21281509)

## Citation

> Daniel Ari Friedman (2026). *template_pitch_deck: Reproducible, Validated Pitch-Deck Generation*. Zenodo. DOI: 10.5281/zenodo.21281509. URL: https://doi.org/10.5281/zenodo.21281509.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
