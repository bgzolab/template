#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-07-28
@Links : https://github.com/bGZo
"""
import os
import re

from bs4 import BeautifulSoup

from bangumi.collection import mark_subject
from bangumi.enum import SubjectCollectionType


def get_all_bgm_id_from_html_files(directory: str) -> set:
    pattern = re.compile(r'/subject/(\d+)$')
    result = set()
    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
                h3_tags = soup.find_all('h3')
                for h3 in h3_tags:
                    a_tag = h3.find('a', href=True)
                    if a_tag:
                        match = pattern.search(a_tag['href'])
                        if match:
                            result.add(match.group(1))
                            print(f'文件: {filename}, ID: {match.group(1)}')
    return result


def mark_want_subjects_form_files():
    target_set = get_all_bgm_id_from_html_files('./history/want')
    print(len(target_set))
    for item in target_set:
        response = mark_subject(item, SubjectCollectionType.WANT.value)
        print(response)

def mark_done_subjects_form_files():
    target_set = get_all_bgm_id_from_html_files('./history/done')
    print(len(target_set))
    for item in target_set:
        response = mark_subject(item, SubjectCollectionType.DONE.value)
        print(response)

if __name__ == '__main__':
    mark_want_subjects_form_files()
    mark_done_subjects_form_files()