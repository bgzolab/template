#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-12-27
@Links : https://github.com/bGZo
"""
from typing import Optional
from weibo.api_endpoints import WEIBO_LIKE_URL
from weibo.cilent import WeiboClient
from weibo.entity import WeiboResponse

def get_weibo_like_list(uid: int, page: int) -> Optional[WeiboResponse]:
    wb = WeiboClient()
    response = wb.session.get(WEIBO_LIKE_URL, params={
        "page": page,
        "uid": uid,
        "with_total": True,
    })
    if response.status_code == 200:
        return WeiboResponse.from_dict(response.json())
    return None

if __name__ == '__main__':
    print(get_weibo_like_list(8221250887, 1))
