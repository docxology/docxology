# AGENTS.md — `artworks/`

944 generated per-artwork pages, one per work: `<flickr-id>-<slug>.html`. Read this
directory as output, not as source.

- `../code/orchestrators/build_artwork_pages.py` writes these pages;
  `build_artwork_index.py` and `sync_art_gallery.py` are the neighbouring stages of the
  same pipeline. A wrong title, link or metadata value is fixed in the artwork data and
  re-generated — a hand edit is overwritten by the next run and hides the cause.
- The structured source is `../data/artworks.json`; per-work metadata is in `../art/` as
  `<id>_…_metadata.json`, and 941 of these 944 ids appear there. An id present
  here and absent there is a metadata gap, not a page defect.
- Each page links to `../art.html`, `../collections.html` and `../data/artworks.json`;
  keep those targets when changing the template.
- Repository rules are in [`../AGENTS.md`](../AGENTS.md).
