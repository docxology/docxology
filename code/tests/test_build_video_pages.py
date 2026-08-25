from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
ORCH_DIR = REPO_ROOT / "code" / "orchestrators"
sys.path.insert(0, str(ORCH_DIR))
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

import build_video_pages  # noqa: E402
from fetch_video_transcripts import transcript_from_vtt  # noqa: E402
from generated_outputs import UnsafeGeneratedOutputPathError  # noqa: E402


def sample_video() -> dict:
    return {
        "id": "abc123",
        "title": "pymdp Active Inference ModelStream with GNN",
        "channel": "institute",
        "channel_name": "Active Inference Institute",
        "channel_label": "Active Inference Institute",
        "channel_url": "https://www.youtube.com/@activeinference",
        "upload_date": "20260601",
        "date": "2026-06-01",
        "year": 2026,
        "duration": 3600,
        "duration_text": "1h 00m 00s",
        "view_count": 42,
        "youtube_url": "https://www.youtube.com/watch?v=abc123",
        "embed_url": "https://www.youtube-nocookie.com/embed/abc123",
        "thumbnail_url": "https://img.youtube.com/vi/abc123/hqdefault.jpg",
        "page_path": "videos/institute-abc123.html",
        "page_url": "/videos/institute-abc123.html",
        "transcript_available": True,
        "transcript_path": "data/video-transcripts/abc123.txt",
        "transcript_excerpt": "Active inference transcript text.",
    }


def test_infer_topics_links_active_inference_and_computational_methods():
    topics = build_video_pages.infer_topics(sample_video())
    labels = {topic["label"] for topic in topics}
    assert "Active Inference" in labels
    assert "Computational Methods" in labels


def test_related_pages_adds_software_for_computational_video():
    video = sample_video()
    video["topics"] = build_video_pages.infer_topics(video)
    urls = {page["url"] for page in build_video_pages.related_pages(video)}
    assert "/software.html" in urls
    assert "/videos.html" in urls


def test_compact_video_index_excludes_detail_only_metadata():
    payload = {
        "generated_at": "2026-07-18T00:00:00Z",
        "source_files": ["code/data/youtube_personal.json"],
        "count": 1,
        "counts": {"total": 1, "personal": 1, "institute": 0, "with_transcripts": 0},
        "channels": {"personal": {"fetched_at": "2026-07-17T00:00:00Z"}},
        "videos": [{
            "id": "abc123",
            "title": "Example",
            "channel": "personal",
            "upload_date": "20260717",
            "year": 2026,
            "duration": 42,
            "view_count": 7,
            "topics": [{"label": "Research"}],
            "related_works": [{"citation_key": "Example2026"}],
            "transcript_excerpt": "detail text",
        }],
    }
    index = build_video_pages.compact_index(payload)
    assert index["schema_version"] == "VideoIndex.v1"
    assert index["detail_source"] == "data/videos.json"
    assert index["videos"] == [{
        "id": "abc123",
        "title": "Example",
        "channel": "personal",
        "upload_date": "20260717",
        "year": 2026,
        "duration": 42,
        "view_count": 7,
    }]


def test_timeline_runtime_uses_compact_index_not_raw_channel_exports():
    runtime = (REPO_ROOT / "js" / "videos-page.js").read_text(encoding="utf-8")
    assert "data/videos-index.json" in runtime
    assert "code/data/youtube_personal.json" not in runtime
    assert "code/data/youtube_institute.json" not in runtime


def test_orphan_check_tracks_generator_owned_pages_but_leaves_manual_video_pages_unowned(tmp_path: Path):
    video_dir = tmp_path / "videos"
    data_dir = tmp_path / "data"
    video_dir.mkdir()
    data_dir.mkdir()
    expected = {"videos/index.html", "videos/personal-abc123.html"}
    manifest_path = data_dir / "video-pages-manifest.json"
    # The manifest intentionally retains a page from a previous source
    # snapshot. Its contents may have been manually altered, but its ownership
    # remains generator-derived and therefore must be reported rather than
    # deleted during a write run.
    manifest_path.write_text(
        build_video_pages.render_video_page_manifest(expected | {"videos/institute-retired.html"}),
        encoding="utf-8",
    )
    for relative in expected:
        (tmp_path / relative).write_text(build_video_pages.VIDEO_PAGE_MARKER, encoding="utf-8")
    retired = video_dir / "institute-retired.html"
    retired.write_text("review before removal", encoding="utf-8")
    marker_orphan = video_dir / "personal-marked-orphan.html"
    marker_orphan.write_text(build_video_pages.VIDEO_PAGE_MARKER, encoding="utf-8")
    legacy_orphan = video_dir / "personal-legacy-orphan.html"
    legacy_orphan.write_text(
        "\n".join(build_video_pages._LEGACY_VIDEO_FINGERPRINTS), encoding="utf-8"
    )
    hand_authored = video_dir / "editorial-note.html"
    original_hand_authored = "# Hand-authored video notes\n"
    hand_authored.write_text(original_hand_authored, encoding="utf-8")

    orphans, errors = build_video_pages.generated_video_page_orphans(
        expected,
        video_dir=video_dir,
        manifest_path=manifest_path,
        repo_root=tmp_path,
    )

    assert errors == ()
    assert set(orphans) == {retired, marker_orphan, legacy_orphan}
    assert hand_authored not in orphans
    # Detection is strictly observational; cleanup requires an explicit review
    # and a separate destructive operation.
    assert retired.read_text(encoding="utf-8") == "review before removal"
    assert hand_authored.read_text(encoding="utf-8") == original_hand_authored


