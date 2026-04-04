"""
writer.py 的单元测试
"""

import json
import pytest
from datetime import datetime, timezone
from pathlib import Path

from src.writer import resolve_output_path, write_articles


SAMPLE_ARTICLES = [
    {"title": "A", "url": "https://example.com/a", "date": "2026-04-04T10:00:00Z", "description": "desc A"},
    {"title": "B", "url": "https://example.com/b", "date": "2026-04-03T08:00:00Z", "description": "desc B"},
]

FIXED_DATE = datetime(2026, 4, 4, tzinfo=timezone.utc)


class TestResolveOutputPath:
    def test_generates_correct_path(self, tmp_path: Path):
        path = resolve_output_path(FIXED_DATE, api_dir=tmp_path)
        assert path == tmp_path / "2026" / "04" / "04.json"

    def test_different_date_generates_different_path(self, tmp_path: Path):
        date2 = datetime(2025, 12, 1, tzinfo=timezone.utc)
        path = resolve_output_path(date2, api_dir=tmp_path)
        assert path == tmp_path / "2025" / "12" / "01.json"


class TestWriteArticles:
    def test_creates_file_with_correct_content(self, tmp_path: Path):
        out = write_articles(SAMPLE_ARTICLES, date=FIXED_DATE, api_dir=tmp_path)
        assert out.exists()
        data = json.loads(out.read_text(encoding="utf-8"))
        assert len(data) == 2
        assert data[0]["title"] == "A"

    def test_creates_intermediate_directories(self, tmp_path: Path):
        out = write_articles(SAMPLE_ARTICLES, date=FIXED_DATE, api_dir=tmp_path)
        assert out.parent.is_dir()  # api/2026/04/ 已自动创建

    def test_overwrites_existing_file(self, tmp_path: Path):
        write_articles(SAMPLE_ARTICLES, date=FIXED_DATE, api_dir=tmp_path)
        write_articles([SAMPLE_ARTICLES[0]], date=FIXED_DATE, api_dir=tmp_path)
        data = json.loads((tmp_path / "2026" / "04" / "04.json").read_text())
        assert len(data) == 1  # 覆盖后只有 1 篇

    def test_returns_correct_path(self, tmp_path: Path):
        out = write_articles([], date=FIXED_DATE, api_dir=tmp_path)
        assert out == tmp_path / "2026" / "04" / "04.json"

    def test_empty_articles_writes_empty_list(self, tmp_path: Path):
        out = write_articles([], date=FIXED_DATE, api_dir=tmp_path)
        data = json.loads(out.read_text(encoding="utf-8"))
        assert data == []

    def test_uses_utc_today_when_date_not_provided(self, tmp_path: Path):
        out = write_articles([], api_dir=tmp_path)
        today = datetime.now(tz=timezone.utc)
        expected = tmp_path / today.strftime("%Y") / today.strftime("%m") / f"{today.strftime('%d')}.json"
        assert out == expected
