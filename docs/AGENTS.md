# AGENTS.md — `docs/`

Reserved for repository-level documentation beyond the `pages/` hub (architecture notes, runbooks, migration logs).

See root [AGENTS.md](../AGENTS.md) for site/SEO, teaching-line alignment (`index.html`, `pages/PROFILE.md`, `README` Educator bullet), and maintenance log. The [pages/README](../pages/README.md) hub still lists **107** paper folders under `papers/`. Add long-form architecture or runbooks here when they outgrow the root index.

## Bibliography vs paper folders

- [pages/BIBLIOGRAPHY.md](../pages/BIBLIOGRAPHY.md) is the **114-row** unified table (works); the **Docs** column links to a folder under [papers/](../papers/) only when one exists.
- [papers/](../papers/) has **107** per-work folders (README / AGENTS / SKILL); rows without a folder (e.g. some YouTube series or Udemy courses) have no duplicate in-tree index row beyond BIBLIOGRAPHY.
- After table **adds or reorders**, run [`papers/sync_publications_html.py`](../papers/sync_publications_html.py) with `--apply` so [publications.html](../publications.html) **PUBS** and JSON-LD **mainEntity** stay in table order and length.
- [`papers/biblio_table.py`](../papers/biblio_table.py) is the shared eight-column parser used by `sync_publications_html` and [`papers/regenerate_docs.py`](../papers/regenerate_docs.py).

