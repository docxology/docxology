#!/usr/bin/env python3
"""Build JSON and Markdown summaries from the scoped external-link report."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE = REPO_ROOT / "reports" / "external_links_2026-05-13.json"
JSON_OUT = REPO_ROOT / "reports" / "external_links_triage_2026-05-13.json"
MD_OUT = REPO_ROOT / "reports" / "external_links_triage_2026-05-13.md"


def category(row: dict) -> str:
    host = urlparse(row["url"]).netloc.lower()
    status = int(row.get("status") or 0)
    if row.get("ok"):
        return "ok"
    if status == 404:
        return "needs-replacement"
    if status in {401, 402, 403, 429, 999} or host in {"linkedin.com", "www.linkedin.com", "www.researchgate.net"}:
        return "bot-protected-or-rate-limited"
    if status in {500, 502, 503, 504}:
        return "upstream-transient"
    if status == 0 and "timed out" in row.get("error", "").lower():
        return "timeout"
    if status == 0:
        return "connection-failure"
    return "review"


def build() -> tuple[dict, str]:
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    rows = []
    counts: Counter[str] = Counter()
    by_category: dict[str, list[dict]] = defaultdict(list)
    for row in payload["results"]:
        cat = category(row)
        enriched = {
            "url": row["url"],
            "status": row["status"],
            "ok": row["ok"],
            "category": cat,
            "sources": row.get("sources", []),
            "error": row.get("error", ""),
        }
        rows.append(enriched)
        counts[cat] += 1
        if cat != "ok":
            by_category[cat].append(enriched)
    triage = {
        "generated_at": "2026-05-13",
        "source": str(SOURCE.relative_to(REPO_ROOT)),
        "checked_urls": payload["checked_urls"],
        "ok": counts["ok"],
        "warnings": payload["checked_urls"] - counts["ok"],
        "categories": dict(sorted(counts.items())),
        "note": "Warnings classify observed network behavior; bot-protected and rate-limited sources are not automatically stale.",
        "warnings_by_category": {key: value for key, value in sorted(by_category.items())},
    }
    lines = [
        "# External Link Triage",
        "",
        "Scoped network-link triage for public-facing repository hubs.",
        "",
        f"- Source report: `{SOURCE.relative_to(REPO_ROOT)}`",
        f"- Checked URLs: {triage['checked_urls']}",
        f"- OK: {triage['ok']}",
        f"- Warnings: {triage['warnings']}",
        "",
        "## Categories",
        "",
        "| Category | Count | Meaning |",
        "| --- | ---: | --- |",
    ]
    meanings = {
        "ok": "Returned a 2xx/3xx response.",
        "bot-protected-or-rate-limited": "Likely blocks automated checks; verify manually before replacing.",
        "needs-replacement": "Returned 404 and should be replaced or removed if no longer valid.",
        "upstream-transient": "Server-side outage or temporary upstream failure.",
        "timeout": "Timed out under the bounded checker timeout.",
        "connection-failure": "Could not connect during this run.",
        "review": "Unexpected status requiring manual review.",
    }
    for key, count in sorted(counts.items()):
        lines.append(f"| `{key}` | {count} | {meanings.get(key, 'Manual review needed.')} |")
    for key, items in sorted(by_category.items()):
        lines.extend(["", f"## {key}", "", "| Status | URL | Sources |", "| ---: | --- | --- |"])
        for item in items[:80]:
            sources = ", ".join(item["sources"][:3])
            lines.append(f"| {item['status']} | <{item['url']}> | {sources} |")
    return triage, "\n".join(lines).rstrip() + "\n"


def outputs() -> dict[Path, str]:
    payload, markdown = build()
    return {JSON_OUT: json.dumps(payload, indent=2, ensure_ascii=False) + "\n", MD_OUT: markdown}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if triage outputs are stale")
    args = parser.parse_args()
    stale = []
    for path, content in outputs().items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(str(path.relative_to(REPO_ROOT)))
        else:
            path.write_text(content, encoding="utf-8")
    if stale:
        raise SystemExit("Stale external-link triage files: " + ", ".join(stale))
    print(("checked" if args.check else "wrote") + " external-link triage")


if __name__ == "__main__":
    main()
