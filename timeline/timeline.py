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
from timeline.api_endpoints import TIMELINE_DELETE


def get_timeline_page_html(page: int, username: str) -> str:
    request_url = TIMELINE_PAGE % username
    client = BangumiCookieClient()
    response = client.session.get(request_url, params={"page": page})
    return response.text

def get_page_item_id_list(html_content: str) -> list[str]:
    soup = BeautifulSoup(html_content, "html.parser")
    timeline_html = soup.find(id='timeline')
    if not timeline_html:
        return []
    return  [li.get('id')[4:] for li in timeline_html.findAll('li') if li.get('id')]

def delete_timeline_item(item_id: str) -> bool:
    client = BangumiCookieClient()
    request_url = TIMELINE_DELETE % item_id
    response = client.session.get(request_url, params={
        "ajax": 1,
        "gh": "eef61b71"
    })
    print(response.text)
    try:
        if response.status_code == 200 and response.json().get('status') == 'ok':
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


def delete_user_timeline(username: str, max_page: int = 100):
    for page in range(1, max_page + 1):
        html = get_timeline_page_html(page, username)
        id_list = get_page_item_id_list(html)
        if len(id_list) == 0:
            print(f"No more items found on page {page}. Stopping.")
            break
        print(f"Deleting items from page {page}, found {len(id_list)} items.")
        for item_id in id_list:
            try:
                success = delete_timeline_item(item_id)
                if success:
                    print(f"Successfully deleted item with ID: {item_id}")
                else:
                    print(f"Failed to delete item with ID: {item_id}")
            except Exception as e:
                print(f"Error deleting item with ID {item_id}: {e}")
