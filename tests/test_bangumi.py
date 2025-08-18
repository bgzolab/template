#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-08-19
@Links : https://github.com/bGZo
"""
from bangumi.subject import get_subject_info

def test_subject_get():
    res = get_subject_info(1)
    print(res)
