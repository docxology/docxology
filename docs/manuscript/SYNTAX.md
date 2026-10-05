# Manuscript Syntax - docxology

This draft follows numbered section files, Pandoc-style labels and citations, and repository-local references. [`validate_manuscript.py`](../../code/orchestrators/validate_manuscript.py) enforces the local source contract; no sibling checkout is needed for that check.

## Section Labels

| File | H1 | Label |
|---|---|---|
| `00_abstract.md` | Abstract | `{#sec:abstract}` |
| `01_introduction.md` | Introduction | `{#sec:introduction}` |
| `02_system_context.md` | System Context | `{#sec:system_context}` |
| `03_methods.md` | Methods | `{#sec:methods}` |
| `04_artifacts_and_evidence.md` | Artifacts and Evidence | `{#sec:artifacts_evidence}` |
| `05_reproducibility.md` | Reproducibility | `{#sec:reproducibility}` |
| `06_limitations_and_next_steps.md` | Limitations and Next Steps | `{#sec:limitations_next_steps}` |
| `S01_source_surface.md` | Supplemental Source Surface | `{#sec:source_surface}` |
| `98_symbols_glossary.md` | Symbols and Glossary | `{#sec:symbols_glossary}` |
| `99_references.md` | References | `{#sec:references}` |

## Citations

Use Pandoc citation syntax only, for example `[@real_key]`. Every key must exist in `references.bib` before it appears in prose.

## Figures

If a figure producer is introduced, document its command and write inspectable outputs under `../output/figures/`. Reference a real file with a label such as:

```markdown
![Caption text.](../output/figures/example.png){#fig:example width=80%}
```

## Claims

Architecture claims link current source owners. Quantitative and publication claims require appropriate dated evidence; a structural check cannot establish them. Volatile generated-value tokens are rejected until a declared producer resolves them before validation.

The validator resolves inline, reference-style, and shortcut image references and requires regular local figure files. It rejects malformed URLs, NUL characters, and references that escape the repository. Its bounded BibTeX entry/key checks reject unclosed entries, stray text, duplicates, and unresolved citations; complete field grammar, citation style, and TeX processing remain separate. It does not assess image interpretation, figure rendering, or renderer compatibility. Fenced examples are excluded from prose checks so example syntax is not mistaken for a missing artifact.
