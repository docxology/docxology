"""Offline source identity and bounded citation-review regressions."""
import copy
import hashlib
import json
import sys
import subprocess
from pathlib import Path

import pytest

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

from docxology_tools import citation_intake as intake  # noqa: E402
import review_citation_metadata as cli  # noqa: E402


@pytest.fixture
def catalog(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "core.fsmonitor", "false"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "core.untrackedCache", "false"], check=True)
    path = tmp_path / "papers" / "2024_Test" / "metadata.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({"title": "Curated", "citation_metadata": {}}))
    return tmp_path, [{"citation_key": "Test2024", "title": "Gene & research", "doi": "10.1234/example", "year": 2024, "authors": ["Curated, Author"], "docs_path": "papers/2024_Test/", "has_paper_folder": True}]


@pytest.fixture
def message():
    return {"DOI": "10.1234/EXAMPLE", "title": ["<i>Gene</i> &amp; research"], "type": "journal-article", "container-title": ["Science &amp; <i>Research</i>"], "volume": "12", "issue": "2", "page": "4-10", "ISSN": ["1234-567X"], "published": {"date-parts": [[2024, 2, 29]]}}


def run(catalog, message, **kwargs):
    root, works = catalog
    return intake.review_works(works, root, fetch=lambda url: (200, json.dumps({"message": message}).encode()), checked_at="2026-10-13T00:00:00Z", **kwargs)


def test_proposal_preserves_curated_identity_and_files(catalog, message):
    root, works = catalog
    before = copy.deepcopy(works)
    path = root / "papers/2024_Test/metadata.json"
    original = path.read_bytes()
    report = run(catalog, message)
    record = report["records"][0]
    assert report["requires_review"] and report["mode"] == "review-proposals-only"
    assert record["status"] == "proposed"
    candidate = record["candidate_citation_metadata"]
    assert candidate["title"] == "Gene & research"
    assert candidate["journal_title"] == "Science & Research"
    assert candidate["publication_date"] == "2024-02-29"
    assert candidate["source_url"] == "https://api.crossref.org/works/10.1234%2Fexample"
    assert candidate["issn"] == "1234-567X"
    assert "authors" not in candidate and "year" not in candidate
    assert works == before and path.read_bytes() == original


@pytest.mark.parametrize("field,value", [("DOI", "10.1234/unrelated"), ("title", ["Other research"])])
def test_mismatch_has_no_candidate(catalog, message, field, value):
    message[field] = value
    record = run(catalog, message)["records"][0]
    assert record["status"] == "mismatch"
    assert record["candidate_citation_metadata"] is None


@pytest.mark.parametrize("field,value", [("DOI", 10), ("title", "not array"), ("title", []), ("title", [None]), ("type", None), ("container-title", 3), ("volume", 12), ("issue", []), ("page", {}), ("ISSN", ["bad"]), ("published", {"date-parts": [[2024, 2, 30]]}), ("published", {"date-parts": [[True, 2, 1]]}), ("published", {"date-parts": [[2024, 2, 1, 3]]}), ("published", {"date-parts": []}), ("published", "2024")])
def test_malformed_source_never_proposes(catalog, message, field, value):
    message[field] = value
    record = run(catalog, message)["records"][0]
    assert record["status"] == "unavailable"
    assert record["candidate_citation_metadata"] is None


@pytest.mark.parametrize("parts", [[2024], [2024, 2]])
def test_partial_dates_do_not_invent_precision(catalog, message, parts):
    message["published"]["date-parts"] = [parts]
    assert "publication_date" not in run(catalog, message)["records"][0]["candidate_citation_metadata"]


def test_unchanged_keeps_original_checked_at(catalog, message):
    root, _ = catalog
    candidate = run(catalog, message)["records"][0]["candidate_citation_metadata"]
    candidate["checked_at"] = "2020-01-01T00:00:00Z"
    candidate["source_url"] = "https://api.crossref.org/works/10.1234/example"
    (root / "papers/2024_Test/metadata.json").write_text(json.dumps({"citation_metadata": candidate}))
    record = run(catalog, message)["records"][0]
    assert record["status"] == "unchanged"
    assert record["candidate_citation_metadata"]["checked_at"] == candidate["checked_at"]


@pytest.mark.parametrize("response", [(429, b"slow down"), (404, b"missing"), (200, b"bad json"), (200, b"[]"), (200, b'{"message": []}')])
def test_explicit_failure_no_retries(catalog, response):
    root, works = catalog
    calls = []
    def fetch(url):
        calls.append(url)
        return response
    record = intake.review_works(works, root, fetch=fetch)["records"][0]
    assert record["status"] == "unavailable" and len(calls) == 1
    assert record["candidate_citation_metadata"] is None


