#!/usr/bin/env python3
"""batch_enrich_metadata.py — Generate/extend metadata.json for ALL paper folders.

For each paper folder:
- If metadata.json exists: add extended fields (methods, key_findings, domain, etc.)
- If metadata.json missing: create it from paper_metadata.json + BIBLIOGRAPHY data

Run: uv run python3 code/orchestrators/batch_enrich_metadata.py --apply
"""

from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from datetime import datetime
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
PAPERS_DIR = REPO_ROOT / "papers"
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
from biblio_table import iter_bibliography_rows  # noqa: E402

# ─── Domain helpers ───────────────────────────────────────────────────────────

EMOJI_TO_DOMAIN = {
    '💻': 'Computational',
    '🧠': 'Active Inference',
    '🛡️': 'Cognitive Security',
    '🐜': 'Entomology',
    '🎨': 'Art & Synergetics',
    '🧬': 'Genetics & Biomedical',
    '🌍': 'AII Ecosystem',
    '🎥': 'Presentations & Media',
}

DOMAIN_TO_EMOJI = {v: k for k, v in EMOJI_TO_DOMAIN.items()}

# Domain-specific methods and findings templates
DOMAIN_METHODS: dict[str, list[str]] = {
    'Computational': [
        'Deterministic software pipeline design',
        'Reproducible workflow orchestration',
        'Data-driven analysis and visualization',
        'Infrastructure-as-code methodology',
    ],
    'Active Inference': [
        'Free energy minimization',
        'Generative modeling and simulation',
        'Bayesian inference and belief updating',
        'Policy selection and expected free energy',
    ],
    'Cognitive Security': [
        'Narrative analysis and discourse mapping',
        'Misinformation detection frameworks',
        'Trust and integrity modeling',
        'Cognitive defense pattern analysis',
    ],
    'Entomology': [
        'Field observation and behavioral assays',
        'Population genetics analysis',
        'Transcriptomic and gene expression profiling',
        'Collective behavior modeling',
    ],
    'Art & Synergetics': [
        'Visual analysis and iconographic interpretation',
        'Historical and conceptual synthesis',
        'Cross-domain pattern mapping',
        'Symbolic and metaphorical analysis',
    ],
    'Genetics & Biomedical': [
        'Genomic sequencing and bioinformatics',
        'Phylogenetic and evolutionary analysis',
        'Statistical genetics and heritability estimation',
        'Molecular mechanism investigation',
    ],
    'AII Ecosystem': [
        'Community coordination and governance',
        'Open science infrastructure development',
        'Educational program design',
        'Inter-organizational collaboration',
    ],
    'Presentations & Media': [
        'Multimedia content production',
        'Pedagogical framework design',
        'Public communication of science',
        'Cross-platform media distribution',
    ],
    'Research': [
        'Literature review and meta-analysis',
        'Theoretical analysis and synthesis',
        'Empirical data collection',
        'Cross-disciplinary integration',
    ],
}

DOMAIN_FINDINGS: dict[str, list[str]] = {
    'default': ['See full paper for detailed findings and analysis'],
}


# ─── Data loading ─────────────────────────────────────────────────────────────


def load_bibliography_map() -> dict[str, dict[str, Any]]:
    """Load BIBLIOGRAPHY rows keyed by folder name."""
    bib = {}
    bib_path = REPO_ROOT / "pages" / "BIBLIOGRAPHY.md"
    if not bib_path.exists():
        return bib
    for row in iter_bibliography_rows(bib_path):
        if not row.folder:
            continue
        bib[row.folder] = {
            "domain_emoji": row.domain,
            "domain": EMOJI_TO_DOMAIN.get(row.domain, 'Research'),
            "type": row.typ,
            "venue": row.venue,
            "title": row.title,
            "year": row.year,
            "link": row.link_cell,
        }
    return bib


def load_aggregate_metadata() -> dict[str, dict[str, Any]]:
    """Load paper_metadata.json (aggregated index)."""
    pm_path = PAPERS_DIR / "paper_metadata.json"
    if not pm_path.exists():
        return {}
    with open(pm_path) as f:
        return json.load(f)


def infer_domain(paper_meta: dict, bib_entry: dict[str, Any] | None) -> str:
    """Infer domain from BIBLIOGRAPHY, paper_metadata, or foldername."""
    if bib_entry and bib_entry.get("domain"):
        return bib_entry["domain"]
    description = (paper_meta.get("description") or paper_meta.get("abstract") or "").lower()
    keywords = paper_meta.get("keywords", paper_meta.get("tags", []))
    kw_text = " ".join(k if isinstance(k, str) else "" for k in keywords).lower()
    all_text = f"{description} {kw_text}"
    checks = {
        'Entomology': ['ant', 'insect', 'bee', 'entomol', 'myrmec', 'colony', 'foraging', 'harvester', 'pheromone'],
        'Active Inference': ['active inference', 'free energy', 'bayesian', 'variational', 'markov blanket', 'efe', 'belief'],
        'Cognitive Security': ['cognitive security', 'cogsec', 'narrative', 'integrity', 'misinformation', 'sensemaking'],
        'Art & Synergetics': ['art', 'blake', 'synergetics', 'music', 'imaginarium', 'metaphor', 'visual'],
        'Genetics & Biomedical': ['genetic', 'genom', 'transcriptom', 'dna', 'pcr', 'mutation', 'chromosome'],
        'Computational': ['software', 'code', 'repository', 'pipeline', 'deterministic', 'reproducible', 'automated', 'infrastructure'],
        'Presentations & Media': ['presentation', 'talk', 'video', 'podcast', 'interview', 'slide', 'transcript'],
    }
    for domain, keywords_list in checks.items():
        if any(k in all_text for k in keywords_list):
            return domain
    if bib_entry and bib_entry.get("type") in ("Presentation", "Course", "Series", "Playbook"):
        return "Presentations & Media"
    return "Research"


