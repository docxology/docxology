# Manuscript Agent Notes - docxology

This directory follows the docxology/template manuscript contract:

- `00_` through `09_` files are main sections.
- `S01_` files are supplemental material.
- `98_` and `99_` files are back matter.
- Every manuscript section file starts with one H1 and a stable `{#sec:...}` label.
- Citations must use Pandoc syntax and resolve in `references.bib`.
- Generated numbers belong behind `{{TOKEN}}` variables, not hard-coded prose.

## Editing Rules

- Keep this technical draft bound to public repository sources linked in its sections. New architecture statements need current source evidence; new quantitative results need a repeatable method and dated receipts.
- Do not fabricate results, benchmark numbers, citations, DOIs, or release claims.
- Keep project-specific computation in source modules and scripts; keep manuscript files as prose and evidence maps.
- Prefer explicit paths to source surfaces when describing evidence.
- If adding figures, write them under `../output/figures/` and reference them with Pandoc-crossref labels.

## Current Scope

A master profile repository indexing bibliography, software, generated GitHub inventory, and research documentation across entomology, active inference, cognitive security, and art/synergetics.

Evidence boundary: Treat generated inventories and profile pages as index artifacts; distinguish current generated state from external publication readiness.

Run `uv run python3 code/orchestrators/validate_manuscript.py` from the repository root after edits. This read-only gate checks source structure and configuration, not complete BibTeX syntax, rendering, source extraction accuracy, licensing, or scientific/editorial approval. `config.yaml` paths are relative to this repository root. Archived paper bytes and metadata are outside this directory's editing scope.
