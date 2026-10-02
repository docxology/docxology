# AGENTS.md — `docxology/code/tools`

## What this is

Site tooling (incl. `vendor/` third-party libs).

## Layout

- tools + vendored code.

## Invariants & gotchas

- This is the public `docxology/docxology` repository. Follow the root
  ownership and privacy rules; verify the Git destination before publishing.
- Carry authorized changes through review and verification on a work branch.
  Preserve concurrent edits and publish only reviewed public content.
- Generated subfolders (`output/`, `.netlify/`) — regenerate, don't hand-edit.

## Verify

- `ls code/tools`
- Follow the [root repository instructions](../../AGENTS.md) and nearer parent instructions.
