"""
opml.py 的单元测试
"""

import pytest
from pathlib import Path
from xml.etree import ElementTree as ET

from src.opml import read_feeds, add_feed, get_max_xna_index


@pytest.fixture
def opml_file(tmp_path: Path) -> Path:
    """生成一个最小合法的 OPML 测试文件"""
    opml = tmp_path / "test.opml"
    opml.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<opml version="1.0">\n'
        '  <head><title>Test</title></head>\n'
        '  <body>\n'
        '    <outline title="VXNA" text="VXNA">\n'
        '      <outline title="blog1" xmlUrl="https://blog1.example.com/feed.xml"/>\n'
        '    </outline>\n'
        '  </body>\n'
        '</opml>',
        encoding="utf-8",
    )
    return opml


class TestReadFeeds:
    def test_returns_existing_url(self, opml_file: Path):
        feeds = read_feeds(opml_file)
        assert "https://blog1.example.com/feed.xml" in feeds

    def test_returns_empty_list_when_file_missing(self, tmp_path: Path):
        feeds = read_feeds(tmp_path / "nonexistent.opml")
        assert feeds == []

    def test_deduplicates_urls(self, tmp_path: Path):
        content = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<opml version="1.0"><head/><body>'
            '<outline title="g" text="g">'
            '<outline xmlUrl="https://dup.example.com/feed"/>'
            '<outline xmlUrl="https://dup.example.com/feed"/>'
            '</outline></body></opml>'
        )
        f = tmp_path / "dup.opml"
        f.write_text(content, encoding="utf-8")
        feeds = read_feeds(f)
        assert feeds.count("https://dup.example.com/feed") == 1


class TestGetMaxXnaIndex:
    def test_returns_max_index_from_html_url(self, tmp_path: Path):
        opml = tmp_path / "idx.opml"
        opml.write_text(
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<opml version="1.0"><head/><body><outline title="g" text="g">'
            '<outline xmlUrl="https://a.com/feed" htmlUrl="https://www.v2ex.com/xna/s/10"/>'
            '<outline xmlUrl="https://b.com/feed" htmlUrl="https://www.v2ex.com/xna/s/42"/>'
            '<outline xmlUrl="https://c.com/feed" htmlUrl="https://www.v2ex.com/xna/s/7"/>'
            '</outline></body></opml>',
            encoding="utf-8",
        )
        assert get_max_xna_index(opml) == 42

    def test_returns_zero_when_no_html_url(self, opml_file: Path):
        assert get_max_xna_index(opml_file) == 0

    def test_returns_zero_when_file_missing(self, tmp_path: Path):
        assert get_max_xna_index(tmp_path / "missing.opml") == 0


class TestAddFeed:
    def test_adds_new_url(self, opml_file: Path):
        result = add_feed("https://new.example.com/feed.xml", "New Blog", opml_file)
        assert result is True
        assert "https://new.example.com/feed.xml" in read_feeds(opml_file)

    def test_adds_with_xna_index_and_url(self, opml_file: Path):
        url = "https://xna.example.com/feed"
        add_feed(url, "My Blog", opml_file, xna_index=99, xna_url="https://www.v2ex.com/xna/s/99")
        tree = ET.parse(opml_file)
        found = [o for o in tree.getroot().iter("outline") if o.get("xmlUrl") == url]
        assert found[0].get("htmlUrl") == "https://www.v2ex.com/xna/s/99"
        assert "[#99]" in found[0].get("title", "")

    def test_skips_duplicate_url(self, opml_file: Path):
        result = add_feed("https://blog1.example.com/feed.xml", "blog1", opml_file)
        assert result is False
        feeds = read_feeds(opml_file)
        assert feeds.count("https://blog1.example.com/feed.xml") == 1

    def test_backfills_html_url_on_existing_entry_without_it(self, opml_file: Path):
        # blog1 already exists without htmlUrl — backfill should update it
        result = add_feed(
            "https://blog1.example.com/feed.xml", "blog1", opml_file,
            xna_index=5, xna_url="https://www.v2ex.com/xna/s/5",
        )
        assert result is False  # 仍返回 False（非新增）
        tree = ET.parse(opml_file)
        found = [o for o in tree.getroot().iter("outline")
                 if o.get("xmlUrl") == "https://blog1.example.com/feed.xml"]
        assert found[0].get("htmlUrl") == "https://www.v2ex.com/xna/s/5"

    def test_written_file_is_valid_xml(self, opml_file: Path):
        add_feed("https://valid-xml.example.com/feed", "test", opml_file)
        tree = ET.parse(opml_file)
        assert tree.getroot().tag == "opml"

    def test_title_defaults_to_url_when_empty(self, opml_file: Path):
        url = "https://notitle.example.com/feed"
        add_feed(url, "", opml_file)
        tree = ET.parse(opml_file)
        found = [o for o in tree.getroot().iter("outline") if o.get("xmlUrl") == url]
        assert found[0].get("title") == url
