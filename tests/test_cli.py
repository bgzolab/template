from __future__ import annotations

import importlib
from pathlib import Path

from click.testing import CliRunner

from venera_parser_bangumi.cli import cli
from venera_parser_bangumi.models import SyncRunResult

cli_module = importlib.import_module("venera_parser_bangumi.cli")


def test_sync_bangumi_help_shows_required_options() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["sync-bangumi", "--help"])

    assert result.exit_code == 0
    assert "--sync" in result.output
    assert "--dry-run" in result.output


def test_sync_bangumi_requires_sync_argument(sample_archive: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["sync-bangumi", str(sample_archive)])

    assert result.exit_code != 0
    assert "Missing option '--sync'" in result.output


def test_sync_bangumi_rejects_invalid_state(sample_archive: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["sync-bangumi", str(sample_archive), "--sync", "Doing=reading"],
    )

    assert result.exit_code != 0
    assert "invalid Bangumi state 'reading'" in result.output


def test_sync_bangumi_requires_access_token(sample_archive: Path, monkeypatch) -> None:
    runner = CliRunner()
    monkeypatch.delenv("ACCESS_TOKEN", raising=False)

    result = runner.invoke(
        cli,
        ["sync-bangumi", str(sample_archive), "--sync", "Doing=doing", "--dry-run"],
    )

    assert result.exit_code != 0
    assert "ACCESS_TOKEN environment variable is required" in result.output


def test_sync_bangumi_prints_progress_logs(sample_archive: Path, monkeypatch) -> None:
    runner = CliRunner()

    class FakeClient:
        @classmethod
        def from_env(cls):
            return cls()

    def fake_run_sync(_archive, _targets, *, dry_run, client, log):
        assert dry_run is True
        assert isinstance(client, FakeClient)
        log("[start] loaded 1 candidate(s)")
        log("[item 1/1] skip DONE:電鋸人 -> done: no Bangumi subject matched the search keyword")
        return SyncRunResult(archive_path=sample_archive, dry_run=True)

    monkeypatch.setattr(cli_module, "BangumiClient", FakeClient)
    monkeypatch.setattr(cli_module, "run_sync", fake_run_sync)

    result = runner.invoke(
        cli,
        ["sync-bangumi", str(sample_archive), "--sync", "DONE=done", "--dry-run"],
    )

    assert result.exit_code == 0
    assert "[start] loaded 1 candidate(s)" in result.output
    assert "no Bangumi subject matched" in result.output
    assert "Archive:" in result.output