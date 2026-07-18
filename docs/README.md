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
| **Backlog** | [`../TODO.md`](../TODO.md) | Active unfinished release, evidence, accessibility, Pages, and operating-model work; no completed history |
| **Operations** | [`operations/publication-sync.md`](operations/publication-sync.md) | GitHub + Zenodo publication intake, Zenodo-only backfill, and software-only GitHub record triage |
| **Operations** | [`operations/github-pages-artifact.md`](operations/github-pages-artifact.md) | Bounded GitHub Pages deployment projection, 1 GiB limit, and repository-vs-site asset policy |
| **Operations** | [`operations/release-integrity.md`](operations/release-integrity.md) | Source hashes, CV privacy, Pages artifact, deployment, live verification, and report retention gates |
| **Operations** | [`operations/repository-classification.md`](operations/repository-classification.md) | Complete GitHub inventory versus curated software review queue and description-quality triage |
| **Operations** | [`operations/cv-release.md`](operations/cv-release.md) | CV source-of-truth, generated outputs, privacy, reproducibility, and claim-boundary checks |
| **Operations** | [`operations/evidence-refresh.md`](operations/evidence-refresh.md) | Public-source refresh, publication-pair review, coverage exceptions, and dated claim evidence |
| **Operations** | [`operations/accessibility-qa.md`](operations/accessibility-qa.md) | Static accessibility, browser behavior, responsive, reduced-motion, forced-colors, and visual QA |
| **Operations** | [`operations/live-verification.md`](operations/live-verification.md) | Post-deployment route, JSON-count, Pages-status, and propagation checks |
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
- Keep `TODO.md` limited to unfinished work. Do not copy completed maintenance-log entries into it.
