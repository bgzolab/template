"""
爬虫模块

从 https://www.v2ex.com/xna/s/{n} 按数字累增发现新博客，
提取每个博客页面的 RSS/Atom feed 地址，并写入 config/rss.opml。

发现规则：
- 若响应状态码为 404，跳过（该序号未被收录）。
- 否则解析 HTML，提取表格中 "Feed 地址" 行的链接。
- 失败时打印日志并跳过，不中断整体流程。

增量爬取策略：
- 首次运行（--start-index 1）：从序号 1 开始全量扫描。
- 增量运行（GitHub Actions 默认）：从 OPML 中已记录的最大序号 +1 开始，
  连续遇到 max_consecutive_404 个 404 后停止。
"""

import logging
from pathlib import Path

import httpx
from lxml import html

from src.opml import DEFAULT_OPML_PATH, add_feed, get_max_xna_index

logger = logging.getLogger(__name__)

# v2ex xna 博客详情页 URL 模板
XNA_BLOG_URL = "https://www.v2ex.com/xna/s/{index}"


def extract_feed_url(page_html: str, base_url: str = "") -> str | None:
    """
    从 v2ex/xna 博客详情页提取 RSS/Atom feed 地址。

    v2ex 页面结构示例：
        <td align="right">Feed 地址</td>
        <td align="left"><a href="https://example.com/feed.xml">...</a></td>

    Args:
        page_html: HTML 字符串
        base_url:  页面原始 URL（保留扩展，暂未使用）

    Returns:
        feed URL 字符串，未找到时返回 None
    """
    try:
        doc = html.fromstring(page_html)
        # 找到文本为 "Feed 地址" 的 <td>，取其后一个兄弟 <td> 中的 <a href>
        feed_tds = doc.xpath('//td[normalize-space(text())="Feed 地址"]')
        for td in feed_tds:
            siblings = td.xpath('following-sibling::td[1]//a/@href')
            if siblings:
                return siblings[0]
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


def crawl_new_blogs(
    start_index: int | None = None,
    max_consecutive_404: int = 5,
    opml_path: Path = DEFAULT_OPML_PATH,
    client: httpx.Client | None = None,
) -> list[str]:
    """
    顺序爬取 v2ex/xna，发现新博客并写入 OPML。

    - start_index=None（默认）：自动从 OPML 最大已知序号 +1 开始（增量模式）。
    - start_index=1：从头全量扫描（首次运行时使用）。
    - 连续遇到 max_consecutive_404 个 404 后停止。

    每条新增记录包含：
      title   : "[#N] 博客标题"
      htmlUrl : https://www.v2ex.com/xna/s/N（来源页面）
      xmlUrl  : feed 地址

    Args:
        start_index:           起始爬取序号，None 表示自动检测
        max_consecutive_404:   连续 404 上限，超过即停止
        opml_path:             OPML 文件路径
        client:                可注入的 httpx.Client（用于测试 mock）

    Returns:
        本次新增的 feed URL 列表
    """
    if start_index is None:
        start_index = get_max_xna_index(opml_path) + 1
        logger.info("增量模式：从序号 %d 开始爬取", start_index)
    else:
        logger.info("指定起始序号：从 %d 开始爬取", start_index)

    added: list[str] = []
    consecutive_404 = 0
    index = start_index

    _owns_client = client is None
    if _owns_client:
        client = httpx.Client(timeout=15, follow_redirects=True)

    try:
        while consecutive_404 < max_consecutive_404:
            xna_url = XNA_BLOG_URL.format(index=index)
            try:
                resp = client.get(xna_url)
            except Exception as exc:
                logger.warning("请求 %s 失败，跳过: %s", xna_url, exc)
                index += 1
                consecutive_404 += 1
                continue

            if resp.status_code == 404:
                consecutive_404 += 1
                logger.debug("404 跳过: %s (连续 %d)", xna_url, consecutive_404)
                index += 1
                continue

            # 重置连续 404 计数
            consecutive_404 = 0

            feed_url = extract_feed_url(resp.text, base_url=str(resp.url))
            if not feed_url:
                logger.info("未找到 feed 地址，跳过: %s", xna_url)
                index += 1
                continue

            title = extract_blog_title(resp.text)
            was_added = add_feed(
                feed_url, title, opml_path,
                xna_index=index, xna_url=xna_url,
            )
            if was_added:
                logger.info("新增博客 [#%d] %s -> %s", index, title, feed_url)
                added.append(feed_url)
            else:
                logger.debug("已存在（含元数据更新）: [#%d] %s", index, feed_url)

            index += 1
    finally:
        if _owns_client:
            client.close()

    return added
