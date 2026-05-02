from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path
from typing import Callable

from ..constants import STATE_TO_BANGUMI_TYPE
from ..helpers import cjk_substring_overlap, normalize_match_title, similarity_ratio
from ..models import BangumiSubject, SyncItemResult, SyncRunResult, SyncSearchRequest, SyncTarget
from .bangumi import BangumiClient, BangumiClientError
from .candidates import build_search_request, load_sync_candidates
from .matching import match_search_result


def run_sync(
    archive_path: Path,
    sync_targets: list[SyncTarget],
    *,
    dry_run: bool,
    client: BangumiClient,
    log: Callable[[str], None] | None = None,
) -> SyncRunResult:
    candidates = load_sync_candidates(archive_path, sync_targets)
    run_result = SyncRunResult(archive_path=archive_path, dry_run=dry_run)
    cached_results: dict[tuple[str, tuple[str, ...], str], SyncItemResult] = {}
    emit = log or (lambda _message: None)

    emit(f"[start] archive={archive_path} dry_run={dry_run}")
    emit(f"[start] loaded {len(candidates)} candidate(s)")

    for index, candidate in enumerate(candidates, start=1):
        search_request = build_search_request(candidate)
        candidate_label = format_candidate_label(candidate)
        cache_key = build_candidate_cache_key(search_request)
        cached_result = cached_results.get(cache_key)
        if cached_result is not None:
            emit(
                f"[item {index}/{len(candidates)}] reuse cached result for {candidate_label}: "
                f"{cached_result.reason}"
            )
            run_result.item_results.append(replace(cached_result, candidate=candidate))
            continue
        emit(
            f"[item {index}/{len(candidates)}] searching {candidate_label} "
            f"with keyword={search_request.keyword!r}"
        )
        try:
            subjects = client.search_subjects(search_request)
            emit(
                f"[item {index}/{len(candidates)}] Bangumi returned {len(subjects)} candidate(s)"
            )
            match = match_search_result(search_request, subjects)
            subject = resolve_subject_for_sync(client, search_request, subjects, match)
            if subject is None and match.status != "matched":
                emit(
                    f"[item {index}/{len(candidates)}] skip {candidate_label}: "
                    f"{describe_match_status(match.status, match.candidate_subjects)}"
                )
                run_result.item_results.append(
                    cache_and_return_result(
                        cached_results,
                        cache_key,
                        SyncItemResult(
                            candidate=candidate,
                            status="skipped",
                            reason=match.status,
                        ),
                    )
                )
                continue

            if subject is None:
                subject = client.get_subject(match.subject.subject_id)
            subject_media_type = classify_subject_media_type(subject)
            if subject_media_type != "manga":
                emit(
                    f"[item {index}/{len(candidates)}] skip {candidate_label}: "
                    f"matched subject platform={subject.platform or 'unknown'} "
                    f"classified as {subject_media_type}, not syncing"
                )
                run_result.item_results.append(
                    cache_and_return_result(
                        cached_results,
                        cache_key,
                        SyncItemResult(
                            candidate=candidate,
                            status="skipped",
                            reason=(
                                "non_manga_subject"
                                if subject_media_type == "novel"
                                else "unknown_subject_media_type"
                            ),
                            subject=subject,
                        ),
                    )
                )
                continue

            current_collection = client.get_my_subject_collection(subject.subject_id)
            target_type = STATE_TO_BANGUMI_TYPE[candidate.target_state]
            current_type = extract_collection_type(current_collection)
            if current_type == target_type:
                emit(
                    f"[item {index}/{len(candidates)}] skip {candidate_label}: already synced "
                    f"to state={candidate.target_state} subject_id={subject.subject_id}"
                )
                run_result.item_results.append(
                    cache_and_return_result(
                        cached_results,
                        cache_key,
                        SyncItemResult(
                            candidate=candidate,
                            status="skipped",
                            reason="already_synced",
                            subject=subject,
                            current_type=current_type,
                        ),
                    )
                )
                continue

            if dry_run:
                emit(
                    f"[item {index}/{len(candidates)}] would update {candidate_label} -> "
                    f"subject_id={subject.subject_id} state={candidate.target_state}"
                )
                run_result.item_results.append(
                    cache_and_return_result(
                        cached_results,
                        cache_key,
                        SyncItemResult(
                            candidate=candidate,
                            status="would_update",
                            reason="dry_run",
                            subject=subject,
                            current_type=current_type,
                        ),
                    )
                )
                continue

            client.upsert_subject_collection(subject.subject_id, candidate.target_state)
            emit(
                f"[item {index}/{len(candidates)}] updated {candidate_label} -> "
                f"subject_id={subject.subject_id} state={candidate.target_state}"
            )
            run_result.item_results.append(
                cache_and_return_result(
                    cached_results,
                    cache_key,
                    SyncItemResult(
                        candidate=candidate,
                        status="updated",
                        reason="updated",
                        subject=subject,
                        current_type=current_type,
                    ),
                    updated_target_type=target_type,
                )
            )
        except BangumiClientError as exc:
            emit(f"[item {index}/{len(candidates)}] failed {candidate_label}: {exc}")
            run_result.item_results.append(
                cache_and_return_result(
                    cached_results,
                    cache_key,
                    SyncItemResult(
                        candidate=candidate,
                        status="failed",
                        reason=str(exc),
                    ),
                )
            )

    emit(
        "[done] "
        f"updated={run_result.counts['updated']} "
        f"would_update={run_result.counts['would_update']} "
        f"skipped={run_result.counts['skipped']} "
        f"failed={run_result.counts['failed']}"
    )
    return run_result


