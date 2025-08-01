#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-08-01
@Links : https://github.com/bGZo
"""
from bangumi_data.entity import BangumiData, SiteInfo
import requests

def get_data_by_year_month(year: int, month: int) -> list[BangumiData]:
    """
    请求指定年份和月份的 BangumiData 数据，并返回 BangumiData 对象列表
    """
    url = f"https://raw.githubusercontent.com/bangumi-data/bangumi-data/refs/heads/master/data/items/{year:04d}/{month:02d}.json"
    resp = requests.get(url)
    resp.raise_for_status()
    data_list = resp.json()
    # 反序列化为 BangumiData 对象列表
    result = []
    for data in data_list:
        result.append(BangumiData(
            title=data.get("title"),
            titleTranslate=data.get("titleTranslate", {}),
            type=data.get("type"),
            lang=data.get("lang"),
            officialSite=data.get("officialSite"),
            begin=data.get("begin"),
            broadcast=data.get("broadcast"),
            end=data.get("end"),
            comment=data.get("comment"),
            sites=[
                # SiteInfo 反序列化
                SiteInfo(**site)
                for site in data.get("sites", [])
            ]
        ))
    return result