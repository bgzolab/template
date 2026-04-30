---
title: 项目架构
created: 2026-04-30T20:58:38
modified: 2026-04-30T20:58:38
description: 当前 export-to-obsidian 项目的实际结构、入口、模块边界与数据流摘要。
tags:
  - ai-notes
---

这是一个单仓库 Python CLI 工具，用来把多个平台的已保存内容导出为
Obsidian 友好的 Markdown 文件。

## 架构概览

- 单一 CLI 入口：src/export_to_obsidian.py
- 模块按平台拆分：bangumi、bilibili、cnblog、qireader、v2ex、weibo、zhihu
- 通用能力放在 utils、entity
- 输出目标是本地文件系统，不依赖数据库
- 文档与长期上下文放在 docs/memories

## 关键目录

- src: 业务代码
- src/export_to_obsidian.py: click CLI 入口，注册所有子命令与顶层参数
- src/<platform>: 各平台客户端、拉取逻辑、内容转换逻辑
- src/utils: 文件写入、Markdown 转换、模板渲染等通用能力
- config/bangumi_template.md: Bangumi 导出模板
- tests: 当前测试集，覆盖 bangumi、cnblog、qireader、utils
- docs/implementation-plans: 功能计划与执行记录
- docs/memories: 提供给后续对话的稳定上下文
- output: 导出结果样例

## 运行时数据流

1. 用户执行 eto 顶层命令。
2. click 解析顶层参数与子命令。
3. 顶层上下文创建 IndexWriter，并把 --index-file 配置注入根上下文。
4. 子命令调用对应平台模块，分页拉取远端数据。
5. 每条数据转换为 WebPage 或 Video 前言加 Markdown 内容。
6. utils.file_utils 将内容写入 output 目录。
7. IndexWriter 将本轮导出条目打印到终端或写入一个 Markdown 索引文件。

## 已实现命令边界

- cnblog: 导出博客园收藏
- bangumi: 导出 Bangumi 收藏，可按 subject_type 或 collection_type 过滤
- qireader: 导出稍后读列表
- v2ex: 导出收藏主题
- zhihu: 导出收藏夹内容
- weibo: 导出点赞微博
- bilibili: 导出收藏夹视频

## 输出模型

- 统一输出 Markdown 文件
- 文件名通常带 ~ 前缀，避免与普通笔记混淆
- front matter 由 utils.template 与 utils.md_utils 生成
- Bangumi 使用模板文件
- Bilibili 输出 iframe 嵌入块和基础说明

## 当前约束

- 没有数据库，没有任务队列，没有服务端进程
- 主要是同步分页抓取，失败处理以跳过或提前结束为主
- 多个模块用“检测到已存在文件即结束同步”做增量剪枝
- 索引写入逻辑集中在 IndexWriter，位于 src/export_to_obsidian.py

