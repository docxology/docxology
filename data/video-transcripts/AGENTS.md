# AGENTS.md — `data/video-transcripts/`

Video transcripts used when building the video surfaces, named by YouTube video id and
refreshed by `code/orchestrators/fetch_video_transcripts.py`.

- Fetched content, not prose to edit: refresh through the fetcher so the snapshot stays
  attributable, and keep any caveat that came with it.
- The video-page generator and its tests (`code/tests/test_build_video_pages.py`) are
  the consumers; a missing transcript is a gap in a page, not a build failure.
- Listing first: the transcripts present are whatever the last fetch produced.

Repository rules: [root guide](../../AGENTS.md).
