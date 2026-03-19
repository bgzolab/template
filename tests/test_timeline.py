#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-09-06
@Links : https://github.com/bGZo
"""

def test_get_timeline_page_html():
    from timeline.timeline import get_timeline_page_html
    username = "bool"
    page = 1
    html_content = get_timeline_page_html(page, username)
    print(html_content)  # Print the HTML content to verify the operation
    return html_content

def test_get_id_list_from_page_1():
    html = test_get_timeline_page_html()
    from timeline.timeline import get_timeline_page_html, get_page_item_id_list
    id_list = get_page_item_id_list(html)
    print(id_list)


def test_delete_timeline_item():
    from timeline.timeline import delete_timeline_item
    print(delete_timeline_item('57291228'))

def test_delete_user_timeline():
    from timeline.timeline import delete_user_timeline
    delete_user_timeline("bool", '', max_page=100)
