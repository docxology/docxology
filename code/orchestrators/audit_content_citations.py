#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

from docxology_tools.content_audit import audit_content, public_html_paths  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    parser = argparse.ArgumentParser(description="Check public content links and catalog-bound inline citations")
    parser.add_argument("--report", type=Path, help="Save the full source-bound JSON inventory")
    parser.add_argument("--network-report", type=Path, help="Probe every distinct external link in public main content")
    parser.add_argument("--timeout", type=int, default=8)
    parser.add_argument("--workers", type=int, default=12)
    args = parser.parse_args()
    if args.timeout < 1 or args.workers < 1:
        parser.error("--timeout and --workers must be positive")
    works = json.loads((REPO_ROOT / "data/works.json").read_text(encoding="utf-8"))["works"]
    from build_pages_artifact import _relative_paths

    report = audit_content(REPO_ROOT, public_html_paths(REPO_ROOT), works, published_paths=set(_relative_paths()))
    if args.report:
        args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f'Checked {report["html_pages"]} HTML pages, {report["local_links_checked"]} local links, '
          f'{report["fragments_checked"]} fragments, {report["work_links"]} work links')
    if args.network_report:
        from check_external_links import build_report

        network = build_report(args.timeout, args.workers, None, url_sources=report["external_links"])
        network["scope"] = sorted(report["input_sha256"])
        network["input_sha256"] = report["input_sha256"]
        args.network_report.write_text(json.dumps(network, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f'External responses: {network["ok"]}/{network["checked_urls"]} successful; '
              f'{network["warnings"]} require triage')
    if report["errors"]:
        raise SystemExit("\n".join(report["errors"]))


if __name__ == "__main__":
    main()
