# template_pitch_deck: Reproducible, Validated Pitch-Deck Generation

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21281509.svg)](https://doi.org/10.5281/zenodo.21281509)

---

## Abstract

Research groups routinely need to pitch their work — to funders, partners, or collaborators — yet pitch decks are almost never treated as reproducible research artifacts: they are hand-assembled in proprietary slide tools, contain unverifiable claims, and cannot be regenerated when the underlying facts change. template_pitch_deck closes that gap. It generates six artifacts from one token-resolved content source — short, medium, and long decks, each in both PDF and PPTX — with every numeric claim traced back to a live introspection of the repository it describes, every {{TOKEN}} substitution verified to have actually landed, and every sentence checked against a denylist of pitch-deck clichés. The flagship content pitches template_template (../../template_template/), this monorepo's own autopoietic meta-project, to a meta-science and science-integrity audience — the kind of pitch an organization like the Active Inference Institute or COGSEC would actually hand to a funder. The rendering engine itself is new, reusable infrastructure: infrastructure/rendering/slide_deck.py (ReportLab, PDF) and infrastructure/rendering/pptx_deck.py (python-pptx) both consume the same DeckContent model, so a PDF and a PPTX built from identical content carry identical slide counts and identical text — verified by direct read-back of both file formats, not by inspection. Keywords: pitch deck, slide generation, reproducible research communication, meta-science infrastructure, token validation, PPTX, PDF rendering.

## Keywords

pitch deck · slide generation · reproducible research communication · meta-science infrastructure · science integrity · token validation · PPTX · PDF rendering

## Artifacts

| Field | Value |
|------|-------|
| **DOI** | [10.5281/zenodo.21281509](https://doi.org/10.5281/zenodo.21281509) |
| **Published** | 2026-07-08 |
| **Version** | 1.0.0 |
| **Zenodo record** | https://zenodo.org/records/21281509 |
| **GitHub release** | https://github.com/docxology/template-pitch-deck/releases/tag/v1.0.2 |
| **Source repository** | https://github.com/docxology/template-pitch-deck |

## Files

- `template_template_pitch_short.pdf` - Zenodo PDF
- `template_template_pitch_long.pdf` - Zenodo PDF
- `template_template_pitch_medium.pdf` - Zenodo PDF
- `Friedman_2026_Templatepitchdeck_66941950.pdf` - Zenodo PDF

## Citation

> Friedman, D. A. (2026). *template_pitch_deck: Reproducible, Validated Pitch-Deck Generation*. Zenodo. DOI: 10.5281/zenodo.21281509. URL: https://doi.org/10.5281/zenodo.21281509.

## Related

- GitHub release: https://github.com/docxology/template-pitch-deck/releases/tag/v1.0.0

- Zenodo record: https://zenodo.org/records/21281509
- GitHub release: https://github.com/docxology/template-pitch-deck/releases/tag/v1.0.2
- Source repository: https://github.com/docxology/template-pitch-deck
- [Full Bibliography](../../pages/BIBLIOGRAPHY.md) · [All Papers](../README.md)
