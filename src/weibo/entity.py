from dataclasses import dataclass
from typing import List, Optional, Any, Dict

@dataclass
class User:
    id: int
    idstr: str
    screen_name: str
    profile_image_url: str
    profile_url: str
    verified: bool
    avatar_large: str
    avatar_hd: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'User':
        return User(
            id=data.get("id", 0),
            idstr=data.get("idstr", ""),
            screen_name=data.get("screen_name", ""),
            profile_image_url=data.get("profile_image_url", ""),
            profile_url=data.get("profile_url", ""),
            verified=data.get("verified", False),
            avatar_large=data.get("avatar_large", ""),
            avatar_hd=data.get("avatar_hd", "")
        )

@dataclass
class PicInfo:
    thumbnail: Dict[str, Any]
    large: Dict[str, Any]
    original: Dict[str, Any]
    largest: Dict[str, Any]
    object_id: str
    pic_id: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'PicInfo':
        return PicInfo(
            thumbnail=data.get("thumbnail", {}),
            large=data.get("large", {}),
            original=data.get("original", {}),
            largest=data.get("largest", {}),
            object_id=data.get("object_id", ""),
            pic_id=data.get("pic_id", "")
        )

@dataclass
class WeiboItem:
    created_at: str
    id: int
    idstr: str
    mid: str
    mblogid: str
    user: Optional[User]
    text: str
    text_raw: str
    source: str
    favorited: bool
    pic_num: int
    pic_ids: List[str]
    pic_infos: Dict[str, PicInfo]
    reposts_count: int
    comments_count: int
    attitudes_count: int
    isLongText: bool
    region_name: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'WeiboItem':
        pic_infos_data = data.get("pic_infos", {})
        pic_infos = {k: PicInfo.from_dict(v) for k, v in pic_infos_data.items()} if pic_infos_data else {}
        
        return WeiboItem(
            created_at=data.get("created_at", ""),
            id=data.get("id", 0),
            idstr=data.get("idstr", ""),
            mid=data.get("mid", ""),
            mblogid=data.get("mblogid", ""),
            user=User.from_dict(data.get("user")) if data.get("user") else None,
            text=data.get("text", ""),
            text_raw=data.get("text_raw", ""),
            source=data.get("source", ""),
            favorited=data.get("favorited", False),
            pic_num=data.get("pic_num", None),
            pic_ids=data.get("pic_ids", []),
            pic_infos=pic_infos,
            reposts_count=data.get("reposts_count", 0),
            comments_count=data.get("comments_count", 0),
            attitudes_count=data.get("attitudes_count", 0),
            isLongText=data.get("isLongText", False),
            region_name=data.get("region_name", "")
        )

@dataclass
class WeiboData:
    list: List[WeiboItem]

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'WeiboData':
        return WeiboData(
            list=[WeiboItem.from_dict(item) for item in data.get("list", [])]
        )

@dataclass
class WeiboResponse:
    ok: int
    data: Optional[WeiboData]

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'WeiboResponse':
        return WeiboResponse(
            ok=data.get("ok", 0),
            data=WeiboData.from_dict(data.get("data")) if data.get("data") else None
        )
