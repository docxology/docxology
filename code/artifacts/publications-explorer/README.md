# Publications explorer artifact

Standalone interactive bibliography viewer. Loads the same canonical catalog as the live publications page (`/data/works.json` when served from site root).

## Usage

Open [`publications-explorer.html`](publications-explorer.html) in a browser while serving the **repository root** (e.g. `python3 -m http.server` from docxology/) so `/data/works.json` and site assets resolve.

## web-artifacts-builder path (optional React upgrade)

To rebuild as a React + shadcn bundle per the Cursor web-artifacts-builder skill:

```bash
bash ~/.cursor/plugins/cache/anthropic-agent-skills/document-skills/*/skills/web-artifacts-builder/scripts/init-artifact.sh publications-explorer
cd publications-explorer
# implement UI loading /data/works.json
bash ../scripts/bundle-artifact.sh
```

Copy the resulting `bundle.html` here or wire output into [`js/publications.js`](../../../js/publications.js).

The production site uses vanilla [`js/publications.js`](../../../js/publications.js) on [`publications.html`](../../../publications.html) — no React runtime on GitHub Pages unless explicitly bundled.
