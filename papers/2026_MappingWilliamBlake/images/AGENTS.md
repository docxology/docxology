# AGENTS.md — `papers/2026_MappingWilliamBlake/images/`

Historical figures from manuscript edition **0.1.0** of
[Mapping William Blake's Works: Evidence ledgers, source
provenance, text-image diagnostics, and rights-bounded release controls](../README.md)
(`2026_MappingWilliamBlake`). The preserved `../full_text_v0.1.md` embeds their
image links. `../source_evidence.json` binds this gallery to that extraction's
SHA-256, source PDF and edition. Captions did not survive extraction; filenames
provide the retained ordering. Work and paper pages label this gallery as
historical edition 0.1.0 while preserving its GitHub links.

- The binaries are produced from the paper's archived PDF (`blake_working_paper.pdf`) by
  `code/orchestrators/extract_paper_texts.py`, which writes `pageN_imgM.<ext>` for each
  embedded image it keeps and skips icon-sized ones. Regenerate from that source when
  extraction needs repair; never hand-edit, recompress, or swap in a figure from another
  manuscript version.

- The folder held 19 PNG files on 2026-11-02, the day this guide was written. Their
  filename page indices run from 1 to 44 across 17 of the PDF's pages, so 2 of the 19
  share a page with another figure. Treat the directory listing as the current truth:
  this guide is not a manifest and will not be updated when extraction adds or removes
  files. The generated `README.md` beside it and this guide are documentation, not
  figure assets.

- Extracted paper-image binaries are deliberately omitted from the deployed Pages
  projection; the site links to them in the repository. `blake_working_paper.pdf`
  is this historical gallery's identified source. The selected current PDF and
  its separate provenance are documented in the paper overview.

- Shared gallery regressions check source bindings, edition labels and unchanged
  image links. The repository-wide check is
  `uv run python3 code/orchestrators/validate_repo.py`; these checks do not inspect
  image content or figure fidelity.

The paper-folder contract is in [`../../README.md`](../../README.md) and
[`../../AGENTS.md`](../../AGENTS.md).
