#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-07-29
@Links : https://github.com/bGZo
"""

from usp.tree import sitemap_tree_for_homepage

def get_all_public_pages_url(url: str) -> list[str]:
    tree = sitemap_tree_for_homepage(url)
    return [page.url for page in tree.all_pages()]


if __name__ == '__main__':
    get_all_public_pages_url('https://www.hecaitou.com/')
