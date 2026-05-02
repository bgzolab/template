from __future__ import annotations

from venera_parser_bangumi.models import BangumiSubject, SyncCandidate, SyncSearchRequest, SyncTarget
from venera_parser_bangumi.sync import service
from venera_parser_bangumi.sync.service import classify_subject_media_type, extract_collection_type, run_sync


class FakeBangumiClient:
    def __init__(self, *, subjects=None, subject_detail=None, collection=None, fail_on_search=None):
        self.subjects = subjects or []
        self.subject_detail = subject_detail
        self.collection = collection
        self.fail_on_search = fail_on_search
        self.upserts: list[tuple[int, str]] = []
        self.search_limit_calls: list[int] = []

    def search_subjects(self, search_request: SyncSearchRequest, *, limit: int = 100):
        self.search_limit_calls.append(limit)
        if self.fail_on_search is not None:
            raise self.fail_on_search
        return self.subjects

    def get_my_subject_collection(self, subject_id: int):
        return self.collection

    def get_subject(self, subject_id: int):
        if isinstance(self.subject_detail, dict):
            return self.subject_detail[subject_id]
        return self.subject_detail or self.subjects[0]

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


def make_novel_candidates() -> list[SyncCandidate]:
    return [
        SyncCandidate(
            source_table="DONE",
            target_state="done",
            record_id="2",
            name="再见龙生，你好人生",
            author="永島ひろあき",
            subject_type=0,
            tags=["轻小说"],
            translated_tags=["转生"],
        )
    ]


def test_run_sync_marks_dry_run_updates_without_writing(sample_archive, monkeypatch) -> None:
    monkeypatch.setattr(service, "load_sync_candidates", lambda *_args, **_kwargs: make_candidates())
    client = FakeBangumiClient(
        subjects=[BangumiSubject(123, "ONE PIECE", "海贼王")],
        subject_detail=BangumiSubject(123, "ONE PIECE", "海贼王", "漫画"),
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
    assert client.search_limit_calls == [100]


def test_run_sync_emits_progress_logs_for_low_confidence_matches(sample_archive, monkeypatch) -> None:
    monkeypatch.setattr(service, "load_sync_candidates", lambda *_args, **_kwargs: make_candidates())
    client = FakeBangumiClient(subjects=[BangumiSubject(123, "海贼王 特别篇", None)])
    logs: list[str] = []

    result = run_sync(
        sample_archive,
        [SyncTarget("DONE", "done")],
        dry_run=True,
        client=client,
        log=logs.append,
    )

    assert result.counts["skipped"] == 1
    assert any("[start] loaded 1 candidate(s)" in message for message in logs)
    assert any("Bangumi returned 1 candidate(s)" in message for message in logs)
    assert any("low confidence candidates: 123:海贼王 特别篇" in message for message in logs)
    assert any(message.startswith("[done] ") for message in logs)


def test_run_sync_skips_already_synced_items(sample_archive, monkeypatch) -> None:
    monkeypatch.setattr(service, "load_sync_candidates", lambda *_args, **_kwargs: make_candidates())
    client = FakeBangumiClient(
        subjects=[BangumiSubject(123, "ONE PIECE", "海贼王")],
        subject_detail=BangumiSubject(123, "ONE PIECE", "海贼王", "漫画"),
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
        subject_detail=BangumiSubject(123, "ONE PIECE", "海贼王", "漫画"),
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


def test_run_sync_skips_novel_subjects(sample_archive, monkeypatch) -> None:
    monkeypatch.setattr(service, "load_sync_candidates", lambda *_args, **_kwargs: make_novel_candidates())
    client = FakeBangumiClient(
        subjects=[BangumiSubject(171069, "さようなら竜生、こんにちは人生", "再见龙生，你好人生")],
        subject_detail=BangumiSubject(171069, "さようなら竜生、こんにちは人生", "再见龙生，你好人生", "小说"),
        collection=None,
    )
    logs: list[str] = []

    result = run_sync(
        sample_archive,
        [SyncTarget("DONE", "done")],
        dry_run=False,
        client=client,
        log=logs.append,
    )

    assert result.counts["skipped"] == 1
    assert client.upserts == []
    assert result.item_results[0].reason == "non_manga_subject"
    assert any("platform=小说 classified as novel" in message for message in logs)


def test_classify_subject_media_type_prefers_platform_signal() -> None:
    assert classify_subject_media_type(BangumiSubject(1, "foo", platform="漫画")) == "manga"
    assert classify_subject_media_type(BangumiSubject(2, "bar", platform="小说")) == "novel"
    assert classify_subject_media_type(BangumiSubject(3, "baz", platform=None)) == "unknown"


def test_run_sync_resolves_ambiguous_exact_matches_to_single_manga(sample_archive, monkeypatch) -> None:
    monkeypatch.setattr(service, "load_sync_candidates", lambda *_args, **_kwargs: make_novel_candidates())
    client = FakeBangumiClient(
        subjects=[
            BangumiSubject(171069, "さようなら竜生、こんにちは人生", "再见龙生，你好人生"),
            BangumiSubject(235408, "さようなら竜生、こんにちは人生", "再见龙生，你好人生"),
        ],
        subject_detail={
            171069: BangumiSubject(171069, "さようなら竜生、こんにちは人生", "再见龙生，你好人生", "小说"),
            235408: BangumiSubject(235408, "さようなら竜生、こんにちは人生", "再见龙生，你好人生", "漫画"),
        },
        collection=None,
    )

    result = run_sync(
        sample_archive,
        [SyncTarget("DONE", "done")],
        dry_run=True,
        client=client,
    )

    assert result.counts["would_update"] == 1
    assert result.item_results[0].subject is not None
    assert result.item_results[0].subject.subject_id == 235408