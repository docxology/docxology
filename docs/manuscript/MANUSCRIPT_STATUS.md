# Manuscript status — docxology

As of 2026-10-05, this is a source-backed repository-methods draft describing the public research/software/citation index and its static website. It is separate from the research publications archived under [papers/](../../papers/).

## Established source scope

- Sections explain source authority, stable identity, thin command entry points, shared policy, ordered generation, progressive browser discovery, and candidate-bound release evidence.
- Implementation statements link public repository sources and runbooks. Current catalog totals and historical pass counts remain in their generated or dated evidence surfaces.
- `config.yaml` binds `manuscript_dir` to `docs/manuscript` and the bibliography path to this repository.
- The bibliography identifies the repository from `CITATION.cff`; it adds no new manuscript DOI or external study.
- A read-only local validator checks source/configuration structure, citation-key resolution, labels, tokens, and local references.

## Separate, unfinished evidence

There is no declared manuscript rendering command, rendered PDF/HTML receipt, new experimental or comparative result, independent scientific review, or publication-readiness attestation. Complete BibTeX grammar, manuscript licensing, editorial review, and later quantitative results need separate verification. Desired render formats in configuration do not establish that rendering ran.

## Verification

Run from the repository root:

```bash
uv run python3 code/orchestrators/validate_manuscript.py
uv run python3 code/orchestrators/validate_manuscript.py --json
```

These commands inspect current sources without writing an artifact. Report their success as structural source validation. Repository-wide checks and publication evidence remain governed by [development.md](../operations/development.md) and [release-integrity.md](../operations/release-integrity.md).
