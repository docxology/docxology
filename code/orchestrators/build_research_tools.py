#!/usr/bin/env python3
"""Generate research exploration pages and their bounded catalog projections."""

from __future__ import annotations

import argparse
from dataclasses import fields
import html
import json
from pathlib import Path
import sys

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

from docxology_tools.generated_outputs import stale_output_paths, write_output_texts  # noqa: E402
from docxology_tools.research_connections import graph_catalog, valid_key  # noqa: E402
from docxology_tools.site_nav import (  # noqa: E402
    INTERACTIVE_SCRIPTS,
    MENU_ESC_SCRIPT,
    render_nav,
    render_pillar_head,
    breadcrumb_list_jsonld,
)
from docxology_tools.build_stamp import footer_build_stamp_html  # noqa: E402
from build_work_pages import load_bibtex_entries, source_repository_url  # noqa: E402
from docxology_tools.paper_artifacts import PaperResources  # noqa: E402
from export_bibliography import source_paths  # noqa: E402
from export_bibliography import Work, csl_item, ris_record  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
ROUTES = (
    ("collections", "Reading lists"),
    ("trails", "Research trails"),
    ("research-map", "Research map"),
    ("lab", "Probability laboratory"),
)


def h(value: object) -> str:
    return html.escape(str(value), quote=True)


def page(
    slug: str, title: str, description: str, content: str, script: str = ""
) -> str:
    head = render_pillar_head(
        title=title,
        description=description,
        canonical_path=slug + ".html",
        og_image="og-index.jpg",
        style="",
        jsonld={
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "WebPage",
                    "name": title,
                    "url": "https://danielarifriedman.com/" + slug + ".html",
                },
                breadcrumb_list_jsonld([("Home", ""), (title, slug + ".html")]),
            ],
        },
    )
    head = head.replace(
        "</head>", '<link rel="stylesheet" href="/css/research-tools.css?v=1">\n</head>'
    )
    tools_nav = " · ".join(
        f'<a href="/{key}.html"'
        + (' aria-current="page"' if key == slug else "")
        + f">{label}</a>"
        for key, label in ROUTES
    )
    return (
        head
        + f'''<body class="research-tools-page" data-research-tool="{slug}">
<a class="skip-link" href="#main">Skip to content</a>
{render_nav(active=slug)}
<main id="main">
<header class="page-hero"><p class="tool-kicker">RESEARCH DESK</p><h1>{h(title)}</h1><p class="sub">{h(description)}</p><p class="tool-links">{tools_nav}</p></header>
<div class="research-desk">{content}</div>
</main><footer><p><a href="/publications.html">Bibliography</a> · <a href="/exports.html">Citation exports</a> · <a href="/evidence.html">Evidence and source limits</a></p>{footer_build_stamp_html()}</footer>
{INTERACTIVE_SCRIPTS}
{MENU_ESC_SCRIPT}
{f'<script src="/js/{script}?v=1" defer></script>' if script else ""}
</body></html>\n'''
    )


def collection_content() -> str:
    return """<p>Build an ordered selection of public works. Lists are stored only in this browser. Shared links include the list title and citation keys; they do not synchronize edits.</p>
<noscript><p>Reading-list editing needs JavaScript. Browse <a href="/works/">all works</a> or download the complete <a href="/bibliography.bib">BibTeX</a>, <a href="/bibliography.ris">RIS</a> or <a href="/bibliography.csl.json">CSL JSON</a> bibliography.</p></noscript>
<fieldset id="collection-app" class="tool-app" disabled aria-busy="true"><legend>Reading-list editor</legend>
<div class="tool-toolbar"><label for="collection-select">Saved list<select id="collection-select"></select></label><button type="button" id="collection-new">New list</button><button type="button" id="collection-save-shared" hidden>Save shared list</button><button type="button" id="collection-delete">Delete current list</button></div>
<label for="collection-title">List title<input id="collection-title" maxlength="100" value="Reading list"></label>
<div class="tool-panel"><h2>Add a work</h2><label for="collection-search">Find by title, author, year or citation key<input id="collection-search" type="search" maxlength="300"></label><label for="collection-candidate">Catalog matches<select id="collection-candidate"></select></label><button type="button" id="collection-add">Add selected work</button></div>
<h2>Your reading order</h2><ol id="collection-items" class="reading-order"><li>No papers yet. Add a catalog work above.</li></ol>
<div class="tool-toolbar"><button type="button" data-collection-export="bib">Download BibTeX</button><button type="button" data-collection-export="ris">Download RIS</button><button type="button" data-collection-export="csl">Download CSL JSON</button><button type="button" data-collection-export="md">Download Markdown</button><button type="button" id="collection-share">Create share link</button></div>
<label for="collection-share-url" id="collection-share-label" hidden>Share this preview URL<input id="collection-share-url" readonly></label>
<details><summary>Import or back up lists</summary><p>JSON backups retain list names and reading order. Import previews a new list and does not overwrite saved lists.</p><button type="button" id="collection-backup">Download JSON backup</button><button type="button" id="collection-original" hidden>Download original stored data</button><label for="collection-import">Import a JSON backup<input type="file" id="collection-import" accept="application/json,.json"></label><label for="collection-import-choice">Imported list to preview<select id="collection-import-choice"></select></label><button type="button" id="collection-preview-import">Preview imported list</button></details>
</fieldset><p id="collection-status" role="status" aria-live="polite">Loading the citation catalog…</p><button type="button" id="collection-retry" hidden>Retry catalog</button>"""


