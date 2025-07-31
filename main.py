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

from bangumi.collection import mark_subject, get_all_collections_by_pages
from bangumi.enum import CollectionType, SubjectType


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
        response = mark_subject(item, CollectionType.WANT.value)
        print(response)

def mark_done_subjects_form_files():
    target_set = get_all_bgm_id_from_html_files('./history/done')
    print(len(target_set))
    for item in target_set:
        response = mark_subject(item, CollectionType.DONE.value)
        print(response)


def get_user_all_collections_with_status(subject_type: int, collection_type: int):
    # 想看
    print("get user all collections with status: {} and subject type: {}")
    limit = 30
    offset = 0

    response = get_all_collections_by_pages(
        'dandelion_fs',
        subject_type,
        collection_type,
        limit=limit,
        offset=offset,
    )
    print("get response", response)
    for res in response:
        mark_subject(res.subject_id, CollectionType.DONE.value)
        print("Handling done:{}", res.subject_id)

    print(response)

def clone_user_collection_with_subject_type(subject_type: int):
    get_user_all_collections_with_status(
        subject_type, CollectionType.WANT.value)
    get_user_all_collections_with_status(
        subject_type, CollectionType.DONE.value)
    get_user_all_collections_with_status(
        subject_type, CollectionType.DOING.value)
    get_user_all_collections_with_status(
        subject_type, CollectionType.WAITING.value)
    get_user_all_collections_with_status(
        subject_type, CollectionType.CANCEL.value)

if __name__ == '__main__':
    # mark_want_subjects_form_files()
    # mark_done_subjects_form_files()
    clone_user_collection_with_subject_type(SubjectType.BOOK.value)
    clone_user_collection_with_subject_type(SubjectType.GAME.value)
    clone_user_collection_with_subject_type(SubjectType.ANIME.value)
    clone_user_collection_with_subject_type(SubjectType.MUSIC.value)
    clone_user_collection_with_subject_type(SubjectType.REAL_LIFE.value)
