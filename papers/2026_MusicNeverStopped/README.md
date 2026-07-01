# The Music Never Stopped: A Grateful Data Compendium with a Category-Theoretic Interpretation

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20482026.svg)](https://doi.org/10.5281/zenodo.20482026)

---

## Abstract

<p>We present a modular, citation-bound data compendium for the Grateful Dead universe &mdash; shows, songs, performances, personnel timelines, venues, recordings, and reception &mdash; and a category-theoretic interpretation of the performance graph. The work is grounded in the archival reality that Grateful Dead history is both institutional and participatory: UCSC's Grateful Dead Archive and the Internet Archive collection preserve formal and community records , while taping and trading scholarship shows why setlists and recording metadata are cultural evidence, not merely fan trivia . The surrounding source dossier also binds the non-quantitative historical frame -- formation and Acid Test context, Wall of Sound engineering, live recording/liveness scholarship, Deadhead sociology, studio-era reception, and public recognition -- to checked sources rather than to folklore alone . The compendium integrates nine primary sources (Setlist.fm , The SetList Program , the Mark Leone CMU setlist archive , GDsets , gdshowsdb , the Internet Archive Live Music Archive , the Alex Allan / whitegum lyric finder , the official band site , and Wikipedia ) with four reference sources (Britannica , the lineup-changes guide , Dodd and Trist's The Complete Annotated Grateful Dead Lyrics , and the Grateful Stats front-end ) and secondary corpora and community discussions . Each source is parsed by an independently testable reference module written against the documented record shape; the committed compendium under `data/archival/` is the dataset reported here (3341 ingested shows (gdshowsdb + truckin gap-fill; community literature estimates ~2318 canonical concerts), 645 songs, 912 venues, 40757 performance rows). A runtime completeness audit and figure-validation gate certify referential integrity and non-degenerate outputs on every pipeline run. Integration is a deterministic, sort-keyed merge over canonical slugs; registered figures also emit CSV/JSON data tables, and a first-principles claim ledger classifies each major result by irreducible input, hard constraint, assumption, validation artifact, and interpretation limit. Exploratory repertoire/uncertainty panels are labelled as pattern-discovery rather than causal inference. We then exhibit four small but real categorical constructions, situated against transformational and categorical music-theory precedents : a poset category of dates, a discrete category of shows, a monotone cumulative setlist functor and lineup functor from dates into sets, and a span representation that takes each performance to be the apex of a span between its show and its song. Wide pullbacks over a fixed show recover the show's setlist; wide pullbacks over a fixed song recover the song's performance history. The active-band roster, by contrast, is a non-monotone presheaf on the date poset &mdash; a categorical formalization of the familiar fact that members come and go. The artefacts in this paper come from the committed archival snapshot; all source-ingestion modules are written against the real source shape so that `scripts/00_fetch_sources.py --online --write-archival` refreshes the full snapshot. --- Associated artifacts GitHub release: The Music Never Stopped: A Grateful Data Compendium (v1.0.0) (https://github.com/docxology/grateful_data/releases/tag/v1.0.0) PDF SHA-256: 2d42bfd04e0b32e4871d5bcbe2c65bcce58cca336da240af7c6fd03a6563a709</p>

## Keywords

grateful dead · setlist data · category theory · music information retrieval · reproducible data compendium

## Publication Details

| Field | Value |
|------|-------|
| **DOI** | [10.5281/zenodo.20482026](https://doi.org/10.5281/zenodo.20482026) |
| **Published** | 2026-05-31 |
| **Version** | 1.0.0 |
| **Zenodo record** | https://zenodo.org/records/https://zenodo.org/records/20482025 |
| **GitHub release** | https://github.com/docxology/grateful_data/releases/tag/v1.0.0 |
| **Source repository** | https://github.com/docxology/grateful_data |

## Files

- `Friedman_2026_Music_2d42bfd0.pdf` - Zenodo PDF

## Citation

> Friedman, D. A. (2026). *The Music Never Stopped: A Grateful Data Compendium with a Category-Theoretic Interpretation*. Zenodo. https://doi.org/10.5281/zenodo.20482026

## Related

- Zenodo record: https://zenodo.org/records/20482026
- GitHub release: https://github.com/docxology/grateful_data/releases/tag/v1.0.0
- Source repository: https://github.com/docxology/grateful_data
- [Full Bibliography](../../pages/BIBLIOGRAPHY.md) · [All Papers](../README.md)
