# AGENTS.md — `code/artifacts/publications-explorer/`

A standalone interactive bibliography viewer (`publications-explorer.html`) that loads
the same canonical catalog as the live publications page (`/data/works.json` when served
from the site root).

- It is a generated artifact: rebuild it with the command recorded in
  [`../../../GENERATED.md`](../../../GENERATED.md) rather than editing the HTML, and
  check that the rebuild is listed there before assuming it exists.
- Its data comes from `data/works.json`, which is itself regenerated from
  `pages/BIBLIOGRAPHY.md`; a stale viewer usually means the catalog moved, not that the
  viewer is broken.
- Nothing tests it: no CI job opens the page, so a broken catalog path is discovered by
  a reader.

Repository rules: [root guide](../../../AGENTS.md).
