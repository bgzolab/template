#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-12-13
@Links : https://github.com/bGZo
"""
from typing import Optional
from v2ex.api_endpoints import V2EX_API_TOPICS
from v2ex.cilent import V2exClient
from v2ex.entity import TopicResponse


def get_v2ex_topic_info(topic_id: int) -> Optional[TopicResponse]:
    client = V2exClient()
    response = client.session.get(V2EX_API_TOPICS.format(topic_id=topic_id))
    
    if response.status_code == 200:
        return TopicResponse.from_dict(response.json())
    return None
    
if __name__ == '__main__':
    test_topic_id = "1"
    topic_info = get_v2ex_topic_info(test_topic_id)
    print(topic_info)
