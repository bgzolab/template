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

class DemoClient:
    def __init__(self):
        self.token = os.getenv("DEMO_TOKEN")
        self.cookie = os.getenv("DEMO_COOKIE")

        if not self.token:
            raise ValueError("DEMO_TOKEN environment variable is not set.")
        if not self.cookie:
            raise ValueError("DEMO_COOKIE environment variable is not set.")

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Cookie": f"{self.cookie}",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0",
            "Referer": "https://www.example.com"
        })
        self.api_endpoints = api_endpoints

