#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-07-28
@Links : https://github.com/bGZo
"""
import os
import re

import click
import uvicorn
from bs4 import BeautifulSoup

import web.main_web
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


def get_user_all_collections_with_status(username: str, subject_type: int, collection_type: int):
    # 想看
    print(f"get user={username} collections({subject_type}) with status: {collection_type}")
    limit = 30
    offset = 0

    all_results = []
    while True:
        results = get_all_collections_by_pages(
            username,
            subject_type,
            collection_type,
            limit=limit,
            offset=offset
        )
        if not results:
            break
        all_results.extend(results)
        if len(results) < limit:
            break
        offset += limit

    print("get response=", all_results)
    for res in all_results:
        mark_subject(res.subject_id, CollectionType.DONE.value)
        print(f"Handling done={res.subject_id}")


def clone_user_collection_with_subject_type(username: str, subject_type: int):
    get_user_all_collections_with_status(username,
        subject_type, CollectionType.WANT.value)
    get_user_all_collections_with_status(username,
        subject_type, CollectionType.DONE.value)
    get_user_all_collections_with_status(username,
        subject_type, CollectionType.DOING.value)
    get_user_all_collections_with_status(username,
        subject_type, CollectionType.WAITING.value)
    get_user_all_collections_with_status(username,
        subject_type, CollectionType.CANCEL.value)

def clone_from_html_archives():
    mark_want_subjects_form_files()
    mark_done_subjects_form_files()

@click.command()
@click.argument('username')
def clone_someone(username: str):
    clone_user_collection_with_subject_type(username, SubjectType.BOOK.value)
    clone_user_collection_with_subject_type(username, SubjectType.GAME.value)
    clone_user_collection_with_subject_type(username, SubjectType.ANIME.value)
    clone_user_collection_with_subject_type(username, SubjectType.MUSIC.value)
    clone_user_collection_with_subject_type(username, SubjectType.REAL_LIFE.value)

@click.command()
def server():
    uvicorn.run(web.main_web.app, host="0.0.0.0", port=8000)

