from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from venera_parser_bangumi.cli import cli


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