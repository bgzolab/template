from __future__ import annotations

import json
import sqlite3
import tempfile
import zipfile
from pathlib import Path
from typing import Any

from .constants import DATABASE_ENTRIES
from .helpers import normalize_value, quote_identifier
from .models import ArchiveMember


def parse_archive(
    archive_path: Path,
    *,
    include_rows: bool,
    include_cookie_db: bool,
) -> dict[str, Any]:
    with zipfile.ZipFile(archive_path) as archive:
        members = [member_to_dict(info) for info in archive.infolist()]
        appdata = parse_appdata(archive)
        comic_source_files = sorted(
            info.filename
            for info in archive.infolist()
            if info.filename.startswith("comic_source/") and not info.is_dir()
        )
        databases = parse_databases(
            archive,
            include_rows=include_rows,
            include_cookie_db=include_cookie_db,
        )

    return {
        "archive": {
            "path": str(archive_path),
            "size": archive_path.stat().st_size,
            "member_count": len(members),
            "members": members,
        },
        "appdata": appdata,
        "comic_source": {
            "count": len(comic_source_files),
            "files": comic_source_files,
        },
        "databases": databases,
    }


def extract_database(
    archive: zipfile.ZipFile, temp_path: Path, database_name: str
) -> Path | None:
    try:
        data = archive.read(database_name)
    except KeyError:
        return None
    db_path = temp_path / database_name
    db_path.write_bytes(data)
    return db_path


def member_to_dict(info: zipfile.ZipInfo) -> dict[str, Any]:
    member = ArchiveMember(
        name=info.filename,
        size=info.file_size,
        compressed_size=info.compress_size,
        modified_at=(
            f"{info.date_time[0]:04d}-{info.date_time[1]:02d}-{info.date_time[2]:02d} "
            f"{info.date_time[3]:02d}:{info.date_time[4]:02d}:{info.date_time[5]:02d}"
        ),
    )
    return {
        "name": member.name,
        "size": member.size,
        "compressed_size": member.compressed_size,
        "modified_at": member.modified_at,
    }


def parse_appdata(archive: zipfile.ZipFile) -> dict[str, Any] | None:
    try:
        raw = archive.read("appdata.json")
    except KeyError:
        return None

    data = json.loads(raw.decode("utf-8"))
    settings = data.get("settings") if isinstance(data, dict) else None
    summary: dict[str, Any] = {}
    if isinstance(settings, dict):
        for key in (
            "language",
            "theme_mode",
            "color",
            "dataVersion",
            "quickFavorite",
            "followUpdatesFolder",
            "readerMode",
            "proxy",
            "icloudSyncEnabled",
            "trackerSyncEnabled",
        ):
            if key in settings:
                summary[key] = settings[key]
        webdav = settings.get("webdav")
        if isinstance(webdav, list):
            summary["webdavConfigured"] = len(webdav) == 3 and bool(webdav[0])
        summary["favoriteSourceCount"] = len(settings.get("favorites", []))
        summary["searchSourceCount"] = len(settings.get("searchSources", []))
        summary["explorePageCount"] = len(settings.get("explore_pages", []))

    return {
        "summary": summary,
        "raw": data,
    }


def parse_databases(
    archive: zipfile.ZipFile,
    *,
    include_rows: bool,
    include_cookie_db: bool,
) -> dict[str, Any]:
    parsed: dict[str, Any] = {}
    with tempfile.TemporaryDirectory(prefix="venera_parser_") as temp_dir:
        temp_path = Path(temp_dir)
        for name in DATABASE_ENTRIES:
            if name == "cookie.db" and not include_cookie_db:
                continue
            db_path = extract_database(archive, temp_path, name)
            if db_path is None:
                continue
            parsed[name] = parse_sqlite_database(db_path, include_rows=include_rows)
    return parsed


def parse_sqlite_database(db_path: Path, *, include_rows: bool) -> dict[str, Any]:
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    try:
        tables = connection.execute(
            "SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        ).fetchall()
        parsed_tables: dict[str, Any] = {}
        for table in tables:
            table_name = table["name"]
            columns = [
                column["name"]
                for column in connection.execute(
                    f"PRAGMA table_info({quote_identifier(table_name)})"
                )
            ]
            row_count = connection.execute(
                f"SELECT COUNT(*) AS count FROM {quote_identifier(table_name)}"
            ).fetchone()["count"]
            table_data: dict[str, Any] = {
                "schema": table["sql"],
                "columns": columns,
                "row_count": row_count,
            }
            if include_rows:
                rows = connection.execute(
                    f"SELECT * FROM {quote_identifier(table_name)}"
                ).fetchall()
                table_data["rows"] = [normalize_value(dict(row)) for row in rows]
            parsed_tables[table_name] = table_data
        return {
            "path": str(db_path),
            "tables": parsed_tables,
        }
    finally:
        connection.close()


def print_summary(parsed: dict[str, Any]) -> None:
    archive = parsed["archive"]
    print(f"Archive: {archive['path']}")
    print(f"Size: {archive['size']} bytes")
    print(f"Members: {archive['member_count']}")
    print()

    appdata = parsed.get("appdata")
    if appdata is None:
        print("appdata.json: missing")
    else:
        print("appdata.json:")
        summary = appdata.get("summary", {})
        for key, value in summary.items():
            print(f"  {key}: {value}")
        raw = appdata.get("raw", {})
        if isinstance(raw, dict):
            value = raw.get("searchHistory")
            if isinstance(value, list):
                print(f"  searchHistory count: {len(value)}")
        print()

    comic_source = parsed.get("comic_source", {})
    print(f"comic_source files: {comic_source.get('count', 0)}")
    for name in comic_source.get("files", [])[:10]:
        print(f"  {name}")
    if comic_source.get("count", 0) > 10:
        print(f"  ... ({comic_source['count'] - 10} more)")
    print()

    databases = parsed.get("databases", {})
    for db_name, db_data in databases.items():
        print(f"{db_name}:")
        for table_name, table_data in db_data.get("tables", {}).items():
            columns = ", ".join(table_data["columns"])
            print(f"  {table_name}: {table_data['row_count']} rows, columns={columns}")
        print()