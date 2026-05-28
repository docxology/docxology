#!/usr/bin/env python3
"""Build a full public GitHub repository inventory and searchable HTML page."""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
JSON_OUT = REPO_ROOT / "data" / "github-repositories.json"
HTML_OUT = REPO_ROOT / "repositories.html"
OWNERS = ("docxology", "ActiveInferenceInstitute")
USER_AGENT = "docxology-github-inventory/1.0 (+https://danielarifriedman.com/)"
BASELINE_PATH = REPO_ROOT / "data" / "github-repositories-baseline.json"


def request_json(url: str, timeout: int = 30) -> Any:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": USER_AGENT}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_profile(owner: str) -> dict[str, Any]:
    data = request_json(f"https://api.github.com/users/{owner}")
    return {
        "login": data.get("login", owner),
        "html_url": data.get("html_url", f"https://github.com/{owner}"),
        "public_repos": data.get("public_repos", 0),
        "updated_at": data.get("updated_at", ""),
    }


def fetch_repositories(owner: str) -> list[dict[str, Any]]:
    repos: list[dict[str, Any]] = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{owner}/repos?per_page=100&page={page}&sort=updated&direction=desc"
        batch = request_json(url)
        if not isinstance(batch, list):
            raise RuntimeError(f"Unexpected GitHub response for {owner}: {batch!r}")
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return repos


def curated_keys() -> set[str]:
    path = REPO_ROOT / "data" / "software.json"
    if not path.exists():
        return set()
    payload = json.loads(path.read_text(encoding="utf-8"))
    keys = set()
    for repo in payload.get("repositories", []):
        owner = repo.get("owner", "")
        name = repo.get("name", "")
        if owner and name:
            keys.add(f"{owner.lower()}/{name.lower()}")
    return keys


def normalize_repo(repo: dict[str, Any], curated: set[str], generated_at: str) -> dict[str, Any]:
    owner = repo.get("owner", {}).get("login", "")
    name = repo.get("name", "")
    key = f"{owner.lower()}/{name.lower()}"
    pushed_at = repo.get("pushed_at") or ""
    updated_at = repo.get("updated_at") or ""
    recent_since = dt.datetime.fromisoformat(generated_at.replace("Z", "+00:00")) - dt.timedelta(days=90)
    try:
        updated_dt = dt.datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
        recently_updated = updated_dt >= recent_since
    except ValueError:
        recently_updated = False
    return {
        "name": name,
        "full_name": repo.get("full_name", f"{owner}/{name}"),
        "owner": owner,
        "html_url": repo.get("html_url", ""),
        "description": repo.get("description") or "",
        "homepage": repo.get("homepage") or "",
        "language": repo.get("language") or "",
        "stars": repo.get("stargazers_count", 0),
        "forks": repo.get("forks_count", 0),
        "watchers": repo.get("watchers_count", 0),
        "open_issues": repo.get("open_issues_count", 0),
        "visibility": repo.get("visibility", "public"),
        "private": bool(repo.get("private", False)),
        "fork": bool(repo.get("fork", False)),
        "archived": bool(repo.get("archived", False)),
        "disabled": bool(repo.get("disabled", False)),
        "is_template": bool(repo.get("is_template", False)),
        "topics": repo.get("topics") or [],
        "license": (repo.get("license") or {}).get("spdx_id", ""),
        "default_branch": repo.get("default_branch", ""),
        "created_at": repo.get("created_at", ""),
        "updated_at": updated_at,
        "pushed_at": pushed_at,
        "curated": key in curated,
        "recently_updated": recently_updated,
    }


def build_payload() -> dict[str, Any]:
    generated_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    curated = curated_keys()
    profiles = {}
    repositories = []
    warnings = []
    for owner in OWNERS:
        profile = fetch_profile(owner)
        repos = fetch_repositories(owner)
        profiles[owner] = profile
        if profile["public_repos"] != len(repos):
            warnings.append(
                f"{owner} profile public_repos={profile['public_repos']} but fetched {len(repos)} repositories"
            )
        repositories.extend(normalize_repo(repo, curated, generated_at) for repo in repos)
    repositories.sort(key=lambda repo: (repo["owner"].lower(), repo["name"].lower()))
    counts = {
        "total": len(repositories),
        "docxology": sum(1 for repo in repositories if repo["owner"] == "docxology"),
        "ActiveInferenceInstitute": sum(1 for repo in repositories if repo["owner"] == "ActiveInferenceInstitute"),
        "curated": sum(1 for repo in repositories if repo["curated"]),
        "uncataloged": sum(1 for repo in repositories if not repo["curated"]),
        "forks": sum(1 for repo in repositories if repo["fork"]),
        "archived": sum(1 for repo in repositories if repo["archived"]),
        "public": sum(1 for repo in repositories if not repo["private"]),
        "private": sum(1 for repo in repositories if repo["private"]),
        "recently_updated": sum(1 for repo in repositories if repo["recently_updated"]),
    }
    languages = sorted({repo["language"].strip().lower() for repo in repositories if repo["language"]})
    return {
        "generated_at": generated_at,
        "source": "GitHub REST API /users/{owner}/repos",
        "owners": list(OWNERS),
        "profiles": profiles,
        "counts": counts,
        "warnings": warnings,
        "repositories": repositories,
        "languages": languages,
    }


