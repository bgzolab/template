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

class BangumiClient:
    def __init__(self):
        self.token = os.getenv("BGM_ACCESS_TOKEN")
        if not self.token:
            raise ValueError("BGM_ACCESS_TOKEN environment variable is not set.")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "User-Agent": f"bGZo/self-debug-private-project"
        })
        self.api_endpoints = api_endpoints

    def get_user(self):
        resp = self.session.get(USER_CURRENT)
        return resp.json()
