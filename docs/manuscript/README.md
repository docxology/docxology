# Manuscript - docxology

This directory is a template-format manuscript scaffold for:

**docxology: Research, Software, and Citation Index**

A master profile repository indexing bibliography, software, generated GitHub inventory, and research documentation across entomology, active inference, cognitive security, and art/synergetics.

## File Inventory

- `config.yaml`
- `preamble.md`
- `references.bib`
- `00_abstract.md`
- `01_introduction.md`
- `02_system_context.md`
- `03_methods.md`
- `04_artifacts_and_evidence.md`
- `05_reproducibility.md`
- `06_limitations_and_next_steps.md`
- `S01_source_surface.md`
- `98_symbols_glossary.md`
- `99_references.md`
- `AGENTS.md`
- `README.md`
- `SYNTAX.md`

## Source Surfaces

| Surface | Role |
|---|---|
| `pages/` | Source directory to inspect before turning prose into claims. |
| `papers/` | Source directory to inspect before turning prose into claims. |
| `code/` | Source directory to inspect before turning prose into claims. |
| `reports/` | Source directory to inspect before turning prose into claims. |
| `resume/` | Source directory to inspect before turning prose into claims. |
| `works/` | Source directory to inspect before turning prose into claims. |
| `data/` | Source directory to inspect before turning prose into claims. |

## Verification

From the sibling template checkout, after `link-projects` has synced the sidecar:

```bash
uv run python -m infrastructure.orchestration link-projects
uv run python -m infrastructure.validation.cli markdown projects/working/docxology/manuscript/
```

Render only after replacing scaffold prose with project-bound evidence and checking any project-local gates documented in the repository root.
