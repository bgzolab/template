from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class ArchiveMember:
    name: str
    size: int
    compressed_size: int
    modified_at: str


@dataclass(frozen=True)
class SyncTarget:
    table: str
    state: str


@dataclass(frozen=True)
class SyncCandidate:
    source_table: str
    target_state: str
    record_id: str | None
    name: str | None
    author: str | None
    subject_type: int | None
    tags: list[str]
    translated_tags: list[str]


@dataclass(frozen=True)
class SyncSearchRequest:
    candidate: SyncCandidate
    keyword: str
    author_hints: list[str]
    tag_hints: list[str]


@dataclass(frozen=True)
class BangumiSubject:
    subject_id: int
    name: str
    name_cn: str | None = None
    platform: str | None = None
    authors: list[str] = field(default_factory=list)
    aliases: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class MatchResult:
    status: str
    search_request: SyncSearchRequest
    subject: BangumiSubject | None
    candidate_subjects: list[BangumiSubject]


@dataclass(frozen=True)
class SyncItemResult:
    candidate: SyncCandidate
    status: str
    reason: str
    subject: BangumiSubject | None = None
    current_type: int | None = None


@dataclass
class SyncRunResult:
    archive_path: Path
    dry_run: bool
    item_results: list[SyncItemResult] = field(default_factory=list)

    @property
    def counts(self) -> dict[str, int]:
        counts = {
            "updated": 0,
            "would_update": 0,
            "skipped": 0,
            "failed": 0,
        }
        for item in self.item_results:
            if item.status in counts:
                counts[item.status] += 1
        return counts