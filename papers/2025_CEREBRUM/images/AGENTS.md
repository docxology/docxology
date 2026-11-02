# AGENTS.md — `papers/2025_CEREBRUM/images/`

Extracted figures for [CEREBRUM: Case-Enabled Reasoning Engine with Bayesian
Representations for Unified Modeling](../README.md) (`2025_CEREBRUM`). The paper's
`../full_text.md` embeds them, and the generated work and paper pages link the folder as
"Figures on GitHub" when figures exist.

- The binaries are produced from the paper's archived PDFs in `../` by
  `code/orchestrators/extract_paper_texts.py`, which writes each file as
  `pageN_imgM.ext` from the PDF page and image position it came from. The folder holds 2
  candidate PDFs (`2025_CEREBRUM.pdf`, `CEREBRUM_1-4_April-16-2025.pdf`) and nothing
  records which of them an individual figure came from. Regenerate from the same source
  PDF when extraction needs repair; never hand-edit, recompress, or swap in a figure
  from another manuscript version.
- The folder held 15 PNG images on 2026-11-02, named for PDF pages 6 through 23. Treat
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
