from __future__ import annotations

from ..helpers import build_search_keywords, normalize_match_title
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

    keyword_variants = {
        normalize_match_title(keyword)
        for keyword in build_search_keywords(search_request.keyword)
        if normalize_match_title(keyword)
    }
    exact_matches = [
        subject
        for subject in subjects
        if is_exact_match(keyword_variants, subject)
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
        if is_near_match(keyword_variants, subject)
    ]
    return MatchResult(
        status="skipped_low_confidence" if near_matches else "skipped_no_result",
        search_request=search_request,
        subject=None,
        candidate_subjects=near_matches,
    )


def is_exact_match(keyword_variants: set[str], subject: BangumiSubject) -> bool:
    subject_titles = subject_match_titles(subject)
    return bool(keyword_variants and subject_titles and keyword_variants & subject_titles)


def is_near_match(keyword_variants: set[str], subject: BangumiSubject) -> bool:
    if not keyword_variants:
        return False
    subject_titles = subject_match_titles(subject)
    for keyword in keyword_variants:
        for subject_title in subject_titles:
            if keyword in subject_title or subject_title in keyword:
                return True
    return False


def subject_match_titles(subject: BangumiSubject) -> set[str]:
    return {
        normalized
        for normalized in (
            normalize_match_title(subject.name),
            normalize_match_title(subject.name_cn),
        )
        if normalized
    }