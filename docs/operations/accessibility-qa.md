# Accessibility, browser, and visual QA

Run static checks after any HTML/CSS/JavaScript change and dynamic checks after
interactive-layer changes:

```bash
uv run python3 code/orchestrators/accessibility_audit.py --check
uv sync --extra browser-qa
uv run --extra browser-qa playwright install chromium
uv run --extra browser-qa python3 code/orchestrators/browser_smoke.py
uv run --extra browser-qa python3 code/orchestrators/browser_qa.py
uv run --extra browser-qa python3 code/orchestrators/browser_qa.py --check
uv run --extra browser-qa python3 code/orchestrators/visual_qa.py
```

The progressive suite covers no-JavaScript fallbacks, keyboard and Escape
behavior, filter/sort state, lightbox focus restoration, reduced motion,
forced-colors, 320px layout, YouTube iframe policy, console errors, and CSP
warnings. The known meta-CSP `frame-ancestors` limitation is retained as a
warning because GitHub Pages does not provide response-header control; other
console or page errors fail the report.

Check screenshots at representative desktop, mobile, high-zoom, and print
states. Preserve intrinsic image dimensions, meaningful alt text, lazy loading,
transcript links, and non-JavaScript content when changing gallery or video
components. A deployment attestation additionally requires an explicit visual
review record. Capture first, inspect those exact post-deploy PNGs, then record
the review without recapturing them:

```bash
uv run --extra browser-qa python3 code/orchestrators/visual_qa.py
# Inspect reports/visual-qa/<date>/*.png.
uv run --extra browser-qa python3 code/orchestrators/visual_qa.py \
  --approve-existing --reviewed-by "Reviewer name"
```

Approval verifies the existing screenshot hashes and coverage before changing
only the review record; `--reviewed-by` cannot stamp a new capture directly.
