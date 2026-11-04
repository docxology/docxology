# Art collections

6 curated collection pages, each an HTML page for one theme:

- `active-inference.html` — Active Inference
- `americana-seals.html` — Americana & Seals
- `collective-behavior-ants.html` — Collective Behavior & Ants
- `lettering-verse.html` — Lettering & Verse
- `neuroscience-molecular-biology.html` — Neuroscience & Molecular Biology
- `sacred-geometry-kabbalistic-triangles.html` — Sacred Geometry & Kabbalistic Triangles

Each page carries schema.org `CollectionPage` markup with an `ItemList` of the artworks
it shows — those are `../artworks/<id>-<slug>.html` pages — and a breadcrumb back through
`../art.html`. The root `../collections.html` is the index that links them.
