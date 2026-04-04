"""
README 更新模块

读取最近 7 天的 api/{YYYY}/{MM}/{DD}.json 文章数据，
将其格式化后写入 README.md 的 `## Last Week Blog` 章节。

更新规则：
- 章节内容在 `## Last Week Blog` 和下一个 `##` 标题之间。
- 每次全量替换该区间内容。
- 文章按 date 降序排列，格式为 Markdown 无序列表。
"""

import json
import logging
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

logger = logging.getLogger(__name__)

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

DEFAULT_API_DIR = PROJECT_ROOT / "api"
DEFAULT_README = PROJECT_ROOT / "README.md"

# 章节标题（精确匹配）
SECTION_HEADING = "## Last Week Blog"


def load_recent_articles(
    days: int = 7,
    api_dir: Path = DEFAULT_API_DIR,
    reference_date: datetime | None = None,
) -> list[dict]:
    """
    读取最近 N 天的 JSON 文件，过滤出发布时间在最近 N 天内的文章，
    去重后按 date 降序返回。

    注意：过滤依据是文章自身的 `date` 字段，而非 JSON 文件的日期。
    JSON 文件中可能包含博客的历史文章，需要剔除。

    Args:
        days:           往前追溯的天数，默认 7
        api_dir:        api 根目录
        reference_date: 基准日期，默认 UTC 今天

    Returns:
        Article 列表
    """
    if reference_date is None:
        reference_date = datetime.now(tz=timezone.utc)

    # 计算时间窗口下界（N 天前的 00:00:00 UTC）
    cutoff = (reference_date - timedelta(days=days)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    articles: list[dict] = []
    seen_urls: set[str] = set()

    for offset in range(days):
        target = reference_date - timedelta(days=offset)
        path = api_dir / target.strftime("%Y") / target.strftime("%m") / f"{target.strftime('%d')}.json"
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            for item in data:
                url = item.get("url", "")
                if not url or url in seen_urls:
                    continue
                # 按文章自身发布时间过滤
                date_str = item.get("date", "")
                try:
                    pub_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                except (ValueError, AttributeError):
                    continue
                if pub_date < cutoff:
                    continue
                articles.append(item)
                seen_urls.add(url)
        except Exception as exc:
            logger.warning("读取 %s 失败，跳过: %s", path, exc)

    articles.sort(key=lambda a: a.get("date", ""), reverse=True)
    return articles


def _truncate(text: str, max_len: int = 150) -> str:
    """截断文本到 max_len 字符，超出则加省略号。"""
    text = text.strip()
    if len(text) <= max_len:
        return text
    return text[:max_len].rstrip() + "…"


def format_articles_markdown(articles: list[dict]) -> str:
    """
    将文章列表格式化为 Markdown 表格（按 date 降序）。

    列：日期 | 标题 | 摘要（最多 150 字）

    Returns:
        Markdown 字符串（不含前后空行）
    """
    if not articles:
        return "_No articles in the last 7 days._"

    lines = [
        "| Date | Title | Summary |",
        "| --- | --- | --- |",
    ]
    for article in articles:
        title = article.get("title", "Untitled").strip()
        url = article.get("url", "").strip()
        date_str = article.get("date", "")[:10]
        summary = _truncate(article.get("description", ""), 150)
        # 管道符在表格中需转义
        title_cell = f"[{title.replace('|', '&#124;')}]({url})"
        summary_cell = summary.replace("|", "&#124;").replace("\n", " ")
        lines.append(f"| {date_str} | {title_cell} | {summary_cell} |")

    return "\n".join(lines)


def update_readme(
    articles: list[dict],
    readme_path: Path = DEFAULT_README,
) -> None:
    """
    将 articles 写入 README.md 的 `## Last Week Blog` 章节。

    找到该章节与下一个 `##` 标题之间的区域，全量替换。

    Args:
        articles:    文章列表
        readme_path: README.md 文件路径
    """
    content = readme_path.read_text(encoding="utf-8")
    new_section_body = format_articles_markdown(articles)

    # 匹配 "## Last Week Blog\n" 之后、下一个 "##" 或文件尾之间的内容
    pattern = re.compile(
        r"(## Last Week Blog\n)(.*?)(\n##|\Z)",
        re.DOTALL,
    )

    def replacer(m: re.Match) -> str:
        tail = m.group(3)  # 下一个 ## 或文件尾
        return f"{m.group(1)}\n{new_section_body}\n{tail}"

    new_content, count = pattern.subn(replacer, content)
    if count == 0:
        logger.warning("README.md 中未找到 '%s' 章节，跳过更新", SECTION_HEADING)
        return

    readme_path.write_text(new_content, encoding="utf-8")
    logger.info("README.md 更新完成，写入 %d 篇文章", len(articles))


def run(
    days: int = 7,
    api_dir: Path = DEFAULT_API_DIR,
    readme_path: Path = DEFAULT_README,
    reference_date: datetime | None = None,
) -> None:
    """
    一键执行：读取最近 N 天文章，更新 README.md。
    """
    articles = load_recent_articles(days=days, api_dir=api_dir, reference_date=reference_date)
    logger.info("共读取到 %d 篇近期文章", len(articles))
    update_readme(articles, readme_path=readme_path)
