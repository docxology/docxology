# AGENTS.md — `art-collections/`

6 curated collection pages, one per theme:

- `active-inference.html` — Active Inference
- `americana-seals.html` — Americana & Seals
- `collective-behavior-ants.html` — Collective Behavior & Ants
- `lettering-verse.html` — Lettering & Verse
- `neuroscience-molecular-biology.html` — Neuroscience & Molecular Biology
- `sacred-geometry-kabbalistic-triangles.html` — Sacred Geometry & Kabbalistic Triangles

- A page's membership list lives in its own JSON-LD `ItemList` and in its visible grid,
  and the two are written together. Adding or removing a work is an edit to both, plus
  the count in the page's `numberOfItems`; nothing regenerates this list from the
  artwork data.
- Every listed work is an `../artworks/<id>-<slug>.html` page. Keep the slug in step with
  the page it names: the id alone resolves nothing.
- The collection index is `../collections.html`; the gallery index is `../art.html`.
  Repository rules are in [`../AGENTS.md`](../AGENTS.md).
