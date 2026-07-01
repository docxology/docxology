#!/usr/bin/env python3
"""
Deep audit of metadata.json completeness across all paper folders.

Checks:
  - metadata.json exists and parses as JSON
  - domain: present, valid name (no emoji)
  - type: one of Paper/Presentation/Book/Course/Series/Playbook
  - methods: a list with >= 2 entries
  - key_findings: a list with >= 1 entry
  - checked_at: present and valid ISO 8601 datetime
  - paper_metadata.json inclusion (expect 163/164 — 2026_FocusedAttentionMeditation is the one absent)
"""

import json
import os
import re
import sys
from datetime import datetime
from collections import Counter

PAPERS_DIR = os.path.join(os.path.dirname(__file__), "..", "papers")
PAPERS_DIR = os.path.abspath(PAPERS_DIR)
PAPER_META_PATH = os.path.join(PAPERS_DIR, "paper_metadata.json")

VALID_TYPES = frozenset({"Paper", "Presentation", "Book", "Course", "Series", "Playbook"})
ISO_DT_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$"
)
EMOJI_RX = re.compile(
    "[\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map
    "\U0001F1E0-\U0001F1FF"  # flags
    "\U00002702-\U000027B0"  # dingbats
    "\U000024C2-\U0001F251"  # misc
    "]+"
)


def is_valid_iso(s):
    """Check if s is a valid ISO-8601 datetime string."""
    if not isinstance(s, str) or not ISO_DT_RE.match(s):
        return False
    try:
        # Try parsing with various ISO formats
        datetime.fromisoformat(s.replace("Z", "+00:00"))
        return True
    except (ValueError, TypeError):
        return False


def has_emoji(s):
    """Check if string contains emoji characters."""
    return bool(EMOJI_RX.search(s))


