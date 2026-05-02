#!/usr/bin/env python3

from __future__ import annotations

import argparse
import base64
import json
import os
import sqlite3
import sys
import tempfile
import unicodedata
from urllib import error as urllib_error
from urllib import parse as urllib_parse
from urllib import request as urllib_request
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DATABASE_ENTRIES = ("history.db", "local_favorite.db", "cookie.db")
COLLECTION_STATES = ("wish", "done", "doing", "on_hold", "dropped")
STATE_TO_BANGUMI_TYPE = {
    "wish": 1,
    "done": 2,
    "doing": 3,
    "on_hold": 4,
    "dropped": 5,
}
DEFAULT_BANGUMI_API_BASE_URL = "https://api.bgm.tv/v0"
DEFAULT_USER_AGENT = (
    "bgzo/venera-parser-bangumi "
    "(https://github.com/bGZo/playground)"
)


@dataclass
class ArchiveMember:
    name: str
    size: int
    compressed_size: int
    modified_at: str


@dataclass(frozen=True)
class SyncTarget:
    table: str
    state: str


@dataclass(frozen=True)
class SyncCandidate:
    source_table: str
    target_state: str
    record_id: str | None
    name: str | None
    author: str | None
    subject_type: int | None
    tags: list[str]
    translated_tags: list[str]


@dataclass(frozen=True)
class SyncSearchRequest:
    candidate: SyncCandidate
    keyword: str
    author_hints: list[str]
    tag_hints: list[str]


@dataclass(frozen=True)
class BangumiSubject:
    subject_id: int
    name: str
    name_cn: str | None = None


@dataclass(frozen=True)
class MatchResult:
    status: str
    search_request: SyncSearchRequest
    subject: BangumiSubject | None
    candidate_subjects: list[BangumiSubject]


class BangumiClientError(RuntimeError):
    pass


class BangumiAuthError(BangumiClientError):
    pass


class BangumiRequestError(BangumiClientError):
    pass


class BangumiClient:
    def __init__(
        self,
        access_token: str,
        *,
        base_url: str = DEFAULT_BANGUMI_API_BASE_URL,
        user_agent: str = DEFAULT_USER_AGENT,
    ) -> None:
        self.access_token = access_token
        self.base_url = base_url.rstrip("/")
        self.user_agent = user_agent

    @classmethod
    def from_env(cls) -> "BangumiClient":
        access_token = os.environ.get("ACCESS_TOKEN", "").strip()
        if not access_token:
            raise BangumiAuthError("ACCESS_TOKEN environment variable is required")
        return cls(access_token)

    def search_subjects(
        self, search_request: SyncSearchRequest, *, limit: int = 10
    ) -> list[BangumiSubject]:
        payload = {
            "keyword": search_request.keyword,
            "sort": "match",
            "filter": {
                "type": [1],
            },
        }
        response = self.request_json(
            "POST",
            "/search/subjects",
            payload=payload,
            query={"limit": str(limit), "offset": "0"},
        )
        data = response.get("data", []) if isinstance(response, dict) else []
        subjects: list[BangumiSubject] = []
        if isinstance(data, list):
            for item in data:
                if not isinstance(item, dict):
                    continue
                subject_id = item.get("id")
                name = item.get("name")
                if subject_id is None or not isinstance(name, str):
                    continue
                subjects.append(
                    BangumiSubject(
                        subject_id=int(subject_id),
                        name=name,
                        name_cn=string_or_none(item.get("name_cn")),
                    )
                )
        return subjects

    def get_my_subject_collection(self, subject_id: int) -> dict[str, Any] | None:
        try:
            response = self.request_json(
                "GET", f"/users/-/collections/{subject_id}"
            )
        except BangumiRequestError as exc:
            if str(exc).startswith("404 "):
                return None
            raise
        if not isinstance(response, dict):
            raise BangumiRequestError("Unexpected collection response format")
        return response

    def upsert_subject_collection(self, subject_id: int, state: str) -> None:
        collection_type = STATE_TO_BANGUMI_TYPE[state]
        self.request_json(
            "POST",
            f"/users/-/collections/{subject_id}",
            payload={"type": collection_type},
        )

    def request_json(
        self,
        method: str,
        path: str,
        *,
        payload: dict[str, Any] | None = None,
        query: dict[str, str] | None = None,
    ) -> Any:
        url = self.base_url + path
        if query:
            url += "?" + urllib_parse.urlencode(query)
        body = None
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}",
            "User-Agent": self.user_agent,
        }
        if payload is not None:
            body = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"

        request = urllib_request.Request(url, data=body, headers=headers, method=method)
        try:
            with urllib_request.urlopen(request) as response:
                raw = response.read()
        except urllib_error.HTTPError as exc:
            message = exc.read().decode("utf-8", errors="replace").strip()
            if exc.code in {401, 403}:
                raise BangumiAuthError(
                    f"{exc.code} authentication failed: {message or exc.reason}"
                ) from exc
            raise BangumiRequestError(
                f"{exc.code} request failed: {message or exc.reason}"
            ) from exc
        except urllib_error.URLError as exc:
            raise BangumiRequestError(f"Network error: {exc.reason}") from exc

        if not raw:
            return None
        try:
            return json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise BangumiRequestError("Response is not valid JSON") from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Parse a Venera exported .venera data archive."
    )
    subparsers = parser.add_subparsers(dest="command", required=False)

    summary_parser = subparsers.add_parser(
        "summary", help="Print a readable summary for a .venera archive."
    )
    add_common_arguments(summary_parser)

    dump_parser = subparsers.add_parser(
        "dump", help="Dump parsed archive data as JSON."
    )
    add_common_arguments(dump_parser)
    dump_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Write JSON to a file instead of stdout.",
    )
    dump_parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output.",
    )

    sync_parser = subparsers.add_parser(
        "sync-bangumi",
        help="Validate and run Bangumi sync using selected local_favorite tables.",
    )
    sync_parser.add_argument("archive", type=Path, help="Path to a .venera file.")
    sync_parser.add_argument(
        "--sync",
        dest="sync_targets",
        action="append",
        required=True,
        metavar="TABLE=STATE",
        type=parse_sync_target,
        help=(
            "Map a local_favorite table to a Bangumi collection state. "
            "Allowed states: wish, done, doing, on_hold, dropped. "
            "Repeat to sync multiple tables."
        ),
    )
    sync_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run the full decision flow without sending Bangumi write requests.",
    )

    parser.set_defaults(command="summary")
    return parser.parse_args()


