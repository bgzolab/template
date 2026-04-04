---
title: 项目架构
created: 2026-04-04
modified: 2026-04-04T08:28:43
description: 架构需要对项目的整体结构进行说明，明确每个文件夹和文件的作用，以及它们之间的关系。需要列出每个文件的作用，以及它们之间的调用关系。如果有数据库，包含完整数据库结构。
tags: 
  - ai-notes
---

## Tree 目录结构

```shell
$ tree . -L 3 
.
├── .github
│   ├── agents                    # 智能体，copilot 左下角可选择
│   ├── copilot-instructions.md   # 项目全局生效
│   ├── instructions              # 项目默认加载指令
│   ├── ISSUE_TEMPLATE            # 项目 issue 模板
│   ├── prompts                   # 使用 slash 调用的预制提示词
│   └── workflows                 # GitHub CI/CD（每 2h 触发一次完整流程）
├── api                           # 存储模块：输出的 JSON 文章聚合数据
│   └── {YYYY}/{MM}/{DD}.json     # 按日期分层，每文件聚合当日所有文章
├── config                        # 配置模块：存储程序自动维护的 OPML 文件
│   └── rss.opml                  # 所有已收录博客的 RSS/Atom 订阅地址列表
├── src                           # 代码逻辑模块
│   ├── crawler.py                # 爬取 v2ex/xna，发现新博客，提取 feed URL
│   ├── opml.py                   # 读写 config/rss.opml
│   ├── fetcher.py                # 读取 OPML，fetch 所有 feed，聚合文章
│   └── writer.py                 # 将聚合结果写入 api/{YYYY}/{MM}/{DD}.json
├── docs
│   ├── implementation-plans      # 实施计划，每次 Bug 修复 / 新功能全部记录
│   └── memories                  # LLM 必须加载的上下文（架构、设计、技术栈）
│       ├── architecture.md
│       ├── design.md
│       └── tech-stack.md
├── LICENCE
└── README.md                     # 项目简介 + 最新文章列表（由流程自动更新）
```

## 数据流

```
v2ex/xna (HTML)
    ↓ [crawler.py] 按数字累增爬取，提取 feed URL
config/rss.opml
    ↓ [fetcher.py] 读取所有 feed，fetch 文章，聚合排序
api/{YYYY}/{MM}/{DD}.json
    ↓ [writer.py] 写入 JSON
README.md (可选：自动更新最新文章摘要)
```

## GitHub Actions Workflow

- **触发条件**：每 2 小时定时触发（`cron: '0 */2 * * *'`）
- **执行步骤**：
  1. Checkout 仓库
  2. 安装 Python 依赖（uv）
  3. 运行 `crawler.py`：发现新博客，更新 `config/rss.opml`
  4. 运行 `fetcher.py` + `writer.py`：fetch feeds，输出 `api/` JSON
  5. Commit & push 变更（`config/rss.opml` + `api/` 目录）

