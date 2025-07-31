#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
因为第三方API没有这个，所以只能用 传统 Cookie 的方式来获取时间线数据

@Author : bGZo
@Date : 2025-07-31
@Links : https://github.com/bGZo
"""

def get_user_timeline(username: str, limit: int = 30, offset: int = 0) -> list:
    """
    获取用户时间线数据
    :param username: 用户名
    :param limit: 每页数量
    :param offset: 偏移量
    :return: 时间线数据列表
    """
    # https://bgm.tv/user/dandelion_fs/timeline?page=12&ajax=1
    # 这里需要实现获取时间线的逻辑，可能需要使用 requests 库来发送 HTTP 请求
    # TODO 由于没有第三方API，这里假设有一个函数可以获取时间线数据
    raise NotImplementedError("时间线的逻辑")