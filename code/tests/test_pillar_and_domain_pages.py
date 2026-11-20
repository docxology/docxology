"""Tests for high-authority pillar pages and domain page builders."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

REPO_ROOT = Path(__file__).resolve().parents[2]
ORCHESTRATORS = REPO_ROOT / "code" / "orchestrators"

import docxology_tools  # noqa: E402,F401
import build_domain_pages  # noqa: E402
import generate_pillar_pages  # noqa: E402
from docxology_tools.generated_outputs import stale_output_paths, write_output_texts  # noqa: E402

PILLAR_FILES = [
    "cognitive-security.html",
    "computational-entomology.html",
    "insect-cognition.html",
    "active-inference.html",
    "neurosymbolic-ai.html",
]

DOMAIN_FILES = [
    "domain-active-inference.html",
    "domain-aii-ecosystem.html",
    "domain-art-synergetics.html",
    "domain-biomedicine.html",
    "domain-cognitive-security.html",
    "domain-computational.html",
    "domain-entomology.html",
    "domain-presentations-media.html",
]


def test_generate_pillar_pages_check_runs_cleanly():
    res = subprocess.run(
        [sys.executable, str(ORCHESTRATORS / "generate_pillar_pages.py"), "--check"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    assert "checked 5 shared-rendered pillar pages" in res.stdout
    for name in PILLAR_FILES:
        path = REPO_ROOT / name
        assert path.is_file(), f"Expected pillar page {name} to exist"
        content = path.read_text(encoding="utf-8")
        assert "<!DOCTYPE html>" in content
        assert "schema.org" in content
        assert "FAQPage" in content
        assert "BreadcrumbList" in content


def test_pillar_check_detects_stale_output_without_writing(tmp_path):
    outputs = generate_pillar_pages.render_outputs(output_root=tmp_path)
    write_output_texts(outputs, repo_root=tmp_path)
    assert stale_output_paths(outputs, repo_root=tmp_path) == ()
    stale = next(iter(outputs))
    stale.write_text("stale", encoding="utf-8")
    assert stale_output_paths(outputs, repo_root=tmp_path) == (stale,)


def test_build_domain_pages_check_runs_cleanly_without_rewriting_the_repository():
    res = subprocess.run(
        [sys.executable, str(ORCHESTRATORS / "build_domain_pages.py"), "--check"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    assert "checked 10 domain pages" in res.stdout
    for name in DOMAIN_FILES:
        path = REPO_ROOT / name
        assert path.is_file(), f"Expected domain page {name} to exist"
        content = path.read_text(encoding="utf-8")
        assert "<!DOCTYPE html>" in content
        assert "BreadcrumbList" in content


def test_domain_pages_and_markdown_follow_the_same_curated_order():
    works = build_domain_pages.load_json("data/works.json")["works"]
    outputs = build_domain_pages.render_outputs()
    markdown = outputs[REPO_ROOT / "pages" / "DOMAINS.md"]
    for config in build_domain_pages.DOMAINS:
        domain_works = [work for work in works if work["domain"] in config.domains]
        selected = build_domain_pages.select_featured_works(config, domain_works)
        assert tuple(work["num"] for work in selected) == config.featured_work_numbers
        html = outputs[REPO_ROOT / f"domain-{config.slug}.html"]
        html_section = html.split("<h2>Selected Works</h2>", 1)[1].split("</section>", 1)[0]
        html_positions = [html_section.index(f'works/{work["citation_key"]}.html') for work in selected]
        assert html_positions == sorted(html_positions)
        md_section = markdown.split(f"## {config.emoji} [{config.title}]", 1)[1]
        md_section = md_section.split("**Selected works**", 1)[1].split("**Selected repositories**", 1)[0]
        md_positions = [
            md_section.index(f"- {work['year']} — [{work['title']}]({work['url']})")
            for work in selected[:6]
        ]
        assert md_positions == sorted(md_positions)
