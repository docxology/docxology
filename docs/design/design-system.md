# Design system — danielarifriedman.com

Extracted from [`style.css`](../../style.css). Generated pages and new UI should reuse these tokens rather than introducing parallel palettes.

## Principles

- Editorial dark theme: warm neutrals, **red accent** for links and focus, gold/silver as secondary highlights, restrained motion (`prefers-reduced-motion` honored).
- Body copy uses the **Inter / system-UI** stack; display headings use **Playfair Display**.
- Avoid generic “AI landing page” patterns (centered hero stacks, purple gradients, uniform pill buttons everywhere).

## Color tokens (`:root`)

Values below are the source of truth in [`style.css`](../../style.css) `:root`; the interactive swatches in [`components/foundations-colors.html`](components/foundations-colors.html) mirror them.

| Token | Role | Value |
| --- | --- | --- |
| `--bg-primary` | Page background | `#0a0908` |
| `--bg-secondary` | Secondary surfaces | `#100e0c` |
| `--bg-card` | Cards, panels | `rgba(20,18,16,0.96)` |
| `--bg-glass` | Subtle glass overlays | `rgba(255,252,245,0.028)` |
| `--text-primary` | Primary copy | `#f4f1ea` |
| `--text-secondary` | Supporting copy | `#cfc9bd` |
| `--text-muted` | Meta, captions | `#9a958a` |
| `--red` / `--red-bright` / `--red-pure` | Links, focus, entomology accent | `#e23b2e` / `#ff4133` / `#f1463a` |
| `--red-glow` | Red overlay/glow | `rgba(226,59,46,0.16)` |
| `--gold` / `--gold-bright` | Accents, hover, highlights | `#e8e2d4` / `#ffffff` |
| `--gold-glow` | Gold overlay/glow | `rgba(232,226,212,0.13)` |
| `--silver` / `--silver-bright` | Secondary highlights | `#b8b3a8` / `#f2efe8` |
| `--border` / `--border-hover` | Dividers, hover states | `rgba(244,241,234,0.18)` / `rgba(241,70,58,0.6)` |
| `--paper-line` / `--paper-soft` | Newspaper-style rules, subtle overlays | `rgba(244,241,234,0.2)` / `rgba(244,241,234,0.05)` |
| `--radius` | Default corner radius | `3px` |

Hero artwork is tokenized as `--art-a` … `--art-e` (`assets/hero-art/*.webp`).

## Typography

- **Body:** `'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif` (`font-size: 17px`); Inter is loaded site-wide via Google Fonts (weights 300–800)
- **Display (h1, hero, section headings):** `'Playfair Display', serif`
- **Scale:** clamp-based hero headings; body `line-height: 1.78`

## Accessibility

- Skip link (`.skip-link`) on main templates
- `:focus-visible` outline — 2px red (`--red-pure`), 3px offset
- `@media (prefers-reduced-motion: reduce)` collapses animations
- Table captions and `aria-live` on filter result counts (publications, search)

## Layout components

- Fixed nav (68px) with mobile toggle (`.menu-btn`, `.nav-links.open`)
- `.page-hero` / `.section` / `.section-alt` rhythm
- `.btn`, `.btn-gold`, `.btn-outline` for CTAs
- Publications: `.pub-table`, `.filter-row`, `.domain-pill`

## Navigation source of truth

Shared HTML nav: [`code/src/site_nav.py`](../../code/src/site_nav.py).

- **Work pages:** `render_nav(active=..., depth=1)` — regenerate with `python3 code/orchestrators/build_work_pages.py`
- **Domain pages:** `render_nav_domain(active="domains")` — regenerate with `python3 code/orchestrators/build_domain_pages.py`

Hand-maintained pages (e.g. `publications.html`, `index.html`) may use extended link sets; keep href prefixes consistent with [`seo/canonical-policy.md`](../seo/canonical-policy.md) (apex canonical URLs).

## Component library (local + Claude Design sync)

A self-contained preview library mirrors these tokens and components in
[`components/`](components/) — one standalone `*.html` per component, each carrying a
first-line `<!-- @dsCard group="…" -->` marker. It is the **local** side of a `/design-sync`
with the Claude Design project **"danielarifriedman.com Design System"**.

- Foundations: color tokens, type scale, radius/spacing.
- Components: buttons, navigation, content cards, domain pills + type badges, publication table.
- Sync is **incremental** — one component at a time, never a wholesale replace. Edit the
  preview here when `style.css` tokens change, then push it; never hand-edit the remote project.

## Future refresh (Claude Design / Webdesign)

Optional hero/nav refresh via Claude Design should:

1. Read this token table and the [`components/`](components/) previews first.
2. Scope to index + publications shells only.
3. Preserve bibliography copy and machine-readable head metadata.
4. Re-run visual QA (`code/orchestrators/visual_qa.py`) after integration.
