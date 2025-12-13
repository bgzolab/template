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

class V2exClient:
    def __init__(self):
        self.token = os.getenv("V2EX_ACCESS_TOKEN")
        self.cookie = os.getenv("V2EX_COOKIE")

        if not self.token:
            raise ValueError("V2EX_ACCESS_TOKEN environment variable is not set.")
        if not self.cookie:
            raise ValueError("V2EX_COOKIE environment variable is not set.")

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Cookie": f"{self.cookie}",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0",
            "Referer": "https://www.v2ex.com"
        })
        self.api_endpoints = api_endpoints
