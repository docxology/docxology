# Manuscript status — docxology

As of 2026-10-13, this is a source-backed repository-methods draft describing
the public research/software/citation index and its static website. It is
separate from the research publications archived under [papers/](../../papers/).

## Established source and rendering scope

- Numbered sections describe source authority, stable identity, shared policy,
  ordered generation, progressive discovery, and revision-bound evidence.
- Implementation claims link repository sources and runbooks. Volatile catalog
  totals remain in generated or dated evidence surfaces.
- The bibliography identifies the repository from `CITATION.cff`; no new
  manuscript DOI or external study is assigned.
- `validate_manuscript.py` remains a read-only structural source gate.
- `render_manuscript.py` declares pinned Pandoc/crossref/Typst tools and manual
  HTML/PDF/EPUB/PowerPoint outputs with a source/tool/output hash receipt. It
  uses a real bibliography parser, resolves cross-references, and preserves
  prior review directories on failure. See [the command and scope](README.md).
- The explicit offline integration ran successfully on 2026-10-13 with Pandoc
  3.12.1, pandoc-crossref 0.3.26, and Typst 0.15.1. It produced all four declared
  formats, parsed the bibliography, and checked output hashes/package integrity.
  This is automated render evidence; format layout approval remains pending.
- Manuscript text and original manuscript figures use CC BY 4.0. Archived and
  third-party material retain their own rights.

## Separate, unfinished evidence

Human visual and editorial approval, scientific validity, comparative results,
and publication readiness remain unverified. A successful render or automated
artifact check establishes neither approval nor publication readiness. Rendered
outputs stay in explicit external review directories until reviewed publication
is deliberately requested; they are not added to the research bibliography.
Inspect PDF pages, HTML links, and the EPUB/PowerPoint presentation layouts.

## Verification

```bash
uv run python3 code/orchestrators/validate_manuscript.py --json
uv run python3 code/orchestrators/render_manuscript.py --output-dir /private/tmp/docxology-manuscript-review --json
```

Report structural validation and actual rendering separately. Repository-wide
checks remain governed by [development.md](../operations/development.md) and
[release-integrity.md](../operations/release-integrity.md).
