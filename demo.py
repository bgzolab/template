#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-07-29
@Links : https://github.com/bGZo
"""
from bs4 import BeautifulSoup
from usp.tree import sitemap_tree_for_homepage
import os
from urllib.parse import urlparse
import trafilatura
from markdownify import markdownify as md

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

    result = md(downloaded, strip=['a'])
    hostname = urlparse(url).hostname
    if not hostname:
        print(f"无法解析主机名: {url}")
        return
    os.makedirs(hostname, exist_ok=True)
    filename = os.path.join(hostname, title +'.md')
    with open(filename, "w", encoding="utf-8") as f:
        f.write(result)
    print(f"已保存: {filename}")

if __name__ == '__main__':
    url_list = get_all_public_pages_url('https://www.hecaitou.com/')
    for url in url_list:
        fetch_and_save(url)
