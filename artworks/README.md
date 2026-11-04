# Artworks

944 per-artwork HTML pages, one for each work in the gallery, named
`<flickr-id>-<slug>.html` and titled `<Title> — pen and ink drawing by Daniel Ari
Friedman` (e.g. `10313080823-epigenetics.html`). Every page links back to
[`../art.html`](../art.html), [`../collections.html`](../collections.html) and
[`../data/artworks.json`](../data/artworks.json), the structured data the gallery reads.

These pages are pipeline output: `../code/orchestrators/build_artwork_pages.py` writes
them, with `build_artwork_index.py` and `sync_art_gallery.py` elsewhere in the same
pipeline. Correct a work by fixing its data and re-running the pipeline, not by editing
one page.

Per-work metadata lives in [`../art/`](../art/) (1018 files, mostly
`<id>_…_metadata.json`); 941 of the 944 ids here appear there. What the
gallery serves, and why the former JPG mirror was removed, is in
[`../art/README.md`](../art/README.md).
