# AGENTS.md — `code/data/`

JSON inputs consumed by site code rather than published directly: the two YouTube
datasets (`youtube_institute.json`, `youtube_personal.json`) that
`code/orchestrators/build_video_pages.py` builds the video surfaces from, with
`fetch_youtube_data.py` refreshing them.

- These are fetched data, not sources: refresh them through the fetcher so the snapshot
  stays dated, and keep the caveat when fresh data is unavailable rather than
  substituting hand-written records.
- Their tests live in `code/tests/test_fetch_youtube_data.py`,
  `test_youtube_fetcher.py`, and `test_build_video_pages.py`.
- Nothing validates the committed JSON itself; an unexpected shape surfaces in the
  generator that reads it.

Repository rules: [root guide](../../AGENTS.md).
