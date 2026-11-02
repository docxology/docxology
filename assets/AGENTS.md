# AGENTS.md — `assets/`

Static assets the site serves: `hero-art/` (the homepage hero images) and
`curio-cards/`. Hand-maintained content, not generated output — no rebuild step
produces these files.

- A referenced asset is load-bearing. Removing or renaming one breaks the page that
  names it, and because no test renders pages, the break reaches the live site
  unnoticed.
- Keep provenance (source and licence) where the using page or runbook records it; this
  guide does not track licensing.
- Listing first: this guide is not a manifest.

Repository rules: [root guide](../AGENTS.md).
