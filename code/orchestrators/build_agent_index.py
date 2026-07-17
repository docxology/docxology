#!/usr/bin/env python3
"""Build the stable machine-readable route manifest for public agents."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT = REPO_ROOT / "data" / "agent-index.json"
COUNTS = REPO_ROOT / "data" / "current-counts.json"


def payload() -> dict:
    current = json.loads(COUNTS.read_text(encoding="utf-8"))
    counts = current.get("counts", {})
    artworks = json.loads((REPO_ROOT / "data/artworks.json").read_text(encoding="utf-8"))
    videos = json.loads((REPO_ROOT / "data/videos.json").read_text(encoding="utf-8"))
    return {
        "schema_version": "1.0",
        "generated_at": current.get("generated_at"),
        "canonical_origin": "https://danielarifriedman.com/",
        "canonical_sources": {
            "bibliography": "/pages/BIBLIOGRAPHY.md",
            "software": "/pages/SOFTWARE.md",
            "claims": "/data/claims.json",
            "counts": "/data/current-counts.json",
            "verification": "/pages/VERIFICATION_LOG.md",
        },
        "routes": [
            {"id": "home", "path": "/", "format": "text/html", "kind": "profile"},
            {"id": "publications", "path": "/publications.html", "format": "text/html", "kind": "collection"},
            {"id": "works", "path": "/works/", "format": "text/html", "kind": "collection"},
            {"id": "domains", "path": "/domains.html", "format": "text/html", "kind": "taxonomy"},
            {"id": "software", "path": "/software.html", "format": "text/html", "kind": "collection"},
            {"id": "search", "path": "/search.html", "format": "text/html", "kind": "query", "query": "?q={terms}"},
            {"id": "discovery", "path": "/discovery.html", "format": "text/html", "kind": "source-map"},
            {"id": "catalog", "path": "/catalog.html", "format": "text/html", "kind": "data-catalog"},
            {"id": "agent-index", "path": "/data/agent-index.json", "format": "application/json", "kind": "route-manifest"},
        ],
        "datasets": {
            "works": {"path": "/data/works.json", "count": counts.get("bibliography_works"), "schema": "Work"},
            "software": {"path": "/data/software.json", "count": counts.get("software", {}).get("curated_total"), "schema": "SoftwareRepository"},
            "artworks": {"path": "/data/artworks.json", "count": artworks.get("count", len(artworks.get("artworks", []))), "schema": "VisualArtwork"},
            "videos": {"path": "/data/videos.json", "count": videos.get("count", len(videos.get("videos", []))), "schema": "VideoObject"},
            "search": {"path": "/search-index.json", "count": None, "schema": "SearchResult"},
            "claims": {"path": "/data/claims.json", "count": None, "schema": "ClaimWithEvidence"},
        },
        "counts": counts,
        "freshness": {
            "policy": "Use generated_at and checked_at fields; do not infer freshness from page copy.",
            "volatile_sources": ["data/current-counts.json", "data/scholar-snapshot.json", "data/verification-log.json"],
            "verification": "/cite-verify.html",
        },
        "query_recipes": {
            "site_search": "/search.html?q={urlencoded_terms}",
            "publication_filter": "/publications.html?domain={emoji}&type={type}&year={year}",
            "work_by_key": "/works/{citation_key}.html",
            "raw_bibliography": "/pages/BIBLIOGRAPHY.md",
        },
        "notes": [
            "Canonical work URLs use citation_key values and preserve retired numeric gaps.",
            "Paper-folder pages are documentation mirrors; canonical indexable work pages live under /works/.",
            "External facts and metrics are evidence-dated; retain caveats when primary verification is incomplete.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if the manifest is stale")
    args = parser.parse_args()
    rendered = json.dumps(payload(), indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != rendered:
            raise SystemExit(f"stale agent manifest: {OUT.relative_to(REPO_ROOT)}")
        print(f"checked {OUT.relative_to(REPO_ROOT)}")
        return
    OUT.write_text(rendered, encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
