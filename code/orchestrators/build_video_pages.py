#!/usr/bin/env python3
"""Build `videos/*.html` plus `data/videos.json` and `data/videos-index.json`.

Sources: cached YouTube channel payloads (`code/data/youtube_*.json`), the
transcript cache (`data/video-transcripts/*.txt`), `data/works.json`, and
`data/work-enrichment.json`.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from pathlib import PurePosixPath
from urllib.parse import quote_plus

REPO_ROOT = Path(__file__).resolve().parents[2]
VIDEO_DIR = REPO_ROOT / "videos"
DATA_OUT = REPO_ROOT / "data" / "videos.json"
INDEX_OUT = REPO_ROOT / "data" / "videos-index.json"
PAGE_MANIFEST_OUT = REPO_ROOT / "data" / "video-pages-manifest.json"
TRANSCRIPT_DIR = REPO_ROOT / "data" / "video-transcripts"
VIDEO_PAGE_MARKER = "<!-- docxology:generated-video-page; ownership=video-pages-manifest -->"
VIDEO_PAGE_MANIFEST_VERSION = "VideoPages.v1"

sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
from generated_outputs import (  # noqa: E402
    generated_output_files,
    read_generated_output_text,
    safe_generated_output_path,
    stable_generated_output_timestamp,
    write_output_texts,
)
from site_nav import (  # noqa: E402
    BREADCRUMB_CSS,
    HEAD_EXTRAS,
    INTERACTIVE_SCRIPTS,
    MENU_ESC_SCRIPT,
    SITE_ORIGIN,
    breadcrumb_jsonld_script,
    clip_description,
    render_breadcrumb,
    render_nav,
    social_meta_tags,
)

try:
    from report_paths import generated_timestamp
except ImportError:
    from .report_paths import generated_timestamp


@dataclass(frozen=True)
class TopicRule:
    label: str
    url: str
    query: str
    keywords: tuple[str, ...]


CHANNEL_FILES = {
    "personal": REPO_ROOT / "code" / "data" / "youtube_personal.json",
    "institute": REPO_ROOT / "code" / "data" / "youtube_institute.json",
}

CHANNEL_META = {
    "personal": {
        "name": "Daniel Ari Friedman",
        "label": "Personal Channel",
        "url": "https://www.youtube.com/@danielarifriedman",
    },
    "institute": {
        "name": "Active Inference Institute",
        "label": "Active Inference Institute",
        "url": "https://www.youtube.com/@activeinference",
    },
}

TOPIC_RULES = [
    TopicRule(
        "Active Inference",
        "domain-active-inference.html",
        "active inference",
        (
            "active inference",
            "actinf",
            "free energy",
            "pymdp",
            "generative model",
            "markov blanket",
            "variational",
            "friston",
            "modelstream",
        ),
    ),
    TopicRule(
        "Cognitive Security",
        "domain-cognitive-security.html",
        "cognitive security",
        (
            "cognitive security",
            "cogsec",
            "disinformation",
            "information warfare",
            "propaganda",
            "influence",
            "security",
        ),
    ),
    TopicRule(
        "Entomology and Ants",
        "domain-entomology.html",
        "entomology ants",
        (
            "ant",
            "ants",
            "myrmecology",
            "entomology",
            "insect",
            "pheromone",
            "harvester",
            "colony",
        ),
    ),
    TopicRule(
        "Computational Methods",
        "domain-computational.html",
        "computational methods software",
        (
            "gnn",
            "generalized notation",
            "cerebrum",
            "p3if",
            "mdkv",
            "python",
            "software",
            "repository",
            "code",
            "llm",
            "agent",
            "ontology",
        ),
    ),
    TopicRule(
        "Biology and Medicine",
        "domain-biomedicine.html",
        "biology medicine",
        (
            "biology",
            "genome",
            "genetic",
            "medicine",
            "biomedicine",
            "microbiome",
            "phenotype",
            "epidemiology",
        ),
    ),
    TopicRule(
        "Art and Synergetics",
        "domain-art-synergetics.html",
        "art synergetics",
        (
            "art",
            "curio",
            "synergetics",
            "geometry",
            "nft",
            "drawing",
            "design",
            "fuller",
        ),
    ),
    TopicRule(
        "Education and Tutorials",
        "videos.html",
        "tutorial lecture education",
        (
            "tutorial",
            "lecture",
            "course",
            "education",
            "textbook",
            "seminar",
            "workshop",
            "class",
            "learning",
        ),
    ),
    TopicRule(
        "Research Practice",
        "cite-verify.html",
        "research verification reproducibility",
        (
            "research",
            "paper",
            "publication",
            "verification",
            "reproducible",
            "open science",
            "zenodo",
        ),
    ),
]

STOPWORDS = {
    "about",
    "after",
    "again",
    "also",
    "and",
    "are",
    "but",
    "for",
    "from",
    "into",
    "not",
    "the",
    "that",
    "this",
    "with",
    "you",
    "your",
}


def h(value: object) -> str:
    return html.escape(str(value), quote=True)


def page_filename(video: dict) -> str:
    return f"{video['channel']}-{video['id']}.html"


def youtube_url(video_id: str) -> str:
    return f"https://www.youtube.com/watch?v={video_id}"


def thumbnail_url(video_id: str) -> str:
    return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"


def iso_date(upload_date: str) -> str:
    """Convert a YYYYMMDD upload_date to YYYY-MM-DD, or '' if malformed."""
    if not isinstance(upload_date, str) or len(upload_date) != 8 or not upload_date.isdigit():
        return ""
    return f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"


def display_date(upload_date: str) -> str:
    return iso_date(upload_date)


def iso_duration(seconds: object) -> str | None:
    if not isinstance(seconds, (int, float)):
        return None
    total = max(0, int(seconds))
    hours, rem = divmod(total, 3600)
    minutes, secs = divmod(rem, 60)
    parts = "PT"
    if hours:
        parts += f"{hours}H"
    if minutes:
        parts += f"{minutes}M"
    if secs or parts == "PT":
        parts += f"{secs}S"
    return parts


def display_duration(seconds: object) -> str:
    if not isinstance(seconds, (int, float)):
        return "Unknown duration"
    total = max(0, int(seconds))
    hours, rem = divmod(total, 3600)
    minutes, secs = divmod(rem, 60)
    if hours:
        return f"{hours}h {minutes:02d}m {secs:02d}s"
    return f"{minutes}m {secs:02d}s"


def token_set(value: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9][a-z0-9-]{2,}", value.lower())
        if token not in STOPWORDS
    }


def infer_topics(video: dict) -> list[dict]:
    haystack = f"{video.get('title', '')} {video.get('description', '')}".lower()
    topics = []
    for rule in TOPIC_RULES:
        if any(keyword in haystack for keyword in rule.keywords):
            topics.append({"label": rule.label, "url": rule.url, "query": rule.query})
    if not topics and video.get("channel") == "institute":
        rule = TOPIC_RULES[0]
        topics.append({"label": rule.label, "url": rule.url, "query": rule.query})
    elif not topics:
        topics.append({"label": "Research Video Archive", "url": "videos.html", "query": "research video"})
    return topics[:5]


def read_transcript(video_id: str) -> tuple[str, str]:
    txt_path = TRANSCRIPT_DIR / f"{video_id}.txt"
    if txt_path.is_file():
        return txt_path.read_text(encoding="utf-8", errors="ignore").strip(), f"data/video-transcripts/{video_id}.txt"
    return "", ""


def load_channel_payloads() -> tuple[list[dict], dict]:
    videos: list[dict] = []
    meta: dict[str, dict] = {}
    for channel, path in CHANNEL_FILES.items():
        payload = json.loads(path.read_text(encoding="utf-8"))
        meta[channel] = payload.get("meta", {})
        for item in payload.get("videos", []):
            record = dict(item)
            record["channel"] = channel
            videos.append(record)
    videos.sort(key=lambda item: (item.get("upload_date", ""), item.get("id", "")))
    return videos, meta


def load_works() -> list[dict]:
    works_path = REPO_ROOT / "data" / "works.json"
    if not works_path.is_file():
        return []
    return json.loads(works_path.read_text(encoding="utf-8")).get("works", [])


def load_work_enrichments() -> dict[str, dict]:
    path = REPO_ROOT / "data" / "work-enrichment.json"
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8")).get("works", {})


def related_works(video: dict, works: list[dict], enrichments: dict[str, dict]) -> list[dict]:
    video_tokens = token_set(
        " ".join(
            [
                video.get("title", ""),
                " ".join(topic["label"] for topic in video.get("topics", [])),
                video.get("transcript_excerpt", ""),
            ]
        )
    )
    scored = []
    for work in works:
        enrich = enrichments.get(work.get("citation_key", ""), {})
        work_text = " ".join(
            str(part)
            for part in [
                work.get("title", ""),
                work.get("domain_name", ""),
                work.get("type", ""),
                work.get("venue", ""),
                " ".join(enrich.get("keywords", [])),
                " ".join(enrich.get("findings", [])),
                " ".join(enrich.get("methods", [])),
            ]
            if part
        )
        work_tokens = token_set(work_text)
        score = len(video_tokens & work_tokens)
        if video.get("channel") == "institute" and "active" in work_tokens and "inference" in work_tokens:
            score += 1
        if score <= 0:
            continue
        scored.append((score, work))
    scored.sort(key=lambda pair: (-pair[0], pair[1].get("year", 0), pair[1].get("title", "")))
    return [
        {
            "title": work["title"],
            "citation_key": work["citation_key"],
            "year": work["year"],
            "domain": work["domain_name"],
            "url": f"/works/{work['citation_key']}.html",
        }
        for _score, work in scored[:4]
    ]


def build_records(generated_at: str | None = None) -> dict:
    raw_videos, channel_snapshots = load_channel_payloads()
    works = load_works()
    enrichments = load_work_enrichments()
    records = []
    for raw in raw_videos:
        video_id = raw.get("id")
        if not video_id:
            # A payload record without an id cannot be addressed on the site;
            # skip it instead of crashing the whole build on a KeyError.
            print("WARNING: skipping video record with no id", file=sys.stderr)
            continue
        channel_key = raw.get("channel", "")
        channel_meta = CHANNEL_META.get(channel_key, {})
        transcript, transcript_path = read_transcript(video_id)
        transcript_excerpt = clip_description(transcript, 600) if transcript else ""
        video = {
            "id": video_id,
            "title": raw.get("title", ""),
            "channel": channel_key,
            "channel_name": channel_meta.get("name", channel_key),
            "channel_label": channel_meta.get("label", channel_key),
            "channel_url": channel_meta.get("url", ""),
            "upload_date": raw.get("upload_date", ""),
            "date": iso_date(raw.get("upload_date") or ""),
            "year": raw.get("year"),
            "duration": raw.get("duration"),
            "duration_text": display_duration(raw.get("duration")),
            "view_count": raw.get("view_count", 0),
            "youtube_url": youtube_url(video_id),
            "embed_url": f"https://www.youtube-nocookie.com/embed/{video_id}",
            "thumbnail_url": thumbnail_url(video_id),
            "page_path": f"videos/{page_filename(raw)}",
            "page_url": f"/videos/{page_filename(raw)}",
            "transcript_available": bool(transcript),
            "transcript_path": transcript_path,
            "transcript_excerpt": transcript_excerpt,
        }
        video["topics"] = infer_topics(video)
        video["related_pages"] = related_pages(video)
        video["related_works"] = related_works(video, works, enrichments)
        records.append(video)

    records.sort(key=lambda item: (item["upload_date"], item["id"]))
    counts = {
        "total": len(records),
        "personal": sum(1 for item in records if item["channel"] == "personal"),
        "institute": sum(1 for item in records if item["channel"] == "institute"),
        "with_transcripts": sum(1 for item in records if item["transcript_available"]),
    }
    return {
        "generated_at": generated_at or generated_timestamp(),
        "source_files": [str(path.relative_to(REPO_ROOT)) for path in CHANNEL_FILES.values()],
        "transcript_dir": "data/video-transcripts",
        "count": counts["total"],
        "channels": channel_snapshots,
        "counts": counts,
        "videos": records,
    }


def compact_index(payload: dict) -> dict:
    """Return the bounded projection used by the interactive timeline.

    ``data/videos.json`` remains the complete agent/download export, including
    inferred topics, related works, and transcript excerpts. The timeline only
    needs identity, chronology, channel metadata, and display counts, so it
    should not download detail-only fields on first paint.
    """
    fields = ("id", "title", "channel", "upload_date", "year", "duration", "view_count")
    videos = [{field: video.get(field) for field in fields} for video in payload.get("videos", [])]
    return {
        "schema_version": "VideoIndex.v1",
        "generated_at": payload.get("generated_at"),
        "source": "data/videos.json",
        "source_files": payload.get("source_files", []),
        "count": payload.get("count", len(videos)),
        "counts": payload.get("counts", {}),
        "channels": payload.get("channels", {}),
        "fields": list(fields),
        "detail_source": "data/videos.json",
        "videos": videos,
    }


def related_pages(video: dict) -> list[dict]:
    pages = [
        {"label": "Interactive video timeline", "url": "/videos.html"},
    ]
    if any(topic["label"] == "Computational Methods" for topic in video.get("topics", [])):
        pages.append({"label": "Software catalog", "url": "/software.html"})
    pages.append({"label": "Site search", "url": f"/search.html?q={quote_plus(video['title'])}"})
    seen = {item["url"] for item in pages}
    for topic in video.get("topics", []):
        url = "/" + topic["url"] if not topic["url"].startswith("/") else topic["url"]
        if url not in seen:
            seen.add(url)
            pages.append({"label": topic["label"], "url": url})
        search_url = f"/search.html?q={quote_plus(topic['query'])}"
        if search_url not in seen:
            seen.add(search_url)
            pages.append({"label": f"Search: {topic['query']}", "url": search_url})
    return pages[:6]


def title_for_page(video: dict, max_len: int = 65) -> str:
    title = " ".join(video["title"].split())
    if len(title) <= max_len:
        if title == "We Three Pogo":
            return f"We Three Pogo ({video['date']})"
        return title

    parts = [p.strip() for p in title.split("~")]
    if len(parts) >= 3:
        short_parts = [re.sub(r"Active Inference", "ActInf", p) for p in parts]
        cand = " ~ ".join(short_parts)
        if len(cand) <= max_len:
            return cand

        p0 = short_parts[0]
        p_last = short_parts[-1]
        p_mids = short_parts[1:-1]
        p0_short = re.sub(r"Textbook Group", "TBG", p0)
        
        cand4 = f"{p0_short} ~ " + " ~ ".join(p_mids) + f" ~ {p_last}"
        if len(cand4) <= max_len:
            return cand4

        key_mid = ""
        for m in reversed(p_mids):
            if re.search(r"\b(session|chapter|lecture|part|pt)\b", m, re.I):
                key_mid = m
                break
        
        if key_mid:
            other_mids = [m for m in p_mids if m != key_mid]
            other_mid_str = f" ~ {other_mids[0]}" if other_mids else ""
            cand_key = f"{p0_short}{other_mid_str} ~ {key_mid}"
            if len(cand_key) <= max_len:
                return cand_key
            avail = max_len - len(f"{p0_short}{other_mid_str} ~ ")
            if avail >= 8:
                cut_k = key_mid[:avail - 1].rsplit(" ", 1)[0].rstrip(" ,;:.–—-~\"'")
                return f"{p0_short}{other_mid_str} ~ {cut_k}…"

        p_mid_all = " ~ ".join(p_mids)
        avail_mid = max_len - len(p0) - len(p_last) - 6
        if avail_mid >= 8:
            cut_mid = p_mid_all[:avail_mid - 1].rsplit(" ", 1)[0].rstrip(" ,;:.–—-~\"'")
            return f"{p0} ~ {cut_mid}… ~ {p_last}"
        elif len(p0) + len(p_last) + 3 <= max_len:
            return f"{p0} ~ {p_last}"

    elif len(parts) == 2:
        p0 = re.sub(r"Active Inference", "ActInf", parts[0])
        p_rest = parts[1]
        avail_rest = max_len - len(p0) - 3
        if avail_rest >= 15:
            cut = p_rest[:avail_rest - 1].rsplit(" ", 1)[0].rstrip(" ,;:.–—-~\"'")
            if not cut:
                cut = p_rest[:avail_rest - 1]
            cand = f"{p0} ~ {cut}…"
            if len(cand) <= max_len:
                return cand
        elif avail_rest >= 5:
            cut = p_rest[:avail_rest - 1].rstrip(" ,;:.–—-~\"'")
            cand = f"{p0} ~ {cut}…"
            if len(cand) <= max_len:
                return cand

    budget = max_len - 1
    head_len = int(budget * 0.55)
    tail_len = budget - head_len
    head = title[:head_len].rsplit(" ", 1)[0].rstrip(" ,;:.–—-~")
    tail = title[-tail_len:].split(" ", 1)[-1].lstrip(" ,;:.–—-~")
    cand = f"{head}…{tail}"
    if len(cand) > max_len:
        cand = cand[:max_len-1] + "…"
    return cand


def description_for_video(video: dict) -> str:
    topics = ", ".join(topic["label"] for topic in video.get("topics", [])[:3])
    return clip_description(
        f"Video metadata, YouTube link, related papers, and topic routes for {video['title']} ({video['channel_label']}, {video['date']}). Topics: {topics}.",
        155,
    )


def breadcrumb_trail(video: dict) -> list[tuple[str, str]]:
    return [("Home", ""), ("Videos", "videos/"), (video["title"], video["page_path"])]


def video_json_ld(video: dict, transcript: str) -> str:
    payload = {
        "@context": "https://schema.org",
        "@type": "VideoObject",
        "@id": SITE_ORIGIN + video["page_path"] + "#video",
        "name": video["title"],
        "description": description_for_video(video),
        "thumbnailUrl": [video["thumbnail_url"]],
        "uploadDate": video["date"],
        "duration": iso_duration(video.get("duration")),
        "embedUrl": video["embed_url"],
        "contentUrl": video["youtube_url"],
        "url": SITE_ORIGIN + video["page_path"],
        "publisher": {
            "@type": "Organization" if video["channel"] == "institute" else "Person",
            "name": video["channel_name"],
            "url": video["channel_url"],
        },
        "keywords": [topic["label"] for topic in video.get("topics", [])],
        "isPartOf": {"@id": SITE_ORIGIN + "videos.html#collection"},
    }
    if transcript:
        payload["transcript"] = clip_description(transcript, 5000)
    return json.dumps({key: value for key, value in payload.items() if value}, indent=4, ensure_ascii=False)


def transcript_html(transcript: str, video: dict) -> str:
    if not transcript:
        return (
            "<p>Caption transcript text has not been cached in this repository for this video. "
            f'<a href="{h(video["youtube_url"])}">Open the YouTube page</a> for any captions YouTube exposes.</p>'
        )
    chunks = []
    words = transcript.split()
    for i in range(0, len(words), 140):
        chunks.append(" ".join(words[i : i + 140]))
    return "\n".join(f"<p>{h(chunk)}</p>" for chunk in chunks)


def render_video_page(video: dict, *, transcript: str | None = None) -> str:
    """Render one video detail page from its record and optional cached text.

    Supplying ``transcript`` keeps the renderer a deterministic content
    projection for callers that have already loaded the cache.  The production
    build keeps the existing convenience behavior and reads the cached text
    when no explicit value is supplied.
    """
    if transcript is None:
        transcript, _path = read_transcript(video["id"])
    title = title_for_page(video)
    description = description_for_video(video)
    topics = "\n".join(
        f'<a class="pill" href="../{h(topic["url"])}">{h(topic["label"])}</a>' for topic in video.get("topics", [])
    )
    related_pages = "\n".join(
        f'<li><a href="..{h(page["url"])}">{h(page["label"])}</a></li>' for page in video.get("related_pages", [])
    )
    related_works = "\n".join(
        f'<li><a href="..{h(work["url"])}">{h(work["title"])}</a><span class="muted"> - {h(work["year"])} - {h(work["domain"])}</span></li>'
        for work in video.get("related_works", [])
    ) or '<li class="muted">No direct work match inferred from the current title metadata.</li>'
    breadcrumb = breadcrumb_trail(video)
    json_ld = video_json_ld(video, transcript)
    return f"""<!DOCTYPE html>
{VIDEO_PAGE_MARKER}
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{h(title)}</title>
    <meta name="description" content="{h(description)}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{h(SITE_ORIGIN + video['page_path'])}">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="manifest" href="/manifest.json">
    <link rel="alternate" type="application/json" href="/data/videos.json" title="Video metadata JSON">
{HEAD_EXTRAS}
    <meta property="og:type" content="video.other">
    <meta property="og:title" content="{h(title)}">
    <meta property="og:description" content="{h(description)}">
    <meta property="og:url" content="{h(SITE_ORIGIN + video['page_path'])}">
    <meta property="og:image" content="{h(video['thumbnail_url'])}">
    <meta property="og:image:width" content="480">
    <meta property="og:image:height" content="360">
{social_meta_tags(title, description, video['thumbnail_url'], image_alt=title)}
    <link rel="stylesheet" href="../style.css?v=newspaper-glitch-20260530c">
    <style>{BREADCRUMB_CSS}</style>
    <style>
        .video-layout{{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(260px,.6fr);gap:1.25rem;align-items:start}}
        .video-embed{{aspect-ratio:16/9;background:var(--bg-card);border:1px solid var(--border);border-radius:8px;overflow:hidden}}
        .video-embed iframe{{width:100%;height:100%;border:0}}
        .meta-list{{display:grid;gap:.55rem;margin:0;padding:0;list-style:none}}
        .meta-list li{{border-bottom:1px solid var(--border);padding-bottom:.45rem;color:var(--text-secondary)}}
        .meta-list strong{{color:var(--text-primary)}}
        .pill-row{{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:.75rem}}
        .pill{{border:1px solid var(--border);border-radius:999px;padding:.38rem .65rem;background:var(--bg-card);font-size:.82rem}}
        .link-list{{line-height:1.7}}
        .transcript{{max-height:38rem;overflow:auto;border:1px solid var(--border);border-radius:8px;background:var(--bg-card);padding:1rem}}
        .transcript p{{color:var(--text-secondary);line-height:1.65;margin:0 0 .9rem}}
        @media (max-width: 820px){{.video-layout{{grid-template-columns:1fr}}}}
    </style>
    <script type="application/ld+json">
{json_ld}
    </script>
{breadcrumb_jsonld_script(breadcrumb)}
</head>
<body>
    <a href="#main" class="skip-link">Skip to main content</a>
{render_nav(active="videos", depth=1)}
{render_breadcrumb(breadcrumb, depth=1)}
    <header class="page-hero">
        <p class="eyebrow">{h(video['channel_label'])}</p>
        <h1>{h(video['title'])}</h1>
        <p class="sub">{h(video['date'])} - {h(video['duration_text'])} - {h(video['view_count'])} recorded YouTube views in the cached snapshot.</p>
        <div class="pill-row">{topics}</div>
    </header>
    <main id="main" class="main">
        <section class="section video-layout">
            <div>
                <div class="video-embed">
                    <iframe src="{h(video['embed_url'])}" title="{h(video['title'])}" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
                </div>
                <p class="section-note"><a href="{h(video['youtube_url'])}">Open on YouTube</a> - <a href="{h(video['channel_url'])}">{h(video['channel_label'])}</a> - <a href="../videos.html">interactive timeline</a></p>
            </div>
            <aside class="card">
                <h2>Metadata</h2>
                <ul class="meta-list">
                    <li><strong>Video ID:</strong> {h(video['id'])}</li>
                    <li><strong>Channel:</strong> {h(video['channel_name'])}</li>
                    <li><strong>Upload date:</strong> {h(video['date'])}</li>
                    <li><strong>Duration:</strong> {h(video['duration_text'])}</li>
                    <li><strong>Transcript cached:</strong> {'yes' if transcript else 'no'}</li>
                </ul>
            </aside>
        </section>
        <section class="section">
            <div class="section-header"><h2>Related Site Routes</h2><p>Internal links that connect this video to topical pages, site search, and the broader research graph.</p><div class="section-divider"></div></div>
            <ul class="link-list">{related_pages}</ul>
        </section>
        <section class="section">
            <div class="section-header"><h2>Related Works</h2><p>Bibliography entries inferred from the video title, topic tags, and cached transcript excerpt when present.</p><div class="section-divider"></div></div>
            <ul class="link-list">{related_works}</ul>
        </section>
        <section class="section">
            <div class="section-header"><h2>Transcript</h2><p>Cached caption text when YouTube exposes captions and the transcript fetcher has been run.</p><div class="section-divider"></div></div>
            <div class="transcript">{transcript_html(transcript, video)}</div>
        </section>
    </main>
    <footer role="contentinfo"><div class="footer-rule" aria-hidden="true"></div><p>Daniel Ari Friedman, PhD - <a href="../videos/">Video index</a> - <a href="../data/videos.json">video metadata JSON</a></p></footer>
