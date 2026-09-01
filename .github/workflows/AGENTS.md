# AGENTS.md — `docxology/.github/workflows`

Added by the 2026-08-29 ongoing-docs fleet pass.

## What this is

GitHub Actions workflows for docxology (unverified — not run by this pass).

## Layout

- workflow YAMLs.

## Invariants & gotchas

- Local-only under `projects/ongoing/` — never commit.
- `docxology` is a live work tree with THREE git remotes (`origin`/`public` = the
  public mirror, `docxology-private` upstream; local main ahead 114): read, don't
  write, never run git operations here.
- Generated subfolders (`output/`, `.netlify/`) — regenerate, don't hand-edit.

## Verify

- `ls docxology/.github/workflows`
- Parent: `docxology/AGENTS.md`; lane policy: `../../AGENTS.md` (ongoing root).
