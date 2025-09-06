#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-07-27
@Links : https://github.com/bGZo
"""
import os
import requests

from bangumi import api_endpoints
from bangumi.api_endpoints import USER_CURRENT

class BangumiCookieClient:
    def __init__(self):
        self.cookie = os.getenv("BGM_ACCESS_COOKIE")
        if not self.cookie:
            raise ValueError("BGM_ACCESS_COOKIE environment variable is not set.")
        self.session = requests.Session()
        self.session.headers.update({
            "Cookie": self.cookie,
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:143.0) Gecko/20100101 Firefox/143.0"
        })
        self.api_endpoints = api_endpoints
