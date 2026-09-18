# AGENTS.md — `docxology/docs/releases`

Added by the 2026-08-29 ongoing-docs fleet pass.

## What this is

Release notes for the docxology site.

## Layout

- release docs.

## Invariants & gotchas

- Single git remote: `origin` = `https://github.com/docxology/docxology.git`
  (`main` tracks `origin/main`). This is a live work tree: push feature branches
  and open PRs against `origin` rather than committing straight to `main`.
- Release runbook: `docs/operations/release-integrity.md` (and `docs/operations/settle.md`).
- Generated subfolders (`output/`, `.netlify/`) — regenerate, don't hand-edit.

## Verify

- `ls docxology/docs/releases`
- Parent: `docxology/AGENTS.md`; lane policy: `../../AGENTS.md` (ongoing root).
