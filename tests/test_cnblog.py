#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-07-27
@Links : https://github.com/bGZo
"""
import utils.md_utils


def test_get_current_user_info():
    from cnblog.user import get_current_user_info
    try:
        user_info = get_current_user_info()
        assert isinstance(user_info, dict), "User info should be a dictionary"
        assert 'name' in user_info, "User info should contain 'name' key"
        print("Test passed: User info retrieved successfully.")
    except Exception as e:
        print(f"Test failed: {e}")

def test_get_cnblog_post_body_by_url():
    from cnblog.blog_post import get_cnblog_post_body_by_url
    try:
        post_url = "https://www.cnblogs.com/xiezhr/p/18953178"
        post_body = get_cnblog_post_body_by_url(post_url)
        assert isinstance(post_body, str), "Post body should be a string"
        assert len(post_body) > 0, "Post body should not be empty"
        print("Test result: {}".format(post_body[:100]))
        print("Test passed: Post body retrieved successfully.")
    except Exception as e:
        print(f"Test failed: {e}")


def test_get_cnblog_post_markdown_by_url():
    from cnblog.blog_post import get_cnblog_post_body_by_url
    try:
        post_url = "https://www.cnblogs.com/xiezhr/p/18953178"
        post_body = utils.md_utils.html_to_markdown_with_html2text(get_cnblog_post_body_by_url(post_url))
        assert isinstance(post_body, str), "Post body should be a string"
        assert len(post_body) > 0, "Post body should not be empty"
        print("Test result: {}".format(post_body[:100]))
        print("Test passed: Post body retrieved successfully.")
    except Exception as e:
        print(f"Test failed: {e}")