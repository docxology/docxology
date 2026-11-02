# AGENTS.md — `papers/2023_SlidesIris/images/`

Extracted figures for [Slides for Iris](../README.md) (`2023_SlidesIris`). The paper's
`../full_text.md` embeds them, and the generated work and paper pages link the folder as
"Figures on GitHub" when figures exist.

- The binaries are produced from the paper's archived PDF in `../` (`Slides for Iris
  April 17 2023.pdf`) by `code/orchestrators/extract_paper_texts.py`, which writes each
  file as `pageN_imgM.ext` from the PDF page and image position it came from. Regenerate
  from that source when extraction needs repair; never hand-edit, recompress, or swap in
  a figure from another manuscript version.
- The folder held 8 JPEG images on 2026-11-02, named for PDF pages 2 through 7. Treat
  the directory listing as the current truth: this guide is not a manifest and will not
  be updated when extraction adds or removes files.
- Extracted paper-image binaries are deliberately omitted from the deployed Pages
  projection; the site links to them in the repository, and the paper's own PDF remains
  the authoritative figure source.
- There is no test, CI job, or runnable gate for this folder. The
  repository-wide check that would notice a broken link is
  `uv run python3 code/orchestrators/validate_repo.py`; it does not inspect
  image content or figure fidelity.

The paper-folder contract is in [`../../README.md`](../../README.md) and
[`../../AGENTS.md`](../../AGENTS.md).
