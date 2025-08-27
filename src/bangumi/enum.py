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

    @classmethod
    def all(cls) -> list[int]:
        return list(cls)

    @classmethod
    def get_name(cls, value) -> str:
        """
        根据 value 返回对应的收藏类型中文名
        """
        mapping = {
            cls.WANT.value: "想看",
            cls.DONE.value: "看过",
            cls.DOING.value: "正在看",
            cls.WAITING.value: "搁置",
            cls.CANCEL.value: "抛弃"
        }
        return mapping.get(value, "未知")

    @classmethod
    def get_name_en(cls, value) -> str:
        """
        根据 value 返回对应的收藏类型英文名
        """
        mapping = {
            cls.WANT.value: "want",
            cls.DONE.value: "done",
            cls.DOING.value: "doing",
            cls.WAITING.value: "waiting",
            cls.CANCEL.value: "canncel"
        }
        return mapping.get(value, "unknown")



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

    @classmethod
    def get_name(cls, value) -> str:
        """
        根据 value 返回对应的类型中文名
        """
        mapping = {
            cls.BOOK.value: "书籍",
            cls.ANIME.value: "动画",
            cls.MUSIC.value: "音乐",
            cls.GAME.value: "游戏",
            cls.REAL_LIFE.value: "三次元"
        }
        return mapping.get(value, "未知")

    @classmethod
    def get_name_en(cls, value) -> str:
        """
        根据 value 返回对应的类型中英文名
        """
        mapping = {
            cls.BOOK.value: "book",
            cls.ANIME.value: "anime",
            cls.MUSIC.value: "music",
            cls.GAME.value: "game",
            cls.REAL_LIFE.value: "real"
        }
        return mapping.get(value, "unknown")
