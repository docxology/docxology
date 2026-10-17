# AGENTS.md — `works/`

Generated per-work HTML landing pages and the works index. These are tracked
public projections of `pages/BIBLIOGRAPHY.md`, paper metadata, and the work
identifier registry. Follow the root repository instructions.

- Edit authoritative sources and run `code/orchestrators/build_work_pages.py`
  through the ordered `regenerate_all.py` pipeline; do not hand-edit HTML.
- Preserve permanent citation keys and existing inbound URLs.
- Review and commit authorized generated changes on a work branch, following
  the payload/control-tail sequence in `docs/operations/settle.md`.
- Validate generated pages, metadata, local links, and sitemap coverage with
  `code/orchestrators/validate_repo.py` before publishing.