def test_filters_validate_before_network(catalog, message):
    root, works = catalog
    with pytest.raises(ValueError, match="unknown citation"):
        intake.review_works(works, root, citation_keys=["unknown"], fetch=lambda _: pytest.fail("network"))
    assert len(run(catalog, message, citation_keys=["Test2024", "Test2024"])["records"]) == 1
    works[0]["doi"] = "10.5281/zenodo.123"
    assert intake.review_works(works, root, fetch=lambda _: pytest.fail("network"))["records"] == []
    with pytest.raises(ValueError, match="ineligible"):
        intake.review_works(works, root, citation_keys=["Test2024"], fetch=lambda _: pytest.fail("network"))


def test_response_and_request_limits(catalog, monkeypatch):
    root, works = catalog
    monkeypatch.setattr(intake, "MAX_RESPONSE_BYTES", 3)
    assert intake.review_works(works, root, fetch=lambda _: (200, b"1234"))["records"][0]["status"] == "unavailable"
    monkeypatch.setattr(intake, "MAX_REQUESTS", 0)
    with pytest.raises(ValueError, match="request limit"):
        intake.review_works(works, root, fetch=lambda _: pytest.fail("network"))


def test_path_escape_and_source_output_rejected(catalog, monkeypatch):
    root, works = catalog
    works[0]["docs_path"] = "../escape"
    with pytest.raises(ValueError, match="Invalid paper-folder"):
        intake.review_works(works, root, fetch=lambda _: pytest.fail("network"))
    monkeypatch.setattr(cli, "REPO_ROOT", root)
    with pytest.raises(SystemExit):
        cli.main(["--output", str(root / "papers/metadata.json")])


def test_cli_report_only(catalog, message, monkeypatch):
    root, works = catalog
    (root / "data").mkdir()
    (root / "data/works.json").write_text(json.dumps({"works": works}))
    monkeypatch.setattr(cli, "REPO_ROOT", root)
    monkeypatch.setattr(cli, "review_works", lambda w, r, citation_keys: run((r, w), message, citation_keys=citation_keys))
    output = root / "reports/review.json"
    assert cli.main(["--output", str(output), "--citation-key", "Test2024"]) == 0
    assert json.loads(output.read_text())["requires_review"] is True


def test_network_transport_fixed_origin_cap_and_redirects(monkeypatch):
    calls = []
    class Response:
        code = 200
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False
        def read(self, limit):
            calls.append(limit)
            return b"{}"
    class Opener:
        def open(self, request, timeout):
            assert request.full_url == "https://api.crossref.org/works/10.1234%2Fx"
            assert timeout == intake.TIMEOUT_SECONDS
            return Response()
    monkeypatch.setattr(intake.urllib.request, "build_opener", lambda handler: Opener())
    assert intake.fetch_crossref("https://api.crossref.org/works/10.1234%2Fx") == (200, b"{}")
    assert calls == [intake.MAX_RESPONSE_BYTES + 1]
    assert intake._NoRedirect().redirect_request(None, None, 302, None, None, "https://evil.test") is None
    for url in ("http://api.crossref.org/works/a", "https://evil.test/works/a", "https://api.crossref.org/works/a?token=x"):
        with pytest.raises(ValueError, match="fixed-origin"):
            intake.fetch_crossref(url)


@pytest.mark.parametrize("alias", ["file-symlink", "hardlink", "reports-symlink", "external-parent-symlink"])
def test_report_aliases_cannot_overwrite_source(catalog, monkeypatch, alias):
    root, _ = catalog
    source = root / "papers/2024_Test/metadata.json"
    original = source.read_bytes()
    reports = root / "reports"
    external = root.parent / (root.name + "-external")
    external.mkdir()
    if alias == "reports-symlink":
        reports.symlink_to(source.parent, target_is_directory=True)
        output = reports / "metadata.json"
    elif alias == "external-parent-symlink":
        link = external / "alias"
        link.symlink_to(source.parent, target_is_directory=True)
        output = link / "metadata.json"
    else:
        reports.mkdir()
        output = reports / "review.json"
        if alias == "file-symlink":
            output.symlink_to(source)
        else:
            import os
            os.link(source, output)
    monkeypatch.setattr(cli, "REPO_ROOT", root)
    monkeypatch.setattr(cli, "review_works", lambda *a, **kw: pytest.fail("unsafe destination reached intake"))
    assert cli.main(["--output", str(output)]) == 1
    assert source.read_bytes() == original


def test_external_report_uses_existing_real_parent(catalog, message, monkeypatch):
    root, works = catalog
    (root / "data").mkdir()
    (root / "data/works.json").write_text(json.dumps({"works": works}))
    external = root.parent / (root.name + "-external")
    external.mkdir()
    monkeypatch.setattr(cli, "REPO_ROOT", root)
    monkeypatch.setattr(cli, "review_works", lambda w, r, citation_keys: run((r, w), message, citation_keys=citation_keys))
    output = external / "review.json"
    assert cli.main(["--output", str(output)]) == 0
    assert json.loads(output.read_text())["requires_review"] is True