def h(value: object) -> str:
    return html.escape(str(value), quote=True)


VISUAL_EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF\u2600-\u27BF\ufe0f]")


def strip_visual_emoji(value: str) -> str:
    return re.sub(r"\s{2,}", " ", VISUAL_EMOJI_RE.sub("", value)).strip()


def render_rows(repositories: list[dict[str, Any]]) -> str:
    rows = []
    for repo in repositories:
        description = strip_visual_emoji(repo["description"])
        flags = []
        if repo["curated"]:
            flags.append("curated")
        if repo["fork"]:
            flags.append("fork")
        if repo["archived"]:
            flags.append("archived")
        if repo["recently_updated"]:
            flags.append("recent")
        flag_text = ", ".join(flags) if flags else "uncataloged"
        searchable = " ".join(
            [
                repo["name"],
                repo["full_name"],
                description,
                repo["language"].lower(),
                repo["owner"],
                flag_text,
                " ".join(repo.get("topics", [])),
            ]
        ).lower()
        rows.append(
            f"""                    <tr data-owner="{h(repo['owner'])}" data-curated="{str(repo['curated']).lower()}" data-fork="{str(repo['fork']).lower()}" data-archived="{str(repo['archived']).lower()}" data-recent="{str(repo['recently_updated']).lower()}" data-visibility="{h('private' if repo['private'] else 'public')}" data-language="{h((repo['language'] or '').lower())}" data-search="{h(searchable)}">
                        <td><a href="{h(repo['html_url'])}">{h(repo['full_name'])}</a><span>{h(description)}</span></td>
                        <td>{h(repo['language'] or '—')}</td>
                        <td>{h(repo['stars'])}</td>
                        <td>{h(repo['forks'])}</td>
                        <td>{h(repo['updated_at'][:10])}</td>
                        <td>{h(flag_text)}</td>
                    </tr>"""
        )
    return "\n".join(rows)


