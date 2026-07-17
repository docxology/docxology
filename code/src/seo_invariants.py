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
from site_nav import canonical_work_key  # noqa: E402

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
_META_PROPERTY = re.compile(r'<meta\s+property="([^"]+)"\s+content="([^"]*)"', re.I)
_META_NAME = re.compile(r'<meta\s+name="([^"]+)"\s+content="([^"]*)"', re.I)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _meta_robots(html: str) -> str | None:
    match = _META_ROBOTS.search(html)
    return match.group(1).strip().lower() if match else None


def _canonical(html: str) -> str | None:
    match = _LINK_CANONICAL.search(html)
    return match.group(1).strip() if match else None


def _property_meta(html: str, prop: str) -> str | None:
    for key, value in _META_PROPERTY.findall(html):
        if key.lower() == prop.lower():
            return value
    return None


def _name_meta(html: str, name: str) -> str | None:
    for key, value in _META_NAME.findall(html):
        if key.lower() == name.lower():
            return value
    return None


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
            # Duplicate works canonicalize to their primary entry (see WORK_CANONICAL_OVERRIDES).
            expected = f"{SITE_ORIGIN}works/{canonical_work_key(path.stem)}.html"
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


import html as _html_mod


def _meta_description(html: str) -> str | None:
    match = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', html, re.I)
    return match.group(1) if match else None


def check_social_meta(repo_root: Path) -> list[str]:
    """Every indexable page with an og:image must also carry a Twitter Card
    (twitter:card) and og:image:alt, so X/Slack/Discord render rich previews."""
    errors: list[str] = []
    paths = sorted(repo_root.glob("*.html")) + sorted((repo_root / "works").glob("*.html"))
    for path in paths:
        html = _read(path)
        robots = _meta_robots(html)
        if robots and robots.startswith("noindex"):
            continue
        if 'property="og:image"' not in html:
            continue
        rel = str(path.relative_to(repo_root))
        if 'name="twitter:card"' not in html:
            errors.append(f"{rel}: og:image present but missing twitter:card")
        if 'property="og:image:alt"' not in html:
            errors.append(f"{rel}: og:image present but missing og:image:alt")
        if 'name="twitter:image:alt"' not in html:
            errors.append(f"{rel}: og:image present but missing twitter:image:alt")
        if path.parent == repo_root:
            og_title = _property_meta(html, "og:title")
            twitter_title = _name_meta(html, "twitter:title")
            image_alt = _property_meta(html, "og:image:alt")
            if og_title and twitter_title and og_title != twitter_title:
                errors.append(f"{rel}: twitter:title {twitter_title!r} != og:title {og_title!r}")
            if og_title and image_alt and og_title != image_alt:
                errors.append(f"{rel}: og:image:alt {image_alt!r} != og:title {og_title!r}")
    return errors


def check_work_descriptions(repo_root: Path) -> list[str]:
    """Work-page meta descriptions must be clipped on a word boundary, never by
    a hard character cut. Truncated descriptions end with an ellipsis (…); the
    rendered (unescaped) length must stay within the ~160-char SERP budget.
    Word-boundary correctness itself is covered by the clip_description unit
    test in test_site_nav.py."""
    errors: list[str] = []
    for path in sorted((repo_root / "works").glob("*.html")):
        if path.name == "index.html":
            continue
        desc = _meta_description(_read(path))
        if desc is None:
            errors.append(f"works/{path.name}: missing meta description")
            continue
        rendered = _html_mod.unescape(desc)
        if len(rendered) > 160:
            errors.append(f"works/{path.name}: meta description {len(rendered)} rendered chars (>160)")
    return errors


def check_public_html_security(repo_root: Path) -> list[str]:
    """Check security metadata and crawler-visible JSON-LD across public HTML."""
    errors: list[str] = []
    excluded = {".git", "node_modules", "docs", "code", "reports", "netlify-stripe-webhook"}
    for path in sorted(repo_root.rglob("*.html")):
        if excluded.intersection(path.parts):
            continue
        text = _read(path)
        rel = str(path.relative_to(repo_root))
        if path.name == "googlef0f1a1a4a7ba4be8.html":
            continue
        # Redirects, legacy paper folders, and other intentionally non-indexable
        # documents are allowed to omit the indexable-page security head. Their
        # canonical/robots policy is checked separately above.
        robots = _meta_robots(text)
        if robots and "noindex" in robots:
            continue
        if 'http-equiv="Content-Security-Policy"' not in text:
            errors.append(f"{rel}: missing CSP meta policy")
        else:
            match = re.search(r'http-equiv="Content-Security-Policy"\s+content="([^"]+)"', text, re.I)
            policy = match.group(1) if match else ""
            if "frame-src https://www.youtube-nocookie.com" not in policy:
                errors.append(f"{rel}: CSP missing YouTube frame-src allowlist")
            if "fonts.googleapis.com" in policy or "fonts.gstatic.com" in policy:
                errors.append(f"{rel}: CSP retains removed runtime font provider")
        if 'name="referrer"' not in text:
            errors.append(f"{rel}: missing referrer policy")
        if re.search(r'<script\s+type=["\']application/ld\+json["\'][^>]*\ssrc=', text, re.I):
            errors.append(f"{rel}: JSON-LD must be inline, not external script src")
        for iframe in re.findall(r"<iframe\b[^>]*>", text, re.I):
            src = re.search(r'\bsrc="([^"]+)"', iframe, re.I)
            if src and "youtube-nocookie.com" in src.group(1):
                if 'referrerpolicy="strict-origin-when-cross-origin"' not in iframe:
                    errors.append(f"{rel}: YouTube iframe missing referrerpolicy")
                if 'title="' not in iframe:
                    errors.append(f"{rel}: iframe missing accessible title")
    return errors


def collect_seo_errors(repo_root: Path | None = None) -> list[str]:
    root = repo_root or REPO_ROOT
    errors: list[str] = []
    errors.extend(check_paper_pages(root))
    errors.extend(check_work_pages(root))
    errors.extend(check_redirect_stubs(root))
    errors.extend(check_sitemap_policy(root))
    errors.extend(check_social_meta(root))
    errors.extend(check_work_descriptions(root))
    errors.extend(check_public_html_security(root))
    return errors
