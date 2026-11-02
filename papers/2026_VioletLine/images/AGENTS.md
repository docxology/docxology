# AGENTS.md — `papers/2026_VioletLine/images/`

Extracted figures for [The Violet Line: A Consent Ledger of Affected
Parties](../README.md) (`2026_VioletLine`). The paper's `../full_text.md` embeds it as
an image link into this folder, so no caption survives extraction and the filename is
the only stable identifier. The generated work pages carry a "Figures on GitHub" button
to this folder, and the paper's own `../index.html` links it as well.

- The binaries are produced from the paper's archived PDF (`violet_line_combined.pdf`)
  by `code/orchestrators/extract_paper_texts.py`, which writes `pageN_imgM.<ext>` for
  each embedded image it keeps and skips icon-sized ones. Regenerate from that source
  when extraction needs repair; never hand-edit, recompress, or swap in a figure from
  another manuscript version.

- The folder held one PNG on 2026-11-02, the day this guide was written. It is the image
  the extractor kept from PDF page 1. Treat the directory listing as the current truth:
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
