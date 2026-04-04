"""
JSON 写入模块

将聚合后的文章列表写入 api/{YYYY}/{MM}/{DD}.json。
路径按写入时的 UTC 日期自动生成，目录不存在时自动创建。

写入策略（幂等）：
- 过滤发布时间超过 max_age_days 天的文章（默认 2 天），避免文件膨胀。
- 若文件已存在，先读取已有数据与新数据合并：按 URL 去重（新数据优先），
  按 date 降序排序后写入。重复运行不会丢失已有数据。
"""

import json
import logging
from datetime import datetime, timedelta, timezone
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


def _is_recent(article: dict, cutoff: datetime) -> bool:
    """判断文章发布时间是否晚于 cutoff。"""
    try:
        pub = datetime.fromisoformat(article["date"].replace("Z", "+00:00"))
        return pub >= cutoff
    except (KeyError, ValueError):
        return False


def write_articles(
    articles: list[dict],
    date: datetime | None = None,
    api_dir: Path = DEFAULT_API_DIR,
    max_age_days: int = 2,
) -> Path:
    """
    将文章列表合并写入 JSON 文件（幂等）。

    1. 过滤超过 max_age_days 天的文章。
    2. 与已存在文件中的数据合并，按 URL 去重（新数据优先），按 date 降序写入。

    Args:
        articles:     聚合后的文章列表
        date:         目标日期，默认为当前 UTC 时间
        api_dir:      api 根目录路径
        max_age_days: 保留的最大文章天数（默认 2）

    Returns:
        实际写入的文件路径
    """
    if date is None:
        date = datetime.now(tz=timezone.utc)

    cutoff = (date - timedelta(days=max_age_days)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    # 过滤超龄文章
    fresh = [a for a in articles if _is_recent(a, cutoff)]
    filtered_count = len(articles) - len(fresh)
    if filtered_count:
        logger.debug("过滤 %d 篇超过 %d 天的文章", filtered_count, max_age_days)

    output_path = resolve_output_path(date, api_dir)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 读取已有数据，合并去重（新数据优先覆盖同 URL 的旧数据）
    existing: list[dict] = []
    if output_path.exists():
        try:
            existing = json.loads(output_path.read_text(encoding="utf-8"))
        except Exception as exc:
            logger.warning("读取已有文件失败，将覆盖: %s", exc)

    seen: set[str] = set()
    merged: list[dict] = []
    for article in fresh + existing:
        url = article.get("url", "")
        if url and url not in seen:
            merged.append(article)
            seen.add(url)

    # 按日期降序排列
    merged.sort(key=lambda a: a.get("date", ""), reverse=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    logger.info("写入 %d 篇文章 -> %s", len(merged), output_path)
    return output_path
