from __future__ import annotations

from ..helpers import normalize_title
from ..models import BangumiSubject, MatchResult, SyncSearchRequest


def match_search_result(
    search_request: SyncSearchRequest, subjects: list[BangumiSubject]
) -> MatchResult:
    if not subjects:
        return MatchResult(
            status="skipped_no_result",
            search_request=search_request,
            subject=None,
            candidate_subjects=[],
        )

    keyword = normalize_title(search_request.keyword)
    exact_matches = [
        subject
        for subject in subjects
        if keyword
        and keyword in {normalize_title(subject.name), normalize_title(subject.name_cn)}
    ]
    if len(exact_matches) == 1:
        return MatchResult(
            status="matched",
            search_request=search_request,
            subject=exact_matches[0],
            candidate_subjects=exact_matches,
        )
    if len(exact_matches) > 1:
        return MatchResult(
            status="skipped_ambiguous",
            search_request=search_request,
            subject=None,
            candidate_subjects=exact_matches,
        )

    near_matches = [
        subject
        for subject in subjects
        if keyword
        and (
            keyword in normalize_title(subject.name)
            or keyword in normalize_title(subject.name_cn)
            or normalize_title(subject.name) in keyword
            or normalize_title(subject.name_cn) in keyword
        )
    ]
    return MatchResult(
        status="skipped_low_confidence" if near_matches else "skipped_no_result",
        search_request=search_request,
        subject=None,
        candidate_subjects=near_matches,
    )