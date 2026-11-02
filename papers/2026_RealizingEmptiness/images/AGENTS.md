# AGENTS.md — `papers/2026_RealizingEmptiness/images/`

Extracted figures for [Realizing Emptiness: Operational Surrogates for No-Self-Evidence,
QRF Opacification, and Bayesian Model Reduction](../README.md)
(`2026_RealizingEmptiness`). The paper's `../full_text.md` embeds all 56 of them as
image links into this folder, so no captions survive extraction and the filename is the
only stable ordering. The generated work pages carry a "Figures on GitHub" button to
this folder, and the paper's own `../index.html` links it as well.

- The binaries are produced from the paper's archived PDF
  (`realizing_emptiness_combined.pdf`) by `code/orchestrators/extract_paper_texts.py`,
  which writes `pageN_imgM.<ext>` for each embedded image it keeps and skips icon-sized
  ones. Regenerate from that source when extraction needs repair; never hand-edit,
  recompress, or swap in a figure from another manuscript version.

- The folder held 56 PNG files on 2026-11-02, the day this guide was written. Their
  filename page indices run from 1 to 56 across 36 of the PDF's pages, so 20 of the 56
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
