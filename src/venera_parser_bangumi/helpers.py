from __future__ import annotations

import base64
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
    candidates = [raw]
    simplified = to_simplified(raw)
    traditional = to_traditional(raw)
    candidates.extend([simplified, traditional])

    normalized = normalize_search_text(raw)
    candidates.append(normalized)
    candidates.append(normalize_search_text(simplified))
    candidates.append(normalize_search_text(traditional))

    for text in (raw, simplified, traditional, normalized):
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