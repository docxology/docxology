#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote_plus

REPO_ROOT = Path(__file__).resolve().parents[2]
VIDEO_DIR = REPO_ROOT / "videos"
DATA_OUT = REPO_ROOT / "data" / "videos.json"
TRANSCRIPT_DIR = REPO_ROOT / "data" / "video-transcripts"

sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
from site_nav import (  # noqa: E402
    BREADCRUMB_CSS,
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
        channel_key = raw.get("channel", "")
        channel_meta = CHANNEL_META.get(channel_key, {})
        transcript, transcript_path = read_transcript(raw["id"])
        transcript_excerpt = clip_description(transcript, 600) if transcript else ""
        video = {
            "id": raw["id"],
            "title": raw.get("title", ""),
            "channel": channel_key,
            "channel_name": channel_meta.get("name", channel_key),
            "channel_label": channel_meta.get("label", channel_key),
            "channel_url": channel_meta.get("url", ""),
            "upload_date": raw.get("upload_date", ""),
            "date": iso_date(raw.get("upload_date", "00000000")),
            "year": raw.get("year"),
            "duration": raw.get("duration"),
            "duration_text": display_duration(raw.get("duration")),
            "view_count": raw.get("view_count", 0),
            "youtube_url": youtube_url(raw["id"]),
            "embed_url": f"https://www.youtube-nocookie.com/embed/{raw['id']}",
            "thumbnail_url": thumbnail_url(raw["id"]),
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


def title_for_page(video: dict) -> str:
    return clip_description(f"{video['title']} | {video['channel_label']}", 62)


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


def render_video_page(video: dict) -> str:
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
                    <iframe src="{h(video['embed_url'])}" title="{h(video['title'])}" loading="lazy" allowfullscreen></iframe>
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
</body>
</html>
"""


def render_index(payload: dict) -> str:
    videos = sorted(payload["videos"], key=lambda item: item["upload_date"], reverse=True)
    counts = payload["counts"]
    topic_links = "\n".join(
        f'<a class="pill" href="../{h(rule.url)}">{h(rule.label)}</a>' for rule in TOPIC_RULES[:8]
    )
    rows = "\n".join(
        f"""<li>
            <a href="{h(page_filename(video))}">{h(video['title'])}</a>
            <span class="muted"> - {h(video['date'])} - {h(video['channel_label'])} - {h(', '.join(topic['label'] for topic in video['topics'][:3]))}</span>
        </li>"""
        for video in videos
    )
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
        @media (max-width: 760px){{.video-list{{columns:1}}}}
    </style>
    <script type="application/ld+json">
{json.dumps(item_list, indent=4, ensure_ascii=False)}
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
        </section>
    </main>
    <footer role="contentinfo"><div class="footer-rule" aria-hidden="true"></div><p>Daniel Ari Friedman, PhD - <a href="../videos.html">timeline</a> - <a href="../data/videos.json">video metadata JSON</a></p></footer>
</body>
</html>
"""


def existing_generated_at() -> str | None:
    if not DATA_OUT.exists():
        return None
    try:
        return json.loads(DATA_OUT.read_text(encoding="utf-8")).get("generated_at")
    except json.JSONDecodeError:
        return None


def outputs(generated_at: str | None = None) -> dict[Path, str]:
    payload = build_records(generated_at)
    out = {
        DATA_OUT: json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        VIDEO_DIR / "index.html": render_index(payload),
    }
    for video in payload["videos"]:
        out[VIDEO_DIR / page_filename(video)] = render_video_page(video)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if generated video pages are stale")
    args = parser.parse_args()
    stale = []
    for path, content in outputs(existing_generated_at() if args.check else None).items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(str(path.relative_to(REPO_ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    if stale:
        raise SystemExit("Stale generated video artifacts: " + ", ".join(stale[:10]))
    print(("checked" if args.check else "wrote") + " video pages")


if __name__ == "__main__":
    main()
