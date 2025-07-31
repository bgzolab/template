#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-07-28
@Links : https://github.com/bGZo
"""
from http.client import responses

from bangumi.api_endpoints import COLLECTIONS_UPSERT, COLLECTIONS_QUERY_USERS
from bangumi.client import BangumiClient


def mark_subject(subject_id: int, status: int, comment: str = "", tags: list[str] = None) -> bool:
    """
    Mark a subject with a specific status and optional comment and tags.

    :param subject_id: The ID of the subject to mark.
    :param status: The status to set for the subject (e.g., "collect", "wish", "do", "on_hold", "drop").
    :param comment: An optional comment about the subject.
    :param tags: An optional list of tags to associate with the subject.
    :return: A dictionary containing the response from the API.
    """
    # Implementation would go here
    if tags is None:
        tags = []
    client = BangumiClient()
    payload = {
        "type": status,
        "rate": 0,
        # "ep_status": 0,
        # "vol_status": 0,
        "comment": comment,
        "private": False,
        "tags": tags
    }

    response = client.session.post(COLLECTIONS_UPSERT % subject_id, json=payload)
    # Accept special for bgm
    if response.status_code == 202:
        return True
    else:
        print(f"Error marking subject: {response.status_code} {responses[response.status_code]}")
        print("Request payload:", payload)
        print("Response:", response.text)
        print(f"Error marking subject: {response.status_code} {responses[response.status_code]}")  # noqa: E501
        return False

def get_all_collections_by_pages(username: str, subject_type: str, type: str, limit: int = 100, offset: int = 0) -> list:
    """
    Get all collections for a specific subject type and type by pages.

    :param subject_type: The type of the subject (e.g., "anime", "book").
    :param type: The collection type (e.g., "collect", "wish").
    :param limit: The number of items to return per page.
    :param offset: The offset for pagination.
    :return: A list of collections.
    """
    client = BangumiClient()
    response = client.session.get(
        COLLECTIONS_QUERY_USERS % username,
        params={
            "subject_type":subject_type,
            "type":type,
            "limit": limit,
            "offset": offset
        }
    )
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching collections: {response.status_code} {responses[response.status_code]}")
        return []
