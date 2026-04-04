---
title: 项目初始化执行计划
created: 2026-04-04T11:48:29
modified: 2026-04-04T11:48:29
description: 基于 design.md / architecture.md / tech-stack.md，描述从零到 MVP 的分步执行计划。
tags:
  - ai-notes
---

# 项目初始化执行计划

## Step 1: 初始化项目结构

创建项目骨架目录和文件：

- 创建 `src/`、`api/`、`config/` 目录（`config/rss.opml` 已存在）
- 初始化 `uv` 项目，生成 `pyproject.toml`，声明依赖（`httpx`、`feedparser`、`lxml` 等）
- 创建 `src/__init__.py` 及各模块占位文件：`crawler.py`、`opml.py`、`fetcher.py`、`writer.py`

---

## Step 2: 实现 OPML 读写模块（`src/opml.py`）

负责 `config/rss.opml` 的读取与写入：

- 解析现有 OPML，返回已收录 feed URL 列表
- 新增 feed URL 时去重并写回文件
- 单元测试覆盖读、写、去重逻辑

---

## Step 3: 实现爬虫模块（`src/crawler.py`）

从 v2ex/xna 发现新博客：

- 按数字累增（从当前最大索引 +1 开始）请求 `https://www.v2ex.com/xna/s/{n}`
- 若响应非 404，解析 HTML 页面提取 RSS/Atom feed 地址
- 调用 `opml.py` 将新 feed URL 写入 `config/rss.opml`
- 失败时打印日志并跳过，不中断整体流程
- 单元测试覆盖：正常收录、404 跳过、解析失败跳过

---

## Step 4: 实现 Feed 抓取与聚合模块（`src/fetcher.py`）

读取 OPML，拉取所有 feed 并聚合文章：

- 读取 `config/rss.opml`，获取所有 feed URL
- 并发（或顺序）fetch 每个 feed，提取文章的 `title`、`url`、`date`、`description`
- 按 `date` 降序聚合所有文章，返回列表
- 失败时打印日志并跳过
- 单元测试覆盖：正常抓取、单个 feed 失败不影响整体

---

## Step 5: 实现 JSON 写入模块（`src/writer.py`）

将聚合结果写入 `api/` 目录：

- 按当前日期生成路径 `api/{YYYY}/{MM}/{DD}.json`
- 自动创建不存在的目录层级
- 以 JSON 数组格式写入文章列表
- 单元测试覆盖：路径生成、文件写入、目录自动创建

---

## Step 6: 实现主入口（`src/main.py`）

串联完整流程：

```
crawler → opml update → fetcher → writer
```

- 接受命令行参数（可选：仅跑 crawl / 仅跑 fetch）
- 作为 GitHub Actions 的执行入口

---

## Step 7: 配置 GitHub Actions Workflow

在 `.github/workflows/` 创建 `pipeline.yml`：

- 触发条件：`cron: '0 */2 * * *'`（每 2 小时）
- 步骤：checkout → uv install → run `src/main.py` → commit & push `config/rss.opml` + `api/`

---

## Step 8: 端到端验证

手动触发一次完整流程，确认：

- `config/rss.opml` 有新增条目
- `api/{YYYY}/{MM}/{DD}.json` 文件生成且内容格式正确
- GitHub Actions 日志无异常中断
