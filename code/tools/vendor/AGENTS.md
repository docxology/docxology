# AGENTS.md — `code/tools/vendor/`

Vendored third-party libraries — currently `axe.min.js` (axe-core), used by the
repository's accessibility audit.

- Vendored means copied in deliberately, not managed by a package manager: there is no
  lockfile entry to update. When upgrading, replace the file and record the version and
  source where the audit reads it.
- Do not edit a vendored file to change behaviour; fix the call site or upgrade the
  library.

Repository rules: [root guide](../../../AGENTS.md).
