"""
JSON 写入模块

将聚合后的文章列表写入 api/{YYYY}/{MM}/{DD}.json。
路径按写入时的 UTC 日期自动生成，目录不存在时自动创建。
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)

# api 目录的默认路径（相对于项目根目录）
DEFAULT_API_DIR = Path(__file__).parent.parent / "api"


def resolve_output_path(date: datetime, api_dir: Path = DEFAULT_API_DIR) -> Path:
    """
    根据给定日期计算输出文件路径。

    Args:
        date:    目标日期（建议使用 UTC）
        api_dir: api 根目录路径

    Returns:
        形如 api/2026/04/04.json 的 Path 对象
    """
    return api_dir / date.strftime("%Y") / date.strftime("%m") / f"{date.strftime('%d')}.json"


def write_articles(
    articles: list[dict],
    date: datetime | None = None,
    api_dir: Path = DEFAULT_API_DIR,
) -> Path:
    """
    将文章列表写入 JSON 文件。

    若当天文件已存在，直接覆盖（每次 workflow 运行都是全量写入）。

    Args:
        articles: 聚合后的文章列表
        date:     目标日期，默认为当前 UTC 时间
        api_dir:  api 根目录路径

    Returns:
        实际写入的文件路径
    """
    if date is None:
        date = datetime.now(tz=timezone.utc)

    output_path = resolve_output_path(date, api_dir)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    logger.info("写入 %d 篇文章 -> %s", len(articles), output_path)
    return output_path
