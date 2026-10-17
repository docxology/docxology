# AGENTS.md — `videos/`

Tracked public per-video HTML pages and the generated video index. Follow the
root repository instructions and source/iframe policies.

- Refresh approved YouTube metadata through `fetch_youtube_data.py`, then run
  `build_video_pages.py` through the ordered `regenerate_all.py` pipeline.
- Preserve public video IDs and existing inbound URLs; do not hand-edit HTML.
- Keep publication dates, upcoming-item exclusions, and incomplete fetches
  explicit. A failed refresh must preserve the prior cache.
- Review and commit authorized generated changes on a work branch, following
  the repository's validation and payload/control-tail publication sequence.
