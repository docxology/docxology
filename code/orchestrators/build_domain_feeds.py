#!/usr/bin/env python3
"""Generate per-domain RSS 2.0 feeds from the works and video datasets.

One feed per domain slug in ``build_domain_pages.DOMAINS``. Items combine
bibliography works (data/works.json) and videos (data/videos.json) whose
topic links target that domain's hub page. Output is fully deterministic:
dates come from the data (works carry only a year, so their pubDate is the
first instant of that year), sorting is total, and no wall-clock time is
consulted. Feeds are written through the shared generated-output writer so
the release-boundary path validation applies.

Discovery: like feed.xml, feeds are non-HTML XML assets. They are NOT added
to the sitemap (NEW-3 precedent, 2026-08-28); discovery is via
<link rel="alternate"> tags in HTML heads and robots/llms.txt references,
wired by the HTML-head-owning lanes.
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from email.utils import format_datetime
from pathlib import Path
from datetime import datetime, timezone

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

from build_domain_pages import DOMAINS  # noqa: E402
from generated_outputs import stale_output_paths, write_output_texts  # noqa: E402
from sitemap_policy import SITE_ORIGIN  # noqa: E402

FEEDS_DIR = "feeds"
MAX_ITEMS = 30


def h(value: object) -> str:
    return html.escape(str(value), quote=True)


def _load_list(path: Path, key: str) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        payload = payload.get(key, [])
    return [row for row in payload if isinstance(row, dict)]


def load_works(repo_root: Path) -> list[dict]:
    return _load_list(repo_root / "data" / "works.json", "works")


def load_videos(repo_root: Path) -> list[dict]:
    return _load_list(repo_root / "data" / "videos.json", "videos")


def _emoji_to_slug() -> dict[str, str]:
    mapping: dict[str, str] = {}
    for config in DOMAINS:
        for emoji in config.domains:
            mapping[emoji] = config.slug
    return mapping


def _video_slugs() -> dict[str, set[str]]:
    """Map each video record id to the domain slugs its topics target."""
    out: dict[str, set[str]] = {}
    for config in DOMAINS:
        target = f"domain-{config.slug}.html"
        for video in VIDEOS:
            topics = video.get("topics") or []
            if any(t.get("url") == target for t in topics if isinstance(t, dict)):
                out.setdefault(video["id"], set()).add(config.slug)
    return out


VIDEOS: list[dict] = []
_EMOJI_SLUGS: dict[str, str] = {}
_VIDEO_SLUGS: dict[str, set[str]] = {}


def init_taxonomy(works: list[dict], videos: list[dict]) -> None:
    """Bind the dataset-derived taxonomy lookups (idempotent per dataset)."""
    global VIDEOS, _EMOJI_SLUGS, _VIDEO_SLUGS
    VIDEOS = videos
    _EMOJI_SLUGS = _emoji_to_slug()
    _VIDEO_SLUGS = _video_slugs()


def domain_items(slug: str, works: list[dict]) -> list[dict]:
    """Return the sorted, capped item list for one domain slug."""
    items: list[dict] = []
    for work in works:
        if _EMOJI_SLUGS.get(work.get("domain")) != slug:
            continue
        year = int(work.get("year") or 0)
        items.append(
            {
                "sort_date": f"{year:04d}-01-01",
                "title": work.get("title") or f"Work #{work.get('num')}",
                "link": work.get("url") or SITE_ORIGIN,
                "guid": work.get("url") or f"work-{work.get('num')}",
                "pub_date": f"{year:04d}-01-01T00:00:00+00:00",
                "description": f"{work.get('type', 'Work')} \u2014 {work.get('venue', 'Zenodo')}"
                + (f" \u2014 {', '.join(work.get('authors') or [])}" if work.get("authors") else ""),
            }
        )
    for video in VIDEOS:
        if slug not in _VIDEO_SLUGS.get(video.get("id"), set()):
            continue
        date = str(video.get("date") or video.get("upload_date") or "")
        if len(date) == 8 and date.isdigit():
            date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
        items.append(
            {
                "sort_date": date,
                "title": video.get("title") or video.get("id"),
                "link": SITE_ORIGIN + str(video.get("page_url") or "").lstrip("/"),
                "guid": SITE_ORIGIN + str(video.get("page_url") or "").lstrip("/"),
                "pub_date": f"{date}T00:00:00+00:00",
                "description": f"Video \u2014 {video.get('channel_label', 'YouTube')}",
            }
        )
    # Total sort: date desc, then title asc for a stable deterministic order.
    items.sort(key=lambda item: (item["sort_date"], item["title"]), reverse=False)
    items.sort(key=lambda item: item["sort_date"], reverse=True)
    return items[:MAX_ITEMS]


def render_feed(slug: str, title: str, description: str, items: list[dict]) -> str:
    hub = f"{SITE_ORIGIN}domain-{slug}.html"
    self_url = f"{SITE_ORIGIN}{FEEDS_DIR}/domain-{slug}.xml"
    last_build = max((item["pub_date"] for item in items), default="1970-01-01T00:00:00+00:00")
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0">',
        "  <channel>",
        f"    <title>{h(title)} \u2014 RSS</title>",
        f"    <link>{h(hub)}</link>",
        f"    <description>{h(description)}</description>",
        f"    <language>en</language>",
        f"    <lastBuildDate>{h(format_datetime(datetime.fromisoformat(last_build)))}</lastBuildDate>",
        f'    <atom:link href="{h(self_url)}" rel="self" type="application/rss+xml" xmlns:atom="http://www.w3.org/2005/Atom" />',
    ]
    for item in items:
        lines.extend(
            [
                "    <item>",
                f"      <title>{h(item['title'])}</title>",
                f"      <link>{h(item['link'])}</link>",
                f'      <guid isPermaLink="true">{h(item["guid"])}</guid>',
                f"      <pubDate>{h(format_datetime(datetime.fromisoformat(item['pub_date'])))}</pubDate>",
                f"      <description>{h(item['description'])}</description>",
                "    </item>",
            ]
        )
    lines.extend(["  </channel>", "</rss>", ""])
    return "\n".join(lines)


def render_all(works: list[dict], videos: list[dict]) -> dict[Path, str]:
    init_taxonomy(works, videos)
    outputs: dict[Path, str] = {}
    for config in DOMAINS:
        items = domain_items(config.slug, works)
        outputs[Path(FEEDS_DIR) / f"domain-{config.slug}.xml"] = render_feed(
            config.slug, config.title, config.description, items
        )
    return outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate per-domain RSS feeds (deterministic).")
    parser.add_argument("--check", action="store_true", help="Fail if on-disk feeds are stale.")
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    args = parser.parse_args(argv)
    repo_root = args.repo_root.resolve()
    works = load_works(repo_root)
    videos = load_videos(repo_root)
    # Absolutize targets against --repo-root (not CWD) so the shared
    # generated-output writer/checker validates the intended tree.
    expected = {repo_root / rel: content for rel, content in render_all(works, videos).items()}
    if args.check:
        stale = stale_output_paths(expected, repo_root=repo_root)
        if stale:
            for path in stale:
                print(f"stale domain feed: {path.as_posix()}", file=sys.stderr)
            print(f"stale domain feeds: {len(stale)}", file=sys.stderr)
            return 1
        print(f"domain feeds current: {len(expected)}")
        return 0
    write_output_texts(expected, repo_root=repo_root)
    print(f"wrote domain feeds: {len(expected)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
