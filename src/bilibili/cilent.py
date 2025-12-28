#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-12-06
@Links : https://github.com/bGZo
"""
import os

import requests

from demo import (api_endpoints)

class BilibiliClient:
    def __init__(self):
        self.cookie = os.getenv("BILIBILI_COOKIE")

        if not self.cookie:
            raise ValueError("BILIBILI_COOKIE environment variable is not set.")

        self.session = requests.Session()
        self.session.headers.update({
            "Cookie": f"{self.cookie}",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0",
            "Referer": "https://www.bilibili.com/"
        })
        self.api_endpoints = api_endpoints

