"""SEO invariant checks for publication canonicals, sitemap policy, and redirect stubs."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

from build_sitemap import sitemap_locs  # noqa: E402

SITE_ORIGIN = "https://danielarifriedman.com/"

REDIRECT_STUBS: list[tuple[str, str]] = [
    ("about.html", SITE_ORIGIN),
    ("blog/index.html", SITE_ORIGIN),
    ("meditations.html", SITE_ORIGIN),
    ("research.html", SITE_ORIGIN),
    ("nft.html", "https://danielarifriedman.com/art.html"),
    ("blog/winged-snowflake-2021/index.html", "https://danielarifriedman.com/art.html"),
]

_META_ROBOTS = re.compile(r'<meta\s+name="robots"\s+content="([^"]+)"', re.I)
_LINK_CANONICAL = re.compile(r'<link\s+rel="canonical"\s+href="([^"]+)"', re.I)
_SITEMAP_LOC = re.compile(r"<loc>(https://danielarifriedman\.com/[^<]*)</loc>")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _meta_robots(html: str) -> str | None:
    match = _META_ROBOTS.search(html)
    return match.group(1).strip().lower() if match else None


def _canonical(html: str) -> str | None:
    match = _LINK_CANONICAL.search(html)
    return match.group(1).strip() if match else None


def _works_by_docs_path(repo_root: Path) -> dict[str, dict]:
    works = json.loads((repo_root / "data" / "works.json").read_text(encoding="utf-8"))["works"]
    out: dict[str, dict] = {}
    for work in works:
        path = str(work.get("docs_path") or "").strip().rstrip("/")
        if path:
            out[path] = work
    return out


def check_paper_pages(repo_root: Path) -> list[str]:
    errors: list[str] = []
    for docs_path, work in _works_by_docs_path(repo_root).items():
        rel = f"{docs_path}/index.html"
        path = repo_root / rel
        if not path.is_file():
            errors.append(f"missing paper page: {rel}")
            continue
        html = _read(path)
        robots = _meta_robots(html)
        if robots != "noindex, follow":
            errors.append(f"{rel}: expected robots noindex, follow; got {robots!r}")
        expected = f"{SITE_ORIGIN}works/{work['citation_key']}.html"
        canonical = _canonical(html)
        if canonical != expected:
            errors.append(f"{rel}: canonical {canonical!r} != {expected!r}")
        if "application/ld+json" in html:
            errors.append(f"{rel}: noindex paper page must not emit JSON-LD")
    return errors


def check_work_pages(repo_root: Path) -> list[str]:
    errors: list[str] = []
    works_dir = repo_root / "works"
    for path in sorted(works_dir.glob("*.html")):
        rel = f"works/{path.name}"
        html = _read(path)
        robots = _meta_robots(html)
        if robots != "index, follow":
            errors.append(f"{rel}: expected robots index, follow; got {robots!r}")
        canonical = _canonical(html)
        if path.name == "index.html":
            expected = f"{SITE_ORIGIN}works/"
        else:
            expected = f"{SITE_ORIGIN}{rel}"
        if canonical != expected:
            errors.append(f"{rel}: canonical {canonical!r} != {expected!r}")
    return errors


def check_redirect_stubs(repo_root: Path) -> list[str]:
    errors: list[str] = []
    for rel, expected_canonical in REDIRECT_STUBS:
        path = repo_root / rel
        if not path.is_file():
            errors.append(f"missing redirect stub: {rel}")
            continue
        html = _read(path)
        robots = _meta_robots(html)
        if robots != "noindex, follow":
            errors.append(f"{rel}: expected robots noindex, follow; got {robots!r}")
        canonical = _canonical(html)
        if canonical != expected_canonical:
            errors.append(f"{rel}: canonical {canonical!r} != {expected_canonical!r}")
    return errors


def check_sitemap_policy(repo_root: Path) -> list[str]:
    errors: list[str] = []
    text = _read(repo_root / "sitemap.xml")
    actual = _SITEMAP_LOC.findall(text)
    expected = sitemap_locs()
    if sorted(actual) != sorted(expected):
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        if missing:
            errors.append(f"sitemap missing policy URLs: {', '.join(missing[:5])}" + (" ..." if len(missing) > 5 else ""))
        if extra:
            errors.append(f"sitemap has non-policy URLs: {', '.join(extra[:5])}" + (" ..." if len(extra) > 5 else ""))
    for loc in actual:
        if "/papers/" in loc:
            errors.append(f"sitemap must not list paper folder: {loc}")
    return errors


def collect_seo_errors(repo_root: Path | None = None) -> list[str]:
    root = repo_root or REPO_ROOT
    errors: list[str] = []
    errors.extend(check_paper_pages(root))
    errors.extend(check_work_pages(root))
    errors.extend(check_redirect_stubs(root))
    errors.extend(check_sitemap_policy(root))
    return errors
