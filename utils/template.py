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
    title: str
    source: str
    created: str
    modified: str
    type: str
