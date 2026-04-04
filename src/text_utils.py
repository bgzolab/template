"""
文本清理工具

提供 clean_description()，对 RSS/Atom feed 的富文本描述做标准化处理：
  1. 去除 base64 内联图片（<img src="data:...">），防止超长数据污染 JSON
  2. 解码 HTML 实体（&amp; → &，&lt; → <，等）
  3. 去除所有 HTML 标签
  4. 去除 Markdown 加粗/斜体标记（**text**、*text*、__text__、_text_）
  5. 规范化空白：换行、制表符、连续空格 → 单个空格
"""

import html as _html
import re

# 匹配带 base64 数据的 <img> 标签（可能跨行，data URI 极长）
_BASE64_IMG_RE = re.compile(
    r'<img[^>]*\ssrc=["\']data:[^"\']*;base64,[^"\']*["\'][^>]*>',
    re.IGNORECASE | re.DOTALL,
)

# 匹配所有 HTML 标签
_HTML_TAG_RE = re.compile(r"<[^>]+>", re.DOTALL)

# Markdown 加粗/斜体（非贪婪，避免跨段误匹配）
_MD_BOLD_ITALIC_RE = re.compile(r"\*{1,3}(.*?)\*{1,3}", re.DOTALL)
_MD_UNDER_RE = re.compile(r"_{1,3}(.*?)_{1,3}", re.DOTALL)


def clean_description(text: str) -> str:
    """
    清理 RSS description/summary 的富文本，返回纯文本摘要。

    Args:
        text: 原始富文本（可含 HTML、Markdown、base64 图片）

    Returns:
        清理后的单行纯文本，首尾无空格
    """
    if not text:
        return ""
    # 1. 去掉 base64 图片（优先，避免巨型字符串进入后续处理）
    text = _BASE64_IMG_RE.sub(" ", text)
    # 2. HTML 实体解码
    text = _html.unescape(text)
    # 3. 去掉所有 HTML 标签
    text = _HTML_TAG_RE.sub(" ", text)
    # 4. 去掉 Markdown 粗/斜体标记
    text = _MD_BOLD_ITALIC_RE.sub(r"\1", text)
    text = _MD_UNDER_RE.sub(r"\1", text)
    # 5. 规范化空白
    text = re.sub(r"\s+", " ", text)
    return text.strip()
