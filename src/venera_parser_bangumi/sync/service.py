from __future__ import annotations

import json
from pathlib import Path

from ..constants import STATE_TO_BANGUMI_TYPE
from ..models import SyncItemResult, SyncRunResult, SyncTarget
from .bangumi import BangumiClient, BangumiClientError
from .candidates import build_search_request, load_sync_candidates
from .matching import match_search_result


def run_sync(
    archive_path: Path,
    sync_targets: list[SyncTarget],
    *,
    dry_run: bool,
    client: BangumiClient,
) -> SyncRunResult:
    candidates = load_sync_candidates(archive_path, sync_targets)
    run_result = SyncRunResult(archive_path=archive_path, dry_run=dry_run)

    for candidate in candidates:
        search_request = build_search_request(candidate)
        try:
            subjects = client.search_subjects(search_request)
            match = match_search_result(search_request, subjects)
            if match.status != "matched":
                run_result.item_results.append(
                    SyncItemResult(
                        candidate=candidate,
                        status="skipped",
                        reason=match.status,
                    )
                )
                continue

            current_collection = client.get_my_subject_collection(match.subject.subject_id)
            target_type = STATE_TO_BANGUMI_TYPE[candidate.target_state]
            current_type = extract_collection_type(current_collection)
            if current_type == target_type:
                run_result.item_results.append(
                    SyncItemResult(
                        candidate=candidate,
                        status="skipped",
                        reason="already_synced",
                        subject=match.subject,
                        current_type=current_type,
                    )
                )
                continue

            if dry_run:
                run_result.item_results.append(
                    SyncItemResult(
                        candidate=candidate,
                        status="would_update",
                        reason="dry_run",
                        subject=match.subject,
                        current_type=current_type,
                    )
                )
                continue

            client.upsert_subject_collection(match.subject.subject_id, candidate.target_state)
            run_result.item_results.append(
                SyncItemResult(
                    candidate=candidate,
                    status="updated",
                    reason="updated",
                    subject=match.subject,
                    current_type=current_type,
                )
            )
        except BangumiClientError as exc:
            run_result.item_results.append(
                SyncItemResult(
                    candidate=candidate,
                    status="failed",
                    reason=str(exc),
                )
            )

    return run_result


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