def render_html(payload: dict[str, Any]) -> str:
    counts = payload["counts"]
    rows = render_rows(payload["repositories"])
    warning = ""
    if payload["warnings"]:
        warning = f"<p class=\"note\">Warnings: {h('; '.join(payload['warnings']))}</p>"
    language_options = "\n".join(
        f'                <option value="{h(language)}">{h(language)}</option>'
        for language in payload["languages"]
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Repository Inventory — Daniel Ari Friedman</title>
    <meta name="description" content="Full generated inventory of public docxology and Active Inference Institute GitHub repositories, with curated catalog coverage flags.">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://danielarifriedman.com/repositories.html">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="manifest" href="/manifest.json">
    <link rel="alternate" type="application/json" href="/data/github-repositories.json" title="GitHub repositories JSON">
    <meta property="og:type" content="website">
    <meta property="og:title" content="Repository Inventory — Daniel Ari Friedman">
    <meta property="og:description" content="Full generated inventory of public GitHub repositories with curated catalog flags.">
    <meta property="og:url" content="https://danielarifriedman.com/repositories.html">
    <meta property="og:image" content="https://danielarifriedman.com/og-software.jpg">
    <link rel="stylesheet" href="style.css?v=newspaper-glitch-20260528f">
    <style>
        .inventory-controls{{display:flex;flex-wrap:wrap;gap:.65rem;align-items:center;margin:1rem 0}}
        .inventory-search{{flex:1 1 260px;min-width:0;background:var(--bg-card);border:1px solid var(--border);border-radius:8px;color:var(--text-primary);padding:.75rem .9rem}}
        .filter-chip{{border:1px solid var(--border);background:var(--bg-card);color:var(--text-secondary);border-radius:8px;padding:.62rem .78rem;cursor:pointer}}
        .filter-chip.active{{border-color:var(--gold);color:var(--gold)}}
        .inventory-table-wrap{{overflow:auto;border:1px solid var(--border);border-radius:8px;background:var(--bg-card)}}
        .inventory-table{{width:100%;border-collapse:collapse;min-width:840px}}
        .inventory-table th,.inventory-table td{{border-bottom:1px solid var(--border);padding:.75rem;text-align:left;vertical-align:top}}
        .inventory-table th{{font-size:.74rem;text-transform:uppercase;letter-spacing:.08em;color:var(--text-muted);background:rgba(255,255,255,.03)}}
        .inventory-table td{{font-size:.86rem;color:var(--text-secondary)}}
        .inventory-table td:first-child a{{display:block;color:var(--gold);font-weight:700}}
        .inventory-table td:first-child span{{display:block;margin-top:.25rem;max-width:680px;line-height:1.45}}
        .inventory-counts{{display:grid;grid-template-columns:repeat(auto-fit,minmax(145px,1fr));gap:.75rem;margin-top:1rem}}
        .inventory-counts div{{border:1px solid var(--border);border-radius:8px;padding:.85rem;background:var(--bg-card)}}
        .inventory-counts strong{{display:block;color:#fff;font-size:1.35rem}}
        .note{{color:var(--text-muted);font-size:.84rem}}
        .inventory-select{{padding:.62rem .78rem;border-radius:8px;border:1px solid var(--border);background:var(--bg-card);color:var(--text-secondary)}}
    </style>
</head>
<body>
    <a href="#main" class="skip-link">Skip to main content</a>
    <nav role="navigation" aria-label="Main navigation">
        <a href="index.html" class="nav-logo">Daniel Ari Friedman</a>
        <button class="menu-btn" onclick="document.querySelector('.nav-links').classList.toggle('open')" aria-label="Toggle menu">☰</button>
        <div class="nav-links"><a href="publications.html">Publications</a><a href="software.html">Software</a><a href="search.html">Search</a><a href="catalog.html">Catalog</a></div>
    </nav>
    <header class="page-hero">
        <h1>Repository Inventory</h1>
        <p class="sub">Full generated inventory of public GitHub repositories for docxology and the Active Inference Institute.</p>
    </header>
    <main id="main" class="main">
        <section class="section">
        <div class="inventory-counts">
                <div><strong>{counts['total']}</strong>Total public repos</div>
                <div><strong>{counts['docxology']}</strong>docxology</div>
                <div><strong>{counts['ActiveInferenceInstitute']}</strong>AII</div>
                <div><strong>{counts['curated']}</strong>Curated in software catalog</div>
                <div><strong>{counts['public']}</strong>Public visibility</div>
                <div><strong>{counts['private']}</strong>Private visibility</div>
                <div><strong>{counts['forks']}</strong>Forks</div>
                <div><strong>{counts['archived']}</strong>Archived</div>
                <div><strong>{counts['recently_updated']}</strong>Updated in 90 days</div>
            </div>
            {warning}
            <div class="inventory-controls">
                <input id="inventorySearch" class="inventory-search" type="search" placeholder="Search repositories, languages, descriptions, topics..." autocomplete="off">
                <select id="inventoryLanguage" class="inventory-select" aria-label="Filter by language">
                    <option value="">All languages</option>
{language_options}
                </select>
                <button class="filter-chip active" data-filter="all">All</button>
                <button class="filter-chip" data-filter="docxology">docxology</button>
                <button class="filter-chip" data-filter="aii">AII</button>
                <button class="filter-chip" data-filter="curated">Curated</button>
                <button class="filter-chip" data-filter="uncataloged">Uncataloged</button>
                <button class="filter-chip" data-filter="forks">Forks</button>
                <button class="filter-chip" data-filter="archived">Archived</button>
                <button class="filter-chip" data-filter="recent">Recent</button>
                <button class="filter-chip" data-filter="public">Public</button>
                <button class="filter-chip" data-filter="private">Private</button>
            </div>
            <p id="inventoryResultCount" class="note"></p>
            <div class="inventory-table-wrap">
                <table class="inventory-table">
                    <thead><tr><th>Repository</th><th>Language</th><th>Stars</th><th>Forks</th><th>Updated</th><th>Flags</th></tr></thead>
                    <tbody id="inventoryRows">
{rows}
                    </tbody>
                </table>
            </div>
            <p class="note">Generated at {h(payload['generated_at'])}. Curated flags are derived from <a href="software.html">software.html</a> / <a href="pages/SOFTWARE.md">pages/SOFTWARE.md</a>.</p>
        </section>
    </main>
    <footer role="contentinfo">
        <div class="footer-rule" aria-hidden="true"></div>
        <p>Daniel Ari Friedman, PhD · <a href="data/github-repositories.json">github-repositories.json</a></p>
    </footer>
    <script>
        const rows = Array.from(document.querySelectorAll('#inventoryRows tr'));
        const input = document.getElementById('inventorySearch');
        const languageFilter = document.getElementById('inventoryLanguage');
        const count = document.getElementById('inventoryResultCount');
        let filter = 'all';
        function matchesFilter(row) {{
            if (filter === 'docxology') return row.dataset.owner === 'docxology';
            if (filter === 'aii') return row.dataset.owner === 'ActiveInferenceInstitute';
            if (filter === 'curated') return row.dataset.curated === 'true';
            if (filter === 'uncataloged') return row.dataset.curated === 'false';
            if (filter === 'forks') return row.dataset.fork === 'true';
            if (filter === 'archived') return row.dataset.archived === 'true';
            if (filter === 'public' || filter === 'private') return row.dataset.visibility === filter;
            if (filter === 'recent') return row.dataset.recent === 'true';
            return true;
        }}
        function applyFilters() {{
            const q = input.value.trim().toLowerCase();
            const lang = languageFilter.value.toLowerCase();
            let visible = 0;
            rows.forEach(row => {{
                const matchesLanguage = !lang || row.dataset.language === lang;
                const ok = matchesFilter(row) && matchesLanguage && (!q || row.dataset.search.includes(q));
                row.style.display = ok ? '' : 'none';
                if (ok) visible += 1;
            }});
            count.textContent = `${{visible}} repositories shown`;
        }}
        document.querySelectorAll('.filter-chip').forEach(button => {{
            button.addEventListener('click', () => {{
                document.querySelectorAll('.filter-chip').forEach(item => item.classList.remove('active'));
                button.classList.add('active');
                filter = button.dataset.filter;
                applyFilters();
            }});
        }});
        input.addEventListener('input', applyFilters);
        languageFilter.addEventListener('change', applyFilters);
        applyFilters();
    </script>
</body>
</html>
"""


def write_outputs(payload: dict[str, Any]) -> None:
    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    HTML_OUT.write_text(render_html(payload), encoding="utf-8")


def check_outputs() -> None:
    if not JSON_OUT.exists() or not HTML_OUT.exists():
        raise SystemExit("Missing GitHub inventory outputs")
    payload = json.loads(JSON_OUT.read_text(encoding="utf-8"))
    if not payload.get("repositories"):
        raise SystemExit("GitHub inventory has no repositories")
    counts = payload.get("counts", {})
    if counts.get("docxology", 0) <= 0 or counts.get("ActiveInferenceInstitute", 0) <= 0:
        raise SystemExit("GitHub inventory is missing one of the required owners")
    if BASELINE_PATH.exists():
        baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
        base_counts = baseline.get("counts", {})
        for key in ["total", "docxology", "ActiveInferenceInstitute", "forks", "archived"]:
            delta = counts.get(key, 0) - base_counts.get(key, 0)
            if delta:
                print(f"warning: github inventory count delta for {key}: {base_counts.get(key, 0)} -> {counts.get(key, 0)} ({delta:+})")
    counts = payload.get("counts", {})
    html_text = HTML_OUT.read_text(encoding="utf-8")
    if "Repository Inventory" not in html_text or "github-repositories.json" not in html_text:
        raise SystemExit("repositories.html missing expected inventory markers")
    for key in ["total", "docxology", "ActiveInferenceInstitute", "curated", "forks", "archived"]:
        if f"<strong>{counts.get(key)}</strong>" not in html_text:
            raise SystemExit(f"repositories.html rendered count is stale for {key}")
    print("checked GitHub repository inventory")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate cached inventory outputs")
    args = parser.parse_args()
    if args.check:
        check_outputs()
        return
    payload = build_payload()
    write_outputs(payload)
    counts = payload["counts"]
    print(
        "wrote GitHub inventory: "
        f"{counts['total']} repos ({counts['docxology']} docxology, {counts['ActiveInferenceInstitute']} AII)"
    )


if __name__ == "__main__":
    main()
