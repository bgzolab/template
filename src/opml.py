"""
OPML 读写模块

负责读取和维护 config/rss.opml 文件，管理博客订阅地址列表。
所有操作保证幂等性：重复添加同一 URL 不会产生重复条目。
"""

from pathlib import Path
from xml.etree import ElementTree as ET


# OPML 文件的默认路径（相对于项目根目录）
DEFAULT_OPML_PATH = Path(__file__).parent.parent / "config" / "rss.opml"


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


def add_feed(url: str, title: str = "", opml_path: Path = DEFAULT_OPML_PATH) -> bool:
    """
    向 OPML 文件中新增一个 feed URL。若 URL 已存在则跳过。

    Args:
        url:       feed 的 RSS/Atom 地址
        title:     博客标题（可选，用于 OPML outline 的 title 属性）
        opml_path: OPML 文件路径

    Returns:
        True 表示新增成功，False 表示 URL 已存在（跳过）
    """
    existing = read_feeds(opml_path)
    if url in existing:
        return False

    tree = ET.parse(opml_path)
    root = tree.getroot()

    # 找到 body 下第一个 outline 容器，若不存在则创建
    body = root.find("body")
    if body is None:
        body = ET.SubElement(root, "body")

    container = body.find("outline")
    if container is None:
        container = ET.SubElement(body, "outline", {"title": "VXNA", "text": "VXNA"})

    ET.SubElement(container, "outline", {
        "title": title or url,
        "text": title or url,
        "xmlUrl": url,
    })

    # 保持文件可读性：写入时带 xml 声明
    ET.indent(tree, space="    ")
    tree.write(opml_path, encoding="UTF-8", xml_declaration=True)
    return True