def parse_sync_target(value: str) -> SyncTarget:
    table, separator, state = value.partition("=")
    if not separator:
        raise argparse.ArgumentTypeError(
            "sync target must use TABLE=STATE format"
        )

    table = table.strip()
    state = state.strip().lower()
    if not table:
        raise argparse.ArgumentTypeError("sync target table name cannot be empty")
    if state not in COLLECTION_STATES:
        allowed = ", ".join(COLLECTION_STATES)
        raise argparse.ArgumentTypeError(
            f"invalid Bangumi state '{state}', allowed values: {allowed}"
        )

    return SyncTarget(table=table, state=state)


def add_common_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("archive", type=Path, help="Path to a .venera file.")
    parser.add_argument(
        "--include-cookie-db",
        action="store_true",
        help="Parse cookie.db as well. Omitted by default because it often contains sensitive data.",
    )
    parser.add_argument(
        "--include-rows",
        action="store_true",
        help="Include full table rows in parsed database output.",
    )


def main() -> int:
    args = parse_args()
    archive_path = args.archive.expanduser().resolve()
    if not archive_path.is_file():
        print(f"Archive not found: {archive_path}", file=sys.stderr)
        return 1
    if archive_path.suffix.lower() != ".venera":
        print("Warning: file does not use the .venera extension.", file=sys.stderr)

    if args.command == "sync-bangumi":
        return run_sync_bangumi(args, archive_path)

    parsed = parse_archive(
        archive_path,
        include_rows=args.include_rows,
        include_cookie_db=args.include_cookie_db,
    )

    if args.command == "dump":
        dump_json(parsed, getattr(args, "output", None), getattr(args, "pretty", False))
        return 0

    print_summary(parsed)
    return 0


def run_sync_bangumi(args: argparse.Namespace, archive_path: Path) -> int:
    try:
        candidates = load_sync_candidates(archive_path, args.sync_targets)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    search_requests = [build_search_request(candidate) for candidate in candidates]
    try:
        BangumiClient.from_env()
    except BangumiAuthError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"Archive: {archive_path}")
    print(f"Dry run: {args.dry_run}")
    print(f"Loaded {len(candidates)} sync candidate(s).")
    print(f"Prepared {len(search_requests)} search request(s).")
    for target in args.sync_targets:
        count = sum(1 for candidate in candidates if candidate.source_table == target.table)
        print(f"  {target.table} -> {target.state}: {count} item(s)")
    return 0


