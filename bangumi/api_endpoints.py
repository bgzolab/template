#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-07-29
@Links : https://github.com/bGZo
"""
BASE_URL = "https://api.bgm.tv"

#Users
USER_CURRENT = f"{BASE_URL}/v0/me"

# Collection API Endpoints
COLLECTIONS_UPSERT = f"{BASE_URL}/v0/users/-/collections/%s"
# https://api.bgm.tv/v0/users/dandelion_fs/collections?subject_type&type&limit=1&offset=0
COLLECTIONS_QUERY_USERS = f"{BASE_URL}/v0/users/%s/collections"

# Subject API Endpoints
SUBJECT_QUERY = f"{BASE_URL}/v0/subjects/%s"
SUBJECT_CHARACTER_QUERY = f"{BASE_URL}/v0/subjects/%s/characters"