def map_content(works: list[dict]) -> str:
    domains = sorted({w["domain_name"] for w in works})
    fallback = "".join(
        f'<li><a href="/publications.html?domain={h(next(w["domain"] for w in works if w["domain_name"] == name))}">{h(name)}</a></li>'
        for name in domains
    )
    return f"""<p>Explore recorded authorship, catalog domains and associated software. These are metadata relationships, not citation links or causal claims. Author nodes group exact normalized names; homonyms may be grouped and spelling variants remain separate.</p>
<details><summary>Browse domains without the interactive map</summary><ul>{fallback}</ul></details>
<fieldset id="map-app" class="tool-app" disabled aria-busy="true"><legend>Research-map explorer</legend><div class="tool-toolbar"><label for="map-search">Find a node<input type="search" id="map-search" maxlength="300"></label><label for="map-kind">Node type<select id="map-kind"><option value="all">All types</option><option value="work">Works</option><option value="person">People</option><option value="software">Software</option><option value="domain">Domains</option></select></label><label for="map-node">Matching nodes<select id="map-node"></select></label></div>
<h2 id="map-title">Connections</h2><p id="map-summary"></p><svg id="research-map-svg" viewBox="0 0 800 500" role="img" aria-label="Selected node and up to twelve adjacent nodes; the complete connections are listed below"></svg>
<p>The diagram shows up to twelve neighbors. The list below reaches every recorded connection.</p><ul id="map-connections" class="connection-list"></ul><button type="button" id="map-more" hidden>Show more connections</button><p><a href="/data/research-map.json" download>Download the complete graph JSON</a></p></fieldset>
<p id="map-status" role="status">Loading the research map…</p><button type="button" id="map-retry" hidden>Retry map</button>"""


