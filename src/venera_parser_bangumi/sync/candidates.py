from __future__ import annotations

import sqlite3
import tempfile
import zipfile
from pathlib import Path

from ..archive import extract_database
from ..helpers import int_or_none, normalize_text_list, quote_identifier, string_or_none
from ..models import SyncCandidate, SyncSearchRequest, SyncTarget


def load_sync_candidates(
    archive_path: Path, sync_targets: list[SyncTarget]
) -> list[SyncCandidate]:
    with zipfile.ZipFile(archive_path) as archive, tempfile.TemporaryDirectory(
        prefix="venera_sync_"
    ) as temp_dir:
        temp_path = Path(temp_dir)
        db_path = extract_database(archive, temp_path, "local_favorite.db")
        if db_path is None:
            raise ValueError("Archive does not contain local_favorite.db")

        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row
        try:
            existing_tables = {
                row["name"]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
                ).fetchall()
            }
            candidates: list[SyncCandidate] = []
            for target in sync_targets:
                if target.table not in existing_tables:
                    raise ValueError(
                        f"Requested local_favorite table does not exist: {target.table}"
                    )
                rows = connection.execute(
                    f"SELECT * FROM {quote_identifier(target.table)}"
                ).fetchall()
                for row in rows:
                    row_dict = dict(row)
                    candidates.append(
                        SyncCandidate(
                            source_table=target.table,
                            target_state=target.state,
                            record_id=string_or_none(row_dict.get("id")),
                            name=string_or_none(row_dict.get("name")),
                            author=string_or_none(row_dict.get("author")),
                            subject_type=int_or_none(row_dict.get("type")),
                            tags=normalize_text_list(row_dict.get("tags")),
                            translated_tags=normalize_text_list(
                                row_dict.get("translated_tags")
                            ),
                        )
                    )
            return candidates
        finally:
            connection.close()


def build_search_request(candidate: SyncCandidate) -> SyncSearchRequest:
    keyword = candidate.name or candidate.record_id or ""
    author_hints = [candidate.author] if candidate.author else []
    tag_hints = [*candidate.tags, *candidate.translated_tags]
    return SyncSearchRequest(
        candidate=candidate,
        keyword=keyword,
        author_hints=author_hints,
        tag_hints=tag_hints,
    )