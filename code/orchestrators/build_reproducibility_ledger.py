#!/usr/bin/env python3
"""Build the per-work reproducibility ledger.

The Evidence Ledger (``evidence.html``) records *site-level* claims — aggregate
statements such as "the curated bibliography contains N works". This orchestrator
records the complementary *work-level* posture: for each catalogued work, which
independently checkable artifacts exist.

The ledger deliberately scores **availability**, not correctness. A work can hold
a perfect score and still be wrong; a work can score poorly and be a landmark
result published somewhere that predates persistent identifiers. The score answers
one narrow question: *how much of this work can a third party check without asking
the author for anything?*

Signals (each binary, each derived from an existing generated export):

===================  =============================================================
``persistent_id``    A DOI is recorded, so the citation survives link rot.
``public_archive``   A deposited copy exists (Zenodo DOI, or a linked repository
                     with a Zenodo record) rather than only a live web page.
``open_full_text``   Full text was extracted and is served from this site.
``source_documents`` A paper folder with a README accompanies the entry.
``executable_code``  A catalogued repository declares this work as its paper.
``agent_readable``   Structured agent guidance (AGENTS.md or SKILL.md) exists.
===================  =============================================================

Outputs ``data/reproducibility.json``, ``reproducibility.html``, and
``pages/REPRODUCIBILITY.md``. Run with ``--check`` to fail on staleness.
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
JSON_OUT = REPO_ROOT / "data" / "reproducibility.json"
HTML_OUT = REPO_ROOT / "reproducibility.html"
MD_OUT = REPO_ROOT / "pages" / "REPRODUCIBILITY.md"

sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
from site_nav import (  # noqa: E402
    BREADCRUMB_CSS,
    HEAD_EXTRAS,
    INTERACTIVE_SCRIPTS,
    MENU_ESC_SCRIPT,
    breadcrumb_jsonld_script,
    render_breadcrumb,
)

ZENODO_DOI_PREFIX = "10.5281"

# (key, label, one-line description of what a reader may independently do)
SIGNALS: tuple[tuple[str, str, str], ...] = (
    ("persistent_id", "Persistent identifier", "Resolve a DOI instead of trusting a live URL."),
    ("public_archive", "Public archive", "Fetch a deposited copy from a third-party archive."),
    ("open_full_text", "Open full text", "Read the full text without a paywall or request."),
    ("source_documents", "Source documents", "Inspect the working folder behind the entry."),
    ("executable_code", "Executable code", "Run the software that produced or accompanies it."),
    ("agent_readable", "Agent-readable guidance", "Parse structured guidance without scraping prose."),
)
SIGNAL_KEYS: tuple[str, ...] = tuple(key for key, _, _ in SIGNALS)
MAX_SCORE = len(SIGNAL_KEYS)

# Score bands. Names describe reader effort, not research quality.
BANDS: tuple[tuple[str, int, str], ...] = (
    ("independently reproducible", 5, "Code, archive, and text are all reachable without contacting the author."),
    ("independently checkable", 3, "Enough is public to confirm the record and read the argument."),
    ("citable only", 1, "The record resolves, but little beyond it is machine-checkable."),
    ("unverified", 0, "Nothing here is independently checkable from this site alone."),
)

_BREADCRUMB = [("Home", ""), ("Reproducibility", "reproducibility.html")]
_WEBPAGE_LD = {
    "@context": "https://schema.org",
    "@type": "WebPage",
    "@id": "https://danielarifriedman.com/reproducibility.html#page",
    "name": "Reproducibility Ledger — Daniel Ari Friedman",
    "url": "https://danielarifriedman.com/reproducibility.html",
    "isPartOf": {"@id": "https://danielarifriedman.com/#website"},
}


def h(value: object) -> str:
    return html.escape(str(value), quote=True)


def _load(name: str) -> dict:
    with open(REPO_ROOT / "data" / name, encoding="utf-8") as handle:
        return json.load(handle)


def code_index() -> dict[str, list[dict]]:
    """Map a work's ``docs_path`` to the repositories that declare it."""
    index: dict[str, list[dict]] = {}
    for repo in _load("software.json")["repositories"]:
        paper_path = (repo.get("paper_path") or "").strip().strip("/")
        if paper_path:
            index.setdefault(paper_path, []).append(repo)
    return index


