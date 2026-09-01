# AGENTS.md — `docxology/data/video-transcripts`

Added by the 2026-08-29 ongoing-docs fleet pass.

## What this is

Video transcript data feeding the site.

## Layout

- transcript files.

## Invariants & gotchas

- Local-only under `projects/ongoing/` — never commit.
- `docxology` is a live work tree with THREE git remotes (`origin`/`public` = the
  public mirror, `docxology-private` upstream; local main ahead 114): read, don't
  write, never run git operations here.
- Generated subfolders (`output/`, `.netlify/`) — regenerate, don't hand-edit.

## Verify

- `ls docxology/data/video-transcripts`
- Parent: `docxology/AGENTS.md`; lane policy: `../../AGENTS.md` (ongoing root).
