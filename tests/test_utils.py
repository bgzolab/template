#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-07-27
@Links : https://github.com/bGZo
"""
import pytest

def test_html_to_markdown_html2text():
    from utils.md_utils import html_to_markdown_with_html2text

    html_content = "<h1>Test Title</h1><p>This is a test paragraph.</p>"
    expected_markdown = "# Test Title\n\nThis is a test paragraph.\n\n"

    result = html_to_markdown_with_html2text(html_content)
    assert result == expected_markdown, f"Expected: {expected_markdown}, but got: {result}"

def test_html_to_markdown_bs():
    from utils.md_utils import html_to_markdown_with_bs

    html_content = "<h1>Test Title</h1><p>This is a test paragraph.</p>"
    expected_markdown = "# Test Title\nThis is a test paragraph.\n"

    result = html_to_markdown_with_bs(html_content)
    assert result == expected_markdown, f"Expected: {expected_markdown}, but got: {result}"


def test_dump_markdown_with_frontmatter():
    from utils.md_utils import dump_markdown_with_frontmatter
    meta = {"title": "测试标题", "date": "2025-07-27"}
    content = "这是正文内容。"
    md = dump_markdown_with_frontmatter(meta, content)
    assert md.startswith("---")
    assert "title: 测试标题" in md
    assert "date: '2025-07-27'" in md
    assert "这是正文内容。" in md