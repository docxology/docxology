"""Tests for high-authority pillar pages and domain page builders."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ORCHESTRATORS = REPO_ROOT / "code" / "orchestrators"
sys.path.insert(0, str(ORCHESTRATORS))

import generate_pillar_pages  # noqa: E402
from generated_outputs import stale_output_paths, write_output_texts  # noqa: E402

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
