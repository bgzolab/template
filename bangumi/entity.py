#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
上游定义： https://github.com/bangumi/server

@Author : bGZo
@Date : 2025-07-31
@Links : https://github.com/bGZo
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

# https://github.com/bangumi/server/blob/fb44e70f9fac931fc29964cab9c5b5aec41433b0/web/res/image.go#L47
@dataclass
class SubjectImages:
    small: str
    grid: str
    large: str
    medium: str
    common: str

# https://github.com/bangumi/server/blob/fb44e70f9fac931fc29964cab9c5b5aec41433b0/web/res/subject.go#L38-L42
@dataclass
class SubjectTag:
    # 根据实际结构补充字段
    name: str
    count: int
    total_cont: int


# https://github.com/bangumi/server/blob/fb44e70f9fac931fc29964cab9c5b5aec41433b0/web/res/subject.go#L66C1-L81C2
@dataclass
class SlimSubjectV0:
    date: Optional[str]
    images: SubjectImages  # 修正为 images
    name: str
    name_cn: str
    short_summary: str
    tags: List[SubjectTag]
    score: float
    type: int
    id: int
    eps: int
    volumes: int
    collection_total: int
    rank: int

# https://github.com/bangumi/server/blob/fb44e70f9fac931fc29964cab9c5b5aec41433b0/internal/collections/domain/collection/model.go#L34
@dataclass
class UserSubjectCollection:
    id: int
    updated_at: datetime
    comment: Optional[str]
    tags: List[str]
    vol_status: int
    ep_status: int
    subject_id: int
    subject_type: int
    rate: int
    type: int
    private: bool
    subject: SlimSubjectV0
