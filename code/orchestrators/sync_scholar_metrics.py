#!/usr/bin/env python3
"""Sync Google Scholar metrics from the single source of truth.

Source of truth: data/scholar-snapshot.json (see its "policy" field).

This orchestrator rewrites the citation / h-index / i10-index figures in every
hand-maintained surface so they always match the dated snapshot. It is
idempotent: each rule's regex matches both the pre- and post-rewrite forms and
normalises to one canonical, dated form, so a second run produces zero diff.

Usage:
  python code/orchestrators/sync_scholar_metrics.py            # rewrite in place
  python code/orchestrators/sync_scholar_metrics.py --check    # exit 1 on drift, no write

Rationale: the previous model hardcoded a manually-synced number in 12 places
behind a "do not overwrite" caveat with no as-of date or method. That
structurally guaranteed the number could only ratchet upward and never be
corrected downward to match the primary source. A dated snapshot plus this
generator replaces the freeze policy with a provenance envelope.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT = REPO_ROOT / "data" / "scholar-snapshot.json"


def load_snapshot() -> dict:
    return json.loads(SNAPSHOT.read_text(encoding="utf-8"))


def rules(s: dict) -> dict[str, list[tuple[str, str]]]:
    """Per-file list of (pattern, replacement). Patterns match old AND new
    forms so re-running is a no-op."""
    cit, h, i10, as_of = s["citations"], s["h_index"], s["i10_index"], s["as_of"]
    return {
        "README.md": [
            (r"Google_Scholar-\d+_citations", f"Google_Scholar-{cit}_citations"),
            (
                r"\*\*\d+\*\* Google Scholar citations \(h-index: \d+(?:, as of [\d-]+)?\)",
                f"**{cit}** Google Scholar citations (h-index: {h}, as of {as_of})",
            ),
        ],
        "pages/BIBLIOGRAPHY.md": [
            (r"Google_Scholar-\d+_citations", f"Google_Scholar-{cit}_citations"),
        ],
        "index.html": [
            (
                r"(\d+) works, \d+ Scholar citations(?: \(as of [\d-]+\))?",
                rf"\1 works, {cit} Scholar citations (as of {as_of})",
            ),
            (
                r'(<div class="num">)\d+(</div><div class="lbl">Citations</div>)',
                rf"\g<1>{cit}\g<2>",
            ),
            (
                r"(<li><strong>)\d+(</strong> Google Scholar citations)(?: \(as of [\d-]+\))?",
                rf"\g<1>{cit}\g<2> (as of {as_of})",
            ),
        ],
        "publications.html": [
            (
                r"📊 \d+ citations · h-index \d+ · i10-index \d+(?: \(as of [\d-]+\))?",
                f"📊 {cit} citations · h-index {h} · i10-index {i10} (as of {as_of})",
            ),
        ],
        "llms.txt": [
            (
                r"- \d+ Google Scholar citations[^\n]*",
                f"- {cit} Google Scholar citations (h-index {h}, i10-index {i10}; "
                f"direct dual-fetch, as of {as_of}; source of truth: data/scholar-snapshot.json)",
            ),
        ],
        "pages/PROFILE.md": [
            (
                r"\*\*\d+ citations\*\* on Google Scholar \(h-index: \d+, i10-index: \d+"
                r"(?:, as of [\d-]+)?\) across \*\*107\*\* indexed publications",
                f"**{cit} citations** on Google Scholar (h-index: {h}, i10-index: {i10}, "
                f"as of {as_of}) across his Scholar-indexed publications",
            ),
            (
                r"\*\*\d+ citations\*\* on Google Scholar \(h-index: \d+, i10-index: \d+"
                r"(?:, as of [\d-]+)?\) across his Scholar-indexed publications",
                f"**{cit} citations** on Google Scholar (h-index: {h}, i10-index: {i10}, "
                f"as of {as_of}) across his Scholar-indexed publications",
            ),
            (
                r"(\| Google Scholar Citations \| )\d+(?: \(as of [\d-]+\))?( \|)",
                rf"\g<1>{cit} (as of {as_of})\g<2>",
            ),
        ],
        "pages/LINKS.md": [
            (
                r"\d+ citations, h-index \d+, i10-index \d+ \([^)]*\)",
                f"{cit} citations, h-index {h}, i10-index {i10} (as of {as_of})",
            ),
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="exit 1 on drift, no write")
    args = ap.parse_args()

    s = load_snapshot()
    drift = False
    for rel, rule_list in rules(s).items():
        path = REPO_ROOT / rel
        if not path.exists():
            print(f"  skip (missing): {rel}")
            continue
        text = original = path.read_text(encoding="utf-8")
        for pattern, repl in rule_list:
            text = re.sub(pattern, repl, text)
        if text != original:
            drift = True
            if args.check:
                print(f"  DRIFT: {rel}")
            else:
                path.write_text(text, encoding="utf-8")
                print(f"  synced: {rel}")
        else:
            print(f"  ok:     {rel}")

    if args.check and drift:
        print("scholar metrics drift detected (run without --check to fix)")
        return 1
    print(
        f"scholar snapshot: {s['citations']} citations, h-index {s['h_index']}, "
        f"i10-index {s['i10_index']} (as of {s['as_of']})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
