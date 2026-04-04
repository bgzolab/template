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
    _clean_text,
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

    def test_filters_articles_by_publication_date(self, tmp_path: Path):
        # JSON 文件在窗口内，但文章发布日期超出 7 天
        old_article = [{"title": "Old", "url": "https://old.example.com", "date": "2026-01-01T00:00:00Z", "description": ""}]
        api_dir = make_api_dir(tmp_path, {"2026/04/04": old_article})
        articles = load_recent_articles(days=7, api_dir=api_dir, reference_date=FIXED_DATE)
        assert articles == []

    def test_includes_articles_within_date_range(self, tmp_path: Path):
        recent = [{"title": "Recent", "url": "https://recent.example.com", "date": "2026-04-02T00:00:00Z", "description": ""}]
        api_dir = make_api_dir(tmp_path, {"2026/04/04": recent})
        articles = load_recent_articles(days=7, api_dir=api_dir, reference_date=FIXED_DATE)
        assert len(articles) == 1


class TestCleanText:
    def test_strips_html_tags(self):
        assert _clean_text("<p>Hello <b>world</b></p>") == "Hello world"

    def test_decodes_html_entities(self):
        # &amp; → &; &lt;test&gt; → <test> → stripped as tag
        assert _clean_text("AT&amp;T &lt;test&gt;") == "AT&T"
        assert _clean_text("&quot;hello&quot;") == '"hello"'

    def test_removes_markdown_bold(self):
        assert _clean_text("**bold** text") == "bold text"

    def test_removes_markdown_italic(self):
        assert _clean_text("*italic* and _also_") == "italic and also"

    def test_collapses_newlines_and_whitespace(self):
        result = _clean_text("line1\nline2\n\nline3\t  extra")
        assert "\n" not in result
        assert "  " not in result

    def test_handles_empty_string(self):
        assert _clean_text("") == ""

    def test_combined_html_and_markdown(self):
        result = _clean_text("<p>**Hello** &amp; <em>world</em></p>")
        assert "<" not in result
        assert "**" not in result
        assert "&amp;" not in result


class TestFormatArticlesMarkdown:
    def test_formats_articles_as_table(self):
        articles = [{"title": "T", "url": "https://x.com", "date": "2026-04-04T10:00:00Z", "description": "A summary"}]
        result = format_articles_markdown(articles)
        assert "| Date | Title | Summary |" in result
        assert "| 2026-04-04 | [T](https://x.com) | A summary |" in result

    def test_truncates_description_to_150_chars(self):
        long_desc = "x" * 200
        articles = [{"title": "T", "url": "https://x.com", "date": "2026-04-04T00:00:00Z", "description": long_desc}]
        result = format_articles_markdown(articles)
        # 摘要列不超过 150 个字符（加省略号）
        summary_cell = result.split("|")[3].strip()
        assert len(summary_cell) <= 152  # 150 + "…"

    def test_escapes_pipe_in_title(self):
        articles = [{"title": "A|B", "url": "https://x.com", "date": "2026-04-04T00:00:00Z", "description": ""}]
        result = format_articles_markdown(articles)
        assert "&#124;" in result

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
        articles = [{"title": "New", "url": "https://new.example.com", "date": "2026-04-04T00:00:00Z", "description": "desc"}]
        update_readme(articles, readme_path=readme)
        content = readme.read_text()
        assert "[New](https://new.example.com)" in content
        assert "2026-04-04" in content
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
