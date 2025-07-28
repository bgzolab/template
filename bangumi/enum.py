#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-07-28
@Links : https://github.com/bGZo
"""

from enum import Enum

# https://github.com/bangumi/api/blob/4433d6a0265e23a12324180569ac4abc964e682b/open-api/v0.yaml#L2283C5-L2283C26
class SubjectCollectionType(Enum):
    WANT = 1  # 想看
    DONE = 2  # 看过
    DOING = 3  # 在看
    WAITING = 4  # 搁置
    CANCEL = 5  # 抛弃
