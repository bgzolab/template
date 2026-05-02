from __future__ import annotations

import json
import os
from typing import Any
from urllib import error as urllib_error
from urllib import parse as urllib_parse
from urllib import request as urllib_request

from ..constants import (
    DEFAULT_BANGUMI_API_BASE_URL,
    DEFAULT_USER_AGENT,
    STATE_TO_BANGUMI_TYPE,
)
from ..helpers import build_search_keywords, string_or_none
from ..models import BangumiSubject, SyncSearchRequest


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
        self._username: str | None = None

    @classmethod
    def from_env(cls) -> "BangumiClient":
        access_token = os.environ.get("ACCESS_TOKEN", "").strip()
        if not access_token:
            raise BangumiAuthError("ACCESS_TOKEN environment variable is required")
        return cls(access_token)

    def search_subjects(
        self, search_request: SyncSearchRequest, *, limit: int = 100
    ) -> list[BangumiSubject]:
        subjects_by_id: dict[int, BangumiSubject] = {}
        for keyword in build_search_keywords(search_request.keyword):
            payload = {
                "keyword": keyword,
                "sort": "match",
                "filter": {"type": [1]},
            }
            response = self.request_json(
                "POST",
                "/search/subjects",
                payload=payload,
                query={"limit": str(limit), "offset": "0"},
            )
            data = response.get("data", []) if isinstance(response, dict) else []
            if not isinstance(data, list):
                continue
            for item in data:
                subject = parse_subject_payload(item)
                if subject is None:
                    continue
                subjects_by_id.setdefault(subject.subject_id, subject)
        return list(subjects_by_id.values())

    def get_subject(self, subject_id: int) -> BangumiSubject:
        response = self.request_json("GET", f"/subjects/{subject_id}")
        if not isinstance(response, dict):
            raise BangumiRequestError("Unexpected subject response format")
        subject = parse_subject_payload(response)
        if subject is None:
            raise BangumiRequestError("Subject response is missing required fields")
        return subject

    def get_my_subject_collection(self, subject_id: int) -> dict[str, Any] | None:
        try:
            response = self.request_json(
                "GET", f"/users/{self.get_username()}/collections/{subject_id}"
            )
        except BangumiRequestError as exc:
            if str(exc).startswith("404 "):
                return None
            raise
        if response is None:
            return None
        if not isinstance(response, dict):
            raise BangumiRequestError("Unexpected collection response format")
        return response

    def get_username(self) -> str:
        if self._username:
            return self._username
        response = self.request_json("GET", "/me")
        if not isinstance(response, dict):
            raise BangumiRequestError("Unexpected /me response format")
        username = string_or_none(response.get("username"))
        if not username:
            raise BangumiRequestError("Authenticated user response is missing username")
        self._username = username
        return username

    def upsert_subject_collection(self, subject_id: int, state: str) -> None:
        self.request_json(
            "POST",
            f"/users/-/collections/{subject_id}",
            payload={"type": STATE_TO_BANGUMI_TYPE[state]},
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


def parse_subject_payload(item: object) -> BangumiSubject | None:
    if not isinstance(item, dict):
        return None
    subject_id = item.get("id")
    name = item.get("name")
    if subject_id is None or not isinstance(name, str):
        return None
    return BangumiSubject(
        subject_id=int(subject_id),
        name=name,
        name_cn=string_or_none(item.get("name_cn")),
        platform=string_or_none(item.get("platform")),
    )