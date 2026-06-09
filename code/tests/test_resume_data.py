"""Tests for structured resume/CV data and generated artifacts."""

from __future__ import annotations

import re
import sys
from io import BytesIO
from pathlib import Path

from pypdf import PdfReader

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "code" / "src"
ORCH_DIR = REPO_ROOT / "code" / "orchestrators"
sys.path.insert(0, str(SRC_DIR))
sys.path.insert(0, str(ORCH_DIR))

from build_resume import VERIFY_URL, _provenance_base, _sha256_bytes, render_pdf, render_verify_html  # noqa: E402
from resume_data import (  # noqa: E402
    CODA_GLYPH_RE,
    build_resume_payload,
    json_dumps,
    load_resume_inputs,
    render_text,
)


FIXED_TIME = "2026-05-27T00:00:00Z"
SOURCE_SECTIONS = ("education", "experience", "awards", "conferences", "media_outreach", "service", "art_uses")


def test_resume_source_schema_and_required_sections():
    inputs = load_resume_inputs(REPO_ROOT)
    source = inputs["resume/source.json"]
    assert source["contact"]["email"] == [
        "danielarifriedman@gmail.com",
        "daniel@activeinference.institute",
    ]
    assert source["contact"]["keybase"] == "docxology"
    assert source["contact"]["ens"] == "docxology.eth"
    assert len(source["education"]) == 4
    assert len(source["experience"]) >= 16
    assert len(source["conferences"]) >= 13
    assert len(source["media_outreach"]) >= 20
    assert len(source["service"]) >= 20
    assert len(source["art_uses"]) >= 10
    for section in SOURCE_SECTIONS:
        for row in source[section]:
            assert row["links"], f"{section}:{row['id']}"
            assert all(link["label"] and link["url"].startswith(("http://", "https://")) for link in row["links"])


def test_resume_payload_merges_canonical_works_and_software_counts():
    payload = build_resume_payload(FIXED_TIME, REPO_ROOT)
    assert payload["metrics"]["works"] == 164
    assert payload["metrics"]["software_catalogued"] == 88
    assert len(payload["works"]) == 164
    assert len(payload["software"]) == 88
    assert payload["metrics"]["google_scholar"]["citations"] == 777


def test_all_non_full_variants_have_membership():
    payload = build_resume_payload(FIXED_TIME, REPO_ROOT)
    for variant in ["academic", "software-consulting", "teaching-service"]:
        text = render_text(payload, variant)
        assert f"Variant: {variant}" in text
        assert "EDUCATION" in text
        assert "EXPERIENCE" in text
        assert len(text) > 2000


def test_text_outputs_strip_coda_glyphs_and_preserve_doi_lines():
    payload = build_resume_payload(FIXED_TIME, REPO_ROOT)
    text = render_text(payload, "full")
    assert not CODA_GLYPH_RE.search(text)
    assert "10.5281/zenod\no" not in text
    assert "WORKS AND PUBLICATIONS (164)" in text
    assert "SOFTWARE (88)" in text
    doi_lines = [line for line in text.splitlines() if re.search(r"10\.\d{4,9}/", line)]
    assert doi_lines
    assert all(line.startswith("[") or "zenodo:" in line or "DOI" not in line for line in doi_lines)


def test_resume_rendering_is_deterministic_for_fixed_timestamp():
    first = build_resume_payload(FIXED_TIME, REPO_ROOT)
    second = build_resume_payload(FIXED_TIME, REPO_ROOT)
    assert json_dumps(first) == json_dumps(second)
    assert render_text(first, "academic") == render_text(second, "academic")


def test_pdf_generation_is_readable():
    payload = build_resume_payload(FIXED_TIME, REPO_ROOT)
    pdf = render_pdf(payload, "full")
    assert pdf == render_pdf(payload, "full")
    reader = PdfReader(BytesIO(pdf))
    assert len(reader.pages) >= 5
    first_page = reader.pages[0].extract_text()
    assert "Daniel Ari Friedman" in first_page
    assert "PUBLIC STRUCTURED CV" in first_page
    assert "Resume Records" in first_page
    assert "Source-to-Output Flow" in first_page
    assert "manifest sha256" in first_page
    assert "resume/verify.html" in first_page
    full_text = "\n".join(page.extract_text() or "" for page in reader.pages)
    assert VERIFY_URL in full_text
    assert "Current public metrics" in full_text
    assert "Curated Works" in full_text
    assert "Software Rows" in full_text
    assert "Works and Publications" in full_text
    assert "Description and Source Links" in full_text
    source_owned_count = sum(len(payload[section]) for section in SOURCE_SECTIONS)
    assert full_text.count("Source:") >= source_owned_count


def test_pdf_contains_clickable_link_annotations():
    payload = build_resume_payload(FIXED_TIME, REPO_ROOT)
    reader = PdfReader(BytesIO(render_pdf(payload, "full")))
    uris = []
    for page in reader.pages:
        for ref in page.get("/Annots") or []:
            action = ref.get_object().get("/A")
            if action and action.get("/URI"):
                uris.append(action.get("/URI"))

    assert len(uris) > 100
    assert VERIFY_URL in uris
    assert "mailto:danielarifriedman@gmail.com" in uris
    assert "mailto:daniel@activeinference.institute" in uris
    assert "https://github.com/docxology" in uris
    assert "https://doi.org/10.5281/zenodo.17555266" in uris
    assert "http://purl.stanford.edu/pb813wm1484" in uris
    assert "https://www.activeinference.institute/officers" in uris
    assert "https://grantome.com/grant/NSF/DBI-2010290" in uris
    assert "https://doi.org/10.5281/zenodo.17138223" in uris
    assert "https://bathmikec.podbean.com/e/s3e10-the-fep-a-tool-for-understanding-and-modelling-complex-systems/" in uris
    assert "https://www.youtube.com/watch?v=BJ-PAt3cqf4" in uris
    assert "https://www.youtube.com/watch?v=x_VPw1K55BM" in uris
    assert "https://www.isss.org/home/" in uris
    assert "https://www.jove.com/methods-collections/567/field-and-laboratory-methods-for-modern-entomology" in uris
    assert "https://information-professionals.org/" in uris
    assert "https://www.ssbprobe.com/decentraldogma-danielfriedman" in uris
    assert "https://metaverse.sothebys.com/natively-digital/lots/curio-cards-complete-set-1-30-plus-17b" in uris
    assert "https://curio.cards/artist/danielfriedman/" in uris


def test_resume_verify_html_records_hashes_and_artifact_links():
    payload = build_resume_payload(FIXED_TIME, REPO_ROOT)
    json_bytes = json_dumps(payload).encode("utf-8")
    provenance = _provenance_base(payload, json_bytes)
    pdf = render_pdf(payload, "full", provenance)
    provenance = {**provenance, "resume_pdf": {"bytes": len(pdf), "sha256": _sha256_bytes(pdf)}}
    html = render_verify_html(payload, provenance).decode("utf-8")

    assert "Resume Verification" in html
    assert "/resume/resume.pdf" in html
    assert "/data/resume.json" in html
    assert provenance["source_manifest"]["sha256"] in html
    assert provenance["resume_json"]["sha256"] in html
    assert provenance["resume_pdf"]["sha256"] in html
