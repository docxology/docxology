#!/usr/bin/env python3
"""Run a lightweight static accessibility and metadata audit for root HTML pages."""

from __future__ import annotations

import argparse
import json
from html.parser import HTMLParser
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

try:
    from report_paths import dated_report_path, generated_timestamp, latest_report
except ImportError:  # pragma: no cover - package import path
    from .report_paths import dated_report_path, generated_timestamp, latest_report

OUT = dated_report_path("accessibility_static", "json")


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.in_title = False
        self.lang = ""
        self.skip_link = False
        self.nav = False
        self.main = False
        self.viewport = False
        self.canonical = False
        self.og_image = False
        self.images_without_alt: list[str] = []
        self.buttons_without_label = 0
        self._button_stack: list[dict] = []
        self.headings: list[int] = []
        self.label_fors: set[str] = set()
        self.form_controls: list[dict] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {k: v or "" for k, v in attrs}
        if tag == "html":
            self.lang = attr.get("lang", "")
        elif tag == "title":
            self.in_title = True
        elif tag == "a" and attr.get("href") == "#main":
            self.skip_link = True
        elif tag == "nav":
            self.nav = True
        elif tag == "main" and attr.get("id") == "main":
            self.main = True
        elif tag == "meta" and attr.get("name") == "viewport":
            self.viewport = True
        elif tag == "link" and attr.get("rel") == "canonical":
            self.canonical = True
        elif tag == "meta" and attr.get("property") == "og:image":
            self.og_image = True
        elif tag == "img" and not attr.get("alt"):
            self.images_without_alt.append(attr.get("src", "unknown"))
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.headings.append(int(tag[1]))
        elif tag == "label" and attr.get("for"):
            self.label_fors.add(attr["for"])
        elif tag in ("input", "select", "textarea"):
            if attr.get("type", "").lower() not in ("hidden", "submit", "button", "reset", "image"):
                self.form_controls.append(
                    {
                        "id": attr.get("id", ""),
                        "has_label": bool(attr.get("aria-label") or attr.get("aria-labelledby") or attr.get("title")),
                    }
                )
        elif tag == "button":
            self._button_stack.append(
                {
                    "has_programmatic_label": bool(attr.get("aria-label") or attr.get("aria-labelledby") or attr.get("title")),
                    "text": "",
                }
            )

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False
        elif tag == "button" and self._button_stack:
            button = self._button_stack.pop()
            if not button["has_programmatic_label"] and not button["text"].strip():
                self.buttons_without_label += 1

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data
        if self._button_stack:
            self._button_stack[-1]["text"] += data


def audit_page(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="ignore")
    parser = PageParser()
    parser.feed(text)
    checks = {
        "lang": bool(parser.lang),
        "title": bool(parser.title.strip()),
        "viewport": parser.viewport,
        "canonical": parser.canonical,
        "skip_link": parser.skip_link,
        "nav": parser.nav,
        "main": parser.main,
        "og_image": parser.og_image,
        "no_img_alt_gaps": not parser.images_without_alt,
        "buttons_labelled": parser.buttons_without_label == 0,
        "focus_visible_css": "focus-visible" in (REPO_ROOT / "style.css").read_text(encoding="utf-8"),
        "reduced_motion_css": "prefers-reduced-motion" in (REPO_ROOT / "style.css").read_text(encoding="utf-8"),
        "single_h1": parser.headings.count(1) == 1,
        "no_heading_skips": (not parser.headings or parser.headings[0] == 1)
        and all(parser.headings[i] <= parser.headings[i - 1] + 1 for i in range(1, len(parser.headings))),
        "form_controls_labelled": all(
            c["has_label"] or (c["id"] and c["id"] in parser.label_fors) for c in parser.form_controls
        ),
    }
    return {
        "path": str(path.relative_to(REPO_ROOT)),
        "ok": all(checks.values()),
        "checks": checks,
        "images_without_alt": parser.images_without_alt,
        "buttons_without_label": parser.buttons_without_label,
    }


def existing_generated_at(path: Path) -> str | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8")).get("generated_at")
    except json.JSONDecodeError:
        return None


def render(generated_at: str | None = None) -> str:
    pages = []
    for path in sorted(REPO_ROOT.glob("*.html")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if 'http-equiv="refresh"' in text or path.name.startswith("google"):
            continue
        pages.append(path)
    results = [audit_page(path) for path in pages]
    payload = {
        "generated_at": generated_at or generated_timestamp(),
        "scope": "Static root HTML pages; complements, but does not replace, browser-based accessibility testing.",
        "page_count": len(results),
        "passing": sum(1 for r in results if r["ok"]),
        "results": results,
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if the static accessibility report is stale or has failures")
    args = parser.parse_args()
    out = latest_report("accessibility_static_*.json") if args.check else OUT
    content = render(existing_generated_at(out) if args.check else None)
    payload = json.loads(content)
    failures = [r["path"] for r in payload["results"] if not r["ok"]]
    if args.check:
        if not out.exists() or out.read_text(encoding="utf-8") != content:
            raise SystemExit("Stale static accessibility report")
        if failures:
            raise SystemExit("Static accessibility failures: " + ", ".join(failures[:20]))
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(content, encoding="utf-8")
    print(("checked" if args.check else "wrote") + f" static accessibility report ({payload['passing']}/{payload['page_count']} passing)")


if __name__ == "__main__":
    main()
