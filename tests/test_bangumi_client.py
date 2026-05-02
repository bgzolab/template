from __future__ import annotations

import io
from urllib import error as urllib_error

import pytest

from venera_parser_bangumi.sync.bangumi import BangumiAuthError, BangumiClient, parse_subject_payload


def test_bangumi_client_requires_access_token(monkeypatch) -> None:
    monkeypatch.delenv("ACCESS_TOKEN", raising=False)

    with pytest.raises(BangumiAuthError, match="ACCESS_TOKEN"):
        BangumiClient.from_env()


def test_bangumi_client_reports_auth_failure(monkeypatch) -> None:
    client = BangumiClient("bad-token")

    def fake_urlopen(_request):
        raise urllib_error.HTTPError(
            url="https://api.bgm.tv/v0/users/-/collections/1",
            code=401,
            msg="Unauthorized",
            hdrs=None,
            fp=io.BytesIO(b'{"description":"access token has been expired or does not exist"}'),
        )

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    with pytest.raises(BangumiAuthError, match="401 authentication failed"):
        client.get_my_subject_collection(1)


def test_parse_subject_payload_reads_platform() -> None:
    subject = parse_subject_payload(
        {
            "id": 171069,
            "name": "さようなら竜生、こんにちは人生",
            "name_cn": "再见龙生，你好人生",
            "platform": "小说",
        }
    )

    assert subject is not None
    assert subject.subject_id == 171069
    assert subject.platform == "小说"


def test_get_my_subject_collection_uses_authenticated_username(monkeypatch) -> None:
    client = BangumiClient("token")
    calls: list[tuple[str, str]] = []

    def fake_request_json(method: str, path: str, **_kwargs):
        calls.append((method, path))
        if path == "/me":
            return {"username": "bool"}
        if path == "/users/bool/collections/192211":
            return {"type": 3, "subject_id": 192211}
        raise AssertionError(path)

    monkeypatch.setattr(client, "request_json", fake_request_json)

    assert client.get_my_subject_collection(192211) == {"type": 3, "subject_id": 192211}
    assert calls == [
        ("GET", "/me"),
        ("GET", "/users/bool/collections/192211"),
    ]


def test_search_subjects_merges_results_from_keyword_variants(monkeypatch) -> None:
    client = BangumiClient("token")
    seen_keywords: list[str] = []

    def fake_request_json(method: str, path: str, *, payload=None, query=None):
        assert method == "POST"
        assert path == "/search/subjects"
        assert query == {"limit": "100", "offset": "0"}
        seen_keywords.append(payload["keyword"])
        if payload["keyword"] == "想要成為影之實力者":
            return {"data": []}
        if payload["keyword"] == "想要成为影之实力者":
            return {
                "data": [
                    {
                        "id": 270199,
                        "name": "陰の実力者になりたくて!",
                        "name_cn": "想要成为影之实力者！",
                    }
                ]
            }
        return {"data": []}

    monkeypatch.setattr(client, "request_json", fake_request_json)

    results = client.search_subjects(type("Req", (), {"keyword": "想要成為影之實力者"})())

    assert results[0].subject_id == 270199
    assert seen_keywords[:2] == ["想要成为影之实力者", "想要成為影之實力者"]


def test_search_subjects_prefers_better_rank_from_later_keyword_variants(monkeypatch) -> None:
    client = BangumiClient("token")

    def fake_request_json(method: str, path: str, *, payload=None, query=None):
        assert method == "POST"
        assert path == "/search/subjects"
        assert query == {"limit": "100", "offset": "0"}
        if payload["keyword"] == "为这美好世界献上祝福":
            return {
                "data": [
                    {
                        "id": 107681,
                        "name": "この素晴らしい世界に祝福を!",
                        "name_cn": "为美好的世界献上祝福！",
                    }
                ]
            }
        if payload["keyword"] == "祝福这个美好的世界":
            return {
                "data": [
                    {
                        "id": 143035,
                        "name": "この素晴らしい世界に祝福を!",
                        "name_cn": "为美好的世界献上祝福！",
                    },
                    {
                        "id": 107681,
                        "name": "この素晴らしい世界に祝福を!",
                        "name_cn": "为美好的世界献上祝福！",
                    },
                ]
            }
        return {"data": []}

    monkeypatch.setattr(client, "request_json", fake_request_json)

    results = client.search_subjects(type("Req", (), {"keyword": "為這美好世界獻上祝福"})())

    assert [subject.subject_id for subject in results[:2]] == [143035, 107681]