"""Index-priority URL policy for sitemap.xml and IndexNow.

The public site is fully crawlable (robots.txt Allow: /). This module lists URLs
we actively promote for web indexing — not a crawl gate.
"""

from __future__ import annotations

# (relative path, changefreq, priority)
INDEX_PRIORITY_STATIC: list[tuple[str, str, str]] = [
    ("", "weekly", "1.0"),
    ("publications.html", "monthly", "0.9"),
    ("works/", "monthly", "0.8"),
    ("domains.html", "monthly", "0.8"),
    ("domain-entomology.html", "monthly", "0.7"),
    ("domain-active-inference.html", "monthly", "0.7"),
    ("domain-cognitive-security.html", "monthly", "0.7"),
    ("cognitive-security.html", "monthly", "0.8"),
    ("computational-entomology.html", "monthly", "0.8"),
    ("insect-cognition.html", "monthly", "0.8"),
    ("active-inference.html", "monthly", "0.8"),
    ("neurosymbolic-ai.html", "monthly", "0.8"),
    ("domain-art-synergetics.html", "monthly", "0.7"),
    ("domain-computational.html", "monthly", "0.7"),
    ("domain-biomedicine.html", "monthly", "0.7"),
    ("art.html", "weekly", "0.9"),
    # NEW-3 (2026-08-28): videos/ is the static machine-readable index; the
    # interactive timeline (videos.html) is the single indexed surface. The
    # index stays crawlable + linked for agents and no-JS visitors but is not
    # a sitemap entry, avoiding a near-duplicate pair.
    ("videos.html", "weekly", "0.8"),
    ("collaborators.html", "monthly", "0.7"),
    ("media.html", "monthly", "0.7"),
    ("software.html", "monthly", "0.7"),
    ("repositories.html", "monthly", "0.6"),
    ("repositories-forks.html", "monthly", "0.35"),
    ("search.html", "monthly", "0.7"),
    ("catalog.html", "monthly", "0.7"),
    ("exports.html", "monthly", "0.7"),
    ("updates.html", "monthly", "0.6"),
    ("discovery.html", "monthly", "0.7"),
    ("cite-verify.html", "monthly", "0.7"),
    ("evidence.html", "monthly", "0.6"),
    ("reproducibility.html", "monthly", "0.7"),
    # Sitemap hygiene (2026-08-28): feed.xml is a non-HTML XML asset — it is
    # discovered via <link rel="alternate"> and robots, not a crawlable page.
    # Sitemap hygiene (2026-08-27): non-HTML metadata exports (llms.txt,
    # humans.txt, CITATION.cff, bibliography.bib/.csl.json/.ris, codemeta.json)
    # were removed from the sitemap — they remain crawlable, discoverable via
    # llms.txt/discovery.html, and reachable through page links. The resume PDF
    # is a legitimately indexable document and stays listed.
    ("resume/resume.pdf", "monthly", "0.4"),
    ("resume/resume.html", "monthly", "0.5"),
    ("resume/verify.html", "monthly", "0.4"),
]

SITE_ORIGIN = "https://danielarifriedman.com/"

GSC_PRIORITY_PATHS: tuple[str, ...] = (
    "",
    "repositories.html",
    "videos.html",
    "videos/",
    "software.html",
    "exports.html",
    "catalog.html",
    "cite-verify.html",
    "discovery.html",
    "publications.html",
    "works/",
)


def gsc_priority_urls() -> list[str]:
    return [absolute_url(path) for path in GSC_PRIORITY_PATHS]

# Exact non-HTML paths submitted to IndexNow. The metadata exports were removed
# from the sitemap (2026-08-27 sitemap hygiene), so they no longer flow through
# indexnow_urls_from_locs; the resume PDF stays both sitemapped and submitted.
_INDEXNOW_EXACT = {
    "resume/resume.pdf",
    "resume/resume.html",
}


def absolute_url(rel_path: str) -> str:
    return SITE_ORIGIN + rel_path


def indexnow_urls_from_locs(locs: list[str]) -> list[str]:
    """URLs submitted to IndexNow: HTML pages, works/*.html, and citation exports."""
    out: list[str] = []
    for loc in locs:
        if loc == SITE_ORIGIN or loc == SITE_ORIGIN.rstrip("/"):
            out.append(SITE_ORIGIN)
            continue
        path = loc.removeprefix(SITE_ORIGIN)
        if path.endswith(".html") or path in {"works/", "videos/"} or path.startswith(("works/", "videos/")):
            out.append(loc)
        elif path in _INDEXNOW_EXACT:
            out.append(loc)
    return out
