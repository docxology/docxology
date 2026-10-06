"""Tests for parallel public-source refresh and --cache-reports reuse."""

from __future__ import annotations

import http.client
import json
import re
import socket
import ssl
import sys
import unittest.mock as mock
import urllib.error
import urllib.parse
from pathlib import Path

import pytest

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402, F401  (canonical bootstrap: code/src + code/orchestrators onto sys.path)

REPO_ROOT = Path(__file__).resolve().parents[2]

import export_agent_data as ead  # noqa: E402
import refresh_public_source_inventory as inv  # noqa: E402
import refresh_public_sources as rps  # noqa: E402

def _today() -> str:
    """Runtime date — a module-level date goes stale across a midnight pytest run."""
    return __import__("datetime").datetime.now(__import__("datetime").timezone.utc).date().isoformat()


def _ok_section(label: str, url: str = "https://example.com") -> dict:
    return {"label": label, "url": url, "ok": True, "items": [{"status": 200, "title": label}]}


def _write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


# --- 1. parallel refresh: output equality with sequential reference ----------


class _SerialPool:
    """ThreadPoolExecutor stand-in that runs tasks inline (sequential reference)."""

    def __init__(self, *a, **k):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def map(self, fn, iterable):
        return map(fn, iterable)


def test_parallel_refresh_output_identical_to_sequential(monkeypatch):
    """Threaded build_report output is byte-identical (mod timestamps) to the sequential run."""
    captured_urls = []

    def fake_fetch_json(url, **kwargs):
        captured_urls.append(url)
        return {"login": url, "public_repos": 1, "updated_at": "t", "html_url": url,
                "full_name": url, "stargazers_count": 0, "language": "Python",
                "message": {"total-results": 3},
                "esearchresult": {"count": "2", "idlist": ["1", "2"]},
                "hitCount": 7, "group": [{"g": 1}, {"g": 2}],
                "hits": {"total": {"value": 9}, "hits": [{"metadata": {"title": "T", "doi": "d",
                    "publication_date": "2026", "resource_type": {"title": "article"},
                    "creators": [{"name": "x"}]}}]}}

    monkeypatch.setattr(rps, "fetch_json", fake_fetch_json)

    threaded = rps.build_report()
    assert len(captured_urls) == len(rps.expected_check_labels())

    captured_urls.clear()
    with mock.patch.object(rps, "ThreadPoolExecutor", _SerialPool):
        sequential = rps.build_report()

    assert [c["label"] for c in threaded["checks"]] == list(rps.expected_check_labels())
    assert threaded["checks"] == sequential["checks"]
    assert threaded["facts"] == sequential["facts"]
    assert threaded["date"] == sequential["date"]
    for key in ("source_commit", "note", "facts"):
        assert threaded[key] == sequential[key]
    assert all(c["ok"] for c in threaded["checks"])
    del threaded["generated_at"], sequential["generated_at"]
    assert json.dumps(threaded, sort_keys=False) == json.dumps(sequential, sort_keys=False)


# --- 1b. facts shape: Zenodo order, GitHub account type ----------------------


def _zenodo_search_urls(urls):
    return [u for u in urls if urllib.parse.urlparse(u).path == "/api/records"]


def test_zenodo_searches_request_the_newest_deposit_first():
    """first_title/first_doi must name the newest deposit, not a relevance-ranked hit that flips."""
    url = rps.zenodo_query_url('metadata.creators.person_or_org.name:"Friedman, Daniel Ari"')
    params = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
    assert params["sort"] == ["mostrecent"]
    assert params["size"] == ["1"]
    assert params["q"] == ['metadata.creators.person_or_org.name:"Friedman, Daniel Ari"']


def test_both_zenodo_search_checks_send_the_sort(monkeypatch):
    """Every Zenodo search issued by build_report is newest-first; record lookups carry no query."""
    captured: list[str] = []

    def fake_fetch_json(url, **kwargs):
        captured.append(url)
        return {"hits": {"total": {"value": 1}, "hits": [{"metadata": {"title": "T"}, "doi": "d"}]},
                "metadata": {"title": "T", "creators": []}}

    monkeypatch.setattr(rps, "fetch_json", fake_fetch_json)
    rps.build_report()

    searches = _zenodo_search_urls(captured)
    assert len(searches) == 2, "exact-name and ORCID-linked Zenodo searches"
    for url in searches:
        assert urllib.parse.parse_qs(urllib.parse.urlparse(url).query)["sort"] == ["mostrecent"]
    records = [u for u in captured if urllib.parse.urlparse(u).path.startswith("/api/records/")]
    assert len(records) == 5 and all(not urllib.parse.urlparse(u).query for u in records)


