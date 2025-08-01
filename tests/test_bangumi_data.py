#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-08-01
@Links : https://github.com/bGZo
"""
from bangumi_data.client import BangumiDataClient

def test_bangumi_data():
    dataClient = BangumiDataClient()
    data = dataClient.get_bangumi_data(2024, 8)
    print(data)