def lab_content() -> str:
    return """<p>Two small, fully specified teaching models. Change assumptions, inspect the numbers, and export every step. They do not reproduce or validate the linked research. <a href="/js/probability-lab.js" download>Download the model implementations (JavaScript)</a>.</p>
<section id="bayes" class="tool-panel"><p class="tool-kicker">01 / BELIEF UPDATING</p><h2>A binary Bayesian update</h2><p>H is a hypothesis and E is an observation. The two hypotheses H and not-H are exhaustive. Repeated observations are assumed conditionally independent given the hypothesis, with fixed likelihoods.</p><p><code>P(H|E) = P(H) P(E|H) / [P(H) P(E|H) + (1 − P(H)) P(E|not-H)]</code></p><p>Worked example: a prior of 0.20 and likelihoods 0.80 and 0.20 give a posterior of 0.50 after E. A subsequent not-E returns it to 0.20.</p>
<div class="tool-grid"><label for="bayes-prior">Prior P(H), percent<input id="bayes-prior" type="range" min="0" max="100" value="20"><output for="bayes-prior" id="bayes-prior-value">20</output></label><label for="bayes-yes">Likelihood P(E|H), percent<input id="bayes-yes" type="range" min="0" max="100" value="80"><output for="bayes-yes" id="bayes-yes-value">80</output></label><label for="bayes-no">Likelihood P(E|not-H), percent<input id="bayes-no" type="range" min="0" max="100" value="20"><output for="bayes-no" id="bayes-no-value">20</output></label></div>
<div class="tool-toolbar"><button type="button" id="bayes-positive">Observe E</button><button type="button" id="bayes-negative">Observe not-E</button><button type="button" id="bayes-reset">Reset observations</button><button type="button" id="bayes-export">Download Bayesian CSV</button></div><p id="bayes-result" role="status">Enable JavaScript to update the worked example.</p><svg id="bayes-chart" viewBox="0 0 800 280" role="img" aria-label="Posterior probability by observation; exact values appear in the table"></svg><details><summary>Numerical history</summary><table><caption>Binary update history</caption><thead><tr><th scope="col">Step</th><th scope="col">Observation</th><th scope="col">P(H)</th></tr></thead><tbody id="bayes-history"></tbody></table></details><p>Changing any assumption resets the observations. Impossible evidence is reported without changing the state. At most 100 observations per run.</p><p><a href="https://ocw.mit.edu/courses/6-041-probabilistic-systems-analysis-and-applied-probability-fall-2010/pages/lecture-notes/">MIT probability course: conditional probability and inference</a> · <a href="/active-inference.html">Related Active Inference reading</a></p></section>
<section id="urn" class="tool-panel"><p class="tool-kicker">02 / REINFORCEMENT</p><h2>A reinforced urn</h2><p>Draw one token with probability proportional to its color's current count. Replace it and add r extra tokens of that color. With r = 0 the composition stays fixed. Every run uses the displayed 32-bit seed; identical inputs reproduce identical draws.</p>
<div class="tool-grid"><label for="urn-amber">Initial amber tokens<input id="urn-amber" type="number" min="1" max="20" value="1"></label><label for="urn-blue">Initial blue tokens<input id="urn-blue" type="number" min="1" max="20" value="1"></label><label for="urn-reinforcement">Extra tokens r<input id="urn-reinforcement" type="number" min="0" max="5" value="1"></label><label for="urn-draws">Draws<input id="urn-draws" type="number" min="1" max="200" value="100"></label><label for="urn-seed">Seed (0–4294967295)<input id="urn-seed" type="number" min="0" max="4294967295" value="42"></label></div><div class="tool-toolbar"><button type="button" id="urn-run">Run urn</button><button type="button" id="urn-export">Download urn CSV</button></div><p id="urn-result" role="status">With one token of each color, the first draw has amber probability 0.50.</p><svg id="urn-chart" viewBox="0 0 800 280" role="img" aria-label="Amber fraction of the urn after each draw; exact values appear in the table"></svg><details><summary>Every draw and token count</summary><table><caption>Reinforced urn history</caption><thead><tr><th scope="col">Draw</th><th scope="col">Color</th><th scope="col">Amber</th><th scope="col">Blue</th><th scope="col">Amber fraction</th></tr></thead><tbody id="urn-history"></tbody></table></details><p>This stochastic urn illustrates reinforcement. It has no spatial interactions, physiology, pheromone dynamics or fitted biological parameters and is not an ant-colony model.</p><p><a href="https://djalil.chafai.net/blog/2015/11/30/back-to-basics-polya-urns/">Mathematical definition and analysis by Djalil Chafaï</a> · <a href="/computational-entomology.html">Related models and biological evidence</a></p></section>
<noscript><p>The definitions and worked examples above remain readable without JavaScript. Interactive controls require JavaScript.</p></noscript>"""


def resolve_trails(
    source: dict, works: list[dict], videos: list[dict], software: list[dict]
) -> list[dict]:
    if source.get("schema_version") != 1 or not isinstance(source.get("trails"), list):
        raise ValueError("Invalid research trail source schema")
    indexes = {
        "work": {
            w["citation_key"]: {
                "title": w["title"],
                "url": "/works/" + w["citation_key"] + ".html",
            }
            for w in works
        },
        "video": {
            v["page_url"]: {"title": v["title"], "url": v["page_url"]} for v in videos
        },
        "software": {r["url"]: {"title": r["name"], "url": r["url"]} for r in software},
        "demo": {
            "bayes": {"title": "Binary Bayesian update", "url": "/lab.html#bayes"},
            "urn": {"title": "Reinforced urn", "url": "/lab.html#urn"},
        },
    }
    result, ids = [], set()
    for trail in source["trails"]:
        if not valid_key(trail["id"]) or trail["id"] in ids:
            raise ValueError("Invalid or duplicate trail ID")
        ids.add(trail["id"])
        if not all(
            isinstance(trail.get(field), str) and trail[field].strip()
            for field in ("title", "summary", "prerequisites")
        ) or not trail.get("steps"):
            raise ValueError("Trail requires title, summary, prerequisites and steps")
        steps = []
        for step in trail["steps"]:
            item = indexes.get(step["kind"], {}).get(step["ref"])
            if (
                not item
                or type(step["minutes"]) is not int
                or not 1 <= step["minutes"] <= 480
                or not isinstance(step["goal"], str)
                or not step["goal"].strip()
            ):
                raise ValueError(
                    "Unknown trail resource or invalid learning goal/time: " + str(step)
                )
            steps.append({**step, **item})
        result.append({**trail, "steps": steps})
    return result