def load_sync_candidates(
    archive_path: Path, sync_targets: list[SyncTarget]
) -> list[SyncCandidate]:
    with zipfile.ZipFile(archive_path) as archive, tempfile.TemporaryDirectory(
        prefix="venera_sync_"
    ) as temp_dir:
        temp_path = Path(temp_dir)
        db_path = extract_database(archive, temp_path, "local_favorite.db")
        if db_path is None:
            raise ValueError("Archive does not contain local_favorite.db")

        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row
        try:
            existing_tables = {
                row["name"]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
                ).fetchall()
            }
            candidates: list[SyncCandidate] = []
            for target in sync_targets:
                if target.table not in existing_tables:
                    raise ValueError(
                        f"Requested local_favorite table does not exist: {target.table}"
                    )

                rows = connection.execute(
                    f"SELECT * FROM {quote_identifier(target.table)}"
                ).fetchall()
                for row in rows:
                    row_dict = dict(row)
                    candidates.append(
                        SyncCandidate(
                            source_table=target.table,
                            target_state=target.state,
                            record_id=string_or_none(row_dict.get("id")),
                            name=string_or_none(row_dict.get("name")),
                            author=string_or_none(row_dict.get("author")),
                            subject_type=int_or_none(row_dict.get("type")),
                            tags=normalize_text_list(row_dict.get("tags")),
                            translated_tags=normalize_text_list(
                                row_dict.get("translated_tags")
                            ),
                        )
                    )
            return candidates
        finally:
            connection.close()


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


def string_or_none(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def int_or_none(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def normalize_text_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return []
        if stripped[0] == "[":
            try:
                parsed = json.loads(stripped)
            except json.JSONDecodeError:
                parsed = None
            if isinstance(parsed, list):
                return [item.strip() for item in map(str, parsed) if item and str(item).strip()]
        return [item.strip() for item in stripped.split(",") if item.strip()]
    if isinstance(value, list):
        return [item.strip() for item in map(str, value) if item and str(item).strip()]
    return [str(value).strip()] if str(value).strip() else []


def build_search_request(candidate: SyncCandidate) -> SyncSearchRequest:
    keyword = candidate.name or candidate.record_id or ""
    author_hints = [candidate.author] if candidate.author else []
    tag_hints = [*candidate.tags, *candidate.translated_tags]
    return SyncSearchRequest(
        candidate=candidate,
        keyword=keyword,
        author_hints=author_hints,
        tag_hints=tag_hints,
    )


def normalize_title(value: str | None) -> str:
    if value is None:
        return ""
    normalized = unicodedata.normalize("NFKC", value).casefold().strip()
    return "".join(normalized.split())


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
        and keyword
        in {
            normalize_title(subject.name),
            normalize_title(subject.name_cn),
        }
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
    status = "skipped_low_confidence" if near_matches else "skipped_no_result"
    return MatchResult(
        status=status,
        search_request=search_request,
        subject=None,
        candidate_subjects=near_matches,
    )


def dump_json(data: dict[str, Any], output: Path | None, pretty: bool) -> None:
    text = json.dumps(
        data,
        ensure_ascii=False,
        indent=2 if pretty else None,
        sort_keys=pretty,
    )
    if output is None:
        print(text)
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text + ("\n" if pretty else ""), encoding="utf-8")


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
    summary = {}
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
            try:
                data = archive.read(name)
            except KeyError:
                continue
            db_path = temp_path / name
            db_path.write_bytes(data)
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
                for column in connection.execute(f"PRAGMA table_info({quote_identifier(table_name)})")
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


def quote_identifier(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def normalize_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: normalize_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalize_value(item) for item in value]
    if isinstance(value, bytes):
        return {
            "encoding": "base64",
            "data": base64.b64encode(value).decode("ascii"),
        }
    if isinstance(value, str):
        stripped = value.strip()
        if stripped and stripped[0] in "[{":
            try:
                return {
                    "raw": value,
                    "parsed": normalize_value(json.loads(value)),
                }
            except json.JSONDecodeError:
                return value
    return value


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
            for key in ("searchHistory",):
                value = raw.get(key)
                if isinstance(value, list):
                    print(f"  {key} count: {len(value)}")
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
            print(
                f"  {table_name}: {table_data['row_count']} rows, columns={', '.join(table_data['columns'])}"
            )
        print()


if __name__ == "__main__":
    raise SystemExit(main())