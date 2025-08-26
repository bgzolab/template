#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-07-27
@Links : https://github.com/bGZo
"""
import os
import requests

from cnblog import api_endpoints
from cnblog.api_endpoints import USER

class CnblogClient:
    def __init__(self):
        self.token = os.getenv("CNBLOG_ACCESS_TOKEN")
        if not self.token:
            raise ValueError("CNBLOG_ACCESS_TOKEN environment variable is not set.")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}"
        })
        self.api_endpoints = api_endpoints

    def get_user(self):
        resp = self.session.get(USER)
        return resp.json()