""" + INTERACTIVE_SCRIPTS + "\n" + MENU_ESC_SCRIPT + """</body>
</html>
"""


# Crawler-visible static floor for videos/index.html: only the newest N video
# rows are server-rendered into <ol class="video-list">.  The complete list
# remains crawlable through the inline ItemList JSON-LD (one itemListElement per
# video) and the bounded remainder ships in a compact inline JSON payload that
# js/videos-page.js renders on demand ("Show more").  URLs never change.
VIDEO_SSR_FLOOR_ROWS = 50


def video_list_item_fields(video: dict) -> tuple[str, str, str]:
    """(url, title, muted-meta) exactly as the static <li> renders them."""
    url = page_filename(video)
    title = video["title"]
    meta = " - ".join(
        [
            video["date"],
            video["channel_label"],
            ", ".join(topic["label"] for topic in video["topics"][:3]),
        ]
    )
    return url, title, meta


def render_index(payload: dict) -> str:
    videos = sorted(payload["videos"], key=lambda item: item["upload_date"], reverse=True)
    counts = payload["counts"]
    topic_links = "\n".join(
        f'<a class="pill" href="../{h(rule.url)}">{h(rule.label)}</a>' for rule in TOPIC_RULES[:8]
    )
    # Server-render only the floor; the rest rides in a compact inline payload.
    rows = "\n".join(
        f"""<li>
            <a href="{h(video_list_item_fields(video)[0])}">{h(video['title'])}</a>
            <span class="muted"> - {h(video_list_item_fields(video)[2])}</span>
        </li>"""
        for video in videos[:VIDEO_SSR_FLOOR_ROWS]
    )
    tail_payload = [
        {"u": url, "t": title, "m": meta}
        for url, title, meta in (video_list_item_fields(video) for video in videos[VIDEO_SSR_FLOOR_ROWS:])
    ]
    item_list = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "@id": SITE_ORIGIN + "videos/#itemlist",
        "name": "YouTube Video Landing Pages",
        "numberOfItems": counts["total"],
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": idx + 1,
                "url": SITE_ORIGIN + video["page_path"],
                "name": video["title"],
            }
            for idx, video in enumerate(videos)
        ],
    }
    title = "YouTube Video Index | Daniel Ari Friedman & AII"
    description = (
        f"Index of {counts['total']} YouTube videos from Daniel Ari Friedman and the Active Inference Institute, "
        "linked to topics, papers, software, and transcripts when cached."
    )
    breadcrumb = [("Home", ""), ("Videos", "videos/")]
    return f"""<!DOCTYPE html>
{VIDEO_PAGE_MARKER}
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{h(title)}</title>
    <meta name="description" content="{h(clip_description(description, 155))}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{SITE_ORIGIN}videos/">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="manifest" href="/manifest.json">
    <link rel="alternate" type="application/json" href="/data/videos.json" title="Video metadata JSON">
{HEAD_EXTRAS}
    <meta property="og:type" content="website">
    <meta property="og:title" content="{h(title)}">
    <meta property="og:description" content="{h(clip_description(description, 155))}">
    <meta property="og:url" content="{SITE_ORIGIN}videos/">
    <meta property="og:image" content="{SITE_ORIGIN}og-media.jpg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
{social_meta_tags(title, clip_description(description, 155), SITE_ORIGIN + "og-media.jpg", image_alt=title)}
    <link rel="stylesheet" href="../style.css?v=newspaper-glitch-20260530c">
    <style>{BREADCRUMB_CSS}</style>
    <style>
        .pill-row{{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:.75rem}}
        .pill{{border:1px solid var(--border);border-radius:999px;padding:.38rem .65rem;background:var(--bg-card);font-size:.82rem}}
        .video-list{{columns:2;column-gap:2rem;line-height:1.65}}
        .video-list li{{break-inside:avoid;margin-bottom:.45rem}}
        #video-show-more{{margin:.75rem 0 0}}
        @media (max-width: 760px){{.video-list{{columns:1}}}}
    </style>
    <script type="application/ld+json">
{json.dumps(item_list, separators=(",", ":"), ensure_ascii=False)}
    </script>
{breadcrumb_jsonld_script(breadcrumb)}
</head>
<body>
    <a href="#main" class="skip-link">Skip to main content</a>
{render_nav(active="videos", depth=1)}
{render_breadcrumb(breadcrumb, depth=1)}
    <header class="page-hero">
        <p class="eyebrow">YouTube Video Metadata</p>
        <h1>YouTube Video Index</h1>
        <p class="sub">{h(counts['total'])} videos: {h(counts['personal'])} personal channel videos and {h(counts['institute'])} Active Inference Institute videos. {h(counts['with_transcripts'])} have cached transcript text.</p>
        <div class="pill-row">{topic_links}</div>
    </header>
    <main id="main" class="main">
        <section class="section">
            <div class="section-header"><h2>Browse the Video Graph</h2><p>Every cached YouTube item has a stable page with VideoObject metadata, YouTube links, inferred topics, related works, and transcript text when available.</p><div class="section-divider"></div></div>
            <p><a href="../videos.html">Open the interactive timeline</a> or use <a href="../search.html?q=active%20inference%20videos">site search</a> to cross-search videos, works, software, and claims.</p>
        </section>
        <section class="section">
            <div class="section-header"><h2>All Video Pages</h2><p>Newest first; titles link to local indexable landing pages, not directly out to YouTube.</p><div class="section-divider"></div></div>
            <ol class="video-list">{rows}</ol>
            <noscript><p class="muted">The complete list of {counts['total']} video pages, including the {len(tail_payload)} newest entries not shown above, is available in the <a href="../data/videos.json">video metadata JSON</a> and via the page's ItemList structured data.</p></noscript>
        </section>
    </main>
    <footer role="contentinfo"><div class="footer-rule" aria-hidden="true"></div><p>Daniel Ari Friedman, PhD - <a href="../videos.html">timeline</a> - <a href="../data/videos.json">video metadata JSON</a></p></footer>
