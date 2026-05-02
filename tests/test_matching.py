from __future__ import annotations

from venera_parser_bangumi.models import BangumiSubject, SyncCandidate
from venera_parser_bangumi.sync.candidates import build_search_request
from venera_parser_bangumi.sync.matching import match_search_result


def make_request():
    candidate = SyncCandidate(
        source_table="Doing",
        target_state="doing",
        record_id="1",
        name="海贼王",
        author="尾田荣一郎",
        subject_type=0,
        tags=["热血"],
        translated_tags=["冒险"],
    )
    return build_search_request(candidate)


def test_match_search_result_returns_matched_for_single_exact_hit() -> None:
    request = make_request()
    result = match_search_result(request, [BangumiSubject(1, "ONE PIECE", "海贼王")])

    assert result.status == "matched"
    assert result.subject is not None
    assert result.subject.subject_id == 1


def test_match_search_result_returns_no_result_for_empty_hits() -> None:
    request = make_request()
    result = match_search_result(request, [])

    assert result.status == "skipped_no_result"


def test_match_search_result_returns_ambiguous_for_multiple_exact_hits() -> None:
    request = make_request()
    result = match_search_result(
        request,
        [BangumiSubject(1, "海贼王"), BangumiSubject(2, "ONE PIECE", "海贼王")],
    )

    assert result.status == "skipped_ambiguous"
    assert len(result.candidate_subjects) == 2