#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-07-27
@Links : https://github.com/bGZo
"""
from cnblog.client import CnblogClient
from dataclasses import dataclass
from typing import List, Any

@dataclass
class Bookmark:
    WzLinkId: int
    Title: str
    LinkUrl: str
    Summary: str
    Tags: List[Any]
    DateAdded: str
    FromCNBlogs: bool

    @staticmethod
    def from_dict(data: dict) -> "Bookmark":
        return Bookmark(
            WzLinkId=data.get("WzLinkId"),
            Title=data.get("Title"),
            LinkUrl=data.get("LinkUrl"),
            Summary=data.get("Summary"),
            Tags=data.get("Tags", []),
            DateAdded=data.get("DateAdded"),
            FromCNBlogs=data.get("FromCNBlogs"),
        )

def get_bookmark_list() -> list:
    """
    Fetches the list of bookmarks from the CNBlog API.

    Returns:
        list: A list of bookmarks.
    """
    client = CnblogClient()
    response = client.session.get(client.api_endpoints.BOOKMARK)
    if response.status_code == 200:
        data = response.json()
        # 支持单个对象或对象列表
        if isinstance(data, dict):
            return [Bookmark.from_dict(data)]
        return [Bookmark.from_dict(item) for item in data]
    else:
        response.raise_for_status()  # Raise an error for bad responses

if __name__ == '__main__':
    try:
        bookmarks = get_bookmark_list()
        for bm in bookmarks:
            print(bm.Title, bm.LinkUrl)
    except Exception as e:
        print(f"An error occurred: {e}")
