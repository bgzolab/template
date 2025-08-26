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
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class BangumiClient:
    def __init__(self):
        self.token = os.getenv("BGM_ACCESS_TOKEN")
        if not self.token:
            raise ValueError("BGM_ACCESS_TOKEN environment variable is not set.")
        self.session = self._get_retry_session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "User-Agent": f"bGZo/self-debug-private-project"
        })
        self.api_endpoints = api_endpoints

    def _get_retry_session(self, retries=10, backoff_factor=0.3, timeout=30):
        session = requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=(500, 502, 504),
            allowed_methods=frozenset(['GET', 'POST']),
            raise_on_status=False
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        # 给 session 增加默认超时
        session.request = self._wrap_request_with_timeout(session.request, timeout)
        return session

    def _wrap_request_with_timeout(self, func, timeout):
        def wrapper(*args, **kwargs):
            if 'timeout' not in kwargs:
                kwargs['timeout'] = timeout
            return func(*args, **kwargs)
        return wrapper

    def get_user(self):
        resp = self.session.get(USER_CURRENT)
        return resp.json()
