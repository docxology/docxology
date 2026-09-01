# AGENTS.md — `docxology/.well-known`

Added by the 2026-08-29 ongoing-docs fleet pass.

## What this is

Well-known metadata served at the site root.

## Layout

- well-known text files.

## Invariants & gotchas

- Local-only under `projects/ongoing/` — never commit.
- `docxology` is a live work tree with THREE git remotes (`origin`/`public` = the
  public mirror, `docxology-private` upstream; local main ahead 114): read, don't
  write, never run git operations here.
- Generated subfolders (`output/`, `.netlify/`) — regenerate, don't hand-edit.

## Verify

- `ls docxology/.well-known`
- Parent: `docxology/AGENTS.md`; lane policy: `../../AGENTS.md` (ongoing root).
