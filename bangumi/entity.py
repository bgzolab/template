#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
上游定义： https://github.com/bangumi/server

@Author : bGZo
@Date : 2025-07-31
@Links : https://github.com/bGZo
"""

from dataclasses import dataclass
from typing import List, Optional, Any
from datetime import datetime

# https://github.com/bangumi/server/blob/fb44e70f9fac931fc29964cab9c5b5aec41433b0/web/res/image.go#L47
@dataclass
class SubjectImages:
    small: str
    grid: str
    large: str
    medium: str
    common: str

@dataclass
class PersonImages:
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

@dataclass
class Rating:
    rank: Optional[int] = None
    total: Optional[int] = None
    count: Optional[int] = None
    score: Optional[float] = None

@dataclass
class SubjectCollectionStat:
    wish: int = 0
    collect: int = 0
    doing: int = 0
    on_hold: int = 0
    dropped: int = 0
    total: int = 0

@dataclass
class SubjectV0:
    date: Optional[str]
    platform: Optional[str]
    images: SubjectImages
    summary: str
    name: str
    name_cn: str
    tags: List[SubjectTag]
    infobox: Optional[List[Any]]
    rating: Optional[Rating]
    total_episodes: int
    collection: Optional[SubjectCollectionStat]
    id: int
    eps: int
    meta_tags: List[str]
    volumes: int
    series: bool
    locked: bool
    nsfw: bool
    type_id: int
    redirect: Optional[int]

@dataclass
class Actor:
    id: int
    name: str
    images: Optional[PersonImages] = None
    short_summary: str = ""
    career: List[str] = None
    type: int = 0
    locked: bool = False

@dataclass
class SubjectRelatedCharacter:
    images: PersonImages
    name: str
    relation: str
    actors: List[Actor]
    type: int
    id: int

# V0wiki 仅为 infobox 的类型别名，等价于 List[Any]
V0wiki = List[Any]