def evaluate(work: dict, repos_for_work: list[dict]) -> dict:
    doi = (work.get("doi") or "").strip()
    archived_repo = any(repo.get("zenodo_url") for repo in repos_for_work)
    signals = {
        "persistent_id": bool(doi),
        "public_archive": doi.startswith(ZENODO_DOI_PREFIX) or archived_repo,
        "open_full_text": bool(work.get("has_full_text")),
        "source_documents": bool(work.get("has_paper_folder")) and bool(work.get("has_readme")),
        "executable_code": bool(repos_for_work),
        "agent_readable": bool(work.get("has_agents_md")) or bool(work.get("has_skill_md")),
    }
    score = sum(1 for key in SIGNAL_KEYS if signals[key])
    band = next(name for name, floor, _ in BANDS if score >= floor)
    return {
        "num": work["num"],
        "citation_key": work["citation_key"],
        "title": work["title"],
        "year": work["year"],
        "domain_name": work["domain_name"],
        "type": work["type"],
        "score": score,
        "band": band,
        "signals": signals,
        "repositories": sorted(repo["name"] for repo in repos_for_work),
    }


def build_ledger() -> dict:
    works = _load("works.json")["works"]
    repos_by_path = code_index()
    entries = [evaluate(work, repos_by_path.get((work.get("docs_path") or "").strip().strip("/"), [])) for work in works]
    entries.sort(key=lambda entry: (-entry["score"], entry["num"]))

    totals = {key: sum(1 for entry in entries if entry["signals"][key]) for key in SIGNAL_KEYS}
    bands = Counter(entry["band"] for entry in entries)
    scores = Counter(entry["score"] for entry in entries)
    total = len(entries)
    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "schema_ref": "/data/agent-index.json#schemas/ReproducibilityLedger",
        "sources": ["data/works.json", "data/software.json"],
        "measures": "artifact availability, not correctness or peer-review status",
        "signal_definitions": [
            {"key": key, "label": label, "reader_action": action} for key, label, action in SIGNALS
        ],
        "band_definitions": [{"band": name, "min_score": floor, "meaning": meaning} for name, floor, meaning in BANDS],
        "max_score": MAX_SCORE,
        "work_count": total,
        "signal_totals": totals,
        "band_counts": {name: bands.get(name, 0) for name, _, _ in BANDS},
        "score_histogram": {str(score): scores.get(score, 0) for score in range(MAX_SCORE + 1)},
        "mean_score": round(sum(entry["score"] for entry in entries) / total, 3) if total else 0.0,
        "works": entries,
    }


def _pct(count: int, total: int) -> str:
    return f"{(100 * count / total):.0f}%" if total else "0%"


def weakest(ledger: dict, limit: int = 12) -> list[dict]:
    """Lowest-scoring works, worst first. Published deliberately."""
    return sorted(ledger["works"], key=lambda entry: (entry["score"], entry["num"]))[:limit]


