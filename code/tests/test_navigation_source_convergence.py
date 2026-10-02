"""Authoritative catalog templates must agree with the shared head normalizer."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

from docxology_tools.site_nav import NAV_TOGGLE_SCRIPT_TAG  # noqa: E402
import deploy_seo_security as normalizer  # noqa: E402
import sync_publications_html as publications  # noqa: E402
import sync_software_html as software  # noqa: E402


@pytest.mark.parametrize("renderer, path", [
    (publications, publications.PUBLICATIONS_HTML),
    (software, software.SOFTWARE_HTML),
])
def test_catalog_source_render_preserves_early_navigation_through_normalization(renderer, path):
    rendered = renderer.render_outputs()[path]
    head = rendered.split("</head>", 1)[0]
    assert head.count(NAV_TOGGLE_SCRIPT_TAG) == 1
    assert rendered.count("/js/nav-toggle.js") == 1
    assert normalizer.add_early_navigation_if_needed(rendered) == rendered