@pytest.mark.parametrize("alias", ["metadata-symlink", "folder-symlink", "hardlink", "ignored", "missing", "non-object"])
def test_ineligible_metadata_cannot_enter_public_report(catalog, alias):
    import os
    root, works = catalog
    source = root / "papers/2024_Test/metadata.json"
    original = source.read_bytes()
    outside = root / "private.json"
    outside.write_text('{"citation_metadata": {"private": "must not publish"}}')
    if alias == "metadata-symlink":
        source.unlink()
        source.symlink_to(outside)
    elif alias == "folder-symlink":
        source.unlink()
        source.parent.rmdir()
        private = root / "private-folder"
        private.mkdir()
        (private / "metadata.json").write_bytes(original)
        source.parent.symlink_to(private, target_is_directory=True)
    elif alias == "hardlink":
        source.unlink()
        os.link(outside, source)
    elif alias == "ignored":
        (root / ".gitignore").write_text("papers/2024_Test/metadata.json\n")
    elif alias == "missing":
        source.unlink()
    else:
        source.write_text("[]")
    with pytest.raises(ValueError):
        intake.review_works(works, root, fetch=lambda _: pytest.fail("ineligible source reached network"))


@pytest.mark.parametrize("alias", ["symlink", "ancestor-symlink", "hardlink", "ignored"])
def test_ineligible_works_input_rejected(catalog, monkeypatch, alias):
    import os
    root, works = catalog
    data = root / "data"
    data.mkdir()
    source = data / "works.json"
    source.write_text(json.dumps({"works": works}))
    outside = root / "private-works.json"
    outside.write_text(json.dumps({"works": works}))
    if alias == "symlink":
        source.unlink()
        source.symlink_to(outside)
    elif alias == "ancestor-symlink":
        source.unlink()
        data.rmdir()
        private = root / "private-data"
        private.mkdir()
        (private / "works.json").write_bytes(outside.read_bytes())
        data.symlink_to(private, target_is_directory=True)
    elif alias == "hardlink":
        source.unlink()
        os.link(outside, source)
    else:
        (root / ".gitignore").write_text("data/works.json\n")
    monkeypatch.setattr(cli, "REPO_ROOT", root)
    monkeypatch.setattr(cli, "review_works", lambda *a, **kw: pytest.fail("ineligible works reached intake"))
    output = root / "reports/review.json"
    assert cli.main(["--output", str(output)]) == 1
    assert not output.exists()


def test_encoded_math_is_text_not_markup():
    assert intake.plain_text("Entropy &lt; 1 &amp; complexity &gt; 2") == "Entropy < 1 & complexity > 2"
    assert intake.plain_text("<i>Entropy</i> &lt;x&gt; &amp; complexity") == "Entropy <x> & complexity"


def test_response_provenance_binds_exact_bounded_source_bytes(catalog, message):
    root, works = catalog
    body = json.dumps({"message": message}, indent=2).encode()
    record = intake.review_works(works, root, fetch=lambda _: (200, body))["records"][0]
    assert record["response_sha256"] == hashlib.sha256(body).hexdigest()
    assert "response_body" not in record
    error_body = b"rate limited"
    unavailable = intake.review_works(works, root, fetch=lambda _: (429, error_body))["records"][0]
    assert unavailable["response_sha256"] == hashlib.sha256(error_body).hexdigest()
    assert unavailable["candidate_citation_metadata"] is None


@pytest.mark.parametrize("curated,source", [("α peptide", "β peptide"), ("x α = 1", "x β = 1"), ("研究甲", "研究乙"), ("x &lt; y", "x &gt; y"), ("∑ entropy", "∏ entropy")])
def test_unicode_identity_mismatch_has_no_candidate(catalog, message, curated, source):
    catalog[1][0]["title"] = curated
    message["title"] = [source]
    record = run(catalog, message)["records"][0]
    assert record["status"] == "mismatch"
    assert record["candidate_citation_metadata"] is None


@pytest.mark.parametrize("title", ["复杂性与熵", "α peptide", "Исследование энтропии"])
def test_matching_non_latin_identity_can_propose(catalog, message, title):
    catalog[1][0]["title"] = title
    message["title"] = [f"<i>{title}</i>"]
    assert run(catalog, message)["records"][0]["status"] == "proposed"


def test_title_accents_and_punctuation_remain_insignificant():
    assert intake.normalized_title("Café: complexity") == intake.normalized_title("Cafe complexity")
