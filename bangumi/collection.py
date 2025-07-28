#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-07-28
@Links : https://github.com/bGZo
"""
from http.client import responses

from bangumi.api_endpoints import COLLECTIONS_UPSERT
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

