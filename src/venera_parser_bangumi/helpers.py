from __future__ import annotations

import base64
import difflib
import json
import re
import unicodedata
from pathlib import Path
from typing import Any

from opencc import OpenCC


_S2T = OpenCC("s2t")
_T2S = OpenCC("t2s")
_PAREN_PATTERN = re.compile(r"\s*[\(（\[【].*?[\)）\]】]\s*")
_NON_WORD_PATTERN = re.compile(r"[^\w\u3400-\u9fff]+")
_SEARCH_SUFFIX_PATTERN = re.compile(r"\s*(单行本版|單行本版|单行本|單行本|総集編|总集篇|總集篇|漫畫版|漫画版|漫畫|漫画)\s*$")
_SEARCH_KEYWORD_OVERRIDES = {
    "为这美好世界献上祝福": ["祝福这个美好的世界"],
    "异世界归来的舅舅": ["异世界舅舅", "异世界叔叔"],
    "转生成蜘蛛又怎样": ["我是蜘蛛又怎样？"],
    "野生的最终boss出现了": ["野生のラスボスが現れた！"],
}


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
                return [item.strip() for item in map(str, parsed) if str(item).strip()]
        return [item.strip() for item in stripped.split(",") if item.strip()]
    if isinstance(value, list):
        return [item.strip() for item in map(str, value) if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []


def normalize_title(value: str | None) -> str:
    if value is None:
        return ""
    normalized = unicodedata.normalize("NFKC", value).casefold().strip()
    return "".join(normalized.split())


def normalize_search_text(value: str | None) -> str:
    if value is None:
        return ""
    normalized = unicodedata.normalize("NFKC", value).strip()
    normalized = _PAREN_PATTERN.sub(" ", normalized)
    normalized = _NON_WORD_PATTERN.sub(" ", normalized)
    return " ".join(normalized.split())


def normalize_match_title(value: str | None) -> str:
    normalized = normalize_search_text(to_simplified(value))
    return normalized.replace(" ", "")


def to_simplified(value: str | None) -> str:
    if not value:
        return ""
    return _T2S.convert(value)


def to_traditional(value: str | None) -> str:
    if not value:
        return ""
    return _S2T.convert(value)


def build_search_keywords(value: str | None) -> list[str]:
    if value is None:
        return []

    raw = unicodedata.normalize("NFKC", value).strip()
    simplified = to_simplified(raw)
    traditional = to_traditional(raw)
    candidates: list[str] = []

    normalized = normalize_search_text(raw)
    normalized_simplified = normalize_search_text(simplified)
    normalized_traditional = normalize_search_text(traditional)

    stripped_candidates = [
        _SEARCH_SUFFIX_PATTERN.sub("", text).strip()
        for text in (raw, simplified, traditional, normalized)
        if text
    ]

    override_keys = {
        normalize_match_title(text)
        for text in [raw, simplified, traditional, normalized, *stripped_candidates]
        if text
    }
    for key, overrides in _SEARCH_KEYWORD_OVERRIDES.items():
        if key in override_keys:
            candidates.extend(overrides)

    candidates.extend([simplified, raw, traditional, normalized, normalized_simplified, normalized_traditional])
    candidates.extend(text for text in stripped_candidates if text)

    for text in (raw, simplified, traditional, normalized, normalized_simplified, normalized_traditional):
        if not text:
            continue
        for token in re.split(r"\s+", text):
            token = token.strip()
            if len(token) >= 3:
                candidates.append(token)

    seen: set[str] = set()
    keywords: list[str] = []
    for item in candidates:
        item = item.strip()
        if not item or item in seen:
            continue
        seen.add(item)
        keywords.append(item)
    return keywords


def similarity_ratio(left: str | None, right: str | None) -> float:
    left_normalized = normalize_match_title(left)
    right_normalized = normalize_match_title(right)
    if not left_normalized or not right_normalized:
        return 0.0
    return difflib.SequenceMatcher(None, left_normalized, right_normalized).ratio()


def cjk_substring_overlap(left: str | None, right: str | None) -> float:
    left_normalized = normalize_match_title(left)
    right_normalized = normalize_match_title(right)
    if not left_normalized or not right_normalized:
        return 0.0
    common = longest_common_substring(left_normalized, right_normalized)
    if common < 2:
        return 0.0
    return common / max(len(left_normalized), len(right_normalized))


def longest_common_substring(left: str, right: str) -> int:
    if not left or not right:
        return 0
    lengths = [0] * (len(right) + 1)
    best = 0
    for left_char in left:
        previous = 0
        for index, right_char in enumerate(right, start=1):
            current = lengths[index]
            if left_char == right_char:
                lengths[index] = previous + 1
                best = max(best, lengths[index])
            else:
                lengths[index] = 0
            previous = current
    return best


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