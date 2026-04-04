"""
主入口

串联完整数据流：
    1. crawler  — 发现新博客，更新 config/rss.opml
    2. fetcher  — 读取 OPML，抓取所有 feed，聚合文章
    3. writer   — 将聚合结果写入 api/{YYYY}/{MM}/{DD}.json

用法：
    uv run python -m src.main            # 运行完整流程
    uv run python -m src.main --crawl    # 仅运行爬虫（更新 OPML）
    uv run python -m src.main --fetch    # 仅运行抓取+写入
"""

import argparse
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout,
)

logger = logging.getLogger(__name__)


def run_crawl(start_index: int | None = None) -> None:
    """发现新博客，更新 config/rss.opml。start_index=None 表示增量模式。"""
    from src.crawler import crawl_new_blogs

    logger.info("开始爬取 v2ex/xna，起始序号: %s", start_index if start_index else "自动检测")
    added = crawl_new_blogs(start_index=start_index)
    logger.info("爬取完成，本次新增 %d 个 feed", len(added))


def run_fetch() -> None:
    """抓取所有 feed，聚合文章，写入 api/ JSON 文件。"""
    from src.fetcher import fetch_all_feeds
    from src.writer import write_articles

    logger.info("开始抓取 feeds")
    articles = fetch_all_feeds()
    logger.info("共聚合 %d 篇文章", len(articles))

    out_path = write_articles(articles)
    logger.info("写入完成: %s", out_path)


def run_update_readme() -> None:
    """读取近 7 天文章，更新 README.md 的 Last Week Blog 章节。"""
    from src.readme_updater import run as update_readme

    logger.info("更新 README.md Last Week Blog 章节")
    update_readme()


def main() -> None:
    parser = argparse.ArgumentParser(description="VXNA pipeline")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--crawl", action="store_true", help="仅运行爬虫，更新 OPML")
    group.add_argument("--fetch", action="store_true", help="仅运行 feed 抓取和写入")
    group.add_argument("--readme", action="store_true", help="仅更新 README.md Last Week Blog")
    parser.add_argument(
        "--start-index",
        type=int,
        default=None,
        help="爬虫起始序号（默认: 自动从 OPML 最大序号+1 开始）",
    )
    args = parser.parse_args()

    if args.crawl:
        run_crawl(start_index=args.start_index)
    elif args.fetch:
        run_fetch()
    elif args.readme:
        run_update_readme()
    else:
        # 默认：完整流程
        run_crawl(start_index=args.start_index)
        run_fetch()
        run_update_readme()


if __name__ == "__main__":
    main()
