#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-08-18
@Links : https://github.com/bGZo
"""
from bangumi.api_endpoints import SUBJECT_QUERY, SUBJECT_CHARACTER_QUERY
from bangumi.client import BangumiClient
from bangumi.entity import SubjectV0, SubjectImages, SubjectTag, V0wiki, Rating, SubjectCollectionStat, SubjectRelatedCharacter, PersonImages, Actor


def get_subject_info(subject_id: int) -> SubjectV0:
    client = BangumiClient()
    res = client.session.get(
        SUBJECT_QUERY % subject_id
    )
    if res.status_code == 200:
        result = res.json()
        return _dict_to_subject(result)
    else:
        print(f"Error fetching {subject_id} info with response: {res.status_code} {res[res.status_code]}")
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

def _dict_to_subject_character(data: dict) -> SubjectRelatedCharacter:
    # 兼容 images 字段缺失 key 的情况
    images_data = data.get('images', {})
    images = PersonImages(
        small=images_data.get('small', ''),
        grid=images_data.get('grid', ''),
        large=images_data.get('large', ''),
        medium=images_data.get('medium', ''),
        common=images_data.get('common', '')
    ) if images_data else None
    actors = []
    for actor in data.get('actors', []):
        actor_images_data = actor.get('images', {})
        actor_images = PersonImages(
            small=actor_images_data.get('small', ''),
            grid=actor_images_data.get('grid', ''),
            large=actor_images_data.get('large', ''),
            medium=actor_images_data.get('medium', ''),
            common=actor_images_data.get('common', '')
        ) if actor_images_data else None
        actors.append(
            Actor(
                id=actor.get('id'),
                name=actor.get('name', ''),
                images=actor_images,
                short_summary=actor.get('short_summary', ''),
                career=actor.get('career', []) or [],
                type=actor.get('type', 0),
                locked=actor.get('locked', False)
            )
        )
    return SubjectRelatedCharacter(
        images=images,
        name=data.get('name', ''),
        relation=data.get('relation', ''),
        actors=actors,
        type=data.get('type', 0),
        id=data.get('id', 0)
    )

def get_subject_character(subject_id: int) -> list[SubjectRelatedCharacter]:
    client = BangumiClient()
    res = client.session.get(
        SUBJECT_CHARACTER_QUERY % subject_id
    )
    if res.status_code == 200:
        result = res.json()
        return [_dict_to_subject_character(item) for item in result]
    else:
        print(f"Error fetching character of {subject} with response: {res.status_code} {res[res.status_code]}")
        return []
