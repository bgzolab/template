"""
crawler.py 的单元测试

使用 httpx.MockTransport 注入假响应，无需真实网络请求。
"""

import pytest
from pathlib import Path
from unittest.mock import patch

import httpx

from src.crawler import (
    extract_feed_url,
    extract_blog_title,
    crawl_new_blogs,
)

# ---- 测试用 HTML 片段 ----

# 真实 v2ex/xna 博客详情页结构（Feed 地址在表格 td 中）
HTML_WITH_RSS = """
<html>
<head><title>My Tech Blog</title></head>
<body>
  <table>
    <tr>
      <td align="right">Feed 地址</td>
      <td align="left"><a href="https://myblog.example.com/feed.xml" target="_blank">https://myblog.example.com/feed.xml</a></td>
    </tr>
    <tr>
      <td align="right">网站地址</td>
      <td align="left"><a href="https://myblog.example.com" target="_blank">https://myblog.example.com</a></td>
    </tr>
  </table>
</body>
</html>
"""

HTML_WITH_ATOM = """
<html>
<head><title>Atom Blog</title></head>
<body>
  <table>
    <tr>
      <td align="right">Feed 地址</td>
      <td align="left"><a href="https://atom.example.com/feed" target="_blank">https://atom.example.com/feed</a></td>
    </tr>
  </table>
</body>
</html>
"""

HTML_WITHOUT_FEED = """
<html>
<head><title>No Feed</title></head>
<body><p>no feed here</p></body>
</html>
"""


class TestExtractFeedUrl:
    def test_extracts_rss_link(self):
        url = extract_feed_url(HTML_WITH_RSS)
        assert url == "https://myblog.example.com/feed.xml"

    def test_extracts_atom_link(self):
        url = extract_feed_url(HTML_WITH_ATOM)
        assert url == "https://atom.example.com/feed"

    def test_returns_none_when_no_feed(self):
        url = extract_feed_url(HTML_WITHOUT_FEED)
        assert url is None

    def test_returns_none_on_empty_html(self):
        assert extract_feed_url("") is None


class TestExtractBlogTitle:
    def test_extracts_title(self):
        title = extract_blog_title(HTML_WITH_RSS)
        assert title == "My Tech Blog"

    def test_returns_empty_string_on_no_title(self):
        title = extract_blog_title("<html><body></body></html>")
        assert title == ""


# ---- mock transport helpers ----

def _make_response(status_code: int, html: str = "") -> httpx.Response:
    return httpx.Response(status_code, text=html)


class _MockTransport(httpx.MockTransport if hasattr(httpx, "MockTransport") else object):
    """简单的顺序响应 mock transport"""
    pass


def make_mock_client(responses: list[httpx.Response]) -> httpx.Client:
    """
    构造一个按顺序返回预设响应的 httpx.Client。
    responses 列表按请求顺序依次消耗。
    """
    iter_resp = iter(responses)

    def handler(request: httpx.Request) -> httpx.Response:
        return next(iter_resp)

    transport = httpx.MockTransport(handler)
    return httpx.Client(transport=transport)


class TestCrawlNewBlogs:
    def test_adds_new_blog_when_found(self, tmp_path: Path):
        opml = tmp_path / "rss.opml"
        opml.write_text(
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<opml version="1.0"><head/><body>'
            '<outline title="VXNA" text="VXNA"/>'
            '</body></opml>',
            encoding="utf-8",
        )
        responses = [
            _make_response(200, HTML_WITH_RSS),  # index 1: 找到 feed
            _make_response(404),                 # index 2: 404
            _make_response(404),                 # index 3: 404
            _make_response(404),                 # index 4: 404
            _make_response(404),                 # index 5: 404
            _make_response(404),                 # index 6: 404 -> stop
        ]
        client = make_mock_client(responses)
        added = crawl_new_blogs(start_index=1, max_consecutive_404=5, opml_path=opml, client=client)
        assert "https://myblog.example.com/feed.xml" in added

    def test_stops_after_consecutive_404(self, tmp_path: Path):
        opml = tmp_path / "rss.opml"
        opml.write_text(
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<opml version="1.0"><head/><body>'
            '<outline title="VXNA" text="VXNA"/>'
            '</body></opml>',
            encoding="utf-8",
        )
        # 全部 404，应在 max_consecutive_404 后停止，不会无限循环
        responses = [_make_response(404)] * 3
        client = make_mock_client(responses)
        added = crawl_new_blogs(start_index=1, max_consecutive_404=3, opml_path=opml, client=client)
        assert added == []

    def test_skips_page_without_feed(self, tmp_path: Path):
        opml = tmp_path / "rss.opml"
        opml.write_text(
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<opml version="1.0"><head/><body>'
            '<outline title="VXNA" text="VXNA"/>'
            '</body></opml>',
            encoding="utf-8",
        )
        responses = [
            _make_response(200, HTML_WITHOUT_FEED),  # 无 feed，跳过
            _make_response(404),
            _make_response(404),
        ]
        client = make_mock_client(responses)
        added = crawl_new_blogs(start_index=1, max_consecutive_404=2, opml_path=opml, client=client)
        assert added == []

    def test_skips_duplicate_feed(self, tmp_path: Path):
        opml = tmp_path / "rss.opml"
        opml.write_text(
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<opml version="1.0"><head/><body>'
            '<outline title="VXNA" text="VXNA">'
            '<outline xmlUrl="https://myblog.example.com/feed.xml"/>'
            '</outline></body></opml>',
            encoding="utf-8",
        )
        responses = [
            _make_response(200, HTML_WITH_RSS),  # feed 已存在
            _make_response(404),
            _make_response(404),
        ]
        client = make_mock_client(responses)
        added = crawl_new_blogs(start_index=1, max_consecutive_404=2, opml_path=opml, client=client)
        # 不应重复添加
        assert added == []
