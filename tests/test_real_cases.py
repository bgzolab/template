from __future__ import annotations

import json
from pathlib import Path

import pytest

from venera_parser_bangumi.models import BangumiSubject, SyncTarget
from venera_parser_bangumi.sync import service
from venera_parser_bangumi.sync.bangumi import parse_subject_payload
from venera_parser_bangumi.sync.candidates import load_sync_candidates
from venera_parser_bangumi.sync.service import run_sync


class RecordedBangumiClient:
    def __init__(self, case_data: dict):
        self.case_data = case_data
        self.upserts: list[tuple[int, str]] = []

    def search_subjects(self, _search_request, *, limit: int = 100) -> list[BangumiSubject]:
        assert limit == 100
        return [
            subject
            for item in self.case_data["search_results"]
            if (subject := parse_subject_payload(item)) is not None
        ]

    def get_subject(self, subject_id: int) -> BangumiSubject:
        payload = self.case_data["subject_details"][str(subject_id)]
        subject = parse_subject_payload(payload)
        assert subject is not None
        return subject

    def get_my_subject_collection(self, _subject_id: int):
        return None

    def upsert_subject_collection(self, subject_id: int, state: str) -> None:
        self.upserts.append((subject_id, state))


@pytest.fixture
def real_sync_cases(project_root: Path) -> list[dict]:
    fixture_path = project_root / "tests" / "fixtures" / "real_sync_cases.json"
    return json.loads(fixture_path.read_text(encoding="utf-8"))


@pytest.fixture
def real_doing_candidates(sample_archive: Path):
    candidates = load_sync_candidates(sample_archive, [SyncTarget("Doing", "doing")])
    return {candidate.name: candidate for candidate in candidates if candidate.name}


@pytest.mark.parametrize(
    ("title", "expected_subject_id"),
    [
        ("婚姻毒素", 378773),
        ("我在星際國家當惡徳領主", 379172),
        ("忘卻Battery", 259816),
        ("我的首推是惡役大小姐", 306888),
        ("博人傳BORUTO", 173370),
    ],
)
def test_run_sync_resolves_real_archive_cases(
    sample_archive: Path,
    monkeypatch: pytest.MonkeyPatch,
    real_sync_cases: list[dict],
    real_doing_candidates: dict[str, object],
    title: str,
    expected_subject_id: int,
) -> None:
    case_data = next(case for case in real_sync_cases if case["title"] == title)
    candidate = real_doing_candidates[title]
    client = RecordedBangumiClient(case_data)

    monkeypatch.setattr(service, "load_sync_candidates", lambda *_args, **_kwargs: [candidate])

    result = run_sync(
        sample_archive,
        [SyncTarget(case_data["source_table"], case_data["target_state"])],
        dry_run=True,
        client=client,
    )

    assert result.counts["would_update"] == 1
    assert result.item_results[0].subject is not None
    assert result.item_results[0].subject.subject_id == expected_subject_id
    assert client.upserts == []