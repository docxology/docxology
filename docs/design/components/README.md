# danielarifriedman.com — local component library

Source-of-truth previews for the website's design system, extracted from
[`style.css`](../../../style.css) and documented in
[`../design-system.md`](../design-system.md). Each `*.html` file is a standalone,
self-contained preview that carries a first-line `<!-- @dsCard group="…" -->` marker so
the Claude Design ("/design-sync") Design System pane can index it.

## Sync

This directory is the **local** side of a `/design-sync` with the Claude Design project
**"danielarifriedman.com Design System"**. Sync is incremental — one component at a time,
never a wholesale replace.

- Each preview inlines the real token `:root` values so it renders in isolation.
- When `style.css` tokens change, update the affected preview here, then push it.
- Do not hand-edit the remote project; edit here and re-sync.

## Cards

| Group | File | Component |
| --- | --- | --- |
| Foundations | `foundations-colors.html` | Color tokens |
| Foundations | `foundations-typography.html` | Type scale |
| Foundations | `foundations-spacing.html` | Radius + spacing |
| Components | `components-buttons.html` | `.btn` / `.btn-gold` / `.btn-outline` |
| Components | `components-navigation.html` | Top navigation bar |
| Components | `components-cards.html` | `.section` content card |
| Components | `components-pills.html` | Domain pills + type badges |
| Components | `components-publication-table.html` | `.pub-table` row sample |
