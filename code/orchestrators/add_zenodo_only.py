#!/usr/bin/env python3
"""Backfill Zenodo-only publications (no paired GitHub release) into the curated
bibliography and per-paper folder structure.

For each Zenodo record id, this creates papers/<YEAR>_<Slug>/ with README.md,
AGENTS.md, SKILL.md, CITATION.cff, metadata.json, downloads the PDF, appends a
row to pages/BIBLIOGRAPHY.md and papers/README.md, and refreshes volatile counts.

Authorship is preserved verbatim from Zenodo (multi-author works show every
creator); this is a Zenodo-only companion to sync_paired_publications.py, which
handles paired GitHub+Zenodo releases.

Usage: python3 code/orchestrators/add_zenodo_only.py <record_id> [<record_id> ...]
       optional per-record domain override: <record_id>:🐜
"""

from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC = REPO_ROOT / "code" / "src"
sys.path.insert(0, str(SRC))
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

from publication_pairing import slug_topic, yaml_double_quoted, zenodo_record_url_from_doi  # noqa: E402
from sync_paired_publications import refresh_bibliography_counts  # noqa: E402

ORCID = "0000-0001-6232-9096"
UA = "docxology-zenodo-backfill/1.0 (+https://danielarifriedman.com/)"
BIB = REPO_ROOT / "pages" / "BIBLIOGRAPHY.md"
PAPERS = REPO_ROOT / "papers"
PAPER_METADATA = PAPERS / "paper_metadata.json"

TYPE_LABELS = {"publication": "Paper", "presentation": "Presentation", "book": "Book",
               "lesson": "Course", "other": "Paper", "software": "Paper"}


