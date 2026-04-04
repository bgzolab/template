"""
readme_updater.py 的单元测试
"""

import json
import pytest
from datetime import datetime, timezone
from pathlib import Path

from src.readme_updater import (
    load_recent_articles,
    format_articles_markdown,
    update_readme,
)

FIXED_DATE = datetime(2026, 4, 4, tzinfo=timezone.utc)

ARTICLES_DAY1 = [
    {"title": "Article A", "url": "https://a.example.com/1", "date": "2026-04-04T10:00:00Z", "description": ""},
    {"title": "Article B", "url": "https://b.example.com/1", "date": "2026-04-04T08:00:00Z", "description": ""},
]
ARTICLES_DAY2 = [
    {"title": "Article C", "url": "https://c.example.com/1", "date": "2026-04-03T12:00:00Z", "description": ""},
]


def make_api_dir(tmp_path: Path, day_articles: dict[str, list]) -> Path:
    """
    创建临时 api 目录，day_articles: {"2026/04/04": [...], ...}
    """
    api_dir = tmp_path / "api"
    for date_path, articles in day_articles.items():
        parts = date_path.split("/")
        file_path = api_dir / parts[0] / parts[1] / f"{parts[2]}.json"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(json.dumps(articles), encoding="utf-8")
    return api_dir


class TestLoadRecentArticles:
    def test_loads_articles_from_last_7_days(self, tmp_path: Path):
        api_dir = make_api_dir(tmp_path, {
            "2026/04/04": ARTICLES_DAY1,
            "2026/04/03": ARTICLES_DAY2,
        })
        articles = load_recent_articles(days=7, api_dir=api_dir, reference_date=FIXED_DATE)
        assert len(articles) == 3

    def test_ignores_files_outside_range(self, tmp_path: Path):
        api_dir = make_api_dir(tmp_path, {
            "2026/04/04": ARTICLES_DAY1,
            "2026/03/20": ARTICLES_DAY2,  # 超出 7 天
        })
        articles = load_recent_articles(days=7, api_dir=api_dir, reference_date=FIXED_DATE)
        assert len(articles) == 2

    def test_deduplicates_same_url_across_days(self, tmp_path: Path):
        duplicate = [{"title": "Dup", "url": "https://dup.example.com", "date": "2026-04-03T00:00:00Z", "description": ""}]
        api_dir = make_api_dir(tmp_path, {
            "2026/04/04": duplicate,
            "2026/04/03": duplicate,
        })
        articles = load_recent_articles(days=7, api_dir=api_dir, reference_date=FIXED_DATE)
        assert len(articles) == 1

    def test_returns_sorted_by_date_descending(self, tmp_path: Path):
        api_dir = make_api_dir(tmp_path, {
            "2026/04/04": ARTICLES_DAY1,
            "2026/04/03": ARTICLES_DAY2,
        })
        articles = load_recent_articles(days=7, api_dir=api_dir, reference_date=FIXED_DATE)
        dates = [a["date"] for a in articles]
        assert dates == sorted(dates, reverse=True)

    def test_returns_empty_when_no_files(self, tmp_path: Path):
        api_dir = tmp_path / "api"
        api_dir.mkdir()
        articles = load_recent_articles(days=7, api_dir=api_dir, reference_date=FIXED_DATE)
        assert articles == []


class TestFormatArticlesMarkdown:
    def test_formats_articles_as_list(self):
        articles = [{"title": "T", "url": "https://x.com", "date": "2026-04-04T10:00:00Z", "description": ""}]
        result = format_articles_markdown(articles)
        assert "- [T](https://x.com) — 2026-04-04" in result

    def test_returns_placeholder_when_empty(self):
        result = format_articles_markdown([])
        assert "No articles" in result


class TestUpdateReadme:
    def _make_readme(self, tmp_path: Path, content: str) -> Path:
        p = tmp_path / "README.md"
        p.write_text(content, encoding="utf-8")
        return p

    def test_replaces_section_content(self, tmp_path: Path):
        readme = self._make_readme(tmp_path, "# Title\n\n## Last Week Blog\n\nold content\n\n## Other\n\nstuff\n")
        articles = [{"title": "New", "url": "https://new.example.com", "date": "2026-04-04T00:00:00Z", "description": ""}]
        update_readme(articles, readme_path=readme)
        content = readme.read_text()
        assert "- [New](https://new.example.com) — 2026-04-04" in content
        assert "old content" not in content

    def test_preserves_content_after_section(self, tmp_path: Path):
        readme = self._make_readme(tmp_path, "## Last Week Blog\n\nold\n\n## Other\n\nkeep this\n")
        update_readme([], readme_path=readme)
        content = readme.read_text()
        assert "## Other" in content
        assert "keep this" in content

    def test_logs_warning_when_section_missing(self, tmp_path: Path, caplog):
        readme = self._make_readme(tmp_path, "# No Section Here\n")
        import logging
        with caplog.at_level(logging.WARNING):
            update_readme([], readme_path=readme)
        assert "未找到" in caplog.text
