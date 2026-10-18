# Manuscript status — docxology

As of 2026-10-18, this is a source-backed repository-methods draft describing
the public research/software/citation index and its static website. Archived
research publications remain separate under [papers/](../../papers/).

Numbered sections describe source authority, stable identities, shared policy,
ordered generation, progressive discovery, agent inspection, and revision-bound
evidence. Implementation claims link repository sources and runbooks; volatile
totals belong in generated or dated evidence. The bibliography identifies the
repository from `CITATION.cff`; no manuscript DOI or comparative study is assigned.

`validate_manuscript.py` is the structural source gate. The explicit renderer
uses the committed docxology/template 4.0.2 combined-PDF API, Pandoc, crossref,
XeLaTeX, and BibTeX. It produces an informative vector cover from a declared
producer. HTML, EPUB, and PowerPoint use the existing Pandoc/citeproc pipeline.
The [render command](README.md) writes a new external review directory and binds
source, tool, template export, external Python runtime, cover, and output hashes.
Prior review directories are preserved on failure. Template code and the reviewed
LaTeX preamble execute as trusted inputs; process isolation is not an OS sandbox.

Manuscript text and original figures use CC BY 4.0. Archived publications and
third-party material retain their own rights. Automated rendering, package/text
checks, and assistant page inspection remain separate from named human visual
approval, editorial review, scientific validity, and publication readiness.
The native four-format integration passed on 2026-10-18; assistant inspection
covered every page of the eight-page PDF and corrected cramped tables. No text
blocks escaped page bounds. This records draft layout inspection only.
Named human and editorial approvals remain pending. Outputs are review drafts and are not new
research bibliography entries or Zenodo deposits.
