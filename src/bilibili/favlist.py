#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-12-28
@Links : https://github.com/bGZo
"""
from bilibili import api_endpoints
from bilibili.cilent import BilibiliClient
from bilibili.entity import BilibiliFavListResponse

def get_bilibili_favlistd(fid: int, page: int, size: int) -> BilibiliFavListResponse:
    bc = BilibiliClient()
    res = bc.session.get(api_endpoints.BILIBILI_FAV_URL, params={
        # 搜索
        "keyword": "",
        # 收藏夹ID
        "media_id": fid,
        # 排序方式
        # mtime ——》 最近收藏
        "order": "mtime",
        # 网页端
        "platform": "web",
        # 分页
        "pn": page,
        # 大小
        "ps": size,
        # ?
        "tid": 0,
        # ?
        "type": 0,
        # ?
        "web_location": 333.1387,
    })
    return BilibiliFavListResponse.from_dict(res.json())

if __name__ == "__main__":
    print(get_bilibili_favlistd(49128283, 1, 1))
