#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-07-28
@Links : https://github.com/bGZo
"""

from enum import Enum

class CollectionType(Enum):
    """
    https://bangumi.github.io/api/#/model-CollectionType
    1: 想看
    2: 看过
    3: 在看
    4: 搁置
    5: 抛弃
    """
    WANT = 1
    DONE = 2
    DOING = 3
    WAITING = 4
    CANCEL = 5

    @classmethod
    def from_value(cls, value):
        for item in cls:
            if item.value == value:
                return item
        raise ValueError(f"Invalid value for CollectionTypeEnum: {value}")


class SubjectType(Enum):
    """
    via: https://bangumi.github.io/api/#model-SubjectType
    1 为 书籍
    2 为 动画
    3 为 音乐
    4 为 游戏
    6 为 三次元
    没有 5
    """
    BOOK = 1
    ANIME = 2
    MUSIC = 3
    GAME = 4
    REAL_LIFE = 6

    @classmethod
    def from_value(cls, value):
        for item in cls:
            if item.value == value:
                return item
        raise ValueError(f"Invalid value for SubjectTypeEnum: {value}")