def test_github_user_facts_record_the_account_type():
    """A User and an Organization payload keep their `type`, alongside the pre-existing keys."""
    org = rps.github_user_facts({
        "login": "ActiveInferenceInstitute", "type": "Organization", "public_repos": 45,
        "updated_at": "2026-09-22T19:05:32Z", "html_url": "https://github.com/ActiveInferenceInstitute",
        "name": "ignored", "followers": 7,
    })
    assert org == {
        "login": "ActiveInferenceInstitute", "type": "Organization", "public_repos": 45,
        "updated_at": "2026-09-22T19:05:32Z", "html_url": "https://github.com/ActiveInferenceInstitute",
    }
    user = rps.github_user_facts({"login": "docxology", "type": "User", "public_repos": 230})
    assert user["type"] == "User"
    assert rps.github_user_facts({})["type"] is None, "a payload without type records null, not a guess"


def test_build_report_facts_carry_type_for_both_github_accounts(monkeypatch):
    """The two GitHub-user labels expose `type` in facts, the object freshness.yml compares."""
    def fake_fetch_json(url, **kwargs):
        if url.endswith("/users/ActiveInferenceInstitute"):
            return {"login": "ActiveInferenceInstitute", "type": "Organization", "public_repos": 45}
        if url.endswith("/users/docxology"):
            return {"login": "docxology", "type": "User", "public_repos": 230}
        return {}

    monkeypatch.setattr(rps, "fetch_json", fake_fetch_json)
    facts = rps.build_report()["facts"]
    assert facts["GitHub user ActiveInferenceInstitute"]["type"] == "Organization"
    assert facts["GitHub user docxology"]["type"] == "User"
    assert [c["label"] for c in rps.build_report()["checks"]] == list(rps.expected_check_labels())


# --- 1c. fetch_json retry policy (transport seam: urllib.request.urlopen) ----


class _FakeResponse:
    def __init__(self, body: bytes = b'{"ok": true}', read_error: Exception | None = None):
        self._body = body
        self._read_error = read_error

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def read(self):
        if self._read_error is not None:
            raise self._read_error
        return self._body


def _http_error(code: int, retry_after: str | None = None) -> urllib.error.HTTPError:
    headers = http.client.HTTPMessage()
    if retry_after is not None:
        headers["Retry-After"] = retry_after
    return urllib.error.HTTPError("https://example.test/x", code, f"HTTP {code}", headers, None)


