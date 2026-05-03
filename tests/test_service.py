from __future__ import annotations

import pytest

from venera_parser_bangumi.models import BangumiSubject, SyncCandidate, SyncSearchRequest, SyncTarget
from venera_parser_bangumi.sync import service
from venera_parser_bangumi.sync.service import (
    author_matches,
    classify_subject_media_type,
    extract_collection_type,
    resolve_subject_for_sync,
    run_sync,
    score_subject_title,
)


class FakeBangumiClient:
    def __init__(self, *, subjects=None, subject_detail=None, collection=None, fail_on_search=None):
        self.subjects = subjects or []
        self.subject_detail = subject_detail
        self.collection = collection
        self.fail_on_search = fail_on_search
        self.upserts: list[tuple[int, str]] = []
        self.search_limit_calls: list[int] = []
        self.collection_calls: list[int] = []

    def search_subjects(self, search_request: SyncSearchRequest, *, limit: int = 100):
        self.search_limit_calls.append(limit)
        if self.fail_on_search is not None:
            raise self.fail_on_search
        return self.subjects

    def get_my_subject_collection(self, subject_id: int):
        self.collection_calls.append(subject_id)
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


def test_run_sync_reuses_cached_results_for_normalized_duplicate_titles(sample_archive, monkeypatch) -> None:
    duplicate_candidates = [
        SyncCandidate("Doing", "doing", "1", "黃泉的使者", None, 0, [], []),
        SyncCandidate("Doing", "doing", "2", "黄泉的使者", None, 0, [], []),
    ]
    monkeypatch.setattr(service, "load_sync_candidates", lambda *_args, **_kwargs: duplicate_candidates)
    client = FakeBangumiClient(
        subjects=[BangumiSubject(356902, "黄泉のツガイ", "黄泉的使者")],
        subject_detail=BangumiSubject(356902, "黄泉のツガイ", "黄泉的使者", "漫画"),
        collection={"type": 3},
    )

    result = run_sync(
        sample_archive,
        [SyncTarget("Doing", "doing")],
        dry_run=True,
        client=client,
    )

    assert result.counts["skipped"] == 2
    assert client.search_limit_calls == [100]
    assert client.collection_calls == [356902]


def test_run_sync_checks_collection_before_further_resolution_for_direct_match(sample_archive, monkeypatch) -> None:
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
    assert result.item_results[0].reason == "already_synced"
    assert client.search_limit_calls == [100]
    assert client.collection_calls == [123]


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


def test_score_subject_title_prefers_close_translation_over_unrelated_titles() -> None:
    request = SyncSearchRequest(
        candidate=make_candidates()[0],
        keyword="婚姻毒素",
        author_hints=[],
        tag_hints=[],
    )
    close_subject = BangumiSubject(378773, "マリッジトキシン", "婚姻剧毒", "漫画")
    unrelated_subject = BangumiSubject(247532, "婚姻届に判を捺しただけですが", "只是在结婚申请书上盖个章而已", "漫画")

    assert score_subject_title(request, close_subject) > score_subject_title(request, unrelated_subject)


def test_author_matches_accepts_close_japanese_names() -> None:
    assert author_matches(["みかわ繪子"], ["みかわ絵子"])


def test_resolve_subject_for_sync_uses_title_scoring_for_translation_match() -> None:
    request = SyncSearchRequest(
        candidate=make_candidates()[0],
        keyword="婚姻毒素",
        author_hints=["依田瑞稀"],
        tag_hints=[],
    )
    subjects = [
        BangumiSubject(378773, "マリッジトキシン", "婚姻剧毒", "漫画"),
        BangumiSubject(247532, "婚姻届に判を捺しただけですが", "只是在结婚申请书上盖个章而已", "漫画"),
    ]
    match = type("Match", (), {"status": "skipped_no_result", "subject": None, "candidate_subjects": []})()
    client = FakeBangumiClient(subjects=subjects)

    resolved = resolve_subject_for_sync(client, request, subjects, match)

    assert resolved is not None
    assert resolved.subject_id == 378773


def test_resolve_subject_for_sync_uses_author_detail_when_title_diverges() -> None:
    request = SyncSearchRequest(
        candidate=make_candidates()[0],
        keyword="忘卻Battery",
        author_hints=["みかわ繪子"],
        tag_hints=[],
    )
    subjects = [
        BangumiSubject(326770, "忘却的爱丽丝", platform="小说"),
        BangumiSubject(259816, "忘却バッテリー", "失忆投捕", "漫画"),
        BangumiSubject(271409, "プロジェクト東京ドールズ　忘却のイミテーション・ドール", "东京偶像计划 忘却少女", "漫画"),
    ]
    details = {
        326770: BangumiSubject(326770, "忘却的爱丽丝", platform="小说", authors=["日日日"]),
        259816: BangumiSubject(259816, "忘却バッテリー", "失忆投捕", "漫画", authors=["みかわ絵子"]),
        271409: BangumiSubject(271409, "プロジェクト東京ドールズ　忘却のイミテーション・ドール", "东京偶像计划 忘却少女", "漫画", authors=["Somebody Else"]),
    }
    match = type("Match", (), {"status": "skipped_no_result", "subject": None, "candidate_subjects": []})()
    client = FakeBangumiClient(subjects=subjects, subject_detail=details)

    resolved = resolve_subject_for_sync(client, request, subjects, match)

    assert resolved is not None
    assert resolved.subject_id == 259816