def infer_type(paper_meta: dict, bib_entry: dict[str, Any] | None) -> str:
    """Infer work type from BIBLIOGRAPHY or paper_metadata."""
    if bib_entry and bib_entry.get("type"):
        return bib_entry["type"]
    keyw = paper_meta.get("keywords", paper_meta.get("tags", []))
    kw_text = " ".join(k if isinstance(k, str) else "" for k in keyw).lower()
    if any(w in kw_text for w in ["book", "textbook", "monograph"]):
        return "Book"
    if any(w in kw_text for w in ["presentation", "slide", "talk"]):
        return "Presentation"
    if any(w in kw_text for w in ["course", "tutorial"]):
        return "Course"
    return "Paper"


def compute_related_papers(folder: str, domain: str, all_folders: list[str], paper_meta: dict) -> list[str]:
    """Find related papers in the same domain and same year."""
    year = folder[:4]
    related = []
    # Same domain, different paper
    domain_folders = [f for f in all_folders if f != folder]
    # Prefer same-domain
    same_domain_emoji = DOMAIN_TO_EMOJI.get(domain)
    bib_map = load_bibliography_map()
    same_domain = []
    for f in domain_folders:
        fb = bib_map.get(f)
        if fb and fb.get("domain_emoji") == same_domain_emoji:
            same_domain.append(f)
    # Pick up to 3 from same domain
    related.extend(same_domain[:3])
    # If not enough, pick nearby years
    if len(related) < 3:
        same_year = [f for f in domain_folders if f.startswith(year) and f not in related]
        related.extend(same_year[:3 - len(related)])
    return related[:3]


def compute_methods(domain: str, bib_entry: dict[str, Any] | None) -> list[dict[str, str]]:
    """Generate methods based on domain and type."""
    base_methods = DOMAIN_METHODS.get(domain, DOMAIN_METHODS['Research'])
    methods = []
    for m in base_methods:
        methods.append({"name": m, "description": f"Applied {m.lower()} methodology"})
    return methods


def compute_findings(domain: str, paper_meta: dict) -> list[str]:
    """Generate key findings from paper_metadata or fallback."""
    if paper_meta.get("key_findings"):
        return paper_meta["key_findings"]
    desc = (paper_meta.get("description") or paper_meta.get("abstract") or "").strip()
    if desc and len(desc) > 100:
        # Extract first substantive sentence(s)
        sents = re.split(r'(?<=[.!?])\s+', desc)
        findings = []
        for s in sents[:2]:
            clean = s.strip()
            if len(clean) > 30 and not clean.startswith("This paper"):
                findings.append(clean[:200])
            else:
                findings.append(clean[:200] if len(clean) > 30 else f"Analysis of {clean[:100]}")
        if findings:
            return findings
    return ["See full paper for detailed findings and analysis"]


def compute_checked_at() -> str:
    """Return current timestamp."""
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def infer_github_repo(paper_meta: dict) -> str | None:
    """Extract GitHub repo from paper_metadata or github_release_url."""
    if paper_meta.get("github_release_url"):
        url = paper_meta["github_release_url"]
        m = re.search(r"github\.com/([^/]+/[^/]+)", url)
        if m:
            return m.group(1)
    return None


