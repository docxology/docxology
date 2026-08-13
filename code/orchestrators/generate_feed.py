#!/usr/bin/env python3
"""Generate RSS updates feed from bibliography and site-maintenance milestones."""

from __future__ import annotations

import argparse
import html
import json
import re
from email.utils import format_datetime, parsedate_to_datetime
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT = REPO_ROOT / "feed.xml"


def h(value: object) -> str:
    return html.escape(str(value), quote=True)


def load_works() -> list[dict]:
    with open(REPO_ROOT / "data" / "works.json", encoding="utf-8") as f:
        return json.load(f)["works"]


def load_site_updates() -> list[dict]:
    """Load stable site-update items from data/site-updates.json.

    Missing or unreadable JSON is a no-op so the works feed still generates.
    """
    path = REPO_ROOT / "data" / "site-updates.json"
    if not path.exists():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    if not isinstance(payload, list):
        return []
    return [row for row in payload if isinstance(row, dict)]


def _parse_pub_date(value: object, fallback: datetime) -> datetime:
    text = str(value or "").strip()
    if not text:
        return fallback
    try:
        parsed = parsedate_to_datetime(text)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed
    except (TypeError, ValueError, IndexError):
        pass
    try:
        if len(text) == 10 and text[4] == "-" and text[7] == "-":
            return datetime(int(text[:4]), int(text[5:7]), int(text[8:10]), tzinfo=timezone.utc)
        dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except (TypeError, ValueError):
        return fallback


def existing_build_date() -> datetime | None:
    if not OUT.exists():
        return None
    match = re.search(r"<lastBuildDate>([^<]+)</lastBuildDate>", OUT.read_text(encoding="utf-8"))
    if not match:
        return None
    try:
        return parsedate_to_datetime(match.group(1))
    except (TypeError, ValueError):
        return None


def item(title: str, link: str, guid: str, description: str, pub_date: datetime) -> str:
    return f"""    <item>
      <title>{h(title)}</title>
      <link>{h(link)}</link>
      <guid isPermaLink="false">{h(guid)}</guid>
      <pubDate>{format_datetime(pub_date)}</pubDate>
      <description>{h(description)}</description>
    </item>"""


def _year_key(value: object) -> int:
    """Coerce a work ``year`` to an int for sorting, tolerating non-numeric
    (e.g. ``"n.d."`` or ``""``) values that sorter should rank last."""
    try:
        text = str(value)
        return int(text) if text.isdigit() else 0
    except (TypeError, ValueError):
        return 0


def render(build_date: datetime | None = None) -> str:
    build_date = build_date or datetime.now(timezone.utc).replace(microsecond=0)
    works = sorted(
        load_works(),
        key=lambda w: (_year_key(w.get("year")), int(w.get("num", 0) or 0)),
        reverse=True,
    )
    entries = []
    for update in load_site_updates():
        title = update.get("title")
        link = update.get("link")
        guid = update.get("guid")
        description = update.get("description")
        if not title or not link or not guid or description is None:
            continue
        entries.append(
            item(
                title,
                link,
                guid,
                description,
                _parse_pub_date(update.get("pub_date"), build_date),
            )
        )
    for work in works[:25]:
        # Use actual publication year as the pubDate (Jan 1 of that year)
        try:
            work_date = datetime(int(work["year"]), 1, 1, tzinfo=timezone.utc)
        except (ValueError, TypeError):
            work_date = build_date
        entries.append(
            item(
                work["title"],
                f"https://danielarifriedman.com/works/{work['citation_key']}.html",
                f"work-{work['citation_key']}",
                f"{work['type']} · {work['venue']} · {work['domain_name']} · {work['year']}",
                work_date,
            )
        )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Daniel Ari Friedman Updates</title>
    <link>https://danielarifriedman.com/</link>
    <atom:link href="https://danielarifriedman.com/feed.xml" rel="self" type="application/rss+xml" />
    <description>Bibliography, software, evidence, and site metadata updates.</description>
    <language>en-us</language>
    <lastBuildDate>{format_datetime(build_date)}</lastBuildDate>
{chr(10).join(entries)}
  </channel>
</rss>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if feed.xml is stale")
    args = parser.parse_args()
    existing_date = existing_build_date()
    if args.check:
        content = render(existing_date)
    else:
        content = render()
        if existing_date and OUT.read_text(encoding="utf-8") == render(existing_date):
            content = render(existing_date)
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != content:
            raise SystemExit("Stale generated feed.xml")
    else:
        OUT.write_text(content, encoding="utf-8")
    print(("checked" if args.check else "wrote") + " feed.xml")


if __name__ == "__main__":
    main()
