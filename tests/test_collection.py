#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-07-28
@Links : https://github.com/bGZo
"""
from bangumi.collection import mark_subject, get_all_collections_by_pages
from bangumi.enum import CollectionType, SubjectType


def test_mark_subject():
    from bangumi.client import BangumiClient

    client = BangumiClient()
    user = client.get_user()
    print(user)

    subject_id = 515880  # Replace with a valid subject ID
    status = 3  # Replace with the desired status

    response = mark_subject(subject_id, CollectionType.DONE.value)
    print(response)  # Print the response to verify the operation


def test_query_users_collection():
    response = get_all_collections_by_pages(
        'dandelion_fs',
        SubjectType.BOOK.value,
        CollectionType.WANT.value,
        limit=200,
        offset=0)
    print(response)


def test_query_users_collection_paged():
    username = 'dandelion_fs'
    subject_type = SubjectType.BOOK.value
    collection_type = CollectionType.WANT.value
    limit = 50
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
    print(f"总数: {len(all_results)}")
    # print(all_results)  # 如需输出全部内容可取消注释
