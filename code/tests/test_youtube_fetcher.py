"""Unit tests for youtube_fetcher module."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

from docxology_tools import youtube_fetcher as yf  # noqa: E402

SAMPLE_JSONL_LINES = [
    json.dumps({
        "id": "abc123",
        "title": "Active Inference Tutorial #1",
        "upload_date": "20230415",
        "duration": 3600,
        "view_count": 500,
        "thumbnail": "https://img.youtube.com/vi/abc123/mqdefault.jpg",
    }),
    json.dumps({
        "id": "def456",
        "title": "Stream with no date",
        "duration": None,
        "view_count": 0,
    }),
    "not valid json {{",
    json.dumps({
        "id": "ghi789",
        "title": "Drawing Session",
        "upload_date": "20220101",
        "duration": 7200,
        "view_count": 1200,
    }),
]


class _RecordingExecutor:
    """Small local process seam for command construction and exit handling."""

    def __init__(self, *, returncode: int = 0, stdout: str = "", stderr: str = ""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        self.commands: list[list[str]] = []
        self.timeouts: list[int] = []

    def __call__(self, cmd: list[str], timeout: int) -> subprocess.CompletedProcess:
        self.commands.append(cmd)
        self.timeouts.append(timeout)
        return subprocess.CompletedProcess(cmd, self.returncode, self.stdout, self.stderr)


class TestParseJsonl(unittest.TestCase):
    def test_valid_lines(self):
        records = yf.parse_jsonl(SAMPLE_JSONL_LINES[:1])
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["id"], "abc123")

    def test_rejects_malformed(self):
        with self.assertRaisesRegex(ValueError, "malformed yt-dlp JSONL line 1"):
            yf.parse_jsonl(["not json", '{"id": "ok"}'])

    def test_empty_input(self):
        self.assertEqual(yf.parse_jsonl([]), [])

    def test_blank_lines_skipped(self):
        records = yf.parse_jsonl(["", "  ", '{"id": "x"}'])
        self.assertEqual(len(records), 1)

    def test_rejects_any_malformed_sample_line(self):
        with self.assertRaisesRegex(ValueError, "malformed yt-dlp JSONL line 3"):
            yf.parse_jsonl(SAMPLE_JSONL_LINES)


class TestNormalizeVideo(unittest.TestCase):
    FULL_RAW = {
        "id": "abc123",
        "title": "Test Video",
        "upload_date": "20230415",
        "duration": 3600,
        "view_count": 500,
    }

    def test_complete_record(self):
        v = yf.normalize_video(self.FULL_RAW, "personal")
        self.assertIsNotNone(v)
        self.assertEqual(v["id"], "abc123")
        self.assertEqual(v["year"], 2023)
        self.assertEqual(v["month"], 4)
        self.assertEqual(v["day"], 15)
        self.assertEqual(v["channel"], "personal")
        self.assertEqual(v["view_count"], 500)
        self.assertNotIn("thumbnail", v)

    def test_missing_upload_date_returns_none(self):
        raw = {**self.FULL_RAW, "upload_date": None}
        self.assertIsNone(yf.normalize_video(raw, "personal"))

    def test_absent_upload_date_returns_none(self):
        raw = {k: v for k, v in self.FULL_RAW.items() if k != "upload_date"}
        self.assertIsNone(yf.normalize_video(raw, "personal"))

    def test_null_duration_allowed(self):
        raw = {**self.FULL_RAW, "duration": None}
        v = yf.normalize_video(raw, "institute")
        self.assertIsNotNone(v)
        self.assertIsNone(v["duration"])

    def test_missing_view_count_defaults_to_zero(self):
        raw = {k: v for k, v in self.FULL_RAW.items() if k != "view_count"}
        v = yf.normalize_video(raw, "personal")
        self.assertIsNotNone(v)
        self.assertEqual(v["view_count"], 0)

    def test_missing_id_returns_none(self):
        raw = {k: v for k, v in self.FULL_RAW.items() if k != "id"}
        self.assertIsNone(yf.normalize_video(raw, "personal"))

    def test_impossible_calendar_date_returns_none(self):
        # Month 13 / day 40 is not a real date even though it is 8 digits.
        raw = {**self.FULL_RAW, "upload_date": "20231340"}
        self.assertIsNone(yf.normalize_video(raw, "personal"))

    def test_nonexistent_feb_29_returns_none(self):
        # 2023 is not a leap year, so 2023-02-29 does not exist.
        raw = {**self.FULL_RAW, "upload_date": "20230229"}
        self.assertIsNone(yf.normalize_video(raw, "personal"))


class TestRunYtDlp(unittest.TestCase):
    def test_full_mode_command(self):
        executor = _RecordingExecutor(stdout='{"id":"a"}\n')
        yf.run_yt_dlp("https://example.com/channel", mode="full", executor=executor)
        cmd = executor.commands[0]
        self.assertIn("--dump-json", cmd)
        self.assertIn("--no-download", cmd)
        self.assertNotIn("--flat-playlist", cmd)
        self.assertEqual(executor.timeouts, [600])

    def test_approximate_mode_command(self):
        executor = _RecordingExecutor(stdout='{"id":"a"}\n')
        yf.run_yt_dlp("https://example.com/channel", mode="approximate", executor=executor)
        cmd = executor.commands[0]
        self.assertIn("--flat-playlist", cmd)
        self.assertIn("--extractor-args", cmd)
        self.assertIn("youtubetab:approximate_date", cmd)

    def test_success_returns_lines(self):
        executor = _RecordingExecutor(stdout='{"id":"a"}\n{"id":"b"}\n')
        lines = yf.run_yt_dlp("https://example.com", executor=executor)
        self.assertEqual(lines, ['{"id":"a"}', '{"id":"b"}'])

    def test_non_zero_exit_raises(self):
        executor = _RecordingExecutor(returncode=2, stderr="error")
        with self.assertRaises(RuntimeError):
            yf.run_yt_dlp("https://example.com", executor=executor)

    def test_exit_code_1_is_a_failure_even_when_output_exists(self):
        executor = _RecordingExecutor(returncode=1, stdout='{"id":"x"}\n', stderr="unavailable item")
        with self.assertRaisesRegex(RuntimeError, "yt-dlp exited 1"):
            yf.run_yt_dlp("https://example.com", executor=executor)


class _JsonlRunner:
    """Real (non-mock) runner: serves pre-built JSONL per call, may raise.

    Fetch-channel tests exercise real parsing, deduplication, sorting, and
    tab-failure handling through the injected ``runner`` dependency.
    """

    def __init__(self, *groups):
        self.groups = groups
        self.calls: list[tuple[str, str]] = []

    def __call__(self, url: str, mode: str = "full") -> list[str]:
        self.calls.append((url, mode))
        idx = len(self.calls) - 1
        if idx < len(self.groups):
            group = self.groups[idx]
            if isinstance(group, BaseException):
                raise group
            return [json.dumps(r) for r in group]
        return []


class TestFetchChannel(unittest.TestCase):
    def test_deduplicates_across_tabs(self):
        vid_a = {"id": "aaa", "title": "A", "upload_date": "20230101", "duration": 60, "view_count": 1}
        vid_b = {"id": "bbb", "title": "B", "upload_date": "20230601", "duration": 60, "view_count": 1}
        # /videos returns A, /streams returns A+B (A is a duplicate), /shorts empty
        runner = _JsonlRunner([vid_a], [vid_a, vid_b], [])
        result = yf.fetch_channel_result("https://example.com/@ch", "personal", runner=runner)
        videos = result.videos
        self.assertTrue(result.complete)
        self.assertEqual(len(videos), 2)
        ids = [v["id"] for v in videos]
        self.assertIn("aaa", ids)
        self.assertIn("bbb", ids)

    def test_sorted_by_date(self):
        v1 = {"id": "a1", "title": "Old", "upload_date": "20200101", "duration": 60, "view_count": 0}
        v2 = {"id": "a2", "title": "New", "upload_date": "20240101", "duration": 60, "view_count": 0}
        runner = _JsonlRunner([v2], [v1], [])
        videos = yf.fetch_channel_result("https://example.com/@ch", "personal", runner=runner).videos
        self.assertEqual(videos[0]["id"], "a1")
        self.assertEqual(videos[1]["id"], "a2")

    def test_tab_failure_is_structured_and_marks_channel_incomplete(self):
        v = {"id": "ok", "title": "OK", "upload_date": "20230101", "duration": 60, "view_count": 0}
        runner = _JsonlRunner([v], RuntimeError("streams failed"), [])
        result = yf.fetch_channel_result("https://example.com/@ch", "personal", runner=runner)
        self.assertFalse(result.complete)
        self.assertEqual([video["id"] for video in result.videos], ["ok"])
        self.assertEqual(len(result.failures), 1)
        self.assertEqual(result.failures[0].tab, "streams")
        self.assertEqual(result.failures[0].error_type, "RuntimeError")
        self.assertEqual(result.as_dict()["tabs"][1]["failure"]["message"], "streams failed")

    def test_malformed_jsonl_is_a_structured_tab_failure(self):
        class MalformedRunner:
            def __call__(self, url: str, mode: str = "full") -> list[str]:
                if url.endswith("/videos"):
                    return ["not json"]
                return []

        result = yf.fetch_channel_result("https://example.com/@ch", "personal", runner=MalformedRunner())
        self.assertFalse(result.complete)
        self.assertEqual(result.failures[0].tab, "videos")
        self.assertEqual(result.failures[0].error_type, "ValueError")
        self.assertIn("malformed yt-dlp JSONL", result.failures[0].message)

    def test_channel_id_set_on_all_videos(self):
        v = {"id": "x", "title": "T", "upload_date": "20230101", "duration": 60, "view_count": 0}
        runner = _JsonlRunner([v], [], [])
        videos = yf.fetch_channel_result("https://example.com/@ch", "institute", runner=runner).videos
        self.assertEqual(videos[0]["channel"], "institute")

    def test_all_tabs_called(self):
        runner = _JsonlRunner([], [], [])
        result = yf.fetch_channel_result("https://www.youtube.com/@test", "personal", runner=runner)
        self.assertTrue(result.complete)
        self.assertEqual(len(runner.calls), 3)
        urls_called = [url for url, _ in runner.calls]
        self.assertTrue(any("videos" in u for u in urls_called))
        self.assertTrue(any("streams" in u for u in urls_called))
        self.assertTrue(any("shorts" in u for u in urls_called))


class TestSaveLoadJson(unittest.TestCase):
    def test_round_trip(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "out.json"
            videos = [
                {"id": "x", "title": "T", "upload_date": "20230101",
                 "year": 2023, "month": 1, "day": 1, "duration": 60,
                 "view_count": 10, "channel": "personal"}
            ]
            yf.save_json(videos, "https://example.com", "personal", path)
            loaded = yf.load_json(path)
            self.assertIsNotNone(loaded)
            self.assertEqual(loaded["meta"]["video_count"], 1)
            self.assertEqual(loaded["videos"][0]["id"], "x")

    def test_load_nonexistent_returns_none(self):
        self.assertIsNone(yf.load_json(Path("/tmp/no_such_file_abc123.json")))

    def test_creates_parent_dirs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "a" / "b" / "out.json"
            yf.save_json([], "https://example.com", "test", path)
            self.assertTrue(path.exists())





class TestPublicRefreshBoundaries(unittest.TestCase):
    def test_explicit_upcoming_items_are_not_published_videos(self):
        runner = _JsonlRunner([
            {"id": "upcoming", "title": "Scheduled", "live_status": "is_upcoming"},
            {"id": "past", "title": "Archived", "live_status": "was_live", "upload_date": "20261001"},
        ])
        videos = yf.fetch_tab("https://www.youtube.com/@example", "streams", "institute", "approximate", runner)
        self.assertEqual([video["id"] for video in videos], ["past"])

    def test_undated_published_or_live_stream_still_fails(self):
        for state in ("was_live", "is_live", "not_live", None):
            with self.subTest(state=state):
                runner = _JsonlRunner([{"id": "example", "title": "Missing date", "live_status": state}])
                with self.assertRaisesRegex(ValueError, "canonical video validation"):
                    yf.fetch_tab("https://www.youtube.com/@example", "streams", "institute", "approximate", runner)

    def test_missing_optional_shorts_is_structured_complete_empty(self):
        class Runner:
            def __call__(self, url, mode):
                if url.endswith("/shorts"):
                    raise yf.OptionalTabAbsentError("explicit missing tab")
                return []
        result = yf.fetch_channel_result("https://www.youtube.com/@example", "institute", runner=Runner())
        self.assertTrue(result.complete)
        self.assertTrue(result.tabs[-1].absent)
        self.assertTrue(result.as_dict()["tabs"][-1]["absent"])

    def test_optional_absence_cannot_excuse_missing_required_tab(self):
        class Runner:
            def __call__(self, url, mode):
                raise yf.OptionalTabAbsentError("explicit missing tab")
        result = yf.fetch_channel_result("https://www.youtube.com/@example", "institute", tabs=[("videos", "approximate")], runner=Runner())
        self.assertFalse(result.complete)

    def test_absence_requires_exact_error_and_zero_stdout(self):
        error = "ERROR: [youtube:tab] @activeinference: This channel does not have a shorts tab\n"
        executor = _RecordingExecutor(returncode=1, stderr=error)
        with self.assertRaises(yf.OptionalTabAbsentError):
            yf.run_yt_dlp("https://www.youtube.com/@activeinference/shorts", executor=executor)
        for url, stdout, stderr in (
            ("https://www.youtube.com/@activeinference/videos", "", error),
            ("https://www.youtube.com/@activeinference/shorts", '{"id":"partial"}', error),
            ("https://www.youtube.com/@activeinference/shorts", "", error + "ERROR: another failure\n"),
            ("https://www.youtube.com/@activeinference/shorts", "", "ERROR: forbidden\n"),
        ):
            with self.subTest(url=url, stderr=stderr):
                with self.assertRaises(RuntimeError) as failure:
                    yf.run_yt_dlp(url, executor=_RecordingExecutor(returncode=1, stdout=stdout, stderr=stderr))
                self.assertNotIsInstance(failure.exception, yf.OptionalTabAbsentError)

    def test_undated_short_uses_exact_fixed_origin_metadata(self):
        runner = _JsonlRunner(
            [{"id": "kxqkyuMlb84", "title": "Flat title", "url": "https://evil.example/private"}],
            [{"id": "kxqkyuMlb84", "title": "Exact title", "upload_date": "20260325"}],
        )
        videos = yf.fetch_tab("https://www.youtube.com/@example", "shorts", "personal", "approximate", runner)
        self.assertEqual(videos[0]["upload_date"], "20260325")
        self.assertEqual(runner.calls[1], ("https://www.youtube.com/watch?v=kxqkyuMlb84", "metadata"))

    def test_hydration_is_bounded_before_any_item_request(self):
        runner = _JsonlRunner([{"id": "kxqkyuMlb84"} for _ in range(yf.MAX_SHORT_DATE_HYDRATIONS + 1)])
        with self.assertRaisesRegex(ValueError, "hydration limit"):
            yf.fetch_tab("https://www.youtube.com/@example", "shorts", "personal", "approximate", runner)
        self.assertEqual(len(runner.calls), 1)

    def test_exact_hydration_requires_identity_date_and_publication_state(self):
        for exact in (
            [{"id": "other-id-xx", "upload_date": "20260325"}],
            [{"id": "kxqkyuMlb84", "upload_date": "20260230"}],
            [{"id": "kxqkyuMlb84"}],
            [{"id": "kxqkyuMlb84", "upload_date": "20260325", "live_status": "is_upcoming"}],
            [],
        ):
            with self.subTest(exact=exact):
                runner = _JsonlRunner([{"id": "kxqkyuMlb84"}], exact)
                with self.assertRaises(ValueError):
                    yf.fetch_tab("https://www.youtube.com/@example", "shorts", "personal", "approximate", runner)

    def test_malformed_nonempty_date_is_never_hydrated_or_guessed(self):
        runner = _JsonlRunner([{"id": "kxqkyuMlb84", "upload_date": "bad date"}])
        with self.assertRaisesRegex(ValueError, "canonical video validation"):
            yf.fetch_tab("https://www.youtube.com/@example", "shorts", "personal", "approximate", runner)
        self.assertEqual(len(runner.calls), 1)

    def test_hydration_command_is_public_only_and_has_firm_deadline(self):
        executor = _RecordingExecutor(stdout='{"id":"kxqkyuMlb84"}\n')
        yf.run_yt_dlp("https://www.youtube.com/watch?v=kxqkyuMlb84", "metadata", executor=executor)
        self.assertEqual(executor.timeouts, [yf.METADATA_TIMEOUT_SECONDS])
        self.assertIn("--ignore-config", executor.commands[0])
        self.assertIn("--no-cache-dir", executor.commands[0])
        self.assertIn("--no-playlist", executor.commands[0])
        self.assertNotIn("--cookies-from-browser", executor.commands[0])
        with self.assertRaisesRegex(ValueError, "canonical public"):
            yf.run_yt_dlp("https://evil.example/private", "metadata", executor=executor)

    def test_hydration_failure_preserves_existing_cache(self):
        import fetch_youtube_data as orchestrator
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "youtube_personal.json"
            original = {"meta": {"video_count": 1}, "videos": [{"id": "existing", "upload_date": "20200101"}]}
            path.write_text(json.dumps(original))
            before = path.read_bytes()
            runner = _JsonlRunner([{"id": "kxqkyuMlb84"}], [{"id": "wrong-video", "upload_date": "20260325"}])
            def fetcher(url, channel, tabs):
                return yf.fetch_channel_result(url, channel, tabs=[("shorts", "approximate")], runner=runner)
            result = orchestrator.refresh_channel("personal", "https://www.youtube.com/@example", path, fast=True, fetcher=fetcher)
            self.assertFalse(result.saved)
            self.assertEqual(path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
