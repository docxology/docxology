# AGENTS.md — `docxology/docs/design`

Added by the 2026-08-29 ongoing-docs fleet pass.

## What this is

Design documentation for the docxology site.

## Layout

- design docs.

## Invariants & gotchas

- Single git remote: `origin` = `https://github.com/docxology/docxology.git`
  (`main` tracks `origin/main`). This is a live work tree: push feature branches
  and open PRs against `origin` rather than committing straight to `main`.
- Release runbook: `docs/operations/release-integrity.md` (and `docs/operations/settle.md`).
- Generated subfolders (`output/`, `.netlify/`) — regenerate, don't hand-edit.

## Verify

- `ls docxology/docs/design`
- Parent: `docxology/AGENTS.md`; lane policy: `../../AGENTS.md` (ongoing root).
