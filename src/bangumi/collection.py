#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-07-28
@Links : https://github.com/bGZo
"""
from http.client import responses
from datetime import datetime

from bangumi.api_endpoints import COLLECTIONS_UPSERT, COLLECTIONS_QUERY_USERS
from bangumi.client import BangumiClient
from bangumi.entity import UserSubjectCollection, SlimSubjectV0, SubjectImages, SubjectTag


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

def _dict_to_subject_images(d: dict) -> SubjectImages:
    return SubjectImages(**d)

def _dict_to_subject_tag_list(lst: list) -> list:
    return [SubjectTag(**tag) for tag in lst]

def _dict_to_slim_subject_v0(d: dict) -> SlimSubjectV0:
    return SlimSubjectV0(
        date=d.get("date"),
        images=_dict_to_subject_images(d["images"]),
        name=d["name"],
        name_cn=d["name_cn"],
        short_summary=d["short_summary"],
        tags=_dict_to_subject_tag_list(d.get("tags", [])),
        score=d["score"],
        type=d["type"],
        id=d["id"],
        eps=d["eps"],
        volumes=d["volumes"],
        collection_total=d["collection_total"],
        rank=d["rank"]
    )

def _dict_to_user_subject_collection(d: dict) -> UserSubjectCollection:
    return UserSubjectCollection(
        id=d.get("id", 0),
        updated_at=datetime.fromisoformat(d["updated_at"]),
        comment=d.get("comment"),
        tags=d.get("tags", []),
        vol_status=d["vol_status"],
        ep_status=d["ep_status"],
        subject_id=d["subject_id"],
        subject_type=d["subject_type"],
        rate=d["rate"],
        type=d["type"],
        private=d["private"],
        subject=_dict_to_slim_subject_v0(d["subject"])
    )

# TODO 包装返回全部的分页结果
def get_all_collections_by_pages(username: str, subject_type: int, collection_type: int, limit: int = 30, offset: int = 0) -> list[UserSubjectCollection]:
    """
    Get all collections for a specific subject type and type by pages.

    :param subject_type: The type of the subject (e.g., "anime", "book").
    :param collection_type: The collection type (e.g., "collect", "wish").
    :param limit: The number of items to return per page.
    :param offset: The offset for pagination.
    :return: A list of collections.
    """
    client = BangumiClient()
    response = client.session.get(
        COLLECTIONS_QUERY_USERS % username,
        params={
            "subject_type":subject_type,
            "type":collection_type,
            "limit": limit,
            "offset": offset
        }
    )
    if response.status_code == 200:
        result = response.json()
        return [
            _dict_to_user_subject_collection(item)
            for item in result.get("data", [])
        ]
    else:
        print(f"Error fetching collections page with response: {response.status_code} {responses[response.status_code]}")
        return []
