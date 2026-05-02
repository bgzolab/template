---
title: Venera Bangumi Sync Scripts
created: YYYY-MM-DDTHH:MM:SS
modified: YYYY-MM-DDTHH:MM:SS
description: 实现从 20575-2273.venera 到 Bangumi 的同步脚本，包含数据提取和进度同步功能。
tags: 
  - ai-notes
---

实现从 20575-2273.venera 到 Bangumi 的同步脚本，包含以下功能：

1. 数据提取
2. Bangumi 的进度同步

## 数据提取

从 20575-2273.venera 中提取用户的观看历史、评分、收藏等数据。需要解析 venera 的数据结构，提取输出 JSON 结构；

## Bangumi 的进度同步

将提取的数据同步到 Bangumi，更新用户的观看进度、评分和收藏状态。需要使用 Bangumi 的 API 来实现数据的更新。

API 支持：https://bangumi.github.io/api/