def format_candidate_label(item: SyncItemResult | SyncTarget | object) -> str:
    candidate = item.candidate if isinstance(item, SyncItemResult) else item
    name = getattr(candidate, "name", None) or getattr(candidate, "record_id", None) or "<unknown>"
    source_table = getattr(candidate, "source_table", "<unknown>")
    target_state = getattr(candidate, "target_state", "<unknown>")
    return f"{source_table}:{name} -> {target_state}"


def describe_match_status(status: str, subjects: list[object]) -> str:
    if status == "skipped_no_result":
        return "no Bangumi subject matched the search keyword"
    if status == "skipped_ambiguous":
        return f"multiple exact matches: {format_subjects(subjects)}"
    if status == "skipped_low_confidence":
        return f"low confidence candidates: {format_subjects(subjects)}"
    return status


def resolve_subject_for_sync(
    client: BangumiClient,
    search_request: SyncSearchRequest,
    subjects: list[BangumiSubject],
    match,
) -> BangumiSubject | None:
    candidate_pool = combine_subject_candidates(match.candidate_subjects, subjects[:20])
    if match.status == "matched" and match.subject is not None:
        matched_subject = client.get_subject(match.subject.subject_id)
        if classify_subject_media_type(matched_subject) == "manga":
            return None
        candidate_pool = combine_subject_candidates([matched_subject], candidate_pool)

    lightweight_choice = choose_subject_by_title_score(search_request, candidate_pool)
    if lightweight_choice is not None:
        return lightweight_choice

    detailed_subjects = [client.get_subject(subject.subject_id) for subject in candidate_pool[:12]]
    detailed_choice = choose_subject_by_detail_score(search_request, detailed_subjects)
    if detailed_choice is not None:
        return detailed_choice

    if match.status == "skipped_ambiguous":
        manga_subjects = [
            subject
            for subject in detailed_subjects
            if classify_subject_media_type(subject) == "manga"
        ]
        if len(manga_subjects) == 1:
            return manga_subjects[0]
    return None


def choose_subject_by_title_score(
    search_request: SyncSearchRequest,
    subjects: list[BangumiSubject],
) -> BangumiSubject | None:
    scored = sorted(
        (
            (score_subject_title(search_request, subject), subject)
            for subject in subjects
            if classify_subject_media_type(subject) != "novel"
        ),
        key=lambda item: item[0],
        reverse=True,
    )
    if not scored:
        return None
    best_score, best_subject = scored[0]
    second_score = scored[1][0] if len(scored) > 1 else 0.0
    if best_score >= 0.78 and best_score - second_score >= 0.08:
        return best_subject
    return None


def choose_subject_by_detail_score(
    search_request: SyncSearchRequest,
    subjects: list[BangumiSubject],
) -> BangumiSubject | None:
    author_matched_subjects = [
        subject
        for subject in subjects
        if classify_subject_media_type(subject) == "manga"
        and author_matches(search_request.author_hints, subject.authors)
        and not is_probable_volume(subject)
    ]
    if len(author_matched_subjects) == 1:
        return author_matched_subjects[0]
    if author_matched_subjects:
        scored_author_matches = sorted(
            (
                (score_subject_detail(search_request, subject), subject)
                for subject in author_matched_subjects
            ),
            key=lambda item: item[0],
            reverse=True,
        )
        best_score, best_subject = scored_author_matches[0]
        second_score = scored_author_matches[1][0] if len(scored_author_matches) > 1 else 0.0
        if best_score >= 0.55 and best_score - second_score >= 0.05:
            return best_subject
        if best_score >= 0.75 and best_score == second_score:
            return author_matched_subjects[0]

    scored = sorted(
        (
            (score_subject_detail(search_request, subject), subject)
            for subject in subjects
            if classify_subject_media_type(subject) != "novel"
        ),
        key=lambda item: item[0],
        reverse=True,
    )
    if not scored:
        return None
    best_score, best_subject = scored[0]
    second_score = scored[1][0] if len(scored) > 1 else 0.0
    if best_score >= 0.82 and best_score - second_score >= 0.12:
        return best_subject
    return None


def build_candidate_cache_key(search_request: SyncSearchRequest) -> tuple[str, tuple[str, ...], str]:
    title_key = normalize_match_title(search_request.keyword)
    author_keys = tuple(
        sorted(
            {
                normalized
                for author in search_request.author_hints
                if (normalized := normalize_match_title(author))
            }
        )
    )
    return title_key, author_keys, search_request.candidate.target_state


