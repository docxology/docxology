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


def render(build_date: datetime | None = None) -> str:
    build_date = build_date or datetime.now(timezone.utc).replace(microsecond=0)
    works = sorted(load_works(), key=lambda w: (int(w["year"]), -int(w["num"])), reverse=True)
    entries = [
        item(
            "Repository inventory and evidence layer refreshed",
            "https://danielarifriedman.com/repositories.html",
            "site-update-2026-05-15-repositories",
            "Full generated GitHub repository inventory, refreshed evidence ledger, and stable freshness fact comparison added.",
            build_date,
        ),
        item(
            "Discovery, citation, evidence, and domain pages expanded",
            "https://danielarifriedman.com/discovery.html",
            "site-update-2026-05-13-discovery",
            "New machine-readable exports, evidence ledger, domain pages, and agentic discovery metadata.",
            build_date,
        ),
        item(
            "Per-work landing pages and search index generated",
            "https://danielarifriedman.com/works/",
            "site-update-2026-05-13-works",
            "Generated work pages, search-index.json, feed.xml, and verification reports for the profile repository.",
            build_date,
        ),
    ]
    for work in works[:25]:
        entries.append(
            item(
                work["title"],
                f"https://danielarifriedman.com/works/{work['citation_key']}.html",
                f"work-{work['citation_key']}",
                f"{work['type']} · {work['venue']} · {work['domain_name']} · {work['year']}",
                build_date,
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
    content = render(existing_build_date() if args.check else None)
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != content:
            raise SystemExit("Stale generated feed.xml")
    else:
        OUT.write_text(content, encoding="utf-8")
    print(("checked" if args.check else "wrote") + " feed.xml")


if __name__ == "__main__":
    main()
