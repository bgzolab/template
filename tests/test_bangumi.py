#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-08-19
@Links : https://github.com/bGZo
"""
from bangumi.bangumi import get_subject_info, get_subject_character

def test_subject_get():
    res = get_subject_info(1)
    print(res)

def test_subject_character():
    res = get_subject_character(2)
    print(res)
