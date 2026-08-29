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
    # build_image_sitemap.py removed (NEW-2, 2026-08-28): artwork index remains.
    assert "build_image_sitemap.py" not in names
    docs_index = names.index("regenerate_docs.py")
    assert docs_index < names.index("export_bibliography.py", docs_index + 1) < names.index("sync_publications_html.py", docs_index + 1) < names.index("build_work_pages.py")
    assert names.index("generate_redirect_stubs.py") < names.index("deploy_seo_security.py")
    assert names.index("build_pages_artifact.py") < names.index("build_agent_index.py")
    assert names.index("build_pages_artifact.py") < generated_manifest_indices[0] < names.index("build_agent_index.py")
    assert names.index("build_agent_index.py") < names.index("build_release_integrity.py") < generated_manifest_indices[1]
    assert names[-1] == "build_generated_manifest.py"
    site_facts_indices = [i for i, name in enumerate(names) if name == "sync_site_facts.py"]
    accessibility_indices = [i for i, name in enumerate(names) if name == "accessibility_audit.py"]
    assert len(site_facts_indices) >= 2
    assert site_facts_indices[-1] > accessibility_indices[-1]
