#!/usr/bin/env python3
"""Generate a source-bound Blake pathway without creating a second bibliography."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
WORD = re.compile(r"\bBlake\b", re.IGNORECASE)
EXCLUDED = {"other_person", "no_match"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_payload(root: Path = REPO_ROOT) -> dict:
    works = json.loads((root / "data/works.json").read_text())["works"]
    review = json.loads((root / "data/blake-review.json").read_text())
    discovery_path = root / review["metadata_source"]
    discovery = json.loads(discovery_path.read_text())
    if discovery.get("warnings"):
        raise ValueError("Blake metadata source has unresolved API warnings")
    records = {str(x["record_id"]): x for x in discovery["zenodo_records"]}
    by_folder = {x["docs_path"].strip("/").split("/")[-1]: x for x in works if x["docs_path"]}
    decisions = review["reviews"]
    scanned = sorted((root / "papers").glob("*/full_text.md"))
    entries, exclusions, pending = [], [], []
    for path in scanned:
        folder = path.parent.name
        lines = path.read_text().splitlines()
        hits = [i + 1 for i, text in enumerate(lines) if WORD.search(text)]
        decision = decisions.get(folder)
        if not hits and decision is None:
            continue
        work = by_folder.get(folder)
        if work is None:
            raise ValueError(f"Uncatalogued full-text match: {folder}")
        if decision is None:
            pending.append(work["citation_key"])
            decision = {"relation": "needs_review", "note": "Unclassified text match"}
        else:
            if decision["full_text_sha256"] != digest(path):
                raise ValueError(f"Stale passage review: {folder}")
            if bool(hits) == (decision["relation"] == "no_match"):
                raise ValueError(f"Passage classification disagrees with search: {folder}")
            for anchor in decision.get("anchors", []):
                if anchor not in "\n".join(lines):
                    raise ValueError(f"Missing reviewed passage anchor: {folder}: {anchor}")
        metadata_path = path.parent / "metadata.json"
        metadata = json.loads(metadata_path.read_text()) if metadata_path.is_file() else {}
        record_id = str(metadata.get("record_id") or "")
        record = records.get(record_id)
        metadata_verified = bool(record and work["doi"].casefold() in {record["doi"].casefold(), f"10.5281/zenodo.{record_id}"})
        if record and re.sub(r"\s+", " ", record["title"]).strip() != re.sub(r"\s+", " ", work["title"]).strip():
            raise ValueError(f"Primary title mismatch: {folder}")
        row = {
            "citation_key": work["citation_key"],
            "title": work["title"],
            "year": work["year"],
            "work_url": f"/works/{work['citation_key']}.html",
            "citation_doi": work["doi"],
            "citation_url": work["url"],
            "record_id": record_id or None,
            "version_doi": f"10.5281/zenodo.{record_id}" if record_id else None,
            "record_url": f"https://zenodo.org/records/{record_id}" if record_id else None,
            "version": record.get("version") if record else metadata.get("version"),
            "primary_metadata_matched": metadata_verified,
            "relation": decision["relation"],
            "note": decision["note"],
            "edition_note": decision.get("edition_note"),
            "full_text_path": str(path.relative_to(root)),
            "full_text_sha256": digest(path),
            "matching_lines": hits,
            "evidence_lines": decision.get("evidence_lines", hits[:1]),
            "citation_sources_independently_checked": False,
        }
        if any(line not in hits for line in row["evidence_lines"]):
            raise ValueError(f"Reviewed evidence line lacks Blake match: {folder}")
        (exclusions if row["relation"] in EXCLUDED else entries).append(row)
    missing_reviews = sorted(set(decisions) - {p.parent.name for p in scanned})
    if missing_reviews:
        raise ValueError(f"Reviewed text missing: {missing_reviews}")
    title_keys = {x["citation_key"] for x in works if WORD.search(x["title"])}
    if not title_keys.issubset({x["citation_key"] for x in entries}):
        raise ValueError("A Blake-titled work lacks indexed text and a passage review")
    for row in entries:
        row["title_match"] = row["citation_key"] in title_keys
        row["core_subject"] = row["title_match"] or row["relation"] == "core_subject"
    return {
        "schema_version": "BlakeIndex.v1",
        "schema_ref": "/data/agent-index.json#schemas/BlakeIndex",
        "sources": {"bibliography": "pages/BIBLIOGRAPHY.md", "works": "data/works.json", "reviews": "data/blake-review.json", "primary_metadata": review["metadata_source"]},
        "primary_metadata_sha256": digest(discovery_path),
        "metadata_observed_at": discovery["generated_at"],
        "method": "Case-insensitive whole-word Blake search of every local papers/*/full_text.md; hash-bound passage classifications. Title matching is a separate subset.",
        "limits": "Available text and classified passages do not establish full-paper reading or independent verification of cited editions, quotations, historical claims, or scientific findings. Missing or imperfect extractions may hide further references.",
        "count": len(entries),
        "counts": {"catalog_works": len(works), "scanned_full_texts": len(scanned), "title_matches": len(title_keys), "core_subjects": sum(x["core_subject"] for x in entries), "additional_text_matches": sum(not x["title_match"] for x in entries), "excluded_or_no_match": len(exclusions), "needs_review": len(pending)},
        "needs_review": pending,
        "works": sorted(entries, key=lambda x: (not x["title_match"], str(x["year"]), x["title"])),
        "exclusions": exclusions,
    }


def render_markdown(payload: dict) -> str:
    counts = payload["counts"]
    text = [
        "# William Blake publication pathway", "",
        "<!-- Generated by code/orchestrators/build_blake_index.py; edit bibliography, paper metadata, or data/blake-review.json. -->", "",
        "[Complete bibliography](BIBLIOGRAPHY.md) · [Current catalog totals](../reports/current_counts.md) · [Machine-readable pathway](../data/blake-index.json) · [Blake corpus and search repository](https://github.com/docxology/blake)", "",
        "This pathway references the existing bibliography identities. Citation DOIs identify the curated work; version DOIs and Zenodo record links identify a particular deposited artifact. A concept DOI may resolve to a newer version. An absent version label means the API did not supply one; consult the record page.", "",
        f"The current scan covers **{counts['catalog_works']} catalog works** and **{counts['scanned_full_texts']} local full texts**: **{counts['title_matches']} Blake-titled works**, **{counts['additional_text_matches']} additional William Blake text matches**, and **{counts['needs_review']} unclassified matches**. These are indexing counts, not counts of papers read.", "",
        "## Core treatments", "",
        "| Work | Curated citation DOI | Version DOI / primary source | API version |", "| --- | --- | --- | --- |",
    ]
    for row in payload["works"]:
        if row["core_subject"]:
            title = row["title"].replace("|", "\\|")
            text.append(f"| [{title}](..{row['work_url']}) | [{row['citation_doi']}]({row['citation_url']}) | [{row['version_doi']}]({row['record_url']}) | {row['version'] or 'unspecified'} |")
    text += ["", "Core-subject classification also covers works whose subtitle or content explicitly develops Blake, even when the short catalog title omits his name.", "", "## Related and peripheral passages", "", "The relation describes the located passage, including short quotations, references to another work, and program or catalog mentions. It does not classify the whole paper as Blake scholarship.", "", "| Work | Passage relation | Text evidence |", "| --- | --- | --- |"]
    for row in payload["works"]:
        if not row["core_subject"]:
            line = row["evidence_lines"][0]
            url = f"https://github.com/docxology/docxology/blob/main/{row['full_text_path']}?plain=1#L{line}"
            text.append(f"| [{row['title']}](..{row['work_url']}) | {row['note']} | [text, line {line}]({url}) |")
    text += ["", f"The pathway classifies **{counts['core_subjects']} core treatments** and **{payload['count'] - counts['core_subjects']} related or peripheral works**. Core classification and title matching are separate fields in the JSON.", "", "## Deposited versions and printed DOI discrepancies", "", "Printed cover or slide identifiers are preserved in the extraction. They can differ from registry version metadata and must not silently replace it.", ""]
    for row in payload["works"]:
        if row["edition_note"]:
            text.append(f"- **{row['title']}**: {row['edition_note']}")
    text += ["", "## Exclusions and search gaps", ""]
    for row in payload["exclusions"]:
        text.append(f"- [{row['title']}](..{row['work_url']}): {row['note']}")
    text += ["", "## Evidence and verification boundaries", "",
        "- Every included work has metadata and a local extracted full text; matching line numbers and text SHA-256 values are retained in the JSON pathway.",
        "- Passage classifications are bound to the reviewed text hash. Changed text requires renewed classification; new unclassified matches fail the check.",
        f"- Primary publication metadata was compared with [the public discovery snapshot](../{payload['sources']['primary_metadata']}) observed {payload['metadata_observed_at']}; the JSON records metadata-match status per work.",
        "- Located passages are distinct from sections read, complete texts read, and independently checked citation sources. This index makes no full-reading or independent citation-validation claim.",
        "- The search is limited to available local extractions. The [source coverage queue](../data/coverage-exceptions.json) identifies missing full text; image-only, OCR, spelling and edition differences can conceal further references.",
        "- Rebuild with `uv run python code/orchestrators/build_blake_index.py`; verify with the same command plus `--check`. The ordinary regeneration and validation plan includes this check.", ""]
    return "\n".join(text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = build_payload()
    outputs = {"data/blake-index.json": json.dumps(payload, indent=2, ensure_ascii=False) + "\n", "pages/BLAKE.md": render_markdown(payload)}
    if args.check:
        stale = [p for p, body in outputs.items() if not (REPO_ROOT / p).is_file() or (REPO_ROOT / p).read_text() != body]
        if stale or payload["needs_review"]:
            print(f"Blake index needs review or regeneration: {stale}; unclassified: {payload['needs_review']}")
            return 1
    else:
        for path, body in outputs.items():
            (REPO_ROOT / path).write_text(body)
    print(f"Blake index: {payload['counts']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