def cache_and_return_result(
    cache: dict[tuple[str, tuple[str, ...], str], SyncItemResult],
    cache_key: tuple[str, tuple[str, ...], str],
    result: SyncItemResult,
    *,
    updated_target_type: int | None = None,
) -> SyncItemResult:
    if result.status == "updated" and updated_target_type is not None:
        cache[cache_key] = replace(
            result,
            status="skipped",
            reason="already_synced",
            current_type=updated_target_type,
        )
        return result
    cache[cache_key] = result
    return result


def combine_subject_candidates(
    primary: list[BangumiSubject],
    secondary: list[BangumiSubject],
) -> list[BangumiSubject]:
    subjects_by_id: dict[int, BangumiSubject] = {}
    for subject in [*primary, *secondary]:
        subjects_by_id.setdefault(subject.subject_id, subject)
    return list(subjects_by_id.values())


def score_subject_title(search_request: SyncSearchRequest, subject: BangumiSubject) -> float:
    query = search_request.keyword
    subject_titles = [subject.name, subject.name_cn]
    score = max(similarity_ratio(query, title) for title in subject_titles if title)
    score = max(
        score,
        max(cjk_substring_overlap(query, title) + 0.15 for title in subject_titles if title),
    )
    if is_probable_volume(subject):
        score -= 0.18
    if classify_subject_media_type(subject) == "manga":
        score += 0.03
    return score


def score_subject_detail(search_request: SyncSearchRequest, subject: BangumiSubject) -> float:
    titles = [subject.name, subject.name_cn, *subject.aliases]
    candidate_scores = [score_subject_title(search_request, subject)]
    candidate_scores.extend(
        similarity_ratio(search_request.keyword, title)
        for title in titles
        if title
    )
    score = max(candidate_scores, default=0.0)
    if author_matches(search_request.author_hints, subject.authors):
        score += 0.22
    if classify_subject_media_type(subject) == "manga":
        score += 0.05
    if is_probable_volume(subject):
        score -= 0.18
    return score


def author_matches(author_hints: list[str], authors: list[str]) -> bool:
    if not author_hints or not authors:
        return False
    for hint in author_hints:
        for author in authors:
            if similarity_ratio(hint, author) >= 0.72:
                return True
    return False


def is_probable_volume(subject: BangumiSubject) -> bool:
    titles = [subject.name or "", subject.name_cn or ""]
    volume_markers = ["(1)", "（1）", "vol.", "vol ", "第1", "no.1"]
    lowered_titles = [title.casefold() for title in titles]
    return any(marker in title for title in lowered_titles for marker in volume_markers)


def classify_subject_media_type(subject: BangumiSubject) -> str:
    signals = [subject.platform or ""]
    normalized_signals = [signal.casefold() for signal in signals if signal]

    if any("漫画" in signal or "comic" in signal for signal in normalized_signals):
        return "manga"
    if any(
        token in signal
        for signal in normalized_signals
        for token in ("小说", "轻小说", "novel", "文库")
    ):
        return "novel"
    return "unknown"


def format_subjects(subjects: list[object]) -> str:
    if not subjects:
        return "none"
    return ", ".join(
        f"{getattr(subject, 'subject_id', '?')}:{getattr(subject, 'name', '?')}"
        for subject in subjects[:5]
    )


def extract_collection_type(collection: dict[str, object] | None) -> int | None:
    if not isinstance(collection, dict):
        return None
    value = collection.get("type")
    if isinstance(value, int):
        return value
    return None


def render_sync_summary(run_result: SyncRunResult) -> str:
    lines = [
        f"Archive: {run_result.archive_path}",
        f"Dry run: {run_result.dry_run}",
        f"Updated: {run_result.counts['updated']}",
        f"Would update: {run_result.counts['would_update']}",
        f"Skipped: {run_result.counts['skipped']}",
        f"Failed: {run_result.counts['failed']}",
        "Items:",
    ]
    for item in run_result.item_results:
        subject = f" -> {item.subject.subject_id}" if item.subject else ""
        name = item.candidate.name or item.candidate.record_id or "<unknown>"
        lines.append(
            f"  [{item.status}] {item.candidate.source_table}:{name}{subject} ({item.reason})"
        )
    return "\n".join(lines)


def report_as_dict(run_result: SyncRunResult) -> dict[str, object]:
    return {
        "archive_path": str(run_result.archive_path),
        "dry_run": run_result.dry_run,
        "counts": run_result.counts,
        "items": [
            {
                "table": item.candidate.source_table,
                "name": item.candidate.name,
                "record_id": item.candidate.record_id,
                "target_state": item.candidate.target_state,
                "status": item.status,
                "reason": item.reason,
                "subject_id": item.subject.subject_id if item.subject else None,
                "current_type": item.current_type,
            }
            for item in run_result.item_results
        ],
    }


def write_report(run_result: SyncRunResult, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report_as_dict(run_result), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )