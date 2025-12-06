from dataclasses import dataclass
from typing import List, Optional, Any

@dataclass
class Origin:
    feedId: Optional[str] = None

    @staticmethod
    def from_dict(data: dict) -> 'Origin':
        return Origin(feedId=data.get("feedId"))

@dataclass
class Entry:
    id: str
    isSaved: bool
    sourceEntryId: str
    origin: Optional[Origin]
    title: str
    summary: str
    url: str
    publishedAt: int
    crawledAt: int
    timestamp: str
    attachments: List[Any]
    tagIds: List[str]

    @staticmethod
    def from_dict(data: dict) -> 'Entry':
        return Entry(
            id=data.get("id"),
            isSaved=data.get("isSaved"),
            sourceEntryId=data.get("sourceEntryId"),
            origin=Origin.from_dict(data.get("origin")) if data.get("origin") else None,
            title=data.get("title"),
            summary=data.get("summary"),
            url=data.get("url"),
            publishedAt=data.get("publishedAt"),
            crawledAt=data.get("crawledAt"),
            timestamp=data.get("timestamp"),
            attachments=data.get("attachments", []),
            tagIds=data.get("tagIds", [])
        )

@dataclass
class StreamResult:
    id: str
    entries: List[Entry]
    hasMore: bool

    @staticmethod
    def from_dict(data: dict) -> 'StreamResult':
        return StreamResult(
            id=data.get("id"),
            entries=[Entry.from_dict(e) for e in data.get("entries", [])],
            hasMore=data.get("hasMore")
        )

@dataclass
class QiReaderResponse:
    result: StreamResult

    @staticmethod
    def from_dict(data: dict) -> 'QiReaderResponse':
        return QiReaderResponse(
            result=StreamResult.from_dict(data.get("result", {}))
        )
