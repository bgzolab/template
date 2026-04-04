"""
writer.py 的单元测试
"""

import json
import pytest
from datetime import datetime, timezone
from pathlib import Path

from src.writer import resolve_output_path, write_articles


FIXED_DATE = datetime(2026, 4, 4, tzinfo=timezone.utc)

# 文章日期刚好在 2 天内
SAMPLE_ARTICLES = [
    {"title": "A", "url": "https://example.com/a", "date": "2026-04-04T10:00:00Z", "description": "desc A"},
    {"title": "B", "url": "https://example.com/b", "date": "2026-04-03T08:00:00Z", "description": "desc B"},
]


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

    def test_creates_intermediate_directories(self, tmp_path: Path):
        out = write_articles(SAMPLE_ARTICLES, date=FIXED_DATE, api_dir=tmp_path)
        assert out.parent.is_dir()  # api/2026/04/ 已自动创建

    def test_merges_with_existing_file(self, tmp_path: Path):
        """第二次写入应合并而非覆盖已有数据。"""
        write_articles(SAMPLE_ARTICLES, date=FIXED_DATE, api_dir=tmp_path)
        new_article = [{"title": "C", "url": "https://example.com/c", "date": "2026-04-04T12:00:00Z", "description": "desc C"}]
        write_articles(new_article, date=FIXED_DATE, api_dir=tmp_path)
        data = json.loads((tmp_path / "2026" / "04" / "04.json").read_text())
        urls = {a["url"] for a in data}
        assert "https://example.com/c" in urls
        assert "https://example.com/a" in urls  # 旧数据被保留

    def test_deduplicates_by_url(self, tmp_path: Path):
        """相同 URL 写入两次，最终只保留一条（新数据优先）。"""
        old = [{"title": "Old A", "url": "https://example.com/a", "date": "2026-04-04T09:00:00Z", "description": "old"}]
        write_articles(old, date=FIXED_DATE, api_dir=tmp_path)
        new = [{"title": "New A", "url": "https://example.com/a", "date": "2026-04-04T10:00:00Z", "description": "new"}]
        write_articles(new, date=FIXED_DATE, api_dir=tmp_path)
        data = json.loads((tmp_path / "2026" / "04" / "04.json").read_text())
        a_articles = [a for a in data if a["url"] == "https://example.com/a"]
        assert len(a_articles) == 1
        assert a_articles[0]["title"] == "New A"  # 新数据覆盖旧数据

    def test_filters_articles_older_than_max_age_days(self, tmp_path: Path):
        """超过 max_age_days 的文章应被过滤。"""
        old_article = {"title": "Old", "url": "https://example.com/old", "date": "2026-04-01T00:00:00Z", "description": ""}
        articles = SAMPLE_ARTICLES + [old_article]
        out = write_articles(articles, date=FIXED_DATE, api_dir=tmp_path, max_age_days=2)
        data = json.loads(out.read_text(encoding="utf-8"))
        urls = {a["url"] for a in data}
        assert "https://example.com/old" not in urls

    def test_result_sorted_by_date_descending(self, tmp_path: Path):
        out = write_articles(SAMPLE_ARTICLES, date=FIXED_DATE, api_dir=tmp_path)
        data = json.loads(out.read_text(encoding="utf-8"))
        dates = [a["date"] for a in data]
        assert dates == sorted(dates, reverse=True)

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
