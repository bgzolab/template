"""
OPML 读写模块

负责读取和维护 config/rss.opml 文件，管理博客订阅地址列表。
所有操作保证幂等性：重复添加同一 URL 不会产生重复条目。

每条 outline 属性说明：
  title   : "[#N] 博客标题"，N 为 v2ex/xna 序号，便于追踪已爬编号
  xmlUrl  : RSS/Atom feed 地址
  htmlUrl : v2ex/xna 来源页面地址（如 https://www.v2ex.com/xna/s/1）
"""

import re
from pathlib import Path
from xml.etree import ElementTree as ET


# OPML 文件的默认路径（相对于项目根目录）
DEFAULT_OPML_PATH = Path(__file__).parent.parent / "config" / "rss.opml"

# 从 htmlUrl 提取 xna 序号的正则
_XNA_INDEX_RE = re.compile(r"/xna/s/(\d+)$")


def read_feeds(opml_path: Path = DEFAULT_OPML_PATH) -> list[str]:
    """
    读取 OPML 文件，返回所有 feed URL 列表。

    Args:
        opml_path: OPML 文件路径

    Returns:
        feed URL 字符串列表，去重后按原始顺序排列
    """
    if not opml_path.exists():
        return []

    tree = ET.parse(opml_path)
    root = tree.getroot()

    urls = []
    seen = set()
    for outline in root.iter("outline"):
        url = outline.get("xmlUrl")
        if url and url not in seen:
            urls.append(url)
            seen.add(url)

    return urls


def get_max_xna_index(opml_path: Path = DEFAULT_OPML_PATH) -> int:
    """
    从 OPML 中解析所有条目的 htmlUrl，提取 v2ex/xna 序号，返回最大值。
    用于增量爬取时确定下次起始序号。

    Returns:
        已知最大 xna 序号，若无任何已记录序号则返回 0
    """
    if not opml_path.exists():
        return 0

    tree = ET.parse(opml_path)
    root = tree.getroot()

    max_index = 0
    for outline in root.iter("outline"):
        html_url = outline.get("htmlUrl", "")
        m = _XNA_INDEX_RE.search(html_url)
        if m:
            max_index = max(max_index, int(m.group(1)))

    return max_index


def add_feed(
    url: str,
    title: str = "",
    opml_path: Path = DEFAULT_OPML_PATH,
    xna_index: int | None = None,
    xna_url: str = "",
) -> bool:
    """
    向 OPML 文件中新增一个 feed URL。

    若 URL 已存在但缺少 htmlUrl 元数据（历史遗留条目），
    且本次提供了 xna_index，则补充更新元数据后返回 False。

    Args:
        url:       feed 的 RSS/Atom 地址
        title:     博客标题
        opml_path: OPML 文件路径
        xna_index: v2ex/xna 序号，写入 title 前缀 "[#N]" 及 htmlUrl
        xna_url:   v2ex/xna 来源页面地址

    Returns:
        True 表示新增成功，False 表示 URL 已存在（已跳过或补充元数据）
    """
    tree = ET.parse(opml_path)
    root = tree.getroot()

    # 构造带序号前缀的标题
    display_title = f"[#{xna_index}] {title}" if xna_index else (title or url)

    # 检查是否已存在该 xmlUrl
    for outline in root.iter("outline"):
        if outline.get("xmlUrl") == url:
            # 若已存在但缺少 htmlUrl，补充元数据
            if xna_index and not outline.get("htmlUrl"):
                outline.set("htmlUrl", xna_url)
                outline.set("title", display_title)
                outline.set("text", display_title)
                ET.indent(tree, space="    ")
                tree.write(opml_path, encoding="UTF-8", xml_declaration=True)
            return False

    # 新增
    body = root.find("body")
    if body is None:
        body = ET.SubElement(root, "body")

    container = body.find("outline")
    if container is None:
        container = ET.SubElement(body, "outline", {"title": "VXNA", "text": "VXNA"})

    attrs: dict[str, str] = {
        "title": display_title,
        "text": display_title,
        "xmlUrl": url,
    }
    if xna_url:
        attrs["htmlUrl"] = xna_url

    ET.SubElement(container, "outline", attrs)

    ET.indent(tree, space="    ")
    tree.write(opml_path, encoding="UTF-8", xml_declaration=True)
    return True