def _script_transport(monkeypatch, outcomes):
    """Feed urlopen one scripted outcome per call; record every call and every sleep."""
    calls: list[str] = []
    sleeps: list[float] = []
    queue = list(outcomes)

    def fake_urlopen(req, timeout=None):
        calls.append(req.full_url)
        outcome = queue.pop(0)
        if isinstance(outcome, BaseException):
            raise outcome
        return outcome

    monkeypatch.setattr(rps.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(rps.time, "sleep", sleeps.append)
    return calls, sleeps


def test_fetch_json_retries_transient_connection_errors(monkeypatch):
    """URLError, ConnectionResetError and IncompleteRead (also mid-read) retry with 2s, 4s backoff."""
    calls, sleeps = _script_transport(monkeypatch, [
        urllib.error.URLError("proxy closed the tunnel"),
        ConnectionResetError(54, "Connection reset by peer"),
        _FakeResponse(),
    ])
    assert rps.fetch_json("https://example.test/x") == {"ok": True}
    assert len(calls) == 3
    assert sleeps == [2.0, 4.0]

    calls, sleeps = _script_transport(monkeypatch, [
        _FakeResponse(read_error=http.client.IncompleteRead(b"{", 100)),
        _FakeResponse(),
    ])
    assert rps.fetch_json("https://example.test/x") == {"ok": True}
    assert len(calls) == 2
    assert sleeps == [2.0]


def test_fetch_json_gives_up_after_the_bounded_retries(monkeypatch):
    """A connection that never recovers re-raises its last error after retries+1 attempts."""
    calls, sleeps = _script_transport(monkeypatch, [ConnectionResetError("a")] * 3)
    try:
        rps.fetch_json("https://example.test/x")
    except ConnectionResetError:
        pass
    else:
        raise AssertionError("expected ConnectionResetError after the retry budget")
    assert len(calls) == 3
    assert sleeps == [2.0, 4.0], "no sleep after the final attempt"

    calls, sleeps = _script_transport(monkeypatch, [urllib.error.URLError("down")])
    try:
        rps.fetch_json("https://example.test/x", retries=0)
    except urllib.error.URLError:
        pass
    else:
        raise AssertionError("retries=0 must not retry")
    assert len(calls) == 1 and sleeps == []


def test_fetch_json_never_retries_http_errors_other_than_429(monkeypatch):
    """HTTPError is a URLError subclass; a 403 (rate limit) or 404 must still fail on the first call."""
    for code in (400, 401, 403, 404, 410, 422, 500):
        calls, sleeps = _script_transport(monkeypatch, [_http_error(code), _FakeResponse()])
        try:
            rps.fetch_json("https://example.test/x")
        except urllib.error.HTTPError as exc:
            assert exc.code == code
        else:
            raise AssertionError(f"HTTP {code} must not be swallowed")
        assert len(calls) == 1, f"HTTP {code} must not be retried"
        assert sleeps == []


def test_fetch_json_429_honors_retry_after_within_the_cap(monkeypatch):
    """429 keeps its Retry-After handling: numeric values are capped at 10s, junk falls back to 2s."""
    calls, sleeps = _script_transport(monkeypatch, [
        _http_error(429, "3"),
        _http_error(429, "120"),
        _FakeResponse(),
    ])
    assert rps.fetch_json("https://example.test/x") == {"ok": True}
    assert sleeps == [3.0, 10.0]

    calls, sleeps = _script_transport(monkeypatch, [_http_error(429, "soon"), _http_error(429), _FakeResponse()])
    assert rps.fetch_json("https://example.test/x") == {"ok": True}
    assert sleeps == [2.0, 4.0]


def test_safe_fetch_records_a_recovered_transient_failure_as_ok(monkeypatch):
    """A check that recovers after a reset is stored ok:true, so its facts are not dropped."""
    _script_transport(monkeypatch, [ConnectionResetError("once"), _FakeResponse(body=b'{"login": "x", "type": "User"}')])
    check = rps.safe_fetch("GitHub user x", "https://api.github.com/users/x", rps.github_user_facts)
    assert check["ok"] is True
    assert check["result"]["type"] == "User"


def test_main_writes_outputs_outside_the_repo_without_crashing(tmp_path, monkeypatch, capsys):
    """A rehearsal --output in a scratch dir still reports success after the files are written."""
    report = {
        "date": "2026-10-06", "generated_at": "t", "facts": {"b": {"z": 1, "a": 2}, "a": {"type": "Organization"}},
        "checks": [{"label": "a", "ok": True}, {"label": "b", "ok": False}],
    }
    monkeypatch.setattr(rps, "build_report", lambda: report)
    out, facts = tmp_path / "latest.json", tmp_path / "latest.facts.json"
    monkeypatch.setattr(sys, "argv", ["prog", "--output", str(out), "--facts-output", str(facts)])
    rps.main()
    printed = capsys.readouterr().out
    assert f"wrote {out} with 2 checks" in printed
    assert "warnings: b" in printed
    assert json.loads(out.read_text(encoding="utf-8"))["facts"] == report["facts"]
    assert list(json.loads(facts.read_text(encoding="utf-8"))) == ["a", "b"], "facts are written key-sorted"


# --- 1d. transient set, gateway retries, Retry-After sanitizing --------------


@pytest.mark.parametrize(
    "error",
    [
        TimeoutError("timed out"),
        socket.timeout("timed out"),
        ConnectionAbortedError(53, "Software caused connection abort"),
        ConnectionRefusedError(61, "Connection refused"),
        BrokenPipeError(32, "Broken pipe"),
        http.client.RemoteDisconnected("Remote end closed connection without response"),
        ssl.SSLEOFError(8, "EOF occurred in violation of protocol (_ssl.c:2406)"),
        ssl.SSLError(1, "[SSL] record layer failure (_ssl.c:2559)"),
    ],
    ids=lambda error: type(error).__name__,
)
def test_fetch_json_retries_timeouts_and_connection_errors(monkeypatch, error):
    """TimeoutError, every ConnectionError subclass and TLS errors (SSLEOFError, SSLError) retry once."""
    calls, sleeps = _script_transport(monkeypatch, [error, _FakeResponse()])
    assert rps.fetch_json("https://example.test/x") == {"ok": True}
    assert len(calls) == 2
    assert sleeps == [2.0]


def test_fetch_json_retries_a_timeout_raised_while_reading_the_body(monkeypatch):
    """urllib does not wrap a socket timeout during read() in URLError; it must still retry."""
    calls, sleeps = _script_transport(monkeypatch, [
        _FakeResponse(read_error=TimeoutError("read timed out")),
        _FakeResponse(read_error=ConnectionAbortedError("aborted mid-read")),
        _FakeResponse(),
    ])
    assert rps.fetch_json("https://example.test/x") == {"ok": True}
    assert len(calls) == 3
    assert sleeps == [2.0, 4.0]


def test_fetch_json_retries_a_tls_eof_raised_while_reading_the_body(monkeypatch):
    """The peer closing the TLS stream mid-response surfaces as a bare SSLEOFError from read()."""
    eof = ssl.SSLEOFError(8, "EOF occurred in violation of protocol (_ssl.c:2406)")
    calls, sleeps = _script_transport(monkeypatch, [_FakeResponse(read_error=eof), _FakeResponse()])
    assert rps.fetch_json("https://example.test/x") == {"ok": True}
    assert len(calls) == 2
    assert sleeps == [2.0]

    calls, sleeps = _script_transport(monkeypatch, [_FakeResponse(read_error=eof)] * 3)
    with pytest.raises(ssl.SSLEOFError):
        rps.fetch_json("https://example.test/x")
    assert len(calls) == 3
    assert sleeps == [2.0, 4.0], "a TLS failure that never recovers is re-raised after the retry budget"


def test_transient_set_names_the_documented_error_classes():
    """TRANSIENT_ERRORS covers URLError, TimeoutError, ConnectionError, IncompleteRead and ssl.SSLError."""
    for cls in (urllib.error.URLError, TimeoutError, ConnectionError, ConnectionResetError,
                ConnectionAbortedError, http.client.IncompleteRead, ssl.SSLError, ssl.SSLEOFError):
        assert issubclass(cls, rps.TRANSIENT_ERRORS), cls.__name__
    assert not issubclass(ValueError, rps.TRANSIENT_ERRORS), "a parse error is not a flaky link"


@pytest.mark.parametrize("code", [502, 503, 504])
def test_fetch_json_retries_gateway_statuses_with_the_bounded_backoff(monkeypatch, code):
    """502/503/504 retry on the 2s, 4s schedule and recover when the upstream does."""
    calls, sleeps = _script_transport(monkeypatch, [_http_error(code), _http_error(code), _FakeResponse()])
    assert rps.fetch_json("https://example.test/x") == {"ok": True}
    assert len(calls) == 3
    assert sleeps == [2.0, 4.0]


@pytest.mark.parametrize("code", [429, 502, 503, 504])
def test_fetch_json_gives_up_on_a_persistent_retryable_status(monkeypatch, code):
    """A status that never recovers re-raises its HTTPError after retries+1 calls, with no final sleep."""
    calls, sleeps = _script_transport(monkeypatch, [_http_error(code)] * 3)
    with pytest.raises(urllib.error.HTTPError) as caught:
        rps.fetch_json("https://example.test/x")
    assert caught.value.code == code
    assert len(calls) == 3
    assert sleeps == [2.0, 4.0]

    calls, sleeps = _script_transport(monkeypatch, [_http_error(code)])
    with pytest.raises(urllib.error.HTTPError):
        rps.fetch_json("https://example.test/x", retries=0)
    assert len(calls) == 1 and sleeps == []


@pytest.mark.parametrize("code", [500, 501, 505, 507, 400, 401, 403, 404, 410, 422])
def test_fetch_json_never_retries_statuses_outside_the_gateway_set(monkeypatch, code):
    """Only 429/502/503/504 are retried; 500 and every other 4xx/5xx is a verdict raised at once."""
    assert code not in rps.RETRYABLE_HTTP_STATUS
    calls, sleeps = _script_transport(monkeypatch, [_http_error(code), _FakeResponse()])
    with pytest.raises(urllib.error.HTTPError) as caught:
        rps.fetch_json("https://example.test/x")
    assert caught.value.code == code
    assert len(calls) == 1 and sleeps == []


def test_fetch_json_gateway_retry_honors_a_numeric_retry_after(monkeypatch):
    """A 503 Retry-After is honored on the same bounded schedule as 429: seconds, capped at 10s."""
    calls, sleeps = _script_transport(monkeypatch, [
        _http_error(503, "3"),
        _http_error(504, "120"),
        _FakeResponse(),
    ])
    assert rps.fetch_json("https://example.test/x") == {"ok": True}
    assert sleeps == [3.0, 10.0]


def test_safe_fetch_records_a_recovered_gateway_error_as_ok(monkeypatch):
    """A check that recovers after a 502 is stored ok:true, so its facts are not dropped."""
    _script_transport(monkeypatch, [_http_error(502), _FakeResponse(body=b'{"login": "x", "type": "Organization"}')])
    check = rps.safe_fetch("GitHub user x", "https://api.github.com/users/x", rps.github_user_facts)
    assert check["ok"] is True
    assert check["result"]["type"] == "Organization"


@pytest.mark.parametrize("junk", ["-5", "-0.1", "nan", "NaN", "inf", "-inf", "Infinity", "soon", "",
                                  "Wed, 21 Oct 2026 07:28:00 GMT"])
def test_backoff_delay_falls_back_to_the_default_for_unusable_retry_after(junk):
    """Negative, NaN, infinite and non-numeric Retry-After values use 2s, 4s, ... instead."""
    assert rps._backoff_delay(0, junk) == 2.0
    assert rps._backoff_delay(2, junk) == 6.0


@pytest.mark.parametrize(("value", "expected"), [("0", 0.0), ("3", 3.0), ("2.5", 2.5), (" 7 ", 7.0),
                                                 ("10", 10.0), ("120", 10.0), ("1e9", 10.0)])
def test_backoff_delay_honors_finite_non_negative_retry_after_up_to_the_cap(value, expected):
    assert rps._backoff_delay(0, value) == expected
    assert rps._backoff_delay(1, None) == 4.0


def test_fetch_json_429_with_unusable_retry_after_never_sleeps_a_bad_duration(monkeypatch):
    """A negative or NaN Retry-After must not reach time.sleep (which raises ValueError on both)."""
    calls, sleeps = _script_transport(monkeypatch, [
        _http_error(429, "-5"),
        _http_error(429, "nan"),
        _FakeResponse(),
    ])
    assert rps.fetch_json("https://example.test/x") == {"ok": True}
    assert sleeps == [2.0, 4.0]
    assert all(s >= 0 and s == s and s != float("inf") for s in sleeps)


# --- 1e. AII claim wording follows the snapshot's `type` fact ----------------

AII_LABEL = "GitHub user ActiveInferenceInstitute"
_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
_STAMP = "2026-10-06T12:00:00+00:00"


def _snapshot_with_aii(aii_result: dict | None, *, aii_repos: int = 45) -> dict:
    """A public-source snapshot fixture; `aii_result` None omits the AII check altogether."""
    checks = [{"label": "GitHub user docxology", "url": "u", "ok": True,
               "result": {"login": "docxology", "type": "User", "public_repos": 231}}]
    if aii_result is not None:
        checks.append({"label": AII_LABEL, "url": "u", "ok": True,
                       "result": {"login": "ActiveInferenceInstitute", "public_repos": aii_repos, **aii_result}})
    return {"generated_at": _STAMP, "checks": checks}


@pytest.fixture
def use_snapshot(monkeypatch):
    """Point export_agent_data at a fixture snapshot; _claims is @cache'd, so clear it on both sides."""
    def install(snapshot: dict) -> None:
        monkeypatch.setattr(ead, "_latest_snapshot_payload", lambda: snapshot)
        ead._claims.cache_clear()

    yield install
    ead._claims.cache_clear()


def _aii_claim(claims: list[dict]) -> dict:
    return next(claim for claim in claims if claim["id"] == "aii-github-public-repos")


# The caveat head when the snapshot records no recognized account type (absent, null, odd-cased, unknown).
_NO_TYPE_CAVEAT = (
    "The repository count is read from /users/ActiveInferenceInstitute; the public-source snapshot "
    "records no recognized account type, so none is asserted."
)


def _caveat_head(caveat: str) -> str:
    """The snapshot-driven part of the caveat, before the catalog-count sentence each path appends."""
    return caveat.split(" Local software catalog tracks")[0]


AII_BRANCHES = [
    pytest.param(
        {"type": "Organization"},
        "The ActiveInferenceInstitute GitHub account (an Organization) has 45 public repositories.",
        "type: Organization",
        id="organization",
    ),
    pytest.param(
        {"type": "User"},
        "The ActiveInferenceInstitute GitHub account (a User account) has 45 public repositories.",
        "type: User",
        id="user",
    ),
    pytest.param(
        {},
        "The ActiveInferenceInstitute GitHub account has 45 public repositories.",
        None,
        id="type-absent",
    ),
]


@pytest.mark.parametrize(("aii_result", "expected_claim", "type_phrase"), AII_BRANCHES)
def test_static_aii_claim_wording_follows_the_snapshot_type(use_snapshot, aii_result, expected_claim, type_phrase):
    use_snapshot(_snapshot_with_aii(aii_result))
    claim = _aii_claim(ead._claims())
    assert claim["claim"] == expected_claim
    if type_phrase is None:
        assert "type" not in claim["verification_method"].lower(), "an absent type must not be asserted"
        assert "Organization" not in claim["claim"] + claim["verification_method"]
        assert _caveat_head(claim["caveat"]) == _NO_TYPE_CAVEAT
    else:
        assert type_phrase in claim["verification_method"]
        assert "as recorded in the public-source snapshot" in claim["verification_method"]
    for field in ("claim", "verification_method", "caveat"):
        assert not _DATE_RE.search(claim[field]), f"{field} must not hard-code an observation date"
    assert claim["checked_at"] == _STAMP, "freshness comes from the snapshot stamp, not from the wording"


@pytest.mark.parametrize(("aii_result", "expected_claim", "type_phrase"), AII_BRANCHES)
def test_hydrated_aii_claim_agrees_with_the_static_claim(use_snapshot, aii_result, expected_claim, type_phrase):
    """The hydration path reads the same snapshot fact, so static and hydrated texts match, gate on."""
    use_snapshot(_snapshot_with_aii(aii_result))
    static = _aii_claim(ead._claims())
    hydrated = _aii_claim(ead._hydrate_claim_checks(enforce_stale_checks=True))
    assert hydrated["claim"] == static["claim"] == expected_claim
    assert hydrated["verification_method"] == static["verification_method"]
    assert _caveat_head(hydrated["caveat"]) == _caveat_head(static["caveat"])
    assert re.search(r"Local software catalog tracks \d+ AII repositories", hydrated["caveat"])
    assert "has 45 public repositories" in hydrated["claim"], "the stale-fragment gate's fragment"
    for field in ("claim", "verification_method", "caveat"):
        assert not _DATE_RE.search(hydrated[field])


@pytest.mark.parametrize(("aii_result", "expected_claim", "type_phrase"), AII_BRANCHES)
def test_aii_claim_passes_the_stale_fragment_gate_in_every_branch(aii_result, expected_claim, type_phrase):
    claim = {"id": "aii-github-public-repos", "claim": expected_claim, "checked_at": _STAMP}
    assert ead._stale_claim_fragment_errors(
        claim, 1, 1, 231, 45, source_public_source_timestamp=_STAMP
    ) == []
    stale = dict(claim, claim=expected_claim.replace("has 45", "has 44"))
    assert ead._stale_claim_fragment_errors(stale, 1, 1, 231, 45), "a stale count must still be caught"


def test_a_type_flip_in_the_snapshot_rewrites_the_claim(use_snapshot):
    """Same count, different recorded type: the claim and verification method follow the snapshot."""
    use_snapshot(_snapshot_with_aii({"type": "User"}))
    before = _aii_claim(ead._claims())
    use_snapshot(_snapshot_with_aii({"type": "Organization"}))
    after = _aii_claim(ead._claims())
    assert "(a User account)" in before["claim"] and "(an Organization)" in after["claim"]
    assert "type: User" in before["verification_method"] and "type: Organization" in after["verification_method"]
    assert "applies only to Organization accounts" in before["caveat"]
    assert "serves Organization accounts as well as Users" in after["caveat"]


@pytest.mark.parametrize("fact", [None, "", "organization", "Bot", 7, ["Organization"]])
def test_unrecognized_account_types_assert_nothing(fact):
    """A null, odd-cased, non-string or unknown `type` is treated like an absent one."""
    snapshot = _snapshot_with_aii({"type": fact})
    assert ead._aii_account_type(snapshot) is None
    texts = ead._aii_claim_texts(snapshot, 45)
    assert texts["claim"] == "The ActiveInferenceInstitute GitHub account has 45 public repositories."
    assert "type" not in texts["verification_method"].lower()
    assert texts["caveat"] == _NO_TYPE_CAVEAT


def test_aii_account_type_ignores_a_missing_or_failed_check():
    assert ead._aii_account_type({}) is None
    assert ead._aii_account_type(_snapshot_with_aii(None)) is None
    failed = {"checks": [{"label": AII_LABEL, "ok": False, "error": "URLError: down"}]}
    assert ead._aii_account_type(failed) is None
    assert ead._aii_claim_texts(failed, 44)["claim"].endswith("has 44 public repositories.")


def test_real_latest_snapshot_still_yields_a_claim_the_gate_accepts():
    """Whatever the checked-in snapshot records (typed or not), the claim keeps the gate's fragment."""
    ead._claims.cache_clear()
    try:
        hydrated = _aii_claim(ead._hydrate_claim_checks(enforce_stale_checks=True))
    finally:
        ead._claims.cache_clear()
    assert re.search(r"has \d+ public repositories\.$", hydrated["claim"])
    assert not _DATE_RE.search(hydrated["claim"])


# --- 2. cache reuse ----------------------------------------------------------


def _setup_cache(tmp_path, monkeypatch, *, inventory_at: str, snapshot_at: str | None,
                 warnings: int = 0):
    reports = tmp_path / "reports"
    labels = ["ORCID work groups", "Crossref ORCID DOI records"]
    sections = [_ok_section(label) for label in labels]
    for i in range(warnings):
        sections.append({"label": f"warned-{i}", "url": "https://x", "ok": False,
                         "error": "HTTPError: 500", "items": []})
    _write_json(reports / f"public_source_inventory_{_today()}.json", {
        "generated_at": inventory_at, "sections": sections,
        "counts": {s["label"]: len(s["items"]) for s in sections},
    })
    if snapshot_at is not None:
        _write_json(reports / f"public_source_snapshot_{_today()}.json", {
            "generated_at": snapshot_at, "checks": [],
        })
    monkeypatch.setattr(inv, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(inv, "latest_report", lambda pattern, required=False: _latest(pattern, reports))
    return reports, sections


def _latest(pattern: str, reports: Path):
    matches = sorted(reports.glob(pattern), reverse=True)
    return matches[0] if matches else None


def test_cache_reuse_same_day(tmp_path, monkeypatch):
    """Same-day clean cache is reused verbatim; anchors field records provenance; no fetch."""
    inventory_at = f"{_today()}T12:00:00Z"
    reports, sections = _setup_cache(tmp_path, monkeypatch, inventory_at=inventory_at,
                                     snapshot_at=f"{_today()}T12:30:00Z")

    def boom(*a, **k):
        raise AssertionError("live fetch must not run on cache reuse")

    for name in ("orcid_works", "crossref_orcid", "pubmed_exact_author", "europe_pmc_exact_author",
                 "wikidata_person", "dblp_author_profile", "researchgate_profile", "sciprofiles_profile",
                 "philpeople_profile", "semantic_scholar_author_search", "openalex_author_advisory",
                 "github_profile", "public_page"):
        monkeypatch.setattr(inv, name, boom)

    report = inv.build_report(cache_reports=True)
    assert report["sections"] == sections
    assert report["counts"] == {s["label"]: len(s["items"]) for s in sections}
    anchor = report["anchors"]
    assert anchor["mode"] == "cache-reuse"
    assert anchor["source_report"] == f"reports/public_source_inventory_{_today()}.json"
    assert anchor["source_generated_at"] == inventory_at
    assert anchor["cached_section_labels"] == [s["label"] for s in sections]
    assert anchor["source_snapshot_generated_at"] == f"{_today()}T12:30:00Z"


def test_cache_reuse_without_snapshot(tmp_path, monkeypatch):
    """Missing snapshot report is optional: reuse still fires."""
    _setup_cache(tmp_path, monkeypatch, inventory_at=f"{_today()}T09:00:00Z", snapshot_at=None)
    report = inv.build_report(cache_reports=True)
    assert report["anchors"]["mode"] == "cache-reuse"


LIVE_FETCHERS = (
    "orcid_works", "crossref_orcid", "pubmed_exact_author", "europe_pmc_exact_author",
    "wikidata_person", "dblp_author_profile", "researchgate_profile", "sciprofiles_profile",
    "philpeople_profile", "semantic_scholar_author_search", "openalex_author_advisory",
)


def _stub_live_fetchers(monkeypatch, marker):
    """Patch every live fetcher with a stub that records it ran."""
    def stub(*a, **k):
        marker.append(a and a[0] or k.get("label", "fetch"))
        return {"label": "stub", "url": "u", "ok": True, "items": []}
    for name in LIVE_FETCHERS:
        monkeypatch.setattr(inv, name, stub)
    monkeypatch.setattr(inv, "zenodo_records", stub)
    monkeypatch.setattr(inv, "github_profile", stub)
    monkeypatch.setattr(inv, "public_page", stub)


def test_cache_reuse_stale_falls_back_live(tmp_path, monkeypatch):
    """A stale cache is ignored: live fetch runs, no anchors field."""
    _setup_cache(tmp_path, monkeypatch, inventory_at="2000-01-01T12:00:00Z", snapshot_at=None)
    marker: list = []
    _stub_live_fetchers(monkeypatch, marker)
    report = inv.build_report(cache_reports=True)
    assert len(marker) == 20, "stale cache must trigger the full live fetch"
    assert "anchors" not in report


def test_cache_reuse_warning_fails_closed(tmp_path, monkeypatch):
    """ANY warning in the cached report forces a live fetch (fail closed)."""
    _setup_cache(tmp_path, monkeypatch, inventory_at=f"{_today()}T12:00:00Z",
                 snapshot_at=None, warnings=1)
    marker: list = []
    _stub_live_fetchers(monkeypatch, marker)
    report = inv.build_report(cache_reports=True)
    assert len(marker) == 20, "warned cache must trigger the full live fetch"
    assert "anchors" not in report


def test_cache_force_accepts_warnings(tmp_path, monkeypatch):
    """--force reuses a warned cache and records forced-reuse provenance."""
    _setup_cache(tmp_path, monkeypatch, inventory_at=f"{_today()}T12:00:00Z",
                 snapshot_at=None, warnings=1)
    report = inv.build_report(cache_reports=True, force=True)
    anchor = report["anchors"]
    assert anchor["mode"] == "forced-reuse"
    assert anchor["warnings_accepted"] == ["warned-0"]


def test_no_flag_never_reads_cache(tmp_path, monkeypatch):
    """Default (no --cache-reports) always live-fetches, even with a clean same-day cache."""
    _setup_cache(tmp_path, monkeypatch, inventory_at=f"{_today()}T12:00:00Z", snapshot_at=None)
    marker: list = []
    _stub_live_fetchers(monkeypatch, marker)
    report = inv.build_report()
    assert len(marker) == 20, "default run live-fetches even with a clean same-day cache"
    assert "anchors" not in report


def test_main_check_offline(tmp_path, monkeypatch, capsys):
    """--check stays offline: validates the cached report without any fetch."""
    reports = tmp_path / "reports"
    _write_json(reports / f"public_source_inventory_{_today()}.json", {
        "generated_at": f"{_today()}T12:00:00Z", "sections": [_ok_section("L")],
    })
    monkeypatch.setattr(inv, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(sys, "argv", ["prog", "--check"])
    inv.main()
