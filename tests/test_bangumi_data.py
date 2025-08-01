#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-08-01
@Links : https://github.com/bGZo
"""
from bangumi_data.data import get_data_by_year_month

def test_bangumi_data():
    data = get_data_by_year_month(2024, 8)
    print(data)
