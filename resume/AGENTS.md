# AGENTS.md — `docxology/resume/`

Added by the 2026-08-29 ongoing-docs fleet pass.

## What this is

CV/resume source + generated artifacts: `source.json` (single source), plaintext
variants (`academic.txt`, `full.txt`, `software-consulting.txt`, `teaching-service.txt`),
`resume.html` and `resume.pdf` (generated), and a human `README.md`.

## Invariants

- Local-only; never commit. Edit `source.json`, then regenerate; don't hand-edit
  the generated HTML/PDF.
- Live work tree — read, don't write outside a deliberate resume-update mission.
