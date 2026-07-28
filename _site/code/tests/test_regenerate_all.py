"""Regression tests for the ordered local regeneration pipeline."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

import regenerate_all  # noqa: E402


def test_integrity_tail_builds_agent_index_after_pages_projection():
    names = [name for name, _args in regenerate_all.CHAIN]

    assert names.count("build_agent_index.py") == 1
    assert names.index("build_artwork_index.py") < names.index("build_image_sitemap.py")
    assert names.index("build_pages_artifact.py") < names.index("build_agent_index.py")
    assert names.index("build_agent_index.py") < names.index("build_generated_manifest.py")
    assert names[-1] == "build_generated_manifest.py"
