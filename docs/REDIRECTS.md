# Redirect And Canonical Policy

This site is served by GitHub Pages at `https://danielarifriedman.com/`, with `CNAME` set to the apex domain. GitHub Pages does not support arbitrary server-side redirects in this repository, so canonical hygiene is handled with explicit links, canonical tags, and sitemap discipline.

## Canonical Rules

- Use `https://danielarifriedman.com/` for public canonical URLs.
- Keep `www` URLs out of `rel="canonical"`, Open Graph `og:url`, sitemap `loc`, and machine-readable exports.
- Keep redirect-only or compatibility stub pages out of the sitemap when their canonical target is another page.
- Keep source Markdown paths in GitHub links, but use apex URLs for public HTML pages.
- **Full public crawl:** `robots.txt` uses `Allow: /` with no `Disallow` rules. Sitemap lists index-priority URLs only; `llms.txt` documents the full public path inventory.
- **Publication canonicals:** `works/{citation_key}.html` is the primary index target; `papers/{folder}/` pages use `noindex, follow` and canonical to the matching work page.

## Work URLs are a permanent contract

`works/{citation_key}.html` is a **permanent opaque identifier**, not a display string. The
`citation_key` (`Friedman{year}{TitleSlug}{num:03d}`) is also the BibTeX key in
`bibliography.bib`, so external academics may have cited it. This host has no server-side
redirects, so a changed key = a 404 (or a forever-maintained meta-refresh stub).

- **Never re-slug an existing work's key on a title/year edit.** The work's `num` is its
  immutable id; if you must fix a title, keep the URL stable.
- Uniqueness is enforced at build time (`build_work_pages.py` raises on a duplicate
  `citation_key`) and stability is guarded by `code/tests/test_frozen_work_keys.py`
  (freezes every existing `num -> citation_key`; adds/removes are fine, churn fails).
- New works get the next `num` (`max+1`, auto-assigned by `add_zenodo_only.py`); gaps from
  removed works are retired, never renumbered (`sync_publications_html.validate_rows`).

## Known Entry Points

- Homepage: `https://danielarifriedman.com/`
- Bibliography: `https://danielarifriedman.com/publications.html`
- Works index: `https://danielarifriedman.com/works/`
- Domains: `https://danielarifriedman.com/domains.html`
- Software: `https://danielarifriedman.com/software.html`
- Discovery: `https://danielarifriedman.com/discovery.html`
- Citation: `https://danielarifriedman.com/cite-verify.html`
- Evidence: `https://danielarifriedman.com/evidence.html`

## Maintenance Checklist

- After adding a public page, update or regenerate `sitemap.xml`.
- Add `rel="canonical"` to the page head.
- Add `og:url` and, when useful, a section-specific `og:image`.
- Add the page to `llms.txt` if agents should discover it.
- Add local links from at least one human navigation surface.
- Do not list redirect-only stubs in `sitemap.xml`.
- After major SEO/sitemap changes, run `uv run python3 code/orchestrators/gsc_followup_preflight.py` then follow [GSC_FOLLOWUP.md](GSC_FOLLOWUP.md) in a signed-in browser.
