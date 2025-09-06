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


