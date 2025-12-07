#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : bGZo
@Date : 2025-12-06
@Links : https://github.com/bGZo
"""

READ_LATER = "https://www.qireader.com/api/streams/"
"""
target-url: https://www.qireader.com/api/streams/{tagId}?articleOrder=0&count=25&id={tagId}&unreadOnly=false&olderThan=1764313764608411573

:param id
:param olderThan
------------------------------------------------------------------------------
{
  "result": {
    "id": "tag-xxx",
    "entries": [
      {
        "id": "GWplALGn3z4Vebvn",
        "isSaved": true,
        "sourceEntryId": "GWplALGn3z4Vebvn",
        "origin": {
          "feedId": "0rmREjBzpAQJdNnD"
        },
        "title": "具透 | 当一个视频下载脚本被迫变成半个浏览器；Android 侧载保住了一半",
        "summary": "yt-dlp开始依赖外部JavaScript运行时@PlatyHsu：yt-dlp是开源社区非常有名的视频下载工具，也是youtube-dl停止更新之后，少数保持活跃和可用的选项。除了在终端直接使用外 ...查看全文本文为会员文章，出自《单篇文章》，订阅后可阅读全文。",
        "url": "https://sspai.com/prime/story/inside-release-notes-251119",
        "publishedAt": 1763545494000,
        "crawledAt": 1763549787159,
        "timestamp": "1763974116059279295",
        "attachments": [],
        "tagIds": [
          "xxx"
        ]
      }
    ],
    "hasMore": true
  }
}
"""

FULL_TEXT = "https://nettools3.oxyry.com/text"
