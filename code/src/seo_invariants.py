"""SEO invariant checks for publication canonicals, sitemap policy, and redirect stubs."""

from __future__ import annotations

import json
import re
import sys
import urllib.parse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

from build_sitemap import sitemap_locs  # noqa: E402
from deploy_seo_security import EXCLUDED_HTML_PATH_PARTS  # noqa: E402
from redirect_stubs import REDIRECT_STUBS, collect_redirect_errors  # noqa: E402
from site_nav import canonical_work_key  # noqa: E402

SITE_ORIGIN = "https://danielarifriedman.com/"

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
    return collect_redirect_errors(repo_root)


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


def _dir_form(rel: str) -> str:
    """Normalize "dir/index.html", "dir/", "index.html", and "" to one form."""
    if rel in ("index.html", ""):
        return ""
    if rel.endswith("/index.html"):
        return rel[: -len("index.html")]
    return rel


def check_canonical_integrity(repo_root: Path) -> list[str]:
    """Zero internal links may target a page whose own canonical points elsewhere.

    A link to a URL that self-canonicalizes to a different address dilutes
    ranking signals and contradicts the site canonical policy (docs/seo/
    canonical-policy.md): internal links must target the canonical form.
    Redirect stubs (noindex + canonical away) are the known exception — a link
    to them is a policy violation, not a page defect, and is reported as such.
    """
    errors: list[str] = []
    href_re = re.compile(r'<a\b[^>]*?href=["\x27]([^"\x27]+)["\x27]', re.I)
    canonical_by_rel: dict[str, str] = {}
    pages: list[Path] = []
    for path in sorted(repo_root.rglob("*.html")):
        if EXCLUDED_HTML_PATH_PARTS.intersection(path.parts):
            continue
        if path.name == "googlef0f1a1a4a7ba4be8.html":
            continue
        pages.append(path)
    # Pass 1: record each page's own canonical target (relative to repo root),
    # keyed by the page's own root-relative path. stub.html -> good.html means
    # canonical_by_rel["stub.html"] == "good.html" != "stub.html".
    for path in pages:
        canonical = _canonical(_read(path))
        if not canonical:
            continue
        parsed = urllib.parse.urlsplit(canonical)
        if parsed.netloc and parsed.netloc != "danielarifriedman.com":
            continue
        page_rel = urllib.parse.unquote(
            urllib.parse.urlsplit(f"https://danielarifriedman.com/{path.relative_to(repo_root)}").path
        ).lstrip("/")
        canonical_target = urllib.parse.unquote(parsed.path).lstrip("/")
        canonical_by_rel[page_rel] = canonical_target

    def canonical_points_elsewhere(rel: str) -> bool:
        if rel not in canonical_by_rel:
            return False
        return _dir_form(canonical_by_rel[rel]) != _dir_form(rel)

    # Pass 2: every internal href must not land on an away-canonical page.
    for path in pages:
        html_text = _read(path)
        rel_self = str(path.relative_to(repo_root))
        for href in href_re.findall(html_text):
            link = href.strip()
            if link.startswith(("#", "http://", "https://", "mailto:", "tel:", "javascript:", "data:")):
                if link.startswith("https://danielarifriedman.com/"):
                    link = link.removeprefix("https://danielarifriedman.com/")
                else:
                    continue
            if not link or link.startswith("//"):
                continue
            if "${" in link or "{" in link:
                continue
            link = urllib.parse.unquote(link.split("#", 1)[0].split("?", 1)[0])
            if not link:
                continue
            # Resolve to a repo-root-relative path.
            if link.startswith("/"):
                rel_target = link.lstrip("/")
            else:
                resolved = (path.parent / link).resolve()
                try:
                    rel_target = str(resolved.relative_to(repo_root.resolve()))
                except ValueError:
                    continue
            if canonical_points_elsewhere(rel_target):
                errors.append(
                    f"{rel_self}: internal link {href!r} targets {rel_target}, "
                    "whose canonical points elsewhere"
                )
    return errors


def check_public_html_security(repo_root: Path) -> list[str]:
    """Check security metadata and crawler-visible JSON-LD across public HTML."""
    errors: list[str] = []
    for path in sorted(repo_root.rglob("*.html")):
        # The writer and the invariant checker must agree on what is public
        # HTML. In particular, a local browser/PDF optional dependency must
        # never turn bundled third-party diagnostic pages into site failures.
        if EXCLUDED_HTML_PATH_PARTS.intersection(path.parts):
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
    errors.extend(check_canonical_integrity(root))
    return errors
