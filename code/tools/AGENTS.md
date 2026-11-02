# AGENTS.md — `code/tools/`

Site tooling that is not an orchestrator: `rendered_site_fixture.py` (builds the
rendered-site fixture the accessibility audit runs against) and `vendor/` for vendored
third-party libraries.

- Keep the distinction: `code/orchestrators/` holds the runnable pipeline steps listed
  in `GENERATED.md`, while this folder holds supporting code with no entry in the
  generated-file matrix.
- `rendered_site_fixture.py` exists so the audit can run offline; it does not publish
  anything.
- Nothing here is covered by its own test module; the audit and validation that use it
  are the checks.

Repository rules: [root guide](../../AGENTS.md).
