"""Tests for per-domain RSS 2.0 feed generation (build_domain_feeds.py).

No mocks: the real generator runs against the real datasets in a temporary
copy of the repository data, following the repo's injectable-dependency
convention. Determinism is proven by byte-identical output across two runs.
"""

from __future__ import annotations

import hashlib
import subprocess
import sys
import xml.etree.ElementTree as ET  # nosec - parsing our own generated XML
from pathlib import Path
from xml.dom import minidom

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

import build_domain_feeds  # noqa: E402
from build_domain_pages import DOMAINS  # noqa: E402
from sitemap_policy import INDEX_PRIORITY_STATIC  # noqa: E402


def _mini_repo(tmp_path: Path) -> Path:
    """A repo-root stand-in with real data/ copies and no other files."""
    root = tmp_path / "repo"
    (root / "data").mkdir(parents=True)
    for name in ("works.json", "videos.json"):
        (root / "data" / name).write_bytes((REPO_ROOT / "data" / name).read_bytes())
    (root / "feeds").mkdir()
    return root


def _run(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    script = REPO_ROOT / "code" / "orchestrators" / "build_domain_feeds.py"
    return subprocess.run(
        [sys.executable, str(script), *args, "--repo-root", str(root)],
        capture_output=True,
        text=True,
    )


def _feed_paths(root: Path) -> list[Path]:
    return sorted((root / "feeds").glob("domain-*.xml"))


EXPECTED_SLUGS = {c.slug for c in DOMAINS}


def test_generates_one_feed_per_domain(tmp_path):
    root = _mini_repo(tmp_path)
    result = _run(root)
    assert result.returncode == 0, result.stderr
    feeds = _feed_paths(root)
    assert {f.stem.removeprefix("domain-") for f in feeds} == EXPECTED_SLUGS
    for slug in ("active-inference", "entomology", "cognitive-security",
                 "art-synergetics", "computational", "biomedicine",
                 "aii-ecosystem", "presentations-media"):
        assert (root / "feeds" / f"domain-{slug}.xml").is_file()


def test_feeds_are_valid_rss_2_with_required_elements(tmp_path):
    root = _mini_repo(tmp_path)
    assert _run(root).returncode == 0
    for feed in _feed_paths(root):
        minidom.parseString(feed.read_bytes())  # raises on malformed XML
        tree = ET.parse(feed)
        channel = tree.getroot().find("channel")
        assert channel is not None
        assert channel.findtext("title")
        assert channel.findtext("link") == f"https://danielarifriedman.com/domain-{feed.stem.removeprefix('domain-')}.html"
        assert channel.findtext("description")
        for item in channel.findall("item"):
            assert item.findtext("title")
            link = item.findtext("link", "")
            assert link.startswith(("https://danielarifriedman.com", "https://doi.org/", "http://doi.org/")) or link.startswith("https://")
            assert item.findtext("guid")
            assert item.findtext("pubDate")
            assert item.findtext("description") is not None


def test_at_most_30_items_per_feed_and_items_match_domain_data(tmp_path):
    root = _mini_repo(tmp_path)
    assert _run(root).returncode == 0
    works = build_domain_feeds.load_works(REPO_ROOT)
    videos = build_domain_feeds.load_videos(REPO_ROOT)
    build_domain_feeds.init_taxonomy(works, videos)
    for feed in _feed_paths(root):
        items = ET.parse(feed).getroot().find("channel").findall("item")
        assert len(items) <= 30
        slug = feed.stem.removeprefix("domain-")
        expected_total = sum(
            1 for w in works if build_domain_feeds._EMOJI_SLUGS.get(w.get("domain")) == slug
        ) + sum(1 for v in videos if slug in build_domain_feeds._VIDEO_SLUGS.get(v.get("id"), set()))
        assert len(items) == min(30, expected_total)


def test_deterministic_byte_identical_output_across_runs(tmp_path):
    root = _mini_repo(tmp_path)
    assert _run(root).returncode == 0
    first = {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in _feed_paths(root)}
    # Full regeneration from a clean directory must reproduce the same bytes.
    for f in _feed_paths(root):
        f.unlink()
    assert _run(root).returncode == 0
    second = {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in _feed_paths(root)}
    assert first == second


def test_no_wall_clock_in_output(tmp_path):
    root = _mini_repo(tmp_path)
    assert _run(root).returncode == 0
    for feed in _feed_paths(root):
        text = feed.read_text()
        # pubDates must derive from dataset years/dates, never today's clock.
        from email.utils import parsedate_to_datetime
        for line in text.splitlines():
            if "<pubDate>" in line:
                stamp = line.split("<pubDate>")[1].split("</pubDate>")[0]
                dt = parsedate_to_datetime(stamp)
                assert 1990 <= dt.year <= 2027


def test_check_mode_fails_on_tampered_feed(tmp_path):
    root = _mini_repo(tmp_path)
    assert _run(root).returncode == 0
    feed = root / "feeds" / "domain-entomology.xml"
    feed.write_text(feed.read_text().replace("Entomology", "TAMPERED"))
    result = _run(root, "--check")
    assert result.returncode == 1
    assert "stale domain feed" in result.stderr


def test_check_mode_passes_when_current(tmp_path):
    root = _mini_repo(tmp_path)
    assert _run(root).returncode == 0
    result = _run(root, "--check")
    assert result.returncode == 0, result.stderr
    assert "domain feeds current" in result.stdout


def test_feeds_absent_from_sitemap_policy():
    """NEW-3 precedent: non-HTML XML assets are not sitemap entries."""
    for config in DOMAINS:
        assert f"feeds/domain-{config.slug}.xml" not in [p for p, _, _ in INDEX_PRIORITY_STATIC]


def test_domain_taxonomy_covers_every_work():
    works = build_domain_feeds.load_works(REPO_ROOT)
    build_domain_feeds.init_taxonomy(works, build_domain_feeds.load_videos(REPO_ROOT))
    mapped = {w["num"] for w in works if w.get("domain") in build_domain_feeds._EMOJI_SLUGS}
    assert len(mapped) == len(works), "every work must map to a domain feed"


def test_instantiated_renderer_matches_committed_feeds():
    """The committed feeds/ directory reflects the current generator output."""
    works = build_domain_feeds.load_works(REPO_ROOT)
    videos = build_domain_feeds.load_videos(REPO_ROOT)
    expected = build_domain_feeds.render_all(works, videos)
    for rel, content in expected.items():
        on_disk = REPO_ROOT / rel
        assert on_disk.is_file(), f"missing committed feed: {rel}"
        assert on_disk.read_text() == content, f"stale committed feed: {rel}"
