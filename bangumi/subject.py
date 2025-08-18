#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-08-18
@Links : https://github.com/bGZo
"""
from bangumi.api_endpoints import SUBJECT_QUERY
from bangumi.client import BangumiClient
from bangumi.entity import SubjectV0, SubjectImages, SubjectTag, V0wiki, Rating, SubjectCollectionStat


def get_subject_info(subject_id: int) -> SubjectV0:
    client = BangumiClient()
    res = client.session.get(
        SUBJECT_QUERY % subject_id
    )
    if res.status_code == 200:
        result = res.json()
        return _dict_to_subject(result)
    else:
        print(f"Error fetching collections: {res.status_code} {res[res.status_code]}")
        return None


def _dict_to_subject(data: dict) -> SubjectV0:
    images = SubjectImages(**data.get('images', {})) if data.get('images') else None
    tags = [SubjectTag(**tag) for tag in data.get('tags', [])]
    # infobox: List[Any]，此处直接传递原始list
    infobox = data.get('infobox', None)
    rating_data = data.get('rating', None)
    rating = None
    if rating_data:
        # rating.count 可能是 dict，需特殊处理
        count = rating_data.get('count')
        if isinstance(count, dict):
            # 直接存原始dict
            rating = Rating(
                rank=rating_data.get('rank'),
                total=rating_data.get('total'),
                count=count,
                score=rating_data.get('score')
            )
        else:
            rating = Rating(**rating_data)
    collection_data = data.get('collection', None)
    collection = None
    if collection_data:
        collection = SubjectCollectionStat(
            wish=collection_data.get('wish', 0),
            collect=collection_data.get('collect', 0),
            doing=collection_data.get('doing', 0),
            on_hold=collection_data.get('on_hold', 0),
            dropped=collection_data.get('dropped', 0),
            total=collection_data.get('total', 0)
        )
    return SubjectV0(
        date=data.get('date'),
        platform=data.get('platform'),
        images=images,
        summary=data.get('summary', ''),
        name=data.get('name', ''),
        name_cn=data.get('name_cn', ''),
        tags=tags,
        infobox=infobox,
        rating=rating,
        total_episodes=data.get('total_episodes', 0),
        collection=collection,
        id=data.get('id', 0),
        eps=data.get('eps', 0),
        meta_tags=data.get('meta_tags', []),
        volumes=data.get('volumes', 0),
        series=data.get('series', False),
        locked=data.get('locked', False),
        nsfw=data.get('nsfw', False),
        type_id=data.get('type', 0),
        redirect=data.get('redirect')
    )
