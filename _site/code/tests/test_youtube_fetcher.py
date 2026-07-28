"""Unit tests for youtube_fetcher module."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, call, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
import youtube_fetcher as yf

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


class TestParseJsonl(unittest.TestCase):
    def test_valid_lines(self):
        records = yf.parse_jsonl(SAMPLE_JSONL_LINES[:1])
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["id"], "abc123")

    def test_skips_malformed(self):
        records = yf.parse_jsonl(["not json", '{"id": "ok"}'])
        self.assertEqual(len(records), 1)

    def test_empty_input(self):
        self.assertEqual(yf.parse_jsonl([]), [])

    def test_blank_lines_skipped(self):
        records = yf.parse_jsonl(["", "  ", '{"id": "x"}'])
        self.assertEqual(len(records), 1)

    def test_all_sample_lines(self):
        records = yf.parse_jsonl(SAMPLE_JSONL_LINES)
        self.assertEqual(len(records), 3)  # 1 malformed skipped


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


class TestRunYtDlp(unittest.TestCase):
    @patch("youtube_fetcher.subprocess.run")
    def test_full_mode_command(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout='{"id":"a"}\n', stderr="")
        yf.run_yt_dlp("https://example.com/channel", mode="full")
        cmd = mock_run.call_args[0][0]
        self.assertIn("--dump-json", cmd)
        self.assertIn("--no-download", cmd)
        self.assertNotIn("--flat-playlist", cmd)

    @patch("youtube_fetcher.subprocess.run")
    def test_approximate_mode_command(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout='{"id":"a"}\n', stderr="")
        yf.run_yt_dlp("https://example.com/channel", mode="approximate")
        cmd = mock_run.call_args[0][0]
        self.assertIn("--flat-playlist", cmd)
        self.assertIn("--extractor-args", cmd)
        self.assertIn("youtubetab:approximate_date", cmd)

    @patch("youtube_fetcher.subprocess.run")
    def test_success_returns_lines(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout='{"id":"a"}\n{"id":"b"}\n', stderr="")
        lines = yf.run_yt_dlp("https://example.com")
        self.assertEqual(lines, ['{"id":"a"}', '{"id":"b"}'])

    @patch("youtube_fetcher.subprocess.run")
    def test_non_zero_exit_raises(self, mock_run):
        mock_run.return_value = MagicMock(returncode=2, stdout="", stderr="error")
        with self.assertRaises(RuntimeError):
            yf.run_yt_dlp("https://example.com")

    @patch("youtube_fetcher.subprocess.run")
    def test_exit_code_1_ok(self, mock_run):
        mock_run.return_value = MagicMock(returncode=1, stdout='{"id":"x"}\n', stderr="")
        lines = yf.run_yt_dlp("https://example.com")
        self.assertEqual(len(lines), 1)


class TestFetchChannel(unittest.TestCase):
    def _make_jsonl(self, records):
        return [json.dumps(r) for r in records]

    @patch("youtube_fetcher.run_yt_dlp")
    def test_deduplicates_across_tabs(self, mock_run):
        vid_a = {"id": "aaa", "title": "A", "upload_date": "20230101", "duration": 60, "view_count": 1}
        vid_b = {"id": "bbb", "title": "B", "upload_date": "20230601", "duration": 60, "view_count": 1}
        # /videos returns A, /streams returns A+B (A is a duplicate), /shorts empty
        mock_run.side_effect = [
            self._make_jsonl([vid_a]),         # videos
            self._make_jsonl([vid_a, vid_b]),   # streams (a is dupe)
            [],                                 # shorts
        ]
        videos = yf.fetch_channel("https://example.com/@ch", "personal")
        self.assertEqual(len(videos), 2)
        ids = [v["id"] for v in videos]
        self.assertIn("aaa", ids)
        self.assertIn("bbb", ids)

    @patch("youtube_fetcher.run_yt_dlp")
    def test_sorted_by_date(self, mock_run):
        v1 = {"id": "a1", "title": "Old", "upload_date": "20200101", "duration": 60, "view_count": 0}
        v2 = {"id": "a2", "title": "New", "upload_date": "20240101", "duration": 60, "view_count": 0}
        mock_run.side_effect = [
            self._make_jsonl([v2]),  # videos
            self._make_jsonl([v1]),  # streams
            [],                      # shorts
        ]
        videos = yf.fetch_channel("https://example.com/@ch", "personal")
        self.assertEqual(videos[0]["id"], "a1")
        self.assertEqual(videos[1]["id"], "a2")

    @patch("youtube_fetcher.run_yt_dlp")
    def test_tab_failure_continues(self, mock_run):
        v = {"id": "ok", "title": "OK", "upload_date": "20230101", "duration": 60, "view_count": 0}
        mock_run.side_effect = [
            self._make_jsonl([v]),   # videos ok
            RuntimeError("streams failed"),  # streams fails
            [],                              # shorts ok
        ]
        videos = yf.fetch_channel("https://example.com/@ch", "personal")
        self.assertEqual(len(videos), 1)

    @patch("youtube_fetcher.run_yt_dlp")
    def test_channel_id_set_on_all_videos(self, mock_run):
        v = {"id": "x", "title": "T", "upload_date": "20230101", "duration": 60, "view_count": 0}
        mock_run.side_effect = [self._make_jsonl([v]), [], []]
        videos = yf.fetch_channel("https://example.com/@ch", "institute")
        self.assertEqual(videos[0]["channel"], "institute")

    @patch("youtube_fetcher.run_yt_dlp")
    def test_all_tabs_called(self, mock_run):
        mock_run.return_value = []
        yf.fetch_channel("https://www.youtube.com/@test", "personal")
        self.assertEqual(mock_run.call_count, 3)
        urls_called = [mock_run.call_args_list[i][0][0] for i in range(3)]
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


if __name__ == "__main__":
    unittest.main()
