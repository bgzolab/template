from dataclasses import dataclass
from typing import List, Optional, Any, Dict

@dataclass
class Member:
    id: int
    username: str
    bio: str
    website: str
    github: str
    url: str
    avatar: str
    created: int
    pro: Optional[int] = None

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Member':
        return Member(
            id=data.get("id", 0),
            username=data.get("username", ""),
            bio=data.get("bio", ""),
            website=data.get("website", ""),
            github=data.get("github", ""),
            url=data.get("url", ""),
            avatar=data.get("avatar", ""),
            created=data.get("created", 0),
            pro=data.get("pro")
        )

@dataclass
class Node:
    id: int
    url: str
    name: str
    title: str
    header: str
    footer: str
    avatar: str
    topics: int
    created: int
    last_modified: int

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Node':
        return Node(
            id=data.get("id", 0),
            url=data.get("url", ""),
            name=data.get("name", ""),
            title=data.get("title", ""),
            header=data.get("header", ""),
            footer=data.get("footer", ""),
            avatar=data.get("avatar", ""),
            topics=data.get("topics", 0),
            created=data.get("created", 0),
            last_modified=data.get("last_modified", 0)
        )

@dataclass
class TopicResult:
    id: int
    title: str
    content: str
    syntax: int
    url: str
    replies: int
    last_reply_by: str
    created: int
    last_modified: int
    last_touched: int
    member: Optional[Member]
    node: Optional[Node]
    supplements: List[Any]

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'TopicResult':
        return TopicResult(
            id=data.get("id", 0),
            title=data.get("title", ""),
            content=data.get("content", ""),
            syntax=data.get("syntax", 0),
            url=data.get("url", ""),
            replies=data.get("replies", 0),
            last_reply_by=data.get("last_reply_by", ""),
            created=data.get("created", 0),
            last_modified=data.get("last_modified", 0),
            last_touched=data.get("last_touched", 0),
            member=Member.from_dict(data.get("member")) if data.get("member") else None,
            node=Node.from_dict(data.get("node")) if data.get("node") else None,
            supplements=data.get("supplements", [])
        )

@dataclass
class TopicResponse:
    success: bool
    message: str
    result: Optional[TopicResult]

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'TopicResponse':
        return TopicResponse(
            success=data.get("success", False),
            message=data.get("message", ""),
            result=TopicResult.from_dict(data.get("result")) if data.get("result") else None
        )
