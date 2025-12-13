from dataclasses import dataclass
from typing import List, Optional, Any, Dict

@dataclass
class Paging:
    is_end: bool
    is_start: bool
    next: str
    previous: str
    totals: int

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Paging':
        return Paging(
            is_end=data.get("is_end", False),
            is_start=data.get("is_start", False),
            next=data.get("next", ""),
            previous=data.get("previous", ""),
            totals=data.get("totals", 0)
        )

@dataclass
class Question:
    id: str
    title: str
    url: str
    type: str
    created: int
    updated_time: int

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Question':
        return Question(
            id=str(data.get("id", "")),
            title=data.get("title", ""),
            url=data.get("url", ""),
            type=data.get("type", ""),
            created=data.get("created", 0),
            updated_time=data.get("updated_time", 0)
        )

@dataclass
class Author:
    id: str
    name: str
    url_token: str
    headline: str
    url: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Author':
        return Author(
            id=data.get("id", ""),
            name=data.get("name", ""),
            url_token=data.get("url_token", ""),
            headline=data.get("headline", ""),
            url=data.get("url", "")
        )

@dataclass
class Content:
    id: str
    type: str
    url: str
    content: str
    voteup_count: int
    comment_count: int
    created_time: int
    updated_time: int
    author: Optional[Author] = None
    question: Optional[Question] = None
    title: Optional[str] = None

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Content':
        return Content(
            id=str(data.get("id", "")),
            type=data.get("type", ""),
            url=data.get("url", ""),
            content=data.get("content", ""),
            voteup_count=data.get("voteup_count", 0),
            comment_count=data.get("comment_count", 0),
            created_time=data.get("created_time", 0),
            updated_time=data.get("updated_time", 0),
            author=Author.from_dict(data.get("author")) if data.get("author") else None,
            question=Question.from_dict(data.get("question")) if data.get("question") else None,
            title=data.get("title")
        )

@dataclass
class CollectionItem:
    content: Content
    created: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'CollectionItem':
        return CollectionItem(
            content=Content.from_dict(data.get("content", {})),
            created=data.get("created", "")
        )

@dataclass
class CollectionResponse:
    paging: Paging
    data: List[CollectionItem]

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'CollectionResponse':
        return CollectionResponse(
            paging=Paging.from_dict(data.get("paging", {})),
            data=[CollectionItem.from_dict(item) for item in data.get("data", [])]
        )

