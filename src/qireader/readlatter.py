#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-12-06
@Links : https://github.com/bGZo
"""
from typing import List, Optional
from charset_normalizer import from_fp

from qireader.cilent import QiReaderClient
from qireader.models import QiReaderResponse, Entry


def get_list_from_read_latter(tag_id: str, oldThan: Optional[str]) -> List[Entry]:
    """
    target-url: https://www.qireader.com/api/streams/{tagId}?articleOrder=0&count=25&id={tagId}&unreadOnly=false&olderThan=1764313764608411573

    :param tag-xxx
    """
    client = QiReaderClient()
    response = client.session.get(client.api_endpoints.READ_LATER + tag_id,  params={
        'articleOrder': 0,
        'count': 25,
        'id': tag_id,
        'unreadOnly': "False",
        'olderThan': oldThan
    })
    
    if response.status_code == 200:
        return QiReaderResponse.from_dict(response.json()).result.entries
    return []


def get_all_list_from_read_latter_debug(tag_id: str) -> List[Entry]:
    all_entries = []
    older_than = None

    while True:
        entries = get_list_from_read_latter(tag_id, older_than)
        if not entries:
            break
        all_entries.extend(entries)
        older_than = str(entries[-1].timestamp)

    return all_entries

if __name__ == '__main__':
    try:
        bookmarks = get_list_from_read_latter("tag-xxx", None)
        # bookmarks = get_all_list_from_read_latter("tag-Jw3lnV59k7Vaky2g")
        print(bookmarks)
    except Exception as e:
        print(f"An error occurred: {e}")
