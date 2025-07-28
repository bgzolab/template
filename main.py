#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-07-28
@Links : https://github.com/bGZo
"""
import os
from bs4 import BeautifulSoup


def get_all_bgm_id_from_html_files(directory: str) -> set:
    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
                h3_tags = soup.find_all('h3')
                print(f'文件: {filename}')
                for tag in h3_tags:
                    print(tag.get_text(strip=True))
    return set()

if __name__ == '__main__':
    get_all_bgm_id_from_html_files('./history')