# AGENTS.md — `papers/2016_ForagingGene/images/`

Extracted figures for [🐜 Context-dependent expression of the foraging gene in field colonies of ants: t](../README.md) (`2016_ForagingGene`). The paper's `../full_text.md` embeds them, and the generated work and paper
pages link the folder as "Figures on GitHub" when figures exist.

- The binaries are produced from the paper's archived PDF by
  `code/orchestrators/extract_paper_texts.py`. Regenerate from that source when
  extraction needs repair; never hand-edit, recompress, or swap in a figure from
  another manuscript version.
- The folder held 13 JPEG/PNG files when this guide was written (2026-11-02). Treat the directory
  listing as the current truth: this guide is not a manifest and will not be updated
  when extraction adds or removes files.
- Extracted paper-image binaries are deliberately omitted from the deployed Pages
  projection; the site links to them in the repository, and the paper's own PDF remains
  the authoritative figure source.
- There is no test, CI job, or runnable gate for this folder. The repository-wide check
  that would notice a broken link is `uv run python3 code/orchestrators/validate_repo.py`;
  it does not inspect image content or figure fidelity.

The paper-folder contract is in [`../../README.md`](../../README.md) and
[`../../AGENTS.md`](../../AGENTS.md).