def render_html(ledger: dict) -> str:
    total = ledger["work_count"]
    signal_rows = "\n".join(
        f"""                        <tr><th scope="row">{h(label)}</th>"""
        f"""<td>{ledger['signal_totals'][key]} / {total}</td>"""
        f"""<td>{h(_pct(ledger['signal_totals'][key], total))}</td>"""
        f"""<td>{h(action)}</td></tr>"""
        for key, label, action in SIGNALS
    )
    band_rows = "\n".join(
        f"""                        <tr><th scope="row">{h(name)}</th>"""
        f"""<td>{ledger['band_counts'][name]}</td>"""
        f"""<td>{h(_pct(ledger['band_counts'][name], total))}</td>"""
        f"""<td>{h(meaning)}</td></tr>"""
        for name, _, meaning in BANDS
    )
    gap_rows = "\n".join(
        f"""                        <tr><td><a href="works/{h(entry['citation_key'])}.html">{h(entry['title'])}</a></td>"""
        f"""<td>{h(entry['year'])}</td><td>{entry['score']} / {MAX_SCORE}</td>"""
        f"""<td>{h(', '.join(label for key, label, _ in SIGNALS if not entry['signals'][key]) or '—')}</td></tr>"""
        for entry in weakest(ledger)
    )
    hist = ledger["score_histogram"]
    peak = max(hist.values()) or 1
    bars = "\n".join(
        f"""                    <div class="repro-bar"><span class="repro-bar-label">{score} / {MAX_SCORE}</span>"""
        f"""<span class="repro-bar-track"><span class="repro-bar-fill" style="width:{(100 * hist[str(score)] / peak):.1f}%"></span></span>"""
        f"""<span class="repro-bar-value">{hist[str(score)]}</span></div>"""
        for score in range(MAX_SCORE, -1, -1)
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reproducibility Ledger — Daniel Ari Friedman</title>
    <meta name="description" content="Per-work reproducibility ledger: which of {total} catalogued works carry a persistent identifier, an archived copy, open full text, source documents, executable code, and agent-readable guidance.">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://danielarifriedman.com/reproducibility.html">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="manifest" href="/manifest.json">
    <link rel="alternate" type="application/rss+xml" href="/feed.xml" title="Daniel Ari Friedman updates">
    <link rel="alternate" type="text/plain" href="/llms.txt" title="LLMs.txt">
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="Daniel Ari Friedman">
    <link rel="alternate" type="application/json" href="/search-index.json" title="Site search index">
    {HEAD_EXTRAS}
    <meta property="og:type" content="website">
    <meta property="og:title" content="Reproducibility Ledger — Daniel Ari Friedman">
    <meta property="og:description" content="What a third party can check without asking the author: per-work reproducibility signals across {total} catalogued works.">
    <meta property="og:url" content="https://danielarifriedman.com/reproducibility.html">
    <meta property="og:image" content="https://danielarifriedman.com/og-cite-verify.jpg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:alt" content="Reproducibility Ledger — Daniel Ari Friedman">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Reproducibility Ledger — Daniel Ari Friedman">
    <meta name="twitter:description" content="What a third party can check without asking the author: per-work reproducibility signals.">
    <meta name="twitter:image" content="https://danielarifriedman.com/og-cite-verify.jpg">
    <meta name="twitter:image:alt" content="Reproducibility Ledger — Daniel Ari Friedman">
    <link rel="stylesheet" href="style.css?v=newspaper-glitch-20260530c">
    <meta name="theme-color" content="#0c0c0e">
    <style>
        .repro-table{{width:100%;border-collapse:collapse;font-size:.86rem}}
        .repro-table th,.repro-table td{{padding:.55rem .6rem;border-bottom:1px solid var(--border);text-align:left;vertical-align:top}}
        .repro-table thead th{{font-size:.68rem;text-transform:uppercase;letter-spacing:.08em;color:var(--text-muted)}}
        .repro-table tbody th{{color:var(--silver-bright);font-weight:600}}
        .repro-scroll{{overflow-x:auto}}
        .repro-bar{{display:grid;grid-template-columns:4.5rem 1fr 2.5rem;align-items:center;gap:.6rem;margin-bottom:.35rem}}
        .repro-bar-label,.repro-bar-value{{font-size:.74rem;color:var(--text-muted);font-variant-numeric:tabular-nums}}
        .repro-bar-value{{text-align:right}}
        .repro-bar-track{{background:var(--bg-card);border:1px solid var(--border);border-radius:3px;height:.85rem;overflow:hidden}}
        .repro-bar-fill{{display:block;height:100%;background:var(--silver-bright);opacity:.55}}
        .repro-note{{font-size:.84rem;color:var(--text-secondary);line-height:1.65}}
    </style>
{_head_extra()}</head>
<body>
    <a href="#main" class="skip-link">Skip to main content</a>
    <nav role="navigation" aria-label="Main navigation">
        <a href="index.html" class="nav-logo">Daniel Ari Friedman</a>
        <button class="menu-btn" aria-label="Toggle menu" aria-expanded="false">☰</button>
        <div class="nav-links">
            <a href="index.html#about">About</a>
            <a href="publications.html">Publications</a>
            <a href="domains.html">Domains</a>
            <a href="software.html">Software</a>
            <a href="discovery.html">Discovery</a>
            <a href="cite-verify.html">Cite</a>
            <a href="data/agent-index.json">Agent Map</a>
        </div>
    </nav>
{render_breadcrumb(_BREADCRUMB)}
    <header class="page-hero">
        <h1>Reproducibility Ledger</h1>
        <p class="sub">What a third party can check about each of {total} catalogued works without asking me for anything.</p>
    </header>
    <main id="main" class="main">
        <section class="section">
            <div class="section-header"><h2>What this measures</h2><div class="section-divider"></div></div>
            <p class="repro-note">This ledger scores <strong>artifact availability, not correctness</strong>. A work can score {MAX_SCORE}/{MAX_SCORE} and still be wrong, and an important result published before persistent identifiers existed can score low through no fault of its own. The score answers one narrow question: how much of the record is independently checkable from public artifacts alone. Every value is computed from <a href="data/works.json">works.json</a> and <a href="data/software.json">software.json</a> by <a href="https://github.com/docxology/docxology/blob/main/code/orchestrators/build_reproducibility_ledger.py">one generator</a>, and the build fails if this page drifts from that computation.</p>
        </section>
        <section class="section">
            <div class="section-header"><h2>Signal coverage</h2><p>Each row is a distinct thing a reader can do without corresponding with the author.</p><div class="section-divider"></div></div>
            <div class="repro-scroll"><table class="repro-table">
                <thead><tr><th scope="col">Signal</th><th scope="col">Works</th><th scope="col">Share</th><th scope="col">What it lets a reader do</th></tr></thead>
                <tbody>
{signal_rows}
                </tbody>
            </table></div>
        </section>
        <section class="section">
            <div class="section-header"><h2>Score distribution</h2><p>Mean score {ledger['mean_score']} of {MAX_SCORE}.</p><div class="section-divider"></div></div>
{bars}
            <div class="repro-scroll mt-2"><table class="repro-table">
                <thead><tr><th scope="col">Band</th><th scope="col">Works</th><th scope="col">Share</th><th scope="col">Meaning</th></tr></thead>
                <tbody>
{band_rows}
                </tbody>
            </table></div>
        </section>
        <section class="section">
            <div class="section-header"><h2>Weakest entries</h2><p>Published deliberately. A ledger that only showed its strongest records would not be evidence of anything.</p><div class="section-divider"></div></div>
            <div class="repro-scroll"><table class="repro-table">
                <thead><tr><th scope="col">Work</th><th scope="col">Year</th><th scope="col">Score</th><th scope="col">Missing</th></tr></thead>
                <tbody>
{gap_rows}
                </tbody>
            </table></div>
            <p class="text-center mt-2"><a class="btn btn-outline" href="data/reproducibility.json">Ledger JSON</a> <a class="btn btn-outline" href="evidence.html">Evidence Ledger</a> <a class="btn btn-outline" href="cite-verify.html">Cite &amp; Verify</a></p>
        </section>
    </main>
    <footer role="contentinfo">
        <div class="footer-rule" aria-hidden="true"></div>
        <p>Daniel Ari Friedman, PhD · <a href="https://danielarifriedman.com/">danielarifriedman.com</a></p>
        <div class="footer-links"><a href="evidence.html">Evidence</a><a href="cite-verify.html">Cite &amp; Verify</a><a href="pages/REPRODUCIBILITY.md">Markdown</a><a href="https://github.com/docxology/docxology">Source Repo</a></div>
    </footer>
{INTERACTIVE_SCRIPTS}
{MENU_ESC_SCRIPT}</body>
</html>
"""


def _head_extra() -> str:
    return (
        f"    <style>{BREADCRUMB_CSS}</style>\n"
        f'    <script type="application/ld+json">\n{json.dumps(_WEBPAGE_LD, indent=4, ensure_ascii=False)}\n    </script>\n'
        f"{breadcrumb_jsonld_script(_BREADCRUMB)}\n"
    )


def render_md(ledger: dict) -> str:
    total = ledger["work_count"]
    lines = [
        "---",
        'title: "REPRODUCIBILITY - Daniel Ari Friedman"',
        'description: "Per-work reproducibility ledger scoring artifact availability across the curated bibliography."',
        'keywords: "Daniel Ari Friedman, reproducibility, open science, verification, research artifacts"',
        "---",
        '<div align="center">',
        "",
        "# Reproducibility Ledger",
        "",
        "> **Navigation**: [🏠 Home](../README.md) | [🧾 Evidence](EVIDENCE.md) | [🧭 Discovery](DISCOVERY.md) | [📚 Bibliography](BIBLIOGRAPHY.md)",
        "",
        "[Website version](../reproducibility.html) · [Ledger JSON](../data/reproducibility.json)",
        "",
        "</div>",
        "",
        "---",
        "",
        f"What a third party can check about each of {total} catalogued works without asking the author for anything.",
        "",
        "This ledger scores **artifact availability, not correctness**. A work can hold a perfect",
        "score and still be wrong; an important result published before persistent identifiers",
        "existed can score low through no fault of its own. Values are computed from",
        "`data/works.json` and `data/software.json` by",
        "`code/orchestrators/build_reproducibility_ledger.py`; the build fails if this file drifts",
        "from that computation.",
        "",
        "## Signal coverage",
        "",
        "| Signal | Works | Share | What it lets a reader do |",
        "| --- | --- | --- | --- |",
    ]
    for key, label, action in SIGNALS:
        count = ledger["signal_totals"][key]
        lines.append(f"| {label} | {count} / {total} | {_pct(count, total)} | {action} |")
    lines += [
        "",
        f"Mean score {ledger['mean_score']} of {MAX_SCORE}.",
        "",
        "## Bands",
        "",
        "| Band | Works | Share | Meaning |",
        "| --- | --- | --- | --- |",
    ]
    for name, _, meaning in BANDS:
        count = ledger["band_counts"][name]
        lines.append(f"| {name} | {count} | {_pct(count, total)} | {meaning} |")
    lines += [
        "",
        "## Weakest entries",
        "",
        "Published deliberately. A ledger that only showed its strongest records would not be",
        "evidence of anything.",
        "",
        "| Work | Year | Score | Missing |",
        "| --- | --- | --- | --- |",
    ]
    for entry in weakest(ledger):
        missing = ", ".join(label for key, label, _ in SIGNALS if not entry["signals"][key]) or "—"
        lines.append(
            f"| [{entry['title']}](../works/{entry['citation_key']}.html) | {entry['year']} | "
            f"{entry['score']} / {MAX_SCORE} | {missing} |"
        )
    lines += [
        "",
        "## Maintenance",
        "",
        "- Regenerate with `uv run python3 code/orchestrators/build_reproducibility_ledger.py`.",
        "- Verify without writing using `--check`; `validate_repo.py` runs that check.",
        "- Raising a score means shipping the missing artifact, never editing this file.",
    ]
    return "\n".join(lines).rstrip() + "\n"


def _preserve_generated_at(ledger: dict, *, json_out: Path = JSON_OUT) -> dict:
    """Retain a prior timestamp when the ledger's substantive body is unchanged.

    The JSON timestamp is informational, not a new reproducibility result.  If
    write mode refreshes it every pass, it changes the Pages manifest, which in
    turn makes a supposedly idempotent release pipeline perpetually dirty.
    """
    if not json_out.exists():
        return ledger
    try:
        existing = json.loads(json_out.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ledger
    current_body = dict(ledger)
    existing_body = dict(existing) if isinstance(existing, dict) else {}
    current_body.pop("generated_at", None)
    existing_body.pop("generated_at", None)
    prior_timestamp = existing.get("generated_at") if isinstance(existing, dict) else None
    if current_body == existing_body and isinstance(prior_timestamp, str) and prior_timestamp:
        ledger["generated_at"] = prior_timestamp
    return ledger


def outputs(
    *,
    json_out: Path = JSON_OUT,
    html_out: Path = HTML_OUT,
    md_out: Path = MD_OUT,
) -> dict[Path, str]:
    """Render the ledger for explicit output paths without writing them."""
    ledger = _preserve_generated_at(build_ledger(), json_out=json_out)
    return {
        json_out: json.dumps(ledger, indent=2, ensure_ascii=False) + "\n",
        html_out: render_html(ledger),
        md_out: render_md(ledger),
    }


def _comparable(path: Path, content: str) -> tuple[str, str]:
    """Return (on-disk, freshly-generated) normalized for comparison.

    Only ``reproducibility.json`` carries a wall-clock ``generated_at``; that one
    field is stripped from both sides so ``--check`` measures substance rather than
    clock drift. Every other output is compared byte-for-byte against disk.
    """
    on_disk = path.read_text(encoding="utf-8")
    if path != JSON_OUT:
        return on_disk, content
    existing = json.loads(on_disk)
    fresh = json.loads(content)
    existing.pop("generated_at", None)
    fresh.pop("generated_at", None)
    return json.dumps(existing, sort_keys=True), json.dumps(fresh, sort_keys=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the per-work reproducibility ledger.")
    parser.add_argument("--check", action="store_true", help="Fail if ledger outputs are stale")
    args = parser.parse_args()
    stale: list[str] = []
    for path, content in outputs().items():
        if args.check:
            if not path.exists():
                stale.append(str(path.relative_to(REPO_ROOT)))
                continue
            current, fresh = _comparable(path, content)
            if current != fresh:
                stale.append(str(path.relative_to(REPO_ROOT)))
        else:
            path.write_text(content, encoding="utf-8")
    if stale:
        raise SystemExit("Stale generated reproducibility outputs: " + ", ".join(stale))
    print(("checked" if args.check else "wrote") + " reproducibility ledger")


if __name__ == "__main__":
    main()
