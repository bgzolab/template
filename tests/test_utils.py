#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-07-27
@Links : https://github.com/bGZo
"""
import pytest
from click.testing import CliRunner

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


def test_index_writer_flush_stdout(capsys):
    from export_to_obsidian import IndexWriter

    writer = IndexWriter()
    writer.add("- [[item-1|标题1]]")
    writer.add("- [[item-2|标题2]]")

    writer.flush("zhihu", "导出index")

    captured = capsys.readouterr()
    assert "导出index:" in captured.out
    assert "- [[item-1|标题1]]" in captured.out
    assert "- [[item-2|标题2]]" in captured.out
    assert writer.render() == ""


def test_index_writer_flush_file(tmp_path):
    from export_to_obsidian import IndexWriter

    target = tmp_path / "index.md"
    writer = IndexWriter(file_path=str(target))
    writer.add("- [[zhihu-1|标题1]]")

    writer.flush("zhihu", "导出index")
    writer.add("- [[bilibili-1|标题2]]")
    writer.flush("bilibili", "导出index")
    writer.add("- [[zhihu-2|标题3]]")
    writer.flush("zhihu", "导出index")

    assert target.read_text(encoding="utf-8") == (
        "## zhihu\n\n"
        "### 导出index\n\n"
        "- [[zhihu-1|标题1]]\n\n"
        "### 导出index\n\n"
        "- [[zhihu-2|标题3]]\n\n"
        "## bilibili\n\n"
        "### 导出index\n\n"
        "- [[bilibili-1|标题2]]\n"
    )


def test_cli_accepts_index_file_without_output_mode():
    from export_to_obsidian import eto

    runner = CliRunner()
    result = runner.invoke(eto, ["--index-file", "output/index.md", "--help"])

    assert result.exit_code == 0
    assert "--index-file" in result.output


def test_cli_rejects_removed_index_output_option():
    from export_to_obsidian import eto

    runner = CliRunner()
    result = runner.invoke(
        eto,
        ["--index-output", "stdout", "cnblog", "-o", "output/cnblog"],
    )

    assert result.exit_code != 0
    assert "No such option: --index-output" in result.output