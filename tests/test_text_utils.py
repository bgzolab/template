"""
text_utils.py 的单元测试
"""

import pytest
from src.text_utils import clean_description


class TestCleanDescription:
    def test_removes_base64_img(self):
        html = '<img src="data:image/png;base64,AAABBBCCC==" alt="logo">'
        result = clean_description(html)
        assert "base64" not in result
        assert "data:image" not in result

    def test_removes_base64_img_preserves_surrounding_text(self):
        html = 'Before <img src="data:image/jpeg;base64,XYZ="> After'
        result = clean_description(html)
        assert "Before" in result
        assert "After" in result
        assert "base64" not in result

    def test_strips_html_tags(self):
        assert clean_description("<p>Hello <b>world</b></p>") == "Hello world"

    def test_strips_br_tags(self):
        assert clean_description("line1<br>line2<br/>line3") == "line1 line2 line3"

    def test_decodes_html_entities(self):
        # &amp; → &; &lt;test&gt; decodes then tag is stripped
        assert clean_description("AT&amp;T") == "AT&T"
        assert clean_description("&lt;b&gt;text&lt;/b&gt;") == "text"

    def test_removes_markdown_bold(self):
        assert clean_description("**bold** text") == "bold text"

    def test_removes_markdown_italic(self):
        assert clean_description("*italic* and _also_") == "italic and also"

    def test_collapses_newlines_and_whitespace(self):
        result = clean_description("line1\nline2\n\nline3\t  extra")
        assert "\n" not in result
        assert "  " not in result

    def test_handles_empty_string(self):
        assert clean_description("") == ""

    def test_combined_html_markdown_base64(self):
        html = (
            '<p>**Hello** &amp; <em>world</em></p>'
            '<img src="data:image/png;base64,LONGDATA==">'
        )
        result = clean_description(html)
        assert "<" not in result
        assert "**" not in result
        assert "&amp;" not in result
        assert "base64" not in result
        assert "Hello" in result
        assert "world" in result
