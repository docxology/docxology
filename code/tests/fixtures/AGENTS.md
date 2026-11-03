# AGENTS.md — `code/tests/fixtures/`

Test fixture data: `frozen-work-keys.json` freezes the bibliography's
`num → citation_key` mapping so `code/tests/test_frozen_work_keys.py` can fail if an
existing work is ever re-slugged.

- This is a contract, not a convenience: `works/{citation_key}.html` is a permanent
  public URL, so a changed key is a 404 for anyone citing it. Update the fixture only
  through the workflow that adds a new work, never by editing an existing entry.
- The suite that reads it is the check; there is no separate schema validation of the
  fixture.

Repository rules: [root guide](../../../AGENTS.md).
