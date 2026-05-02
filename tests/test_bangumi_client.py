from __future__ import annotations

import io
from urllib import error as urllib_error

import pytest

from venera_parser_bangumi.sync.bangumi import BangumiAuthError, BangumiClient


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