def fetch(record_id: str) -> dict:
    req = urllib.request.Request(f"https://zenodo.org/api/records/{record_id}",
                                 headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def record_url(rec: dict) -> str:
    """Concept-DOI-derived Zenodo landing page URL, consistent with the DOI shown
    alongside it. rec['id'] is the version-specific record id, which can differ
    from the concept id and would otherwise make the same document cite two
    different Zenodo URLs for one work (see ZenodoRecord.record_url)."""
    meta = rec.get("metadata") or {}
    doi = rec.get("conceptdoi") or meta.get("conceptdoi") or rec.get("doi") or meta.get("doi") or ""
    return zenodo_record_url_from_doi(doi) or f"https://zenodo.org/records/{rec.get('id')}"


def clean(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")
    return re.sub(r"\s+", " ", text).strip()


def infer_type(rtype: str, subtype: str, title: str) -> str:
    blob = f"{rtype} {subtype}".lower()
    if "book" in blob:
        return "Book"
    if "presentation" in blob or "poster" in blob:
        return "Presentation"
    if "lesson" in blob or "course" in blob:
        return "Course"
    return "Paper"


def _contains_term(text: str, term: str) -> bool:
    """Whole-word/whole-phrase match so e.g. "ant" does not hit "dominant" and "art" does not hit "smart"."""
    return re.search(rf"\b{re.escape(term)}\b", text) is not None


def infer_domain(text: str) -> str:
    t = text.lower()
    if any(_contains_term(t, w) for w in ["ant", "bee", "insect", "ento", "foraging", "olfact", "semiochem"]):
        return "🐜"
    if any(_contains_term(t, w) for w in ["cognitive security", "cogsec", "narrative", "sensemaking", "rhetoric", "trust", "integrity", "memetic"]):
        return "🛡️"
    if any(_contains_term(t, w) for w in ["blake", "synergetics", "fuller", "quadray", "art"]):
        return "🎨"
    if any(_contains_term(t, w) for w in ["genetic", "genomic", "transcriptomic", "biomedical", "hippocampus", "cortex", "neuro"]):
        return "🧬"
    if any(_contains_term(t, w) for w in ["active inference", "free energy", "bayesian", "markov", "friston", "allostasis", "interoception"]):
        return "🧠"
    if any(_contains_term(t, w) for w in ["software", "code", "pipeline", "reproducible", "computational", "benchmark", "harness", "agent"]):
        return "💻"
    if "active inference institute" in t or _contains_term(t, "ecosystem"):
        return "🌍"
    return "🧠"


def unique_folder(base: str) -> str:
    candidate, i = base, 2
    while (PAPERS / candidate).exists():
        candidate = f"{base}{i}"
        i += 1
    return candidate


def authors_inline(creators: list[dict]) -> str:
    names = []
    for c in creators:
        nm = c.get("name", "")
        if "," in nm:
            fam, _, given = nm.partition(",")
            nm = f"{given.strip()} {fam.strip()}".strip()
        names.append(nm)
    if not names:
        return "Daniel Ari Friedman"
    if len(names) <= 6:
        return ", ".join(names)
    return ", ".join(names[:6]) + f", and {len(names) - 6} others"


def render_readme(rec: dict, meta: dict) -> str:
    title = meta.get("title", "")
    year = (meta.get("publication_date") or "")[:4] or "n.d."
    doi = rec.get("doi", "")
    kws = meta.get("keywords") or []
    kw_line = " · ".join(kws) if kws else "Zenodo publication"
    pdfs = [f["key"] for f in rec.get("files", []) if str(f.get("key", "")).lower().endswith(".pdf")]
    files = "\n".join(f"- `{p}` - Zenodo PDF" for p in pdfs) or "- Zenodo PDF: see record"
    return f"""# {title}

**{authors_inline(meta.get('creators', []))}** ({year}) · *Zenodo*

[![DOI](https://zenodo.org/badge/DOI/{doi}.svg)](https://doi.org/{doi})

---

## Abstract

{clean(meta.get('description')) or 'Publication metadata synchronized from Zenodo.'}

## Keywords

{kw_line}

## Publication Details

| Field | Value |
|------|-------|
| **DOI** | [{doi}](https://doi.org/{doi}) |
| **Published** | {meta.get('publication_date') or 'Unknown'} |
| **Version** | {meta.get('version') or 'Unknown'} |
| **Zenodo record** | {record_url(rec)} |

## Files

{files}

## Citation

> {authors_inline(meta.get('creators', []))} ({year}). *{title}*. Zenodo. https://doi.org/{doi}

## Related

- Zenodo record: {record_url(rec)}
- [Full Bibliography](../../pages/BIBLIOGRAPHY.md) · [All Papers](../README.md)
"""


def render_agents(rec: dict, meta: dict) -> str:
    title = meta.get("title", "")
    year = (meta.get("publication_date") or "")[:4] or "n.d."
    return f"""# AGENTS.md - {title}

**Paper**: {title} ({year})
**DOI**: [{rec.get('doi','')}](https://doi.org/{rec.get('doi','')})
**Zenodo record**: {record_url(rec)}

---

## Agent Roles

### Citation Agent
- Use the Zenodo DOI as the canonical citation.
- Preserve full authorship: {authors_inline(meta.get('creators', []))}.

### Integration Agent
- Keep README, CITATION.cff, metadata.json, paper_metadata.json, and BIBLIOGRAPHY.md synchronized.

## Extraction Log

- **Zenodo record**: {record_url(rec)}
- **Source**: Zenodo-only record (no paired GitHub release)
"""


def render_skill(rec: dict, meta: dict) -> str:
    title = meta.get("title", "")
    kws = meta.get("keywords") or ["zenodo-publication"]
    tags = [k.lower().replace(" ", "-") for k in kws[:8]]
    concepts = "\n".join(f"- **{k}**" for k in kws)
    return f"""---
name: "{slug_topic(title)}"
description: "Use for {yaml_double_quoted(title)}, a Zenodo publication with DOI {rec.get('doi','')}."
tags: {json.dumps(tags)}
---

# {title}

## Instructions

Use this skill when working with the publication **{title}** or its archival record.

1. Ground citations in DOI `{rec.get('doi','')}`.
2. Treat the Zenodo record as the archival source.

## Key Concepts

{concepts}

## Related

- [README.md](README.md)
- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
"""


def render_citation(rec: dict, meta: dict) -> str:
    title = meta.get("title", "")
    year = (meta.get("publication_date") or "")[:4] or "n.d."
    version = f'\nversion: "{meta.get("version")}"' if meta.get("version") else ""
    authors = []
    for c in meta.get("creators", []):
        nm = c.get("name", "")
        fam, _, given = nm.partition(",")
        if given.strip():
            line = f"  - family-names: {fam.strip()}\n    given-names: {given.strip()}"
        else:
            parts = nm.split()
            line = f"  - family-names: {parts[-1]}\n    given-names: {' '.join(parts[:-1])}" if len(parts) > 1 else f"  - name: {nm}"
        if c.get("orcid"):
            line += f'\n    orcid: "https://orcid.org/{c["orcid"]}"'
        authors.append(line)
    return f"""cff-version: 1.2.0
message: "If you use this work, please cite it as below."
type: article
title: "{yaml_double_quoted(title)}"{version}
date-released: {meta.get('publication_date') or year}
doi: {rec.get('doi','')}
url: "https://doi.org/{rec.get('doi','')}"
authors:
{chr(10).join(authors)}
identifiers:
  - type: doi
    value: {rec.get('doi','')}
    description: "Zenodo DOI"
  - type: url
    value: "{record_url(rec)}"
    description: "Zenodo landing page"
"""


def metadata_payload(rec: dict, meta: dict) -> dict:
    files = [{"name": f.get("key"), "size_bytes": f.get("size"),
              "checksum": f.get("checksum", ""),
              "download_url": (f.get("links") or {}).get("self", "")}
             for f in rec.get("files", [])]
    return {
        "title": meta.get("title"),
        "version": meta.get("version"),
        "doi": rec.get("doi"),
        "doi_url": f"https://doi.org/{rec.get('doi')}",
        "zenodo_record": f"{record_url(rec)}",
        "record_id": str(rec.get("id")),
        "publication_date": meta.get("publication_date"),
        "resource_type": meta.get("resource_type"),
        "creators": meta.get("creators"),
        "description": clean(meta.get("description")),
        "keywords": meta.get("keywords") or [],
        "files": files,
        "related_resources": [],
        "github_repo": "",
        "source": "zenodo-only",
        "checked_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }


def download_pdf(rec: dict, folder: Path) -> None:
    for f in rec.get("files", []):
        name = str(f.get("key", ""))
        if not name.lower().endswith(".pdf"):
            continue
        url = (f.get("links") or {}).get("self")
        if not url:
            continue
        target = folder / name
        if target.exists():
            return
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=180) as r:
            target.write_bytes(r.read())
        return


def next_bib_num() -> int:
    nums = []
    for line in BIB.read_text(encoding="utf-8").splitlines():
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cells and cells[0].isdigit():
                nums.append(int(cells[0]))
    return max(nums, default=0) + 1


def add_bib_row(num: int, year: str, domain: str, typ: str, title: str, doi: str, folder: str) -> None:
    text = BIB.read_text(encoding="utf-8")
    if doi in text:
        return
    row = (f"| {num} | {year} | {domain} | {typ} | {title} | *Zenodo* | "
           f"[{doi}](https://doi.org/{doi}) | [📁](../papers/{folder}/) |")
    lines = text.splitlines()
    insert_at = len(lines)
    in_table = False
    for idx, line in enumerate(lines):
        if line.startswith("| # | Year | Domain | Type |"):
            in_table = True
            continue
        if in_table and line.startswith("|"):
            continue
        if in_table:
            insert_at = idx
            break
    lines.insert(insert_at, row)
    BIB.write_text(refresh_bibliography_counts("\n".join(lines).rstrip() + "\n"), encoding="utf-8")


def add_papers_readme_row(folder: str, year: str, has_pdf: bool) -> None:
    path = PAPERS / "README.md"
    text = path.read_text(encoding="utf-8")
    if f"]({folder}/)" in text:
        return
    rows = [l for l in text.splitlines() if re.match(r"\| \d+ \|", l)]
    num = len(rows) + 1
    topic = folder.split("_", 1)[1]
    row = f"| {num} | [{folder}]({folder}/) | {'✅' if has_pdf else '—'} | {year} | {topic} |"
    lines = text.splitlines()
    insert_at = next((i for i, l in enumerate(lines) if l.startswith("## Scripts")), len(lines))
    lines.insert(insert_at, row)
    text = "\n".join(lines).rstrip() + "\n"
    count = len([l for l in text.splitlines() if re.match(r"\| \d+ \|", l)])
    text = re.sub(r"## Papers \(\d+\)", f"## Papers ({count})", text)
    path.write_text(text, encoding="utf-8")


def add_paper_metadata(folder: str, meta: dict, doi: str) -> None:
    data = json.loads(PAPER_METADATA.read_text(encoding="utf-8")) if PAPER_METADATA.exists() else {}
    year, topic = folder.split("_", 1)
    data[folder] = {
        "year": year, "topic": topic, "name": meta.get("title"),
        "description": clean(meta.get("description")),
        "authors": authors_inline(meta.get("creators", [])),
        "abstract": clean(meta.get("description")),
        "keywords": meta.get("keywords") or [], "doi": doi,
    }
    PAPER_METADATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def refresh_papers_agents() -> None:
    path = PAPERS / "AGENTS.md"
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r"for \d+ publications",
        "for bibliography entries with in-tree documentation",
        text,
    )
    text = re.sub(
        r"\(\d+ entries as of [^)]+\)",
        "; current folder/export counts live in [`../reports/current_counts.md`](../reports/current_counts.md)",
        text,
    )
    text = re.sub(
        r"README\.md present \| \d+/\d+ folders[^|]*",
        "README.md present | required per folder; current coverage is generated in [`../reports/current_counts.md`](../reports/current_counts.md) ",
        text,
    )
    text = re.sub(r"AGENTS\.md present \| \d+/\d+", "AGENTS.md present | required per folder", text)
    text = re.sub(r"SKILL\.md present \| \d+/\d+", "SKILL.md present | required per folder", text)
    path.write_text(text, encoding="utf-8")


def main(argv: list[str]) -> int:
    # --no-regenerate skips the post-add local rebuild (e.g. when batching several adds).
    regenerate = "--no-regenerate" not in argv
    argv = [a for a in argv if a != "--no-regenerate"]
    overrides = {}
    ids = []
    for a in argv:
        if ":" in a:
            rid, dom = a.split(":", 1)
            overrides[rid] = dom
            ids.append(rid)
        else:
            ids.append(a)
    added = []
    for rid in ids:
        rec = fetch(rid)
        meta = rec.get("metadata", {})
        title = meta.get("title", "").strip()
        doi = rec.get("doi", "")
        if doi in BIB.read_text(encoding="utf-8"):
            print(f"skip {rid}: DOI already in bibliography")
            continue
        year = (meta.get("publication_date") or "")[:4] or "n.d."
        rtype = (meta.get("resource_type") or {}).get("type", "")
        subtype = (meta.get("resource_type") or {}).get("subtype", "")
        typ = infer_type(rtype, subtype, title)
        blob = f"{title} {clean(meta.get('description'))} {' '.join(meta.get('keywords') or [])}"
        domain = overrides.get(rid) or infer_domain(blob)
        folder = unique_folder(f"{year}_{slug_topic(title)}")
        fpath = PAPERS / folder
        fpath.mkdir(parents=True, exist_ok=True)
        (fpath / "README.md").write_text(render_readme(rec, meta), encoding="utf-8")
        (fpath / "AGENTS.md").write_text(render_agents(rec, meta), encoding="utf-8")
        (fpath / "SKILL.md").write_text(render_skill(rec, meta), encoding="utf-8")
        (fpath / "CITATION.cff").write_text(render_citation(rec, meta), encoding="utf-8")
        (fpath / "metadata.json").write_text(json.dumps(metadata_payload(rec, meta), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        download_pdf(rec, fpath)
        has_pdf = any(p.suffix == ".pdf" for p in fpath.iterdir())
        num = next_bib_num()
        add_bib_row(num, year, domain, typ, title, doi, folder)
        add_papers_readme_row(folder, year, has_pdf)
        add_paper_metadata(folder, meta, doi)
        added.append((num, folder, domain, typ, title))
        print(f"added #{num} [{domain} {typ}] {folder}  <- {title[:55]}")
    refresh_papers_agents()
    print(f"\n{len(added)} record(s) added.")

    # Close the partial-regeneration gap: a Zenodo-only add touches the bibliography and
    # paper folders but leaves works.json, counts, agent data, pages, search/feed/sitemap,
    # and the manifest stale. Rebuild the local generated layer in one dependency-ordered
    # pass (same driver the publication-sync runbook documents). Network freshness and the
    # live-site snapshot remain a deliberate follow-up.
    if added and regenerate:
        print("\nRegenerating local generated layer (regenerate_all.py)...")
        subprocess.run(
            ["python3", "code/orchestrators/regenerate_all.py"],
            cwd=REPO_ROOT, check=True,
        )
        print("Run `verify_live_site.py` (if counts changed) then `validate_repo.py` before committing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
