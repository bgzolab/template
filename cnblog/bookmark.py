#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-07-27
@Links : https://github.com/bGZo
"""
from cnblog.client import CnblogClient


def get_bookmark_list() -> list:
    """
    Fetches the list of bookmarks from the CNBlog API.

    Returns:
        list: A list of bookmarks.
    """
    client = CnblogClient()
    response = client.session.get(client.api_endpoints.BOOKMARK)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()  # Raise an error for bad responses

