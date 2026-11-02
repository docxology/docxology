# AGENTS.md — `feeds/`

The site's per-domain feeds (`domain-*.xml`), built from the published works and pages
by the domain-page generator rather than edited by hand.

- Regenerate them through the pipeline (see [`../GENERATED.md`](../GENERATED.md) and the
  ordered plan in `code/src/generation_plan.py`) instead of editing XML: the feed
  content is a view over the bibliography and the domain pages.
- Feed URLs are public interfaces — readers cache them — so a filename change is a
  breaking change, not a tidy-up.
- Nothing validates the XML in CI directly; the generated-layer checks cover the
  surrounding pages, so a malformed feed can survive the gate.

Repository rules: [root guide](../AGENTS.md).