def test_check_mode_reports_an_orphan_without_rewriting_any_video_page(tmp_path: Path):
    video_dir = tmp_path / "videos"
    data_dir = tmp_path / "data"
    video_dir.mkdir()
    data_dir.mkdir()
    expected_pages = {"videos/index.html", "videos/personal-abc123.html"}
    manifest_path = data_dir / "video-pages-manifest.json"
    rendered = {
        tmp_path / "videos" / "index.html": build_video_pages.VIDEO_PAGE_MARKER,
        tmp_path / "videos" / "personal-abc123.html": build_video_pages.VIDEO_PAGE_MARKER,
        manifest_path: build_video_pages.render_video_page_manifest(expected_pages),
    }
    for path, content in rendered.items():
        path.write_text(content, encoding="utf-8")
    orphan = video_dir / "institute-retired.html"
    original = build_video_pages.VIDEO_PAGE_MARKER + "\nretired output\n"
    orphan.write_text(original, encoding="utf-8")

    stale = build_video_pages.stale_video_outputs(
        rendered,
        repo_root=tmp_path,
        video_dir=video_dir,
        manifest_path=manifest_path,
    )

    assert stale == ("orphaned generated video page: videos/institute-retired.html",)
    assert orphan.read_text(encoding="utf-8") == original


def test_video_check_rejects_a_symlinked_generated_output(tmp_path: Path):
    video_dir = tmp_path / "videos"
    video_dir.mkdir()
    outside = tmp_path / "outside.html"
    outside.write_text("outside must survive\n", encoding="utf-8")
    target = video_dir / "index.html"
    target.symlink_to(outside)

    with pytest.raises(UnsafeGeneratedOutputPathError):
        build_video_pages.stale_video_outputs(
            {target: build_video_pages.VIDEO_PAGE_MARKER},
            repo_root=tmp_path,
            video_dir=video_dir,
            manifest_path=tmp_path / "data" / "video-pages-manifest.json",
        )

    assert outside.read_text(encoding="utf-8") == "outside must survive\n"


def test_render_video_page_uses_local_page_and_youtube_embed():
    video = sample_video()
    video["topics"] = build_video_pages.infer_topics(video)
    video["related_pages"] = build_video_pages.related_pages(video)
    video["related_works"] = [
        {
            "title": "Generalized Notation Notation",
            "citation_key": "Friedman2026GNN",
            "year": 2026,
            "domain": "Computational",
            "url": "/works/Friedman2026GNN.html",
        }
    ]
    html = build_video_pages.render_video_page(video, transcript="transcript body")
    assert 'rel="canonical" href="https://danielarifriedman.com/videos/institute-abc123.html"' in html
    assert "https://www.youtube-nocookie.com/embed/abc123" in html
    assert "Generalized Notation Notation" in html
    assert '"@type": "VideoObject"' in html
    assert "transcript body" in html


def test_transcript_from_vtt_cleans_timestamps_and_duplicate_partials():
    vtt = (
        "WEBVTT\n"
        "Kind: captions\n"
        "Language: en\n\n"
        "00:00:01.000 --> 00:00:02.000\n"
        "active\n\n"
        "00:00:02.000 --> 00:00:03.000\n"
        "active<00:00:02.200><c> inference</c>\n\n"
        "00:00:03.000 --> 00:00:04.000\n"
        "active inference\n"
        "model\n"
    )
    text = transcript_from_vtt(vtt)
    assert "<" not in text
    assert "-->" not in text
    assert text == "active inference model"
