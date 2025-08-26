#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-07-27
@Links : https://github.com/bGZo
"""
from multiprocessing.connection import Client

import requests

from cnblog.api_endpoints import USER
from cnblog.client import CnblogClient


def get_current_user_info() -> dict:
    client = CnblogClient()
    response = client.session.get(USER)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()  # Raise an error for bad responses

if __name__ == '__main__':
    try:
        user_info = get_current_user_info()
        print(user_info)
    except requests.RequestException as e:
        print(f"An error occurred: {e}")