"""
爬虫模块

从 https://www.v2ex.com/xna/s/{n} 按数字累增发现新博客，
提取每个博客页面的 RSS/Atom feed 地址，并写入 config/rss.opml。

发现规则：
- 若响应状态码为 404，跳过（该序号未被收录）。
- 否则解析 HTML，提取 <link rel="alternate" type="application/..."> 标签。
- 失败时打印日志并跳过，不中断整体流程。
"""

import logging
from pathlib import Path

import httpx
from lxml import html

from src.opml import DEFAULT_OPML_PATH, add_feed, read_feeds

logger = logging.getLogger(__name__)

# v2ex xna 博客详情页 URL 模板
XNA_BLOG_URL = "https://www.v2ex.com/xna/s/{index}"

# 支持的 feed MIME 类型
FEED_MIME_TYPES = {
    "application/rss+xml",
    "application/atom+xml",
    "application/feed+json",
}


def extract_feed_url(page_html: str, base_url: str = "") -> str | None:
    """
    从 HTML 页面中提取 RSS/Atom feed 地址。

    Args:
        page_html: HTML 字符串
        base_url:  页面的原始 URL，用于处理相对路径（暂未使用，保留扩展）

    Returns:
        feed URL 字符串，未找到时返回 None
    """
    try:
        doc = html.fromstring(page_html)
        for mime in FEED_MIME_TYPES:
            links = doc.xpath(f'//link[@rel="alternate"][@type="{mime}"]/@href')
            if links:
                return links[0]
    except Exception as exc:
        logger.warning("解析 HTML 提取 feed URL 失败: %s", exc)
    return None


def extract_blog_title(page_html: str) -> str:
    """
    从 HTML 页面中提取博客标题（<title> 标签）。

    Returns:
        标题字符串，解析失败时返回空字符串
    """
    try:
        doc = html.fromstring(page_html)
        titles = doc.xpath("//title/text()")
        if titles:
            return titles[0].strip()
    except Exception as exc:
        logger.warning("解析博客标题失败: %s", exc)
    return ""


def get_current_max_index(opml_path: Path = DEFAULT_OPML_PATH) -> int:
    """
    从现有 OPML 推断当前已知最大 XNA 索引。
    由于 OPML 中只存储 feed URL 而非 XNA 索引，暂时返回固定起始值。

    实际增量发现逻辑：每次从上次停止的索引继续，
    连续遇到 MAX_CONSECUTIVE_404 个 404 后停止。

    Returns:
        起始爬取序号（从 1 开始，调用方自行管理）
    """
    _ = read_feeds(opml_path)  # 预留：未来可记录最大已知索引
    return 1


def crawl_new_blogs(
    start_index: int,
    max_consecutive_404: int = 5,
    opml_path: Path = DEFAULT_OPML_PATH,
    client: httpx.Client | None = None,
) -> list[str]:
    """
    从 start_index 开始顺序爬取 v2ex/xna，发现新博客并写入 OPML。

    连续遇到 max_consecutive_404 个 404 后停止，避免无限扫描。

    Args:
        start_index:           起始爬取序号
        max_consecutive_404:   连续 404 上限，超过即停止
        opml_path:             OPML 文件路径
        client:                可注入的 httpx.Client（用于测试 mock）

    Returns:
        本次新增的 feed URL 列表
    """
    added: list[str] = []
    consecutive_404 = 0
    index = start_index

    # 支持外部注入 client，方便测试；否则新建
    _owns_client = client is None
    if _owns_client:
        client = httpx.Client(timeout=15, follow_redirects=True)

    try:
        while consecutive_404 < max_consecutive_404:
            url = XNA_BLOG_URL.format(index=index)
            try:
                resp = client.get(url)
            except Exception as exc:
                logger.warning("请求 %s 失败，跳过: %s", url, exc)
                index += 1
                consecutive_404 += 1
                continue

            if resp.status_code == 404:
                consecutive_404 += 1
                logger.debug("404 跳过: %s (连续 %d)", url, consecutive_404)
                index += 1
                continue

            # 重置连续 404 计数
            consecutive_404 = 0

            feed_url = extract_feed_url(resp.text, base_url=str(resp.url))
            if not feed_url:
                logger.info("未找到 feed 地址，跳过: %s", url)
                index += 1
                continue

            title = extract_blog_title(resp.text)
            was_added = add_feed(feed_url, title, opml_path)
            if was_added:
                logger.info("新增博客 [%d] %s -> %s", index, title, feed_url)
                added.append(feed_url)
            else:
                logger.debug("已存在，跳过: %s", feed_url)

            index += 1
    finally:
        if _owns_client:
            client.close()

    return added
