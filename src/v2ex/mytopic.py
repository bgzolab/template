#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
因为API没有提供这个接口，所以只能通过解析HTML来实现获取我的主题列表功能，进度参考：

https://www.v2ex.com/t/1035675

总体希望不大

@Author : bGZo
@Date : 2025-12-13
@Links : https://github.com/bGZo
"""
from bs4 import BeautifulSoup

from v2ex.cilent import V2exClient
from v2ex.api_endpoints import V2EX_FAV


def get_fav_html_with_page(page: int) -> str:
    """
    获取我的主题页面的HTML内容

    :param page: 页码
    :return: HTML内容字符串
    """
    client = V2exClient()
    response = client.session.get(V2EX_FAV, params={"p": page})
    return response.text


def get_fav_list_topic_id_page(page: int) -> list[int]:
    """
    获取我的主题页面的主题ID列表

    :param page: 页码
    :return: 主题ID列表
    """
    fav_html = get_fav_html_with_page(page)
    soup = BeautifulSoup(fav_html, 'html.parser')
    topic_id_list = []
    for topic_link in soup.select('a[href^="/t/"]'):
        href = topic_link.get('href')
        if href:
            try:
                topic_id = int(href.split('/t/')[1].split('#')[0])
                topic_id_list.append(topic_id)
            except ValueError:
                continue
    return list(set(topic_id_list))


if __name__ == '__main__':
    page = 1
    # fav_html = get_fav_html_with_page(page)
    # print(fav_html)
    topic_ids = get_fav_list_topic_id_page(page)
    print(topic_ids)
