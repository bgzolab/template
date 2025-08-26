#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-07-27
@Links : https://github.com/bGZo
"""
BASE_URL = "https://api.cnblogs.com/api"

#Users
USER = f"{BASE_URL}/users"

# Bookmarks API Endpoints
BOOKMARK = f"{BASE_URL}/Bookmarks"
BOOKMARK_DELETE = f"{BASE_URL}/bookmarks/"

# Articles API Endpoints
# https://api.cnblogs.com/api/blogposts/9953718/body
BLOG_POST = f"{BASE_URL}/blogposts/%s/body"