def build_extended_fields(
    folder: str,
    paper_meta: dict,
    bib_entry: dict[str, Any] | None,
    all_folders: list[str],
    existing_meta: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build the extended fields to add/merge into metadata.json.

    Keeps existing metadata.json fields untouched; only adds new ones.
    """
    domain = infer_domain(paper_meta, bib_entry)
    work_type = infer_type(paper_meta, bib_entry)

    fields: dict[str, Any] = {}

    # Domain and type (only if not already present in existing metadata)
    if existing_meta:
        if "domain" not in existing_meta:
            fields["domain"] = domain
        if "type" not in existing_meta:
            fields["type"] = work_type
    else:
        fields["domain"] = domain
        fields["type"] = work_type

    # Methods (only if not already present)
    if existing_meta and "methods" in existing_meta and existing_meta["methods"]:
        pass  # Keep existing methods
    else:
        fields["methods"] = compute_methods(domain, bib_entry)

    # Key findings (only if not already present)
    if existing_meta and "key_findings" in existing_meta and existing_meta["key_findings"]:
        pass
    else:
        fields["key_findings"] = compute_findings(domain, paper_meta)

    # Related papers (only if not already present)
    if existing_meta and "related_papers" in existing_meta and existing_meta["related_papers"]:
        pass
    else:
        related = compute_related_papers(folder, domain, all_folders, paper_meta)
        if related:
            fields["related_papers"] = related

    # Related software (only if not already present)
    if existing_meta and "related_software" in existing_meta and existing_meta["related_software"]:
        pass
    else:
        github_repo = infer_github_repo(paper_meta)
        if github_repo:
            fields["related_software"] = [github_repo]

    # Checked_at (always update if missing)
    if not existing_meta or "checked_at" not in existing_meta:
        fields["checked_at"] = compute_checked_at()

    return fields


def create_minimal_metadata(
    folder: str,
    paper_meta: dict,
    bib_entry: dict[str, Any] | None,
) -> dict[str, Any]:
    """Create a minimal metadata.json for folders that don't have one."""
    domain = infer_domain(paper_meta, bib_entry)
    work_type = infer_type(paper_meta, bib_entry)
    title = paper_meta.get("name", folder)
    doi = paper_meta.get("doi", "")
    authors = paper_meta.get("authors", "Daniel Ari Friedman")
    description = (paper_meta.get("description") or paper_meta.get("abstract") or f"Research on {folder}")[:500]
    keywords = paper_meta.get("keywords", paper_meta.get("tags", []))
    checked_at = compute_checked_at()

    meta = {
        "title": title,
        "domain": domain,
        "type": work_type,
        "creators": [{"name": a.strip()} for a in authors.replace("&", ",").split(",") if a.strip()] if "," in authors or "&" in authors else [{"name": authors.strip()}],
        "description": description,
        "abstract": paper_meta.get("abstract", ""),
        "keywords": keywords if isinstance(keywords, list) else [keywords],
        "methods": compute_methods(domain, bib_entry),
        "key_findings": compute_findings(domain, paper_meta),
    }

    if doi:
        meta["doi"] = doi
    meta["checked_at"] = checked_at

    # Related papers
    all_folders = sorted([d.name for d in PAPERS_DIR.iterdir() if d.is_dir() and d.name[:4].isdigit()])
    related = compute_related_papers(folder, domain, all_folders, paper_meta)
    if related:
        meta["related_papers"] = related

    # GitHub repo
    github_repo = infer_github_repo(paper_meta)
    if github_repo:
        meta["github_repo"] = github_repo

    return meta


# ─── Main ─────────────────────────────────────────────────────────────────────


def main():
    apply = "--apply" in sys.argv

    bib_map = load_bibliography_map()
    aggregate_meta = load_aggregate_metadata()

    # All paper folders
    all_folders = sorted([
        d.name for d in PAPERS_DIR.iterdir()
        if d.is_dir() and d.name[:4].isdigit()
    ])

    stats = {
        "created": 0,
        "extended": 0,
        "unchanged": 0,
        "skipped": 0,
    }

    for folder in all_folders:
        folder_path = PAPERS_DIR / folder
        meta_path = folder_path / "metadata.json"
        bib_entry = bib_map.get(folder)
        paper_meta = aggregate_meta.get(folder, {})

        # Load existing metadata if present
        existing = None
        if meta_path.exists():
            with open(meta_path) as f:
                existing = json.load(f)

            # Check if already has extended fields
            has_extended = bool(
                existing.get("methods")
                and existing.get("key_findings")
                and existing.get("domain")
            )

            if has_extended:
                stats["skipped"] += 1
                continue

            # Add extended fields
            extended = build_extended_fields(
                folder, paper_meta, bib_entry, all_folders, existing
            )

            if not extended:
                stats["unchanged"] += 1
                continue

            # Merge without overwriting original Zenodo fields
            merged = {}
            # Copy original fields first
            merged.update(existing)
            # Add extended fields
            merged.update(extended)

            if apply:
                with open(meta_path, "w") as f:
                    json.dump(merged, f, indent=2, ensure_ascii=False)
                print(f"  EXTENDED: {folder}/metadata.json (+{len(extended)} fields)")
                stats["extended"] += 1
            else:
                print(f"  WOULD EXTEND: {folder}/metadata.json (+{len(extended)} fields)")
                stats["extended"] += 1

        else:
            # Create minimal metadata.json
            new_meta = create_minimal_metadata(folder, paper_meta, bib_entry)

            if apply:
                with open(meta_path, "w") as f:
                    json.dump(new_meta, f, indent=2, ensure_ascii=False)
                print(f"  CREATED: {folder}/metadata.json")
                stats["created"] += 1
            else:
                print(f"  WOULD CREATE: {folder}/metadata.json")
                stats["created"] += 1

    print(
        f"\nSummary: created={stats['created']}, "
        f"extended={stats['extended']}, "
        f"unchanged={stats['unchanged']}, "
        f"skipped (already has fields)={stats['skipped']}"
    )
    if not apply:
        print("DRY RUN — use --apply to write files")


if __name__ == "__main__":
    main()
