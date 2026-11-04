# css

Site stylesheets that the repository's own pages do not all link directly.

- `home.css` — homepage composition. Its first line records the split: "Shared site
  styles and navigation remain in style.css", which lives at `../style.css`. The only
  tracked page that links it is `../index.html`.
- `research-tools.css` — "Research desk primitives extend the existing editorial design
  tokens." No tracked HTML page links it: `../code/orchestrators/build_research_tools.py`
  injects `<link rel="stylesheet" href="/css/research-tools.css?v=1">` into the pages it
  builds, and the file is listed in the asset budget
  (`../code/orchestrators/audit_assets.py`, 50,000 bytes) and in
  `../code/orchestrators/verify_deployed_artifact.py`.
