# Accessibility, browser, and visual QA

Run static checks after any HTML/CSS/JavaScript change and dynamic checks after
interactive-layer changes:

```bash
python3 code/orchestrators/accessibility_audit.py --strict
python3 code/orchestrators/browser_smoke.py
/opt/homebrew/opt/python@3.13/bin/python3.13 code/orchestrators/browser_qa.py
/opt/homebrew/opt/python@3.13/bin/python3.13 code/orchestrators/browser_qa.py --check
python3 code/orchestrators/visual_qa.py
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
components.
