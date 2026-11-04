# AGENTS.md — `css/`

Two stylesheets with different consumers; the difference decides how a change is checked.

- `home.css` is linked from `../index.html`, the only tracked page that links it. The
  shared styles and navigation it deliberately leaves out live in `../style.css`;
  the file's own first line points there.
- `research-tools.css` is not linked from any tracked page.
  `build_research_tools.py` injects it into generated research pages, `audit_assets.py`
  holds it to a 50,000-byte budget, and `verify_deployed_artifact.py` lists it as a
  deployed asset. Adding it to a hand-written page's `<head>` would be a second,
  unverified consumer.
- Design tokens and the editorial system are documented in
  [`../docs/design/design-system.md`](../docs/design/design-system.md).
- Repository rules are in [`../AGENTS.md`](../AGENTS.md).
