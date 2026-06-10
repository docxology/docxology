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
    ("domain-art-synergetics.html", "monthly", "0.7"),
    ("domain-computational.html", "monthly", "0.7"),
    ("domain-biomedicine.html", "monthly", "0.7"),
    ("art.html", "weekly", "0.9"),
    ("videos.html", "weekly", "0.8"),
    ("collaborators.html", "monthly", "0.7"),
    ("media.html", "monthly", "0.7"),
    ("software.html", "monthly", "0.7"),
    ("repositories.html", "monthly", "0.6"),
    ("search.html", "monthly", "0.7"),
    ("catalog.html", "monthly", "0.7"),
    ("exports.html", "monthly", "0.7"),
    ("updates.html", "monthly", "0.6"),
    ("discovery.html", "monthly", "0.7"),
    ("cite-verify.html", "monthly", "0.7"),
    ("evidence.html", "monthly", "0.6"),
    ("feed.xml", "weekly", "0.5"),
    ("llms.txt", "monthly", "0.5"),
    ("humans.txt", "monthly", "0.3"),
    ("CITATION.cff", "monthly", "0.5"),
    ("bibliography.bib", "monthly", "0.5"),
    ("bibliography.csl.json", "monthly", "0.5"),
    ("bibliography.ris", "monthly", "0.5"),
    ("codemeta.json", "monthly", "0.5"),
    ("resume/resume.pdf", "monthly", "0.4"),
    ("resume/verify.html", "monthly", "0.4"),
]

SITE_ORIGIN = "https://danielarifriedman.com/"

GSC_PRIORITY_PATHS: tuple[str, ...] = (
    "",
    "exports.html",
    "catalog.html",
    "cite-verify.html",
    "discovery.html",
    "publications.html",
)


def gsc_priority_urls() -> list[str]:
    return [absolute_url(path) for path in GSC_PRIORITY_PATHS]

_INDEXNOW_EXACT = {
    "CITATION.cff",
    "bibliography.bib",
    "bibliography.csl.json",
    "bibliography.ris",
    "codemeta.json",
    "llms.txt",
    "feed.xml",
    "humans.txt",
    "resume/resume.pdf",
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
        if path.endswith(".html") or path == "works/" or path.startswith("works/"):
            out.append(loc)
        elif path in _INDEXNOW_EXACT:
            out.append(loc)
    return out
