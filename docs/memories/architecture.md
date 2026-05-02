---
title: 项目架构
created: 2026-05-02T00:00:00
modified: 2026-05-02T00:00:00
description: 记录 venera-parser-bangumi 当前仓库结构、数据流和关键文件职责，作为后续实现 Bangumi 同步功能的上下文基线。
tags: 
  - ai-notes
---

## 项目定位

该仓库当前是一个单脚本工具项目，用于解析 Venera 导出的 `.venera` 数据包，并为后续同步到 Bangumi 做数据准备。

当前已实现的能力：

1. 读取 `.venera` zip 包。
2. 解析 `appdata.json`。
3. 解析 `history.db`、`local_favorite.db`，可选解析 `cookie.db`。
4. 以摘要或 JSON dump 的方式输出解析结果。

当前未实现但已进入设计范围的能力：

1. 从 `local_favorite.db` 指定文件夹表读取待同步条目。
2. 使用 Bangumi API 搜索条目并同步收藏状态。
3. 对模糊匹配、已存在收藏和失败请求产出可审计结果。

## 目录结构

```text
.
├── 20575-2273.venera
├── LICENCE
├── README.md
├── docs/
│   ├── implementation-plans/
│   │   └── 20260502-sync-bangumi.md
│   └── memories/
│       ├── architecture.md
│       ├── design.md
│       └── tech-stack.md
├── src/
│   └── parser.py
└── venera_dump.json
```

## 文件职责

### `src/parser.py`

当前唯一的程序入口，负责：

1. CLI 参数解析。
2. 打开 `.venera` 归档。
3. 读取 zip 成员清单。
4. 解析 `appdata.json`。
5. 将 sqlite 数据库解压到临时目录并读取 schema、列信息、行数，以及可选完整行数据。

当前 CLI 子命令：

1. `summary`：打印可读摘要。
2. `dump`：导出完整 JSON。

### `20575-2273.venera`

样本输入数据，已确认与 Venera 上游导出逻辑一致。它本质上是 zip 归档，至少包含以下成员：

1. `appdata.json`
2. `history.db`
3. `local_favorite.db`
4. `cookie.db`
5. `comic_source/` 下的脚本和 `.data` 文件

### `venera_dump.json`

样本 `.venera` 经过 `dump --include-rows --pretty` 后得到的参考输出，可用于：

1. 观察当前解析结构。
2. 编写过滤和映射逻辑。
3. 为同步计划补充字段依据。

### `docs/memories/*.md`

长期维护的项目记忆，记录架构、设计决策和技术栈事实，避免后续实现偏离现状。

### `docs/implementation-plans/*.md`

阶段性实施计划，要求每一步都可验收，并且只在通过该步验收后进入下一步。

## 数据结构基线

### `.venera` 包格式

Venera 导出文件是 zip 归档，不是自定义二进制协议。当前解析器直接使用 `zipfile` 读取。

### `history.db`

已确认包含以下表：

1. `history`
2. `image_favorites`

这部分当前仅用于解析展示，不在本阶段 Bangumi 同步范围内。

### `local_favorite.db`

已确认包含以下固定表：

1. `folder_order`
2. `folder_sync`

以及若干动态收藏夹表，例如样本里的：

1. `Doing`
2. `DONE`

动态收藏夹表列是 Bangumi 同步的核心来源，样本已确认包含以下列：

1. `id`
2. `name`
3. `author`
4. `type`
5. `tags`
6. `cover_path`
7. `time`
8. `display_order`
9. `translated_tags`
10. `last_update_time`
11. `has_new_update`
12. `last_check_time`

不同动态表列可能略有差异，后续实现需按表级 schema 做兼容读取，而不是硬编码要求所有列都存在。

## 当前调用关系

当前主数据流如下：

1. CLI 解析子命令和通用参数。
2. `parse_archive()` 打开归档并调度成员解析。
3. `parse_appdata()` 处理 JSON 设置摘要。
4. `parse_databases()` 将数据库临时落盘。
5. `parse_sqlite_database()` 读取 schema、列、行数和可选行数据。
6. `print_summary()` 或 `dump_json()` 输出结果。

后续 Bangumi 同步功能应沿着现有 CLI 入口扩展，不应绕过当前解析层直接操作原始 zip 内容。