def test_resolve_subject_for_sync_considers_full_search_results_after_low_confidence_match() -> None:
    request = SyncSearchRequest(
        candidate=make_candidates()[0],
        keyword="我們不可能成為戀人！絕對不行。 (※似乎可行？)",
        author_hints=["みかみてれん"],
        tag_hints=[],
    )
    subjects = [
        BangumiSubject(306812, "わたしたちは恋人になれない。", "我们不可能成为恋人！绝对不行。 (※似乎可行？)"),
        BangumiSubject(300270, "わたしたちは恋人になれない。", "我们不可能成为恋人！绝对不行。 (※似乎可行？)"),
        BangumiSubject(249879, "あんたなんかと付き合えるわけないじゃん！ムリ！ムリ！大好き！"),
    ]
    details = {
        306812: BangumiSubject(306812, "わたしたちは恋人になれない。", "我们不可能成为恋人！绝对不行。 (※似乎可行？)", "漫画", authors=["むっしゅ", "みかみてれん"]),
        300270: BangumiSubject(300270, "わたしたちは恋人になれない。", "我们不可能成为恋人！绝对不行。 (※似乎可行？)", "小说", authors=["みかみてれん"]),
        249879: BangumiSubject(249879, "あんたなんかと付き合えるわけないじゃん！ムリ！ムリ！大好き！", "", "漫画", authors=["内堀優一"]),
    }
    match = type("Match", (), {"status": "skipped_low_confidence", "subject": None, "candidate_subjects": [subjects[2]]})()
    client = FakeBangumiClient(subjects=subjects, subject_detail=details)

    resolved = resolve_subject_for_sync(client, request, subjects, match)

    assert resolved is not None
    assert resolved.subject_id == 306812


def test_resolve_subject_for_sync_prefers_manga_when_exact_novel_match_exists() -> None:
    request = SyncSearchRequest(
        candidate=make_candidates()[0],
        keyword="野生的最終BOSS出現了",
        author_hints=["葉月翼"],
        tag_hints=[],
    )
    novel = BangumiSubject(224177, "野生のラスボスが現れた!", "野生的最终BOSS出现了！")
    manga = BangumiSubject(220773, "野生のラスボスが現れた! 黒翼の覇王", "野生的最终BOSS出现了！ 黑翼的霸王")
    details = {
        224177: BangumiSubject(224177, "野生のラスボスが現れた!", "野生的最终BOSS出现了！", "小说", authors=["炎頭"]),
        220773: BangumiSubject(220773, "野生のラスボスが現れた! 黒翼の覇王", "野生的最终BOSS出现了！ 黑翼的霸王", "漫画", authors=["葉月翼", "炎頭", "YahaKo"]),
    }
    match = type("Match", (), {"status": "matched", "subject": novel, "candidate_subjects": [novel]})()
    client = FakeBangumiClient(subjects=[novel, manga], subject_detail=details)

    resolved = resolve_subject_for_sync(client, request, [novel, manga], match)

    assert resolved is not None
    assert resolved.subject_id == 220773


def test_resolve_subject_for_sync_breaks_author_matched_manga_ties_by_title_score() -> None:
    request = SyncSearchRequest(
        candidate=make_candidates()[0],
        keyword="博人傳BORUTO",
        author_hints=["岸本齊史"],
        tag_hints=[],
    )
    subjects = [
        BangumiSubject(173370, "BORUTO-ボルト- -NARUTO NEXT GENERATIONS-", "博人传-火影次世代-"),
        BangumiSubject(181994, "BORUTO ─ NARUTO THE MOVIE─", "博人传 -火影忍者 剧场版小说-"),
        BangumiSubject(213055, "BORUTO-ボルト- -NARUTO NEXT GENERATIONS- NOVEL", "博人传-火影次世代- 小说"),
        BangumiSubject(476934, "BORUTO-ボルト- -TWO BLUE VORTEX-", "博人传-双蓝漩涡-"),
    ]
    details = {
        173370: BangumiSubject(
            173370,
            "BORUTO-ボルト- -NARUTO NEXT GENERATIONS-",
            "博人传-火影次世代-",
            "漫画",
            authors=["岸本斉史（原作·监修）", "池本幹雄"],
            aliases=["博人传 火影忍者新时代"],
        ),
        181994: BangumiSubject(
            181994,
            "BORUTO ─ NARUTO THE MOVIE─",
            "博人传 -火影忍者 剧场版小说-",
            "小说",
            authors=["小太刀右京"],
        ),
        213055: BangumiSubject(
            213055,
            "BORUTO-ボルト- -NARUTO NEXT GENERATIONS- NOVEL",
            "博人传-火影次世代- 小说",
            "小说",
            authors=["岸本斉史", "重信康", "三輪清宗"],
        ),
        476934: BangumiSubject(
            476934,
            "BORUTO-ボルト- -TWO BLUE VORTEX-",
            "博人传-双蓝漩涡-",
            "漫画",
            authors=["池本幹雄", "岸本斉史(原作．监修)"],
        ),
    }
    match = type("Match", (), {"status": "skipped_no_result", "subject": None, "candidate_subjects": []})()
    client = FakeBangumiClient(subjects=subjects, subject_detail=details)

    resolved = resolve_subject_for_sync(client, request, subjects, match)

    assert resolved is not None
    assert resolved.subject_id == 173370