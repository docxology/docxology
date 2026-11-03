# AGENTS.md — `papers/2026_CaliforniaPublicRecords/images/`

Extracted figures for [California Public Records: A Technical and Legal Reference for
the Post-AB 473 Era](../README.md) (`2026_CaliforniaPublicRecords`). The paper's
`../full_text.md` embeds all 14 of them as image links into this folder, so no captions
survive extraction and the filename is the only stable ordering. The generated work
pages carry a "Figures on GitHub" button to this folder, and the paper's own
`../index.html` links it as well.

- The binaries are produced from the paper's archived PDF
  (`Friedman_2026_California_8f09eac2.pdf`) by
  `code/orchestrators/extract_paper_texts.py`, which writes `pageN_imgM.<ext>` for each
  embedded image it keeps and skips icon-sized ones. Regenerate from that source when
  extraction needs repair; never hand-edit, recompress, or swap in a figure from another
  manuscript version.

- The folder held 14 PNG files on 2026-11-02, the day this guide was written. Their
  filename page indices run from 1 to 19 across 11 of the PDF's pages, so 3 of the 14
  share a page with another figure. Treat the directory listing as the current truth:
  this guide is not a manifest and will not be updated when extraction adds or removes
  files. The generated `README.md` beside it and this guide are documentation, not
  figure assets.

- Extracted paper-image binaries are deliberately omitted from the deployed Pages
  projection; the site links to them in the repository, and the paper's own PDF remains
  the authoritative figure source.

- There is no test, CI job, or runnable gate for this folder. The repository-wide check
  is `uv run python3 code/orchestrators/validate_repo.py`; it reports a broken link but
  does not inspect image content or figure fidelity.

The paper-folder contract is in [`../../README.md`](../../README.md) and
[`../../AGENTS.md`](../../AGENTS.md).
