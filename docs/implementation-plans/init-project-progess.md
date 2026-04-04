---
title: 项目初始化执行进度
created: 2026-04-04T11:54:10
modified: 2026-04-04T19:59:04
description: 记录 init-project.md 计划的逐步执行进度与验证结果。
tags:
  - ai-notes
---

# 执行进度

关联计划：[init-project.md](./init-project.md)

## Step 1: 初始化项目结构 — DONE

- 执行 `uv init` 生成 `pyproject.toml`
- 添加运行时依赖：`httpx`、`feedparser`、`lxml`
- 添加开发依赖：`pytest`、`pytest-cov`
- 创建 `src/__init__.py`、`tests/__init__.py`
- 验证：`uv sync` 成功，依赖全部锁定

## Step 2: 实现 `src/opml.py` — DONE

- `read_feeds(opml_path)` — 读取所有 xmlUrl，去重返回列表
- `add_feed(url, title, opml_path)` — 新增 feed，已存在时幂等跳过
- 测试：`tests/test_opml.py` 7/7 通过

## Step 3: 实现 `src/crawler.py` — DONE

- `extract_feed_url(html)` — 从 HTML 中提取 RSS/Atom link 标签
- `extract_blog_title(html)` — 提取页面 title
- `crawl_new_blogs(start_index, max_consecutive_404, ...)` — 按数字累增爬取 v2ex/xna；连续 404 超过阈值自动停止；失败打印日志跳过
- 支持注入 `httpx.Client` 以便测试 mock
- 测试：`tests/test_crawler.py` 10/10 通过

## Step 4: 实现 `src/fetcher.py` — DONE

- `fetch_feed(url, client)` — 抓取单个 feed，解析为 Article 列表
- `fetch_all_feeds(opml_path, client)` — 读取 OPML，聚合所有文章，按 date 降序排列
- Article 结构：`{title, url, date, description}`
- 失败时打印日志跳过，不影响其他 feed
- 测试：`tests/test_fetcher.py` 9/9 通过

## Step 5: 实现 `src/writer.py` — DONE

- `resolve_output_path(date, api_dir)` — 生成 `api/{YYYY}/{MM}/{DD}.json` 路径
- `write_articles(articles, date, api_dir)` — 写入 JSON，自动创建目录，覆盖已有文件
- 测试：`tests/test_writer.py` 8/8 通过

## Step 6: 实现 `src/main.py` — DONE

- 支持 `--crawl`（仅更新 OPML）、`--fetch`（仅抓取写入）、无参数（完整流程）
- `--start-index` 参数控制爬虫起始序号
- 验证：`uv run python -m src.main --help` 输出正常

## Step 7: GitHub Actions Workflow — DONE

- 新建 `.github/workflows/pipeline.yml`
- 每 2 小时触发（`cron: '0 */2 * * *'`），支持 `workflow_dispatch` 手动触发
- 步骤：checkout → uv install → run pipeline → git commit & push

## Step 8: 端到端验证 — DONE

- 全量测试：**34/34 通过**
- 冒烟测试（`--fetch`）：成功抓取真实 feed，聚合 50 篇文章，写入 `api/2026/04/04.json`

---

## 最终文件结构

```
src/
  __init__.py
  opml.py       # OPML 读写
  crawler.py    # v2ex/xna 爬虫
  fetcher.py    # feed 抓取与聚合
  writer.py     # JSON 写入
  main.py       # 流程入口
tests/
  __init__.py
  test_opml.py
  test_crawler.py
  test_fetcher.py
  test_writer.py
.github/workflows/pipeline.yml
api/2026/04/04.json   # 首次冒烟测试产出
pyproject.toml
uv.lock
```
