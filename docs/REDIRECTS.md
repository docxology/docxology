# Redirect And Canonical Policy

This site is served by GitHub Pages at `https://danielarifriedman.com/`, with `CNAME` set to the apex domain. GitHub Pages does not support arbitrary server-side redirects in this repository, so canonical hygiene is handled with explicit links, canonical tags, and sitemap discipline.

## Canonical Rules

- Use `https://danielarifriedman.com/` for public canonical URLs.
- Keep `www` URLs out of `rel="canonical"`, Open Graph `og:url`, sitemap `loc`, and machine-readable exports.
- Keep redirect-only or compatibility stub pages out of the sitemap when their canonical target is another page.
- Keep source Markdown paths in GitHub links, but use apex URLs for public HTML pages.
- **Full public crawl:** `robots.txt` uses `Allow: /` with no `Disallow` rules. Sitemap lists index-priority URLs only; `llms.txt` documents the full public path inventory.
- **Publication canonicals:** `works/{citation_key}.html` is the primary index target; `papers/{folder}/` pages use `noindex, follow` and canonical to the matching work page.

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
