#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-09-06
@Links : https://github.com/bGZo
"""
from timeline.api_endpoints import TIMELINE_PAGE
from timeline.client import BangumiCookieClient
from bs4 import BeautifulSoup


def get_timeline_page_html(page: int, username: str) -> str:
    request_url = TIMELINE_PAGE % username
    client = BangumiCookieClient()
    response = client.session.get(request_url, params={"page": page})
    return response.text

def get_page_item_ids(html_content: str) -> list[str]:
    soup = BeautifulSoup(html_content, "html.parser")
    item_ids = [li.get('id')[4:] for li in soup.find(id='timeline').findAll('li') if li.get('id')]
    return item_ids