def check_paper(folder_name, paper_meta_keys):
    """Run all checks on one paper folder and return results dict."""
    folder_path = os.path.join(PAPERS_DIR, folder_name)
    meta_path = os.path.join(folder_path, "metadata.json")
    failures = {}

    # 1. metadata.json exists and is valid JSON
    if not os.path.isfile(meta_path):
        failures["exists"] = "metadata.json not found"
        # Cannot check further fields
        return folder_name, failures, True

    try:
        with open(meta_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        failures["valid_json"] = f"Invalid JSON: {e}"
        return folder_name, failures, True

    if not isinstance(data, dict):
        failures["valid_json"] = f"Expected dict, got {type(data).__name__}"
        return folder_name, failures, True

    # 2. domain: present, valid name, no emoji
    domain = data.get("domain")
    if domain is None or (isinstance(domain, str) and not domain.strip()):
        failures["domain"] = "Missing or empty"
    elif not isinstance(domain, str):
        failures["domain"] = f"Not a string: {type(domain).__name__}"
    elif has_emoji(domain):
        failures["domain"] = f"Contains emoji: {repr(domain)}"

    # 3. type: one of valid set
    ptype = data.get("type")
    if ptype is None:
        failures["type"] = "Missing"
    elif ptype not in VALID_TYPES:
        failures["type"] = f"Invalid: {repr(ptype)} (valid: {', '.join(sorted(VALID_TYPES))})"

    # 4. methods: list with >= 2 entries
    methods = data.get("methods")
    if methods is None:
        failures["methods"] = "Missing"
    elif not isinstance(methods, list):
        failures["methods"] = f"Not a list: {type(methods).__name__}"
    elif len(methods) < 2:
        failures["methods"] = f"Has {len(methods)} entries, need >= 2"
    else:
        # Check each method has a name (not just empty objects)
        valid_methods = [m for m in methods if isinstance(m, dict) and isinstance(m.get("name"), str) and m["name"].strip()]
        if len(valid_methods) < 2:
            failures["methods"] = f"Only {len(valid_methods)} entries with valid name, need >= 2"

    # 5. key_findings: list with >= 1 entry
    kf = data.get("key_findings")
    if kf is None:
        failures["key_findings"] = "Missing"
    elif not isinstance(kf, list):
        failures["key_findings"] = f"Not a list: {type(kf).__name__}"
    elif len(kf) < 1:
        failures["key_findings"] = "Empty list (need >= 1 entry)"
    else:
        valid_kf = [k for k in kf if isinstance(k, str) and k.strip()]
        if len(valid_kf) < 1:
            failures["key_findings"] = "No non-empty string entries"

    # 6. checked_at: valid ISO date
    checked_at = data.get("checked_at")
    if checked_at is None:
        failures["checked_at"] = "Missing"
    elif not isinstance(checked_at, str):
        failures["checked_at"] = f"Not a string: {type(checked_at).__name__}"
    elif not is_valid_iso(checked_at):
        failures["checked_at"] = f"Invalid ISO datetime: {repr(checked_at)}"

    # 7. paper_metadata.json inclusion
    in_meta = folder_name in paper_meta_keys

    return folder_name, failures, in_meta


def main():
    # Load paper_metadata.json
    if not os.path.isfile(PAPER_META_PATH):
        print(f"ERROR: paper_metadata.json not found at {PAPER_META_PATH}", file=sys.stderr)
        sys.exit(1)

    with open(PAPER_META_PATH, "r", encoding="utf-8") as f:
        paper_meta = json.load(f)

    if isinstance(paper_meta, list):
        paper_meta_keys = {item.get("folder") or item.get("id") or item.get("name") for item in paper_meta if isinstance(item, dict)}
    elif isinstance(paper_meta, dict):
        paper_meta_keys = set(paper_meta.keys())
    else:
        paper_meta_keys = set()
        print(f"WARNING: paper_metadata.json is type {type(paper_meta).__name__}, cannot extract keys")

    # Gather all paper folders
    folders = sorted([
        d for d in os.listdir(PAPERS_DIR)
        if os.path.isdir(os.path.join(PAPERS_DIR, d))
    ])
    print(f"Total paper folders found: {len(folders)}")
    print(f"paper_metadata.json entries: {len(paper_meta)}")
    print()

    # Run checks
    all_results = {}
    failure_counter = Counter()
    total_pass = 0
    total_in_meta = 0
    total_not_in_meta_names = []

    for folder in folders:
        name, failures, in_meta = check_paper(folder, paper_meta_keys)
        all_results[name] = {"failures": failures, "in_meta": in_meta}

        if in_meta:
            total_in_meta += 1
        else:
            total_not_in_meta_names.append(name)

        if not failures:
            total_pass += 1
        else:
            for check_name in failures:
                failure_counter[check_name] += 1

    # ── Summary ──────────────────────────────────────────────────────────
    print("=" * 72)
    print("OVERALL SUMMARY")
    print("=" * 72)
    print(f"  Folders passing ALL checks:       {total_pass}/{len(folders)}")
    print(f"  Folders with ≥1 failure:          {len(folders) - total_pass}/{len(folders)}")
    print(f"  In paper_metadata.json:           {total_in_meta}/{len(folders)}")
    print(f"  Not in paper_metadata.json:       {len(folders) - total_in_meta}")
    for n in total_not_in_meta_names:
        print(f"    - {n}")
    print()

    # ── Failure breakdown ────────────────────────────────────────────────
    print("=" * 72)
    print("FAILURES BY CHECK")
    print("=" * 72)
    if failure_counter:
        for check_name, count in sorted(failure_counter.items(), key=lambda x: -x[1]):
            print(f"  {check_name:25s} {count:3d} failures")
    else:
        print("  (none)")
    print()

    # ── Per-folder failure breakdown ─────────────────────────────────────
    print("=" * 72)
    print("PER-FOLDER FAILURE BREAKDOWN")
    print("=" * 72)
    # List all folders that have failures
    failing = [(name, res) for name, res in all_results.items() if res["failures"]]
    if failing:
        # Sort so most failures come first
        failing.sort(key=lambda x: -len(x[1]["failures"]))
        for name, res in failing:
            details = "; ".join(f"{k}: {v}" for k, v in res["failures"].items())
            meta_status = "✓ in paper_metadata" if res["in_meta"] else "✗ NOT in paper_metadata"
            print(f"  {name}")
            print(f"    {details}")
            print(f"    {meta_status}")
        print()
        print(f"  Total failing folders: {len(failing)}")
    else:
        print("  (none)")
    print()

    # ── Detailed table ───────────────────────────────────────────────────
    print("=" * 72)
    print("COMPLETE RESULTS TABLE")
    print("=" * 72)
    print(f"{'Folder':45s} {'Exists':6s} {'Domain':8s} {'Type':8s} {'Methods':8s} {'Findings':9s} {'CheckedAt':10s} {'InMeta':7s} {'Fail?':5s}")
    print("-" * 106)
    for name, res in all_results.items():
        f = res["failures"]
        exists_status = "✓" if "exists" not in f and "valid_json" not in f else "✗"
        domain_status = "✓" if "domain" not in f else "✗"
        type_status = "✓" if "type" not in f else "✗"
        methods_status = "✓" if "methods" not in f else "✗"
        findings_status = "✓" if "key_findings" not in f else "✗"
        checked_status = "✓" if "checked_at" not in f else "✗"
        in_meta_status = "✓" if res["in_meta"] else "✗"
        has_fail = "YES" if f else ""

        print(f"{name[:44]:45s} {exists_status:6s} {domain_status:8s} {type_status:8s} {methods_status:8s} {findings_status:9s} {checked_status:10s} {in_meta_status:7s} {has_fail:5s}")
    print("-" * 106)
    print(f"PASS: {total_pass}/{len(folders)}  |  FAIL: {len(folders) - total_pass}/{len(folders)}")
    print(f"In paper_metadata.json: {total_in_meta}  |  Not in paper_metadata.json: {len(folders) - total_in_meta}")
    for n in total_not_in_meta_names:
        print(f"  Not in paper_metadata.json: {n}")


if __name__ == "__main__":
    main()
