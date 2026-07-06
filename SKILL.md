---
name: docxology-site
description: "Maintain and extend the docxology public GitHub Pages static site (danielarifriedman.com)"
version: "1.0.0"
tags:
  - github-pages
  - static-site
  - seo
  - accessibility
  - tts
category: web-development
---

# docxology-site — Workflows for danielarifriedman.com

## Overview

This skill guides work on the [docxology](https://github.com/docxology/docxology) public research index site, published via GitHub Pages at `https://danielarifriedman.com/`. The site is a **static generated-artifact repository**: almost every HTML page and JSON file is generated from a source of truth and checked into git.

## Key Architecture Rules

| Principle | Detail |
|-----------|--------|
| **Sources over artifacts** | Edit `pages/BIBLIOGRAPHY.md`, `pages/SOFTWARE.md`, `resume/source.json`, etc. — never hand-edit generated files like `publications.html`, `works/*.html`, `data/*.json` |
| **Rebuild ordering** | After editing a source, run the matching orchestrator from `GENERATED.md`. Order: bibliography → works/exports → domains → search → feed → sitemap |
| **Volatile counts** | Never hard-code current totals in hand-authored docs. Link to `reports/current_counts.md` / `data/current-counts.json` |
| **Work URLs are permanent** | `works/{citation_key}.html` is a permanent opaque identifier. Never re-slug an existing work — if in doubt, freeze with `test_frozen_work_keys.py` |

## Environment

```bash
# Setup (from repo root):
uv venv --python 3.12
uv sync

# Validate generated layer (run before declaring work done):
uv run python3 code/orchestrators/validate_repo.py

# Run tests:
uv run pytest code/tests -q
```

## Interactive Components (added 2026-07-05)

The site now ships three interactive JavaScript modules loaded via `<script defer>`:

### `js/tts-controls.js`
- Web Speech API text-to-speech with a floating control panel
- Auto-collects page content from `<main>` elements
- Controls: play/pause/stop, speed slider, voice selection
- Keyboard shortcut: `T` to toggle TTS panel
- Respects `prefers-reduced-motion`
- Persists speed/voice prefs in `sessionStorage`
- Highlights the paragraph being read
- Public API: `window.__tts.speak(text)`, `window.__tts.stop()`, `window.__tts.toggle()`

### `js/interactive.js`
- **Reading progress bar**: thin gradient bar at the top of every page
- **Scroll-to-top button**: appears after 300px of scrolling
- **Keyboard shortcuts overlay**: press `?` to see all shortcuts
- **Section anchor links**: hover section headings to see `#` copy link
- **Search autocomplete**: loads `search-index.json` and provides live suggestions on search inputs
- **Image lazy loading**: adds `loading="lazy"` to content images
- **External link handling**: adds `rel="noopener noreferrer"` and `target="_blank"`
- Respects `prefers-reduced-motion` throughout

### Adding to new pages
```html
<script src="/js/tts-controls.js?v=20260705" defer></script>
<script src="/js/interactive.js?v=20260705" defer></script>
```

### CSS
All component styles are in `style.css` at the end of the file:
- `.tts-toggle`, `.tts-panel`, `.tts-btn` — TTS controls (z-index 299-300)
- `.reading-progress` — progress bar (z-index 999)
- `.scroll-top`, `.scroll-top-visible` — scroll-to-top button (z-index 290)
- `.shortcuts-overlay`, `.shortcuts-panel` — keyboard shortcuts overlay (z-index 500)
- `.anchor-link` — section heading anchors
- `.search-suggestions`, `.search-suggestion` — autocomplete dropdown
- `.tts-highlight` — highlight for content being read aloud

All components have responsive breakpoints at 860px and 480px, print styles, and reduced-motion overrides.

## SEO Standards

Every page must have:
- `<link rel="canonical" href="https://danielarifriedman.com/...">`
- `<meta name="robots" content="index, follow">`
- `og:title`, `og:description`, `og:url`, `og:image`
- `twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`
- JSON-LD `BreadcrumbList` for navigation context
- Resource hints: `dns-prefetch` for Google Fonts, `prefetch` for expected next pages
- `rel="me"` for identity verification
- `hreflang` support
- `dateModified` / `datePublished` structured data

## Testing Interactive Components

To verify the interactive layer:
1. Open any page and press `T` — TTS panel should appear
2. Press `?` — keyboard shortcuts overlay should appear
3. Scroll down — progress bar should fill, scroll-to-top button appears
4. On search page — typing in search should show autocomplete suggestions
5. Hover any section heading (`h2` inside a section) — anchor link `#` should appear
6. Service worker should cache the new JS files (check Application → Service Workers in DevTools)

## Pitfalls

- **TTS not available**: `speechSynthesis` is undefined in some browsers (FireFox private mode, older browsers). The TTS module gracefully degrades — no errors.
- **Service worker update**: After changing cache name (`CACHE_NAME`), the old cache is cleaned automatically on `activate`. Force-refresh clients to see new content immediately.
- **Autocomplete only works on pages with `search-input` class input**: The MutationObserver catches dynamically added inputs.
- **Section anchors**: Only work on `<section>` / `.section` elements with `id` attributes that contain `<h2>` children.
- **Menu-esc script**: The `/*menu-esc*/` minimal script must remain the very last `<script>` tag before `</body>` so it runs after all other scripts.