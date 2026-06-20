# AGENTS.md — `docs/design/components/`

Local component-preview library for danielarifriedman.com — the **local** side of a
`/design-sync` with the Claude Design project **"danielarifriedman.com Design System"**.

## Rules

- Each `*.html` is a **standalone** preview: it inlines the real token `:root` values from
  [`../../../style.css`](../../../style.css) so it renders in isolation. Do not depend on
  `style.css` at runtime.
- The **first line** must be `<!-- @dsCard group="…" title="…" -->` — the Design System pane
  builds its card index from this marker.
- Tokens are mirrored from `style.css`; when those change, update the affected preview here,
  then re-sync that component. Sync is **incremental** (one component at a time), never a
  wholesale replace. Never hand-edit the remote project — edit here and push.
- See [`README.md`](README.md) for the card inventory and
  [`../design-system.md`](../design-system.md) for the canonical token table.
