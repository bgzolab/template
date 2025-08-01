#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-08-01
@Links : https://github.com/bGZo
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union

@dataclass
class SiteInfo:
    site: str
    id: Optional[str] = None
    url: Optional[str] = None
    begin: Optional[str] = None
    broadcast: Optional[str] = None
    comment: Optional[str] = None

@dataclass
class BangumiData:
    title: str
    titleTranslate: Dict[str, List[str]]
    type: str
    lang: str
    officialSite: str
    begin: str
    broadcast: Optional[str]
    end: str
    comment: Optional[str]
    sites: List[SiteInfo]
