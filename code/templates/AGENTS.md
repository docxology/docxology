# AGENTS.md — `docxology/code/templates`

Added by the 2026-08-29 ongoing-docs fleet pass.

## What this is

Templates used by the site generators.

## Layout

- template files.

## Invariants & gotchas

- Local-only under `projects/ongoing/` — never commit.
- `docxology` is a live work tree with THREE git remotes (`origin`/`public` = the
  public mirror, `docxology-private` upstream; local main ahead 114): read, don't
  write, never run git operations here.
- Generated subfolders (`output/`, `.netlify/`) — regenerate, don't hand-edit.

## Verify

- `ls docxology/code/templates`
- Parent: `docxology/AGENTS.md`; lane policy: `../../AGENTS.md` (ongoing root).
