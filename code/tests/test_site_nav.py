"""Tests for shared site navigation HTML."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from site_nav import render_nav, render_nav_domain


def test_render_nav_marks_active_and_depth():
    html = render_nav(active="works", depth=1)
    assert 'href="../publications.html"' in html
    assert 'class="active"' in html
    assert "Works" in html


def test_render_nav_domain_marks_domains_active():
    html = render_nav_domain(active="domains")
    assert 'href="domains.html" class="active"' in html
    assert "Software" in html
