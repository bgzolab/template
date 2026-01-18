#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-07-27
@Links : https://github.com/bGZo
"""
from dataclasses import dataclass

# Webpage Meta Template
@dataclass
class WebPage:
    comments:bool
    draft:bool
    title: str
    source: str
    created: str
    modified: str
    type: str

# Video Meta Template
@dataclass
class Video:
    comments:bool
    draft:bool
    title: str
    cover: str
    author: str
    created: str
    modified: str
    published: str
    description: str
    source: str
    tags: list[str]
    type: str

