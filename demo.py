#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-07-29
@Links : https://github.com/bGZo
"""
import datetime

from bs4 import BeautifulSoup
from usp.tree import sitemap_tree_for_homepage
import os
from urllib.parse import urlparse
import trafilatura
from markdownify import markdownify as md

from template import TEMPLATE_FRONT_MATTER, TEMPLATE_INDEX


def get_all_public_pages_url(url: str) -> list[str]:
    tree = sitemap_tree_for_homepage(url)
    return [page.url for page in tree.all_pages()]

def fetch_and_save_with_trafilatura(url: str):
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        print(f"无法下载: {url}")
        return
    result = trafilatura.extract(downloaded)
    if not result:
        print(f"无法提取正文: {url}")
        return
    hostname = urlparse(url).hostname
    if not hostname:
        print(f"无法解析主机名: {url}")
        return
    os.makedirs(hostname, exist_ok=True)
    filename = os.path.join(hostname, "content.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(result)
    print(f"已保存: {filename}")


def fetch_and_save(url: str):
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        print(f"无法下载: {url}")
        return

    soup = BeautifulSoup(downloaded, "html.parser")
    title = soup.title.string if soup.title else "无标题"
    hostname = urlparse(url).hostname

    date_str = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    frontmatter = TEMPLATE_FRONT_MATTER.format(
        title,
        date_str,date_str,
        url,
        hostname,
        title
    )
    result = frontmatter + md(downloaded, strip=['a'])
    if not hostname:
        print(f"无法解析主机名: {url}")
        return
    os.makedirs(hostname, exist_ok=True)
    name = title +'.md'
    filename = os.path.join(hostname, name)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(result)
    print(f"已保存: {filename}")
    return hostname, name

def test_download_from(url):
    # TEMPLATE_FRONT_MATTER
    fetch_and_save(url)

def test_url_list_fetch():
    url_list = [
        'https://www.hecaitou.com/2025/07/in-the-eternal-flow.html',
        'https://www.hecaitou.com/2025/07/what-music-are-you-listening-to-lately.html'
    ]
    fetch_from_url_list(url_list)

def fetch_from_url_list(url_list: list[str]):
    if len(url_list) == 0:
        return

    index_content = TEMPLATE_INDEX
    index_dir = urlparse(url_list[0]).hostname

    for url in url_list:
        hostname, name = fetch_and_save(url)
        index_content = (index_content + f"- [{name[:-3]}](./{name})\n" )

    index_filename = os.path.join(index_dir, "index.md")
    with open(index_filename, "w", encoding="utf-8") as f:
        f.write(index_content)


if __name__ == '__main__':
    url_list = get_all_public_pages_url('https://cn.apkjam.com/')
    fetch_from_url_list(url_list)
