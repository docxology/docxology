# Design system — danielarifriedman.com

Extracted from [`style.css`](../../style.css). Generated pages and new UI should reuse these tokens rather than introducing parallel palettes.

## Principles

- Editorial dark theme: warm neutrals, gold accent, restrained motion (`prefers-reduced-motion` honored).
- Body copy uses system UI stack; display headings use **Playfair Display** where loaded.
- Avoid generic “AI landing page” patterns (centered hero stacks, purple gradients, uniform pill buttons everywhere).

## Color tokens (`:root`)

| Token | Role |
| --- | --- |
| `--bg-primary` | Page background `#0c0c0e` |
| `--bg-secondary` | Secondary surfaces |
| `--bg-card` | Cards, panels |
| `--bg-glass` | Subtle glass overlays |
| `--text-primary` | Primary copy |
| `--text-secondary` | Supporting copy |
| `--text-muted` | Meta, captions |
| `--gold` / `--gold-bright` | Links, accents, focus |
| `--red` | Entomology domain accent |
| `--silver` | Secondary highlights |
| `--border` / `--border-hover` | Dividers, hover states |
| `--radius` | Default corner radius (14px) |

## Typography

- **Body:** `system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- **Display (h1, hero):** `'Playfair Display', Georgia, serif` where font link present
- **Scale:** clamp-based hero headings; body ~1.7 line-height

## Accessibility

- Skip link (`.skip-link`) on main templates
- `:focus-visible` outline — 2px gold, 3px offset
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
