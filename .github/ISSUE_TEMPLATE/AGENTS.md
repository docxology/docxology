# AGENTS.md — `.github/ISSUE_TEMPLATE/`

The repository's issue forms: broken link, publication correction, software metadata,
and source verification, plus `config.yml` for the chooser. They are the structured
public intake for corrections to a bibliography, a catalog entry, or a page.

- A field in a form is a promise that something downstream reads it: check the
  orchestrator or validation that consumes a field before renaming or removing one.
- Nothing tests these files. A malformed form is visible only to someone trying to open
  an issue, and no CI job parses them.

Repository rules: [root guide](../../AGENTS.md).
