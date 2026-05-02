from __future__ import annotations

from pathlib import Path

import click

from .archive import parse_archive, print_summary
from .constants import COLLECTION_STATES
from .helpers import dump_json
from .models import SyncTarget
from .sync import BangumiAuthError, BangumiClient, run_sync
from .sync.service import render_sync_summary, write_report


class SyncTargetParam(click.ParamType):
    name = "table=state"

    def convert(self, value, param, ctx):
        table, separator, state = value.partition("=")
        if not separator:
            self.fail("sync target must use TABLE=STATE format", param, ctx)
        table = table.strip()
        state = state.strip().lower()
        if not table:
            self.fail("sync target table name cannot be empty", param, ctx)
        if state not in COLLECTION_STATES:
            allowed = ", ".join(COLLECTION_STATES)
            self.fail(
                f"invalid Bangumi state '{state}', allowed values: {allowed}",
                param,
                ctx,
            )
        return SyncTarget(table=table, state=state)


SYNC_TARGET = SyncTargetParam()


def validate_archive_path(_ctx, _param, value: Path) -> Path:
    archive_path = value.expanduser().resolve()
    if not archive_path.is_file():
        raise click.BadParameter(f"Archive not found: {archive_path}")
    return archive_path


@click.group()
def cli() -> None:
    """Parse Venera exported archives and sync selected favorites to Bangumi."""


@cli.command("summary")
@click.argument("archive", type=click.Path(path_type=Path), callback=validate_archive_path)
@click.option("--include-cookie-db", is_flag=True, default=False)
@click.option("--include-rows", is_flag=True, default=False)
def summary_command(archive: Path, include_cookie_db: bool, include_rows: bool) -> None:
    parsed = parse_archive(
        archive,
        include_rows=include_rows,
        include_cookie_db=include_cookie_db,
    )
    print_summary(parsed)


@cli.command("dump")
@click.argument("archive", type=click.Path(path_type=Path), callback=validate_archive_path)
@click.option("--include-cookie-db", is_flag=True, default=False)
@click.option("--include-rows", is_flag=True, default=False)
@click.option("--output", "output_path", type=click.Path(path_type=Path))
@click.option("--pretty", is_flag=True, default=False)
def dump_command(
    archive: Path,
    include_cookie_db: bool,
    include_rows: bool,
    output_path: Path | None,
    pretty: bool,
) -> None:
    parsed = parse_archive(
        archive,
        include_rows=include_rows,
        include_cookie_db=include_cookie_db,
    )
    dump_json(parsed, output_path, pretty)


@cli.command("sync-bangumi")
@click.argument("archive", type=click.Path(path_type=Path), callback=validate_archive_path)
@click.option("--sync", "sync_targets", type=SYNC_TARGET, multiple=True, required=True)
@click.option("--dry-run", is_flag=True, default=False)
@click.option("--report-output", type=click.Path(path_type=Path))
def sync_bangumi_command(
    archive: Path,
    sync_targets: tuple[SyncTarget, ...],
    dry_run: bool,
    report_output: Path | None,
) -> None:
    try:
        client = BangumiClient.from_env()
    except BangumiAuthError as exc:
        raise click.ClickException(str(exc)) from exc

    run_result = run_sync(
        archive,
        list(sync_targets),
        dry_run=dry_run,
        client=client,
        log=click.echo,
    )
    click.echo(render_sync_summary(run_result))
    if report_output is not None:
        write_report(run_result, report_output)


def main() -> None:
    cli(standalone_mode=True)