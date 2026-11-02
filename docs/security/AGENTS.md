# AGENTS.md — `docs/security/`

The written security posture: [`security-posture.md`](security-posture.md) states what
the site is (static GitHub Pages, no server-side execution except the separate Netlify
webhook service) and which controls hold it there.

- The enforcement lives elsewhere: CSP is delivered by page `<meta>` tags, the SEO and
  accessibility invariants are checked by `code/src/seo_invariants.py` and the audit
  orchestrators, and validation is the repository gate. Change the control and update
  this document, or the document describes a posture nobody maintains.
- No test reads these documents.

Docs-tree guide: [`../AGENTS.md`](../AGENTS.md).
