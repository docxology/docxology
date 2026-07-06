# TTS Controls — Text-to-Speech Integration

Added: 2026-07-05

## Overview

The TTS (Text-to-Speech) system integrates the Web Speech API to provide read-aloud functionality across the site. It appears as a floating button in the bottom-right corner of every page.

## Source Files

| File | Purpose |
|------|---------|
| `js/tts-controls.js` | Core TTS logic |
| `style.css` | All `.tts-*` CSS classes (appended at end of file) |

## Architecture

```
User clicks 🔊 → Panel slides up → User presses ▶
  → JS collects all <p>, <h1-6>, <li>, <td> content from <main>
  → Filters out short fragments (< 15 chars) and boilerplate
  → speechSynthesis.speak(utterance) with selected voice + speed
  → Each paragraph highlighted with .tts-highlight
  → Auto-scrolls to current paragraph
  → Progress bar fills as reading advances
```

## Features

### Content Detection
- Auto-collects readable paragraphs from `<main>` element
- Skips elements with `data-tts="skip"` attribute
- Skips navigation bars, filter rows, table headers, footer, profile links
- Adds heading prefix (e.g. `H2: ...`) for context
- Filters out fragments < 15 characters and boilerplate patterns

### Voice Selection
- Default: prefers British English (en-GB) local voices, then US English (en-US), then any English
- User can select from all available system voices via the dropdown
- Voice preference persisted in `sessionStorage`

### Speed Control
- Range slider from 0.3× to 2.0× (default: 0.95×)
- When changed mid-speech, restarts current paragraph at new speed
- Pref persisted in `sessionStorage`

### Controls
| Button | Action |
|--------|--------|
| ▶ | Play / Resume |
| ⏸ | Pause |
| ⏹ | Stop |
| × | Close panel |
| `T` key | Toggle TTS panel |

### Visual Feedback
- `.tts-highlight` outline + background on the paragraph being read
- Progress bar at bottom of panel
- Status text ("Reading paragraph 3 of 42…")
- Auto-scroll (configurable via checkbox)

## Public API

```js
// Programmatic access (console or other scripts):
window.__tts.speak()       // Read current page content
window.__tts.speak("Custom text here")  // Read custom text
window.__tts.stop()        // Stop reading
window.__tts.pause()       // Pause
window.__tts.resume()      // Resume
window.__tts.toggle()      // Open/close panel
```

## Adding TTS to New Pages

The TTS script auto-initializes on DOMContentLoaded. To add to a new page:

```html
<script src="/js/tts-controls.js?v=20260705" defer></script>
```

No additional markup required. The script creates:
- A floating toggle button (`.tts-toggle`) appended to `document.body`
- A floating panel (`.tts-panel`) appended to `document.body`

### Excluding Elements from TTS

Add `data-tts="skip"` to any element that should be skipped during reading:

```html
<aside data-tts="skip" class="sidebar">…</aside>
```

Elements inside `<nav>`, `.filter-row`, `.media-tabs`, `table thead`, `.footer-links`, and `.profile-links` are auto-skipped.

## Accessibility

- Panel uses `role="region"` with `aria-label="Text to speech controls"`
- Status updates use `aria-live="polite"` region
- Buttons have descriptive `aria-label`
- Respects `prefers-reduced-motion`: all animations disabled
- Close button focus management on panel open
- Escape key closes panel

## Browser Compatibility

| Browser | Support | Notes |
|---------|---------|-------|
| Chrome | Full | Voices load async via `voiceschanged` event |
| Firefox | Full | Some voices may be missing in Private Mode |
| Safari | Full | Limited voice selection |
| Edge | Full | Same engine as Chrome |

The script performs a feature check for `window.speechSynthesis` and exits silently if absent.

## Print & Responsive

- TTS controls hidden in print styles
- Panel collapses to full-width on mobile (< 860px)
- Toggle button repositioned on small screens
- All transitions disabled when `prefers-reduced-motion: reduce`