<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 The Music Never Stopped: A Grateful Data Compendium with a Category-Theoretic Interpretation

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20482025-blue)](https://doi.org/10.5281/zenodo.20482025)

---

## Abstract

> We present a modular, citation-bound data compendium for the Grateful Dead universe — shows, songs, performances, personnel timelines, venues, recordings, and reception — and a category-theoretic interpretation of the performance graph. The work is grounded in the archival reality that Grateful Dead history is both institutional and participatory: UCSC's Grateful Dead Archive and the Internet Archive collection preserve formal and community records , while taping and trading scholarship shows why setlists and recording metadata are cultural evidence, not merely fan trivia . The surrounding source dossier also binds the non-quantitative historical frame -- formation and Acid Test context, Wall of Sound engineering, live recording/liveness scholarship, Deadhead sociology, studio-era reception, and public recognition -- to checked sources rather than to folklore alone . The compendium integrates nine primary sources (Setlist.fm , The SetList Program , the Mark Leone CMU setlist archive , GDsets , gdshowsdb , the Internet Archive Live Music Archive , the Alex Allan / whitegum lyric finder , the official band site , and Wikipedia ) with four reference sources (Britannica , the lineup-changes guide , Dodd and Trist's The Complete Annotated Grateful Dead Lyrics , and the Grateful Stats front-end ) and secondary corpora and community discussions . Each source is parsed by an independently testable reference module written against the documented record shape; the committed compendium under `data/archival/` is the dataset reported here (3341 ingested shows (gdshowsdb + truckin gap-fill; community literature estimates ~2318 canonical concerts), 645 songs, 912 venues, 40757 performance rows). A runtime completeness audit and figure-validation gate certify referential integrity and non-degenerate outputs on every pipeline run. Integration is a deterministic, sort-keyed merge over canonical slugs; registered figures also emit CSV/JSON data tables, and a first-principles claim ledger classifies each major result by irreducible input, hard constraint, assumption, validation artifact, and interpretation limit. Exploratory repertoire/uncertainty panels are labelled as pattern-discovery rather than causal inference. We then exhibit four small but real categorical constructions, situated against transformational and categorical music-theory precedents : a poset category of dates, a discrete category of shows, a monotone cumulative setlist functor and lineup functor from dates into sets, and a span representation that takes each performance to be the apex of a span between its show and its song. Wide pullbacks over a fixed show recover the show's setlist; wide pullbacks over a fixed song recover the song's performance history. The active-band roster, by contrast, is a non-monotone presheaf on the date poset — a categorical formalization of the familiar fact that members come and go. The artefacts in this paper come from the committed archival snapshot; all source-ingestion modules are written against the real source shape so that `scripts/00_fetch_sources.py --online --write-archival` refreshes the full snapshot.

## Keywords

`grateful dead` · `setlist data` · `category theory` · `music information retrieval` · `reproducible data compendium`

## Methods

- **Integration of nine primary Grateful Dead data sources into one schema** — Setlist.fm, SetList Program, CMU archive, GDsets, gdshowsdb, Internet Archive, whitegum, dead.net and Wikipedia are parsed by testable modules and merged.
- **Deterministic canonical-slug merge with frozen-dataclass schema** — Entities validate inputs and use canonical-slug primary keys so cross-source joins reduce to dictionary lookups; integration is a sort-keyed merge.
- **Completeness audit, figure-validation gate, and first-principles claim ledger** — Runtime checks certify referential integrity and non-degenerate figures; a ledger classifies each major result by inputs, assumptions, and limits.
- **First-order Markov model of within-show song order with permutation-null FDR screen** — Fits song-to-song transition probabilities, audits support thresholds, and screens transitions against a permutation null under FDR control.
- **Category-theoretic constructions: date poset, show category, functors, spans** — Builds setlist and lineup functors from dates into sets, an active-roster presheaf, and performances as spans between show and song.

## Key Findings

- The committed compendium contains 3341 ingested shows, 645 songs, 912 venues, and 40757 performance rows.
- Completeness is referential only: 282 of the 3341 catalogued shows have an empty setlist in gdshowsdb.
- Repertoire is highly skewed: the song-performance Gini coefficient is 0.74 and the top decile of songs accounts for 50.61% of non-segment performances.
- The most frequent explicit segue in the corpus is the structural "drums" -> "space" passage, with 1197 occurrences.
- Wide pullbacks over a show recover its setlist and over a song recover its performance history, while the active roster is a non-monotone presheaf on the date poset.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [docxology/grateful_data](https://github.com/docxology/grateful_data)
- GitHub release: [v1.0.0](https://github.com/docxology/grateful_data/releases/tag/v1.0.0)
- DOI: [10.5281/zenodo.20482025](https://doi.org/10.5281/zenodo.20482025)
- Zenodo record: [https://zenodo.org/records/20482025](https://zenodo.org/records/20482025)
- PDF: [Friedman_2026_Music_2d42bfd0.pdf](Friedman_2026_Music_2d42bfd0.pdf)
- PDF SHA-256: 296b3b5c5e9f3d628e15ae5d467dd5cc418bd018f0166194c9494b33b3367dda

## Citation

> Daniel Ari Friedman (2026). *The Music Never Stopped: A Grateful Data Compendium with a Category-Theoretic Interpretation*. Zenodo. DOI: 10.5281/zenodo.20482025. URL: https://doi.org/10.5281/zenodo.20482025.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
