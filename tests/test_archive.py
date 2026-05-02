from __future__ import annotations

from pathlib import Path

from venera_parser_bangumi.archive import parse_archive


def test_parse_archive_summary_counts(sample_archive: Path) -> None:
    parsed = parse_archive(sample_archive, include_rows=False, include_cookie_db=False)

    assert parsed["archive"]["member_count"] == 43
    assert parsed["comic_source"]["count"] == 39
    assert "cookie.db" not in parsed["databases"]


def test_parse_archive_with_rows_reads_tables(sample_archive: Path) -> None:
    parsed = parse_archive(sample_archive, include_rows=True, include_cookie_db=False)

    history_tables = parsed["databases"]["history.db"]["tables"]
    assert history_tables["history"]["row_count"] == 112
    assert len(history_tables["history"]["rows"]) == 112