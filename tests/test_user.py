#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-07-28
@Links : https://github.com/bGZo
"""
from bangumi.client import BangumiClient


def test_get_user():
    client = BangumiClient()
    print(client.get_user())