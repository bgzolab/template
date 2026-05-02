from __future__ import annotations

from venera_parser_bangumi.models import BangumiSubject, SyncCandidate, SyncSearchRequest, SyncTarget
from venera_parser_bangumi.sync import service
from venera_parser_bangumi.sync.service import extract_collection_type, run_sync


class FakeBangumiClient:
    def __init__(self, *, subjects=None, collection=None, fail_on_search=None):
        self.subjects = subjects or []
        self.collection = collection
        self.fail_on_search = fail_on_search
        self.upserts: list[tuple[int, str]] = []

    def search_subjects(self, search_request: SyncSearchRequest, *, limit: int = 10):
        if self.fail_on_search is not None:
            raise self.fail_on_search
        return self.subjects

    def get_my_subject_collection(self, subject_id: int):
        return self.collection

    def upsert_subject_collection(self, subject_id: int, state: str) -> None:
        self.upserts.append((subject_id, state))


def make_candidates() -> list[SyncCandidate]:
    return [
        SyncCandidate(
            source_table="DONE",
            target_state="done",
            record_id="1",
            name="海贼王",
            author="尾田荣一郎",
            subject_type=0,
            tags=["热血"],
            translated_tags=["冒险"],
        )
    ]


def test_run_sync_marks_dry_run_updates_without_writing(sample_archive, monkeypatch) -> None:
    monkeypatch.setattr(service, "load_sync_candidates", lambda *_args, **_kwargs: make_candidates())
    client = FakeBangumiClient(
        subjects=[BangumiSubject(123, "ONE PIECE", "海贼王")],
        collection=None,
    )

    result = run_sync(
        sample_archive,
        [SyncTarget("DONE", "done")],
        dry_run=True,
        client=client,
    )

    assert result.counts["would_update"] == 1
    assert client.upserts == []


def test_run_sync_skips_already_synced_items(sample_archive, monkeypatch) -> None:
    monkeypatch.setattr(service, "load_sync_candidates", lambda *_args, **_kwargs: make_candidates())
    client = FakeBangumiClient(
        subjects=[BangumiSubject(123, "ONE PIECE", "海贼王")],
        collection={"type": 2},
    )

    result = run_sync(
        sample_archive,
        [SyncTarget("DONE", "done")],
        dry_run=False,
        client=client,
    )

    assert result.counts["skipped"] == 1
    assert client.upserts == []


def test_run_sync_updates_when_status_differs(sample_archive, monkeypatch) -> None:
    monkeypatch.setattr(service, "load_sync_candidates", lambda *_args, **_kwargs: make_candidates())
    client = FakeBangumiClient(
        subjects=[BangumiSubject(123, "ONE PIECE", "海贼王")],
        collection={"type": 1},
    )

    result = run_sync(
        sample_archive,
        [SyncTarget("DONE", "done")],
        dry_run=False,
        client=client,
    )

    assert result.counts["updated"] == 1
    assert client.upserts == [(123, "done")]


def test_extract_collection_type_handles_missing_data() -> None:
    assert extract_collection_type(None) is None
    assert extract_collection_type({}) is None
    assert extract_collection_type({"type": 3}) == 3