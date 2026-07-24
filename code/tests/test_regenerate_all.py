"""Regression tests for the ordered local regeneration pipeline."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

import regenerate_all  # noqa: E402


def test_integrity_tail_resolves_generated_manifest_before_agent_index():
    names = [name for name, _args in regenerate_all.CHAIN]
    generated_manifest_indices = [i for i, name in enumerate(names) if name == "build_generated_manifest.py"]

    assert names.count("build_agent_index.py") == 1
    assert len(generated_manifest_indices) == 2
    assert names.index("build_artwork_index.py") < names.index("build_image_sitemap.py")
    assert names.index("build_pages_artifact.py") < names.index("build_agent_index.py")
    assert names.index("build_pages_artifact.py") < generated_manifest_indices[0] < names.index("build_agent_index.py")
    assert names.index("build_agent_index.py") < names.index("build_release_integrity.py") < generated_manifest_indices[1]
    assert names[-1] == "build_generated_manifest.py"
