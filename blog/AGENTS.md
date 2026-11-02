# AGENTS.md — `blog/`

Hand-authored long-form writing: `index.html` for the list plus one folder per post.
This is the documented exception to the repository's rule that HTML is generated —
these pages are sources, and editing them directly is correct.

- Post folders keep their own `index.html`; the blog index links them. Adding a post
  means both.
- Nothing regenerates the blog and nothing tests it: no CI job renders these pages, so
  a broken link or layout is caught only by reading the page.
- The site-wide conventions that still apply (apex canonicals, CSP with `script-src
  'self'`, social meta) are stated in the [root guide](../AGENTS.md) and enforced by
  `code/src/seo_invariants.py` where it can see them.

Repository rules: [root guide](../AGENTS.md).
