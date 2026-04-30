---
title: 技术栈选择与规范
created: 2026-04-30T20:58:38
modified: 2026-04-30T20:58:38
description: 当前实际技术栈、依赖、开发命令与项目内约定的摘要。
tags:
  - ai-notes
---

## 通用编程原则

1. 严格禁止使用 Emoji
2. 注重模块化（多文件）和禁止单体巨文件（monolith），代码行数 < 1000；
3. 任何代码必须包含单元测试，且测试覆盖率尽量达到 100%；
4. 任何大段的代码必须包含文档注释，且注释内容须易于理解、准确，最好使用简体中文；

## 运行时技术栈

- Python >= 3.12
- click: CLI 框架
- requests: HTTP 请求
- beautifulsoup4、html2text、markdownify: HTML 转 Markdown
- python-frontmatter: front matter 处理
- urllib3: HTTP 依赖

## 项目与构建

- 包管理与构建元数据使用 pyproject.toml
- 构建后端: poetry-core
- 发布脚本存在于仓库根目录
- CLI 入口脚本名: eto

## 开发约定

- 源码目录固定为 src
- 测试目录固定为 tests
- 运行测试时通常需要显式设置 PYTHONPATH=src
- 推荐优先保持最小改动，不做无关重构
- 当前 CLI 已明确使用 click，后续命令改造默认沿用 click

## 常用命令

```shell
pip install -e .
source ./export-env.sh
PYTHONPATH=src pytest tests -q
PYTHONPATH=src pytest tests/test_utils.py -q
```

## 测试现状

- 当前已有测试文件: test_bangumi.py、test_cnblog.py、test_qireader.py、test_utils.py
- 尚未看到独立的 bilibili、weibo、zhihu、v2ex 测试文件
- 变更后优先跑受影响切片的最小 pytest 命令

## 文档约定

- README 面向用户，使用简单英文
- docs/memories 面向后续对话，要求完整但精炼
- Markdown 文件必须带 YAML front matter

## 非目标

- 当前不引入数据库
- 当前不引入消息队列、异步任务系统或 Web 服务
- 当前不做复杂插件化框架

