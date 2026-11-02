# AGENTS.md — `code/artifacts/`

A holding folder for generated artifacts that are not part of the site root; today it
contains `publications-explorer/` only.

- Generated output lives here when a generator produces something for direct use rather
  than for publication at the site root. Its rebuild command belongs in
  [`../../GENERATED.md`](../../GENERATED.md) with every other generated path; if it is
  not there, the artifact has no recorded builder.
- Do not edit artifacts here by hand; regenerate them.

Repository rules: [root guide](../../AGENTS.md).
