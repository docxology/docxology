---
name: docxology-site
description: Maintain the docxology profile README, generated research catalog, and static GitHub Pages site at danielarifriedman.com. Use for repository edits, source-to-output regeneration, and validation.
metadata:
  version: "1.0.0"
---

# Maintain the docxology site

Read [AGENTS.md](AGENTS.md) for repository rules and [AGENT_START.md](AGENT_START.md) for task routing. Use the project’s Python pin and locked environment.

```bash
uv sync --locked --python 3.15
uv run --no-sync python3 code/orchestrators/agent.py status --json
uv run --no-sync python3 code/orchestrators/agent.py plan --json
```

## Edit the source

- Use [the bibliography](pages/BIBLIOGRAPHY.md), [software catalog](pages/SOFTWARE.md), [resume source](resume/source.json), and [generated-output map](GENERATED.md) to find the source of each surface. Edit [the root README](README.md) for the GitHub profile and regenerate the `.github/README.md` mirror. Use Markdown links so the mirror can relocate them.
- Preserve work numbers, citation keys, and public URLs. Follow the [canonical policy](docs/seo/canonical-policy.md) for work and paper routes, redirects, and internal query links. Link to [generated counts](reports/current_counts.md) instead of copying totals into authored docs.
- Use [the paper guide](papers/AGENTS.md) for publication folders and the [publication intake runbook](docs/operations/publication-sync.md) for source and PDF custody. Check ownership before regenerating repository-local paper guides.
- For interactive pages, use the shared navigation and script definitions in [site_nav.py](code/src/site_nav.py). Follow the [runtime](docs/operations/site-runtime.md) and [accessibility](docs/operations/accessibility-qa.md) guides for search, text-to-speech, keyboard behavior, and cache changes.

## Verify the change

- Run the relevant writers and checks from the agent plan. Use `uv run --no-sync python3 code/orchestrators/regenerate_all.py --validate` to regenerate and verify the dependent site outputs.
- Follow [development](docs/operations/development.md) for the CI-equivalent core selection, browser and Lighthouse checks, and full-suite prerequisites.
- Follow [settle](docs/operations/settle.md) for payload and release metadata commits. Use [live verification](docs/operations/live-verification.md) to check the exact deployed commit.
