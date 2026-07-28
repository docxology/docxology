from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

import regenerate_docs as rd  # noqa: E402


def test_truncate_display_text_avoids_mid_token_urls():
    text = "Intro " + ("word " * 30) + "https://www.youtube.com/watch?v=abcdef"

    shortened = rd.truncate_display_text(text, limit=150)

    assert "https://www.youtube.co..." not in shortened
    assert shortened.endswith("...")


def test_generate_readme_normalizes_markdown_doi_link():
    meta = {
        "name": "Example Paper",
        "authors": "Daniel Ari Friedman",
        "abstract": (
            "<p>Example &mdash; abstract.</p>\n\n"
            "---\nAssociated artifacts\n"
            "DOI: https://doi.org/10.5281/zenodo.20396328"
        ),
        "doi": "10.5281/zenodo.20396328",
        "doi_url": "https://doi.org/10.5281/zenodo.20396328",
        "github_repo": "docxology/entofile",
        "github_release_url": "https://github.com/docxology/entofile/releases/tag/v0.4",
        "release_tag": "v0.4",
        "zenodo_record": "https://zenodo.org/records/20396328",
        "files": [
            {
                "name": "Enhanced NSF Postdoctoral Reporting via Synthetic Intelligence Language Processing (1).pdf",
                "download_url": "https://zenodo.org/api/records/10160657/files/Enhanced%20NSF%20Postdoctoral%20Reporting%20via%20Synthetic%20Intelligence%20Language%20Processing%20(1).pdf/content",
            }
        ],
        "keywords": ["example"],
    }
    bib_entry = {
        "venue": "Zenodo",
        "link": "[10.5281/zenodo.20396328](https://doi.org/10.5281/zenodo.20396328)",
        "domain": "💻",
    }

    readme = rd.generate_readme("2026_Example", meta, bib_entry)

    assert "> Example \u2014 abstract." in readme
    assert "Associated artifacts" not in readme
    assert "<p>" not in readme
    assert "[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20396328-blue)](https://doi.org/10.5281/zenodo.20396328)" in readme
    assert "- DOI: [10.5281/zenodo.20396328](https://doi.org/10.5281/zenodo.20396328)" in readme
    assert "- GitHub repository: [docxology/entofile](https://github.com/docxology/entofile)" in readme
    assert "- GitHub release: [v0.4](https://github.com/docxology/entofile/releases/tag/v0.4)" in readme
    assert "- Zenodo record: [https://zenodo.org/records/20396328](https://zenodo.org/records/20396328)" in readme
    assert (
        "[Enhanced NSF Postdoctoral Reporting via Synthetic Intelligence Language Processing (1).pdf]"
        "(https://zenodo.org/api/records/10160657/files/"
        "Enhanced%20NSF%20Postdoctoral%20Reporting%20via%20Synthetic%20Intelligence%20Language%20Processing%20%281%29.pdf/content)"
    ) in readme
    assert "https:%2F%2F" not in readme
    assert "]([" not in readme
    assert (
        "> Daniel Ari Friedman (2026). *Example Paper*. Zenodo. "
        "DOI: 10.5281/zenodo.20396328. URL: https://doi.org/10.5281/zenodo.20396328."
    ) in readme
