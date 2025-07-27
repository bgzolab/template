#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-07-27
@Links : https://github.com/bGZo
"""

def get_cnblog_post_body_by_url(url: str):
    """
    获取指定 ID 的博客文章正文内容。

    :param id: 博客文章的 ID
    :return: 博客文章正文内容
    """
    from cnblog.client import CnblogClient
    from cnblog.api_endpoints import BLOG_POST

    client = CnblogClient()

    # 从 URL 中提取 ID
    id = url.split('/')[-1]  # 假设 URL 以 ID
    response = client.session.get(BLOG_POST % id)
    # % 是 Python 早期的字符串格式化操作符。它会查找字符串中的 % 占位符（如 %s），并用后面的值替换它。

    if response.status_code == 200:
        return response.text
    else:
        response.raise_for_status()  # Raise an error for bad responses
