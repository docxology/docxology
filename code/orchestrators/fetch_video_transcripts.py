#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import re
import subprocess
import tempfile
from pathlib import Path

from build_video_pages import REPO_ROOT, TRANSCRIPT_DIR, build_records


def clean_caption_line(line: str) -> str:
    line = re.sub(r"<\d{2}:\d{2}:\d{2}\.\d+>", " ", line)
    line = re.sub(r"</?c[^>]*>", " ", line)
    line = re.sub(r"<[^>]+>", " ", line)
    line = html.unescape(line)
    return re.sub(r"\s+", " ", line).strip()


def append_candidate(lines: list[str], candidate: str) -> None:
    if not candidate:
        return
    if lines:
        last = lines[-1]
        if candidate == last or candidate in last:
            return
        if last in candidate:
            lines[-1] = candidate
            return
        last_tokens = last.split()
        candidate_tokens = candidate.split()
        for size in range(min(len(last_tokens), len(candidate_tokens)), 1, -1):
            if last_tokens[-size:] == candidate_tokens[:size]:
                lines[-1] = " ".join(last_tokens + candidate_tokens[size:])
                return
    lines.append(candidate)


def transcript_from_vtt(text: str) -> str:
    lines: list[str] = []
    current: list[str] = []
    in_cue = False

    def flush() -> None:
        nonlocal current
        candidate = clean_caption_line(" ".join(current))
        append_candidate(lines, candidate)
        current = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            flush()
            in_cue = False
            continue
        if line == "WEBVTT" or line.startswith(("Kind:", "Language:", "NOTE")):
            continue
        if "-->" in line:
            flush()
            in_cue = True
            continue
        if in_cue and not line.isdigit():
            current.append(line)
    flush()
    return re.sub(r"\s+", " ", " ".join(lines)).strip()


def choose_vtt(path: Path) -> Path | None:
    candidates = sorted(path.glob("*.vtt"))
    if not candidates:
        return None
    preferred = [item for item in candidates if item.name.endswith(".en-orig.vtt")]
    preferred.extend(item for item in candidates if item.name.endswith(".en.vtt"))
    return preferred[0] if preferred else candidates[0]


def fetch_one(video: dict, *, force: bool, languages: str, timeout: int) -> str:
    out_path = TRANSCRIPT_DIR / f"{video['id']}.txt"
    if out_path.exists() and not force:
        return "skipped"
    with tempfile.TemporaryDirectory(prefix="docxology-youtube-transcript-") as tmp:
        tmp_path = Path(tmp)
        cmd = [
            "yt-dlp",
            "--skip-download",
            "--write-subs",
            "--write-auto-subs",
            "--sub-langs",
            languages,
            "--sub-format",
            "vtt",
            "--output",
            str(tmp_path / f"{video['id']}.%(ext)s"),
            video["youtube_url"],
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        vtt = choose_vtt(tmp_path)
        if vtt is None:
            if result.returncode not in (0, 1):
                return f"failed:{result.returncode}"
            return "unavailable"
        transcript = transcript_from_vtt(vtt.read_text(encoding="utf-8", errors="ignore"))
        if not transcript:
            return "empty"
        TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)
        out_path.write_text(transcript + "\n", encoding="utf-8")
        return "written"


def selected_videos(channel: str, video_id: str, limit: int | None) -> list[dict]:
    videos = build_records()["videos"]
    if channel != "all":
        videos = [video for video in videos if video["channel"] == channel]
    if video_id:
        videos = [video for video in videos if video["id"] == video_id]
    videos = sorted(videos, key=lambda item: item["upload_date"], reverse=True)
    return videos[:limit] if limit else videos


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch YouTube captions into data/video-transcripts/*.txt")
    parser.add_argument("--channel", choices=["all", "personal", "institute"], default="all")
    parser.add_argument("--video-id", default="")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--sub-langs", default="en.*")
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()

    counts: dict[str, int] = {}
    videos = selected_videos(args.channel, args.video_id, args.limit or None)
    for index, video in enumerate(videos, 1):
        status = fetch_one(video, force=args.force, languages=args.sub_langs, timeout=args.timeout)
        counts[status] = counts.get(status, 0) + 1
        print(f"[{index}/{len(videos)}] {video['id']} {status} {video['title']}")
    print("summary", counts)


if __name__ == "__main__":
    main()