""" + INTERACTIVE_SCRIPTS + "\n" + MENU_ESC_SCRIPT + f"""
<script type="application/json" id="video-tail-payload">{json.dumps(tail_payload, separators=(",", ":"), ensure_ascii=False)}</script>
<script src="/js/videos-index.js?v=20260827" defer></script>
</body>
</html>
"""


def existing_generated_at() -> str | None:
    content = read_generated_output_text(REPO_ROOT, DATA_OUT)
    if content is None:
        return None
    try:
        return json.loads(content).get("generated_at")
    except json.JSONDecodeError:
        return None


def _validate_page_manifest_path(value: object) -> str:
    """Return one safe, direct ``videos/*.html`` manifest path.

    The manifest is an ownership record, so it must not be able to nominate an
    arbitrary file elsewhere in the repository as generator-managed.
    """
    if not isinstance(value, str) or not value:
        raise ValueError("video-page manifest paths must be non-empty strings")
    if "\\" in value:
        raise ValueError(f"video-page manifest path must use '/' separators: {value!r}")
    path = PurePosixPath(value)
    if path.is_absolute() or len(path.parts) != 2 or path.parts[0] != "videos":
        raise ValueError(f"video-page manifest path must be a direct videos/*.html path: {value!r}")
    if path.suffix != ".html" or path.name in {"", ".", ".."}:
        raise ValueError(f"video-page manifest path must name an HTML page: {value!r}")
    return path.as_posix()


def expected_video_page_paths(rendered_outputs: dict[Path, str], *, repo_root: Path = REPO_ROOT) -> set[str]:
    """Return all video HTML outputs from a rendered mapping as safe paths."""
    paths: set[str] = set()
    for path in rendered_outputs:
        try:
            relative = path.relative_to(repo_root).as_posix()
        except ValueError as exc:
            raise ValueError(f"video output escapes repository root: {path}") from exc
        if relative.startswith("videos/") and path.suffix == ".html":
            paths.add(_validate_page_manifest_path(relative))
    return paths


def render_video_page_manifest(paths: set[str]) -> str:
    """Render the stable ownership manifest for generated video HTML pages."""
    payload = {
        "schema_version": VIDEO_PAGE_MANIFEST_VERSION,
        "pages": sorted(_validate_page_manifest_path(path) for path in paths),
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def load_video_page_manifest(path: Path, *, repo_root: Path = REPO_ROOT) -> tuple[set[Path], list[str]]:
    """Load prior generator-owned pages without treating malformed data as safe.

    The return is intentionally an error list rather than a silent empty set:
    check mode must fail closed if its ownership ledger has been corrupted.
    """
    content = read_generated_output_text(repo_root, path)
    if content is None:
        return set(), []
    try:
        payload = json.loads(content)
    except json.JSONDecodeError as exc:
        return set(), [f"invalid video-page manifest {path}: {exc}"]
    if not isinstance(payload, dict) or payload.get("schema_version") != VIDEO_PAGE_MANIFEST_VERSION:
        return set(), [f"invalid video-page manifest schema: {path}"]
    entries = payload.get("pages")
    if not isinstance(entries, list):
        return set(), [f"invalid video-page manifest pages list: {path}"]

    owned: set[Path] = set()
    errors: list[str] = []
    for value in entries:
        try:
            relative = _validate_page_manifest_path(value)
        except ValueError as exc:
            errors.append(f"invalid video-page manifest entry: {exc}")
            continue
        candidate = safe_generated_output_path(repo_root, repo_root / relative)
        if candidate in owned:
            errors.append(f"duplicate video-page manifest entry: {relative}")
        owned.add(candidate)
    return owned, errors


_LEGACY_VIDEO_FILENAME = re.compile(r"^(?:personal|institute)-[A-Za-z0-9_-]{3,}\.html$")
_LEGACY_VIDEO_FINGERPRINTS = (
    '<meta name="description" content="Video metadata, YouTube link, related papers, and topic routes for ',
    'class="video-embed"',
    '<strong>Video ID:</strong>',
    'href="../data/videos.json"',
)


def is_legacy_generated_video_page(path: Path, content: str) -> bool:
    """Recognize pre-manifest generator output without claiming arbitrary pages.

    Existing committed video pages predate the explicit ownership marker.  The
    narrow filename rule plus four renderer-specific fragments permits a safe
    one-way migration: only a page that is clearly this generator's old output
    becomes subject to orphan checking.  Hand-authored editorial pages are
    neither named nor structured this way and are left untouched.
    """
    return bool(_LEGACY_VIDEO_FILENAME.fullmatch(path.name)) and all(
        fragment in content for fragment in _LEGACY_VIDEO_FINGERPRINTS
    )


def generated_video_page_orphans(
    expected_paths: set[str],
    *,
    video_dir: Path = VIDEO_DIR,
    manifest_path: Path = PAGE_MANIFEST_OUT,
    repo_root: Path = REPO_ROOT,
) -> tuple[tuple[Path, ...], tuple[str, ...]]:
    """Return managed video pages no longer produced, never deleting files.

    Ownership comes from three auditable sources: the previous explicit
    manifest, the current marker, and a conservative legacy fingerprint.  The
    function only reports drift; write mode intentionally leaves both orphaned
    generated output and unrelated manual pages on disk for reviewed cleanup.
    """
    owned, errors = load_video_page_manifest(manifest_path, repo_root=repo_root)
    for candidate in generated_output_files(repo_root, video_dir, "*.html"):
        content = read_generated_output_text(repo_root, candidate)
        if content is None:  # A concurrent deletion is ordinary stale state.
            continue
        if VIDEO_PAGE_MARKER in content or is_legacy_generated_video_page(candidate, content):
            owned.add(candidate)

    expected = {
        safe_generated_output_path(repo_root, repo_root / _validate_page_manifest_path(path))
        for path in expected_paths
    }
    orphans = tuple(
        sorted(
            (
                path
                for path in owned - expected
                if read_generated_output_text(repo_root, path) is not None
            ),
            key=lambda path: path.as_posix(),
        )
    )
    return orphans, tuple(sorted(errors))


def check_interactive_page_integrity(
    html_by_path: dict[Path, str],
    *,
    repo_root: Path = REPO_ROOT,
) -> tuple[str, ...]:
    """Every emitted page that loads interactive/tts scripts must link style.css.

    js/tts-controls.js, js/interactive.js, and js/menu-esc.js render UI whose
    CSS lives entirely in style.css. A page that loads any of those scripts
    without the shared stylesheet ships permanently expanded, unstyled
    controls (the P0-2 defect). Enforced at build time rather than as a
    post-hoc lint so every generator output is covered.
    """
    errors: list[str] = []
    interactive_markers = ("/js/interactive.js", "/js/tts-controls.js", "/js/menu-esc.js")
    for path, content in sorted(html_by_path.items(), key=lambda item: item[0].as_posix()):
        if not path.suffix == ".html":
            continue
        loads = any(marker in content for marker in interactive_markers)
        links_stylesheet = 'rel="stylesheet"' in content and "style.css" in content
        if loads and not links_stylesheet:
            relative = path.relative_to(repo_root).as_posix() if path.is_relative_to(repo_root) else path.as_posix()
            errors.append(
                f"{relative}: loads interactive JS without linking style.css "
                "(TTS panel / shortcuts overlay would render unstyled)"
            )
    return tuple(errors)


def outputs(generated_at: str | None = None) -> dict[Path, str]:
    payload = build_records(generated_at)
    index = compact_index(payload)
    out = {
        DATA_OUT: json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        INDEX_OUT: json.dumps(index, indent=2, ensure_ascii=False) + "\n",
        VIDEO_DIR / "index.html": render_index(payload),
    }
    for video in payload["videos"]:
        out[VIDEO_DIR / page_filename(video)] = render_video_page(video)
    out[PAGE_MANIFEST_OUT] = render_video_page_manifest(expected_video_page_paths(out))
    return out


def stale_video_outputs(
    rendered_outputs: dict[Path, str],
    *,
    repo_root: Path = REPO_ROOT,
    video_dir: Path = VIDEO_DIR,
    manifest_path: Path = PAGE_MANIFEST_OUT,
) -> tuple[str, ...]:
    """Return every byte-level output or owned-page orphan that check must flag."""
    stale: list[str] = []
    for path, content in rendered_outputs.items():
        try:
            relative = path.relative_to(repo_root).as_posix()
        except ValueError as exc:
            raise ValueError(f"video output escapes repository root: {path}") from exc
        actual = read_generated_output_text(repo_root, path)
        if actual != content:
            stale.append(relative)

    orphans, ownership_errors = generated_video_page_orphans(
        expected_video_page_paths(rendered_outputs, repo_root=repo_root),
        video_dir=video_dir,
        manifest_path=manifest_path,
        repo_root=repo_root,
    )
    stale.extend(
        f"orphaned generated video page: {path.relative_to(repo_root).as_posix()}"
        for path in orphans
    )
    stale.extend(ownership_errors)
    stale.extend(check_interactive_page_integrity(rendered_outputs, repo_root=repo_root))
    # Hand-authored root pages (art.html, videos.html, ...) are not generator
    # outputs, but they load the same interactive scripts. They are scanned
    # read-only so the same P0-2 invariant holds site-wide.
    public_root_pages: dict[Path, str] = {}
    for candidate in sorted(repo_root.glob("*.html")):
        try:
            text = candidate.read_text(encoding="utf-8")
        except OSError:
            continue
        public_root_pages[candidate] = text
    stale.extend(check_interactive_page_integrity(public_root_pages, repo_root=repo_root))
    return tuple(stale)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if generated video pages are stale")
    args = parser.parse_args()
    generated_at = existing_generated_at() if args.check else None
    if not args.check:
        candidate_outputs = outputs()
        generated_at = stable_generated_output_timestamp(
            REPO_ROOT,
            DATA_OUT,
            json.loads(candidate_outputs[DATA_OUT]),
        )
    rendered_outputs = outputs(generated_at)
    if args.check:
        stale = stale_video_outputs(rendered_outputs)
    else:
        stale = ()
        write_output_texts(rendered_outputs, repo_root=REPO_ROOT)
    if stale:
        raise SystemExit("Stale generated video artifacts: " + ", ".join(stale[:10]))
    print(("checked" if args.check else "wrote") + " video pages")


if __name__ == "__main__":
    main()
