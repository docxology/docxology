# AGENTS.md — `code/templates/`

HTML templates used by the site generators — `publications.html.tmpl` and
`software.html.tmpl`, rendered by `code/orchestrators/sync_publications_html.py` and
`sync_software_html.py`.

- A template change is only half a change: run the matching sync orchestrator with
  `--apply` afterwards so the generated page matches, then
  `uv run python3 code/orchestrators/validate_repo.py`.
- The templates carry the site's head conventions (canonical, social meta, CSP); the
  rules are enforced by `code/src/seo_invariants.py`, not stated here.
- No test renders a template in isolation: a bad edit shows up in the regenerated page
  or in validation, not in a template-specific failure.

Repository rules: [root guide](../../AGENTS.md).
