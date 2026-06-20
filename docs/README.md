# `docs/` — Repository Documentation Index

Repo-level documentation beyond the [`pages/`](../pages/) content hub. Evergreen runbooks
and references live in topic subdirectories; point-in-time snapshots are archived under
[`releases/`](releases/). **Do not repeat volatile counts here** — link to
[`reports/current_counts.md`](../reports/current_counts.md) and
[`data/current-counts.json`](../data/current-counts.json) instead.

Agents: see [`AGENTS.md`](AGENTS.md) for operational guidance (bibliography ↔ folders,
generated-layer rebuild ordering, canonical/reports). This README is the human map.

| Area | Document | What it's for |
|------|----------|---------------|
| **Architecture** | [`AGENTS.md`](AGENTS.md) | Repo structure: bibliography vs paper folders, generated discovery-layer rebuild ordering, volatile-count policy |
| **Operations** | [`operations/publication-sync.md`](operations/publication-sync.md) | GitHub + Zenodo publication intake runbook |
| **SEO** | [`seo/canonical-policy.md`](seo/canonical-policy.md) | Redirect + canonical URL policy; permanent work-URL contract (GitHub Pages) |
| **SEO** | [`seo/gsc-followup.md`](seo/gsc-followup.md) | Google Search Console manual follow-up runbook |
| **Design** | [`design/design-system.md`](design/design-system.md) | Color/type tokens, accessibility, layout, nav source-of-truth |
| **Design** | [`design/components/`](design/components/README.md) | Local component-preview library; `/design-sync` source for the Claude Design project |
| **Security** | [`security/security-posture.md`](security/security-posture.md) | Static-site security posture, XSS, CSP, responsible disclosure |
| **Releases** | [`releases/2026-05-discovery-layer.md`](releases/2026-05-discovery-layer.md) | Archived 2026-05 discovery-layer snapshot |

## Conventions

- **New evergreen doc** → pick the topic directory (`operations/`, `seo/`, `design/`,
  `security/`); create a new dir only when a topic has ≥2 docs.
- **New point-in-time snapshot** → `releases/YYYY-MM-<slug>.md`; never edit an archived
  snapshot in place.
- **Cross-repo entry points:** root [`AGENTS.md`](../AGENTS.md) and
  [`GENERATED.md`](../GENERATED.md) (the exhaustive orchestrator → output rebuild matrix).
- Keep public security/transparency artifacts (`/canary.txt`, `/.well-known/security.txt`)
  documented under [`security/`](security/).
