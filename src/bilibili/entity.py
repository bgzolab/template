#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-12-13
@Links : https://github.com/bGZo
"""
from dataclasses import dataclass
from typing import List, Optional, Any

@dataclass
class BilibiliUpper:
    mid: int
    name: str
    face: str
    followed: Optional[bool] = None
    vip_type: Optional[int] = None
    vip_statue: Optional[int] = None
    jump_link: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'BilibiliUpper':
        if obj is None:
            return None
        return BilibiliUpper(
            mid=obj.get("mid"),
            name=obj.get("name"),
            face=obj.get("face"),
            followed=obj.get("followed"),
            vip_type=obj.get("vip_type"),
            vip_statue=obj.get("vip_statue"),
            jump_link=obj.get("jump_link")
        )

@dataclass
class BilibiliFavCntInfo:
    collect: int
    play: int
    thumb_up: int
    share: int

    @staticmethod
    def from_dict(obj: Any) -> 'BilibiliFavCntInfo':
        if obj is None:
            return None
        return BilibiliFavCntInfo(
            collect=obj.get("collect"),
            play=obj.get("play"),
            thumb_up=obj.get("thumb_up"),
            share=obj.get("share")
        )

@dataclass
class BilibiliFavInfo:
    id: int
    fid: int
    mid: int
    attr: int
    title: str
    cover: str
    upper: BilibiliUpper
    cover_type: int
    cnt_info: BilibiliFavCntInfo
    type: int
    intro: str
    ctime: int
    mtime: int
    state: int
    fav_state: int
    like_state: int
    media_count: int
    is_top: bool

    @staticmethod
    def from_dict(obj: Any) -> 'BilibiliFavInfo':
        if obj is None:
            return None
        return BilibiliFavInfo(
            id=obj.get("id"),
            fid=obj.get("fid"),
            mid=obj.get("mid"),
            attr=obj.get("attr"),
            title=obj.get("title"),
            cover=obj.get("cover"),
            upper=BilibiliUpper.from_dict(obj.get("upper")),
            cover_type=obj.get("cover_type"),
            cnt_info=BilibiliFavCntInfo.from_dict(obj.get("cnt_info")),
            type=obj.get("type"),
            intro=obj.get("intro"),
            ctime=obj.get("ctime"),
            mtime=obj.get("mtime"),
            state=obj.get("state"),
            fav_state=obj.get("fav_state"),
            like_state=obj.get("like_state"),
            media_count=obj.get("media_count"),
            is_top=obj.get("is_top")
        )

@dataclass
class BilibiliMediaCntInfo:
    collect: int
    play: int
    danmaku: int
    vt: int
    play_switch: int
    reply: int
    view_text_1: str

    @staticmethod
    def from_dict(obj: Any) -> 'BilibiliMediaCntInfo':
        if obj is None:
            return None
        return BilibiliMediaCntInfo(
            collect=obj.get("collect"),
            play=obj.get("play"),
            danmaku=obj.get("danmaku"),
            vt=obj.get("vt"),
            play_switch=obj.get("play_switch"),
            reply=obj.get("reply"),
            view_text_1=obj.get("view_text_1")
        )

@dataclass
class BilibiliUgc:
    first_cid: int

    @staticmethod
    def from_dict(obj: Any) -> 'BilibiliUgc':
        if obj is None:
            return None
        return BilibiliUgc(first_cid=obj.get("first_cid"))

@dataclass
class BilibiliMedia:
    id: int
    type: int
    title: str
    cover: str
    intro: str
    page: int
    duration: int
    upper: BilibiliUpper
    attr: int
    cnt_info: BilibiliMediaCntInfo
    link: str
    ctime: int
    pubtime: int
    fav_time: int
    bv_id: str
    bvid: str
    ugc: Optional[BilibiliUgc]
    media_list_link: str
    season: Any = None
    ogv: Any = None

    @staticmethod
    def from_dict(obj: Any) -> 'BilibiliMedia':
        if obj is None:
            return None
        return BilibiliMedia(
            id=obj.get("id"),
            type=obj.get("type"),
            title=obj.get("title"),
            cover=obj.get("cover"),
            intro=obj.get("intro"),
            page=obj.get("page"),
            duration=obj.get("duration"),
            upper=BilibiliUpper.from_dict(obj.get("upper")),
            attr=obj.get("attr"),
            cnt_info=BilibiliMediaCntInfo.from_dict(obj.get("cnt_info")),
            link=obj.get("link"),
            ctime=obj.get("ctime"),
            pubtime=obj.get("pubtime"),
            fav_time=obj.get("fav_time"),
            bv_id=obj.get("bv_id"),
            bvid=obj.get("bvid"),
            ugc=BilibiliUgc.from_dict(obj.get("ugc")),
            media_list_link=obj.get("media_list_link"),
            season=obj.get("season"),
            ogv=obj.get("ogv")
        )

@dataclass
class BilibiliFavListData:
    info: BilibiliFavInfo
    medias: List[BilibiliMedia]
    has_more: bool
    ttl: int

    @staticmethod
    def from_dict(obj: Any) -> 'BilibiliFavListData':
        if obj is None:
            return None
        return BilibiliFavListData(
            info=BilibiliFavInfo.from_dict(obj.get("info")),
            medias=[BilibiliMedia.from_dict(m) for m in obj.get("medias", [])],
            has_more=obj.get("has_more"),
            ttl=obj.get("ttl")
        )

@dataclass
class BilibiliFavListResponse:
    code: int
    message: str
    ttl: int
    data: Optional[BilibiliFavListData]

    @staticmethod
    def from_dict(obj: Any) -> 'BilibiliFavListResponse':
        if obj is None:
            return None
        return BilibiliFavListResponse(
            code=obj.get("code"),
            message=obj.get("message"),
            ttl=obj.get("ttl"),
            data=BilibiliFavListData.from_dict(obj.get("data"))
        )
