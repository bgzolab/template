#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-07-27
@Links : https://github.com/bGZo
"""

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