def trail_content(trails: list[dict]) -> str:
    out = [
        "<p>Curated routes through publications, recorded discussions, software and teaching models. Times are editorial estimates for a first pass, not measured completion times. Follow the original sources for research claims.</p>"
    ]
    for trail in trails:
        out.append(
            f'<section class="tool-panel" id="{h(trail["id"])}"><p class="tool-kicker">{sum(s["minutes"] for s in trail["steps"])} MIN / FIRST PASS</p><h2>{h(trail["title"])}</h2><p>{h(trail["summary"])}</p><p><strong>Prerequisites:</strong> {h(trail["prerequisites"])}</p><ol class="trail-steps">'
        )
        for step in trail["steps"]:
            out.append(
                f'<li><p class="tool-kicker">{h(step["kind"])} / {step["minutes"]} min</p><h3><a href="{h(step["url"])}">{h(step["title"])}</a></h3><p>{h(step["goal"])}</p></li>'
            )
        keys = [s["ref"] for s in trail["steps"] if s["kind"] == "work"]
        from urllib.parse import urlencode

        share = urlencode({"v": "1", "title": trail["title"], "works": ",".join(keys)})
        out.append(
            f'</ol><p><a class="btn btn-outline" href="/collections.html#{h(share)}">Preview these papers as a reading list</a></p></section>'
        )
    return "".join(out)


def render_outputs() -> dict[Path, str]:
    works = json.loads((REPO_ROOT / "data/works.json").read_text())["works"]
    videos = json.loads((REPO_ROOT / "data/videos.json").read_text())["videos"]
    software = json.loads((REPO_ROOT / "data/software.json").read_text())[
        "repositories"
    ]
    source = json.loads((REPO_ROOT / "data/research-trails-source.json").read_text())
    trails = resolve_trails(source, works, videos, software)
    citations = load_bibtex_entries()
    allowed = {field.name for field in fields(Work)}
    records, repositories = [], {}
    visible = source_paths(REPO_ROOT)
    for work in works:
        if not valid_key(work["citation_key"]) or work["citation_key"] not in citations:
            raise ValueError("Missing or invalid citation: " + work["citation_key"])
        parsed = Work(**{key: value for key, value in work.items() if key in allowed})
        role = work.get("contributor_role", "author")
        records.append(
            {
                "key": work["citation_key"],
                "title": work["title"],
                "authors": work.get("authors", []),
                "year": work["year"],
                "url": "/works/" + work["citation_key"] + ".html",
                "bib": citations[work["citation_key"]],
                "ris": ris_record(parsed, contributor_role=role),
                "csl": csl_item(parsed, contributor_role=role),
            }
        )
        resources = PaperResources.load(REPO_ROOT, work.get("docs_path", ""), visible)
        repositories[work["citation_key"]] = source_repository_url(
            work.get("docs_path", ""), resources
        )
    pages = {
        "collections": (
            "Reading lists",
            "Collect papers, arrange a reading order, share a selection, and export its citations.",
            collection_content(),
            "collections.js",
        ),
        "trails": (
            "Research trails",
            "Follow curated routes from an introductory question to papers, discussions and code.",
            trail_content(trails),
            "",
        ),
        "research-map": (
            "Research map",
            "Explore the people, domains and software connected to the publication catalog.",
            map_content(works),
            "research-map.js",
        ),
        "lab": (
            "Probability laboratory",
            "Experiment with Bayesian updating and reinforcement using reproducible teaching models.",
            lab_content(),
            "probability-lab.js",
        ),
    }
    outputs = {
        REPO_ROOT / (slug + ".html"): page(slug, *args) for slug, args in pages.items()
    }
    for name, payload in (
        ("collection-catalog", {"schema_version": 1, "works": records}),
        ("research-map", graph_catalog(works, repositories)),
        ("research-trails", {"schema_version": 1, "trails": trails}),
    ):
        outputs[REPO_ROOT / "data" / (name + ".json")] = (
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
        )
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = render_outputs()
    if args.check:
        stale = stale_output_paths(outputs, repo_root=REPO_ROOT)
        if stale:
            raise SystemExit(
                "Stale research tools: "
                + ", ".join(str(p.relative_to(REPO_ROOT)) for p in stale)
            )
    else:
        write_output_texts(outputs, repo_root=REPO_ROOT)
    print(
        f"{'checked' if args.check else 'wrote'} {len(outputs)} research exploration outputs"
    )


if __name__ == "__main__":
    main()
