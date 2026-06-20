from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ORCH_DIR = REPO_ROOT / "code" / "orchestrators"
sys.path.insert(0, str(ORCH_DIR))

import build_video_pages  # noqa: E402
from fetch_video_transcripts import transcript_from_vtt  # noqa: E402


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


def test_render_video_page_uses_local_page_and_youtube_embed(monkeypatch):
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
    monkeypatch.setattr(build_video_pages, "read_transcript", lambda _id: ("transcript body", "data/video-transcripts/abc123.txt"))
    html = build_video_pages.render_video_page(video)
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
