from __future__ import annotations

from venera_parser_bangumi.helpers import build_search_keywords


def test_build_search_keywords_adds_konosuba_override_keyword() -> None:
    keywords = build_search_keywords("為這美好世界獻上祝福")

    assert "祝福这个美好的世界" in keywords


def test_build_search_keywords_adds_uncle_and_suffix_stripped_keywords() -> None:
    keywords = build_search_keywords("異世界歸來的舅舅")
    stripped_keywords = build_search_keywords("变身Emergence 单行本")

    assert "异世界叔叔" in keywords
    assert "变身Emergence" in stripped_keywords