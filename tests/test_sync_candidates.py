from __future__ import annotations

import pytest

from venera_parser_bangumi.models import SyncTarget
from venera_parser_bangumi.sync.candidates import build_search_request, load_sync_candidates


def test_load_sync_candidates_counts_match_sample_tables(sample_archive) -> None:
    candidates = load_sync_candidates(
        sample_archive,
        [SyncTarget("Doing", "doing"), SyncTarget("DONE", "done")],
    )

    doing = [item for item in candidates if item.source_table == "Doing"]
    done = [item for item in candidates if item.source_table == "DONE"]
    assert len(doing) == 74
    assert len(done) == 1
    assert doing[0].target_state == "doing"


def test_load_sync_candidates_raises_for_missing_table(sample_archive) -> None:
    with pytest.raises(ValueError, match="Requested local_favorite table does not exist"):
        load_sync_candidates(sample_archive, [SyncTarget("Missing", "doing")])


def test_build_search_request_keeps_source_context(sample_archive) -> None:
    candidate = load_sync_candidates(sample_archive, [SyncTarget("DONE", "done")])[0]

    request = build_search_request(candidate)
    assert request.candidate.source_table == "DONE"
    assert request.candidate.target_state == "done"
    assert request.keyword