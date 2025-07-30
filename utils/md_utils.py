#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-07-27
@Links : https://github.com/bGZo
"""

import frontmatter
import sys
import html2text
from bs4 import BeautifulSoup
from markdownify import markdownify as md

"""
=========================================================================
From html to markdown
"""

# using BeautifulSoup to convert HTML to Markdown
def html_to_markdown_with_bs(html):
    soup = BeautifulSoup(html, 'html.parser')
    lines = []

    for elem in soup.recursiveChildGenerator():
        if elem.name:
            if elem.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                level = int(elem.name[1])
                lines.append('#' * level + ' ' + elem.get_text(strip=True))
            elif elem.name == 'p':
                lines.append(elem.get_text(strip=True) + '\n')
            elif elem.name == 'a':
                lines.append(f"[{elem.get_text(strip=True)}]({elem.get('href')})")
            elif elem.name == 'ul':
                for li in elem.find_all('li'):
                    lines.append(f"- {li.get_text(strip=True)}")
            elif elem.name == 'ol':
                for idx, li in enumerate(elem.find_all('li'), 1):
                    lines.append(f"{idx}. {li.get_text(strip=True)}")
    return '\n'.join(lines)

# using markdownify to convert HTML to Markdown
def html_to_markdown_with_md(html: str) -> str:
    return md(html, strip=['a'])

# using html2text to convert HTML to Markdown
def html_to_markdown_with_html2text(html:str):
    # 使用 html2text 库将 HTML 转换为 Markdown
    return html2text.html2text(html)

"""
=========================================================================
"""


def read(path: str):
    # 读取并解析 Markdown 文件
    with open(path, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)
    # 获取 FrontMatter 和正文
    meta = post.metadata
    content = post.content
    return post


def dump_markdown_with_frontmatter(meta: dict, content: str) -> str:
    """
    输出带有FrontMatter的Markdown字符串
    :param meta: FrontMatter元数据（字典）
    :param content: Markdown正文内容
    :return: 合成后的Markdown字符串
    """
    post = frontmatter.Post(content, **meta)
    return frontmatter.dumps(post)

