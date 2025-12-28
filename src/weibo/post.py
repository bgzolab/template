#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-12-28
@Links : https://github.com/bGZo
"""
from utils.file_utils import output_file_path
from weibo.api_endpoints import WEIBO_LONGTEXT_URL
from weibo.cilent import WeiboClient

def get_weibo_longtext_by_id(id: str) -> str:
    wb = WeiboClient()
    response = wb.session.get(WEIBO_LONGTEXT_URL, params={
        "id": id,
    })
    try:
        json = response.json()
        return json['data']['longTextContent']
    except Exception as e:
        return None

if __name__ == '__main__':
    print(get_weibo_longtext_by_id("QjPyj1Vny"))


