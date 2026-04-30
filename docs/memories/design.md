---
title: 项目设计
created: 2026-04-30T20:58:38
modified: 2026-04-30T20:58:38
description: 当前功能设计、命令契约、输入输出与已知行为约束的精炼摘要。
tags:
  - ai-notes
---

## 设计目标

- 用一个简单 CLI 统一导出多个平台数据
- 输出直接可被 Obsidian 使用的 Markdown 文件
- 尽量保持重复执行可增量同步
- 保留一个统一索引输出能力，便于汇总导入结果

## 当前 use case

- 把网页平台里的收藏、点赞、稍后读、视频收藏导出到本地
- 迁移个人内容到 Obsidian
- 定期重复执行导出，持续更新本地资料库
- 为不同平台生成一个合并索引文件

## CLI 契约

- 顶层命令: eto
- 顶层可选参数: --index-file
- 子命令: cnblog、bangumi、qireader、v2ex、zhihu、weibo、bilibili
- --index-file 必须出现在子命令前

## 子命令输入

- cnblog: -o/--output
- bangumi: -t/--template、-s/--subject_type、-o/--output、可选 -c/--collection_type、--force
- qireader: -t/--tag、-o/--output
- v2ex: -o/--output
- zhihu: -c/--collection、-o/--output
- weibo: -u/--uid、-o/--output、可选 --force
- bilibili: -f/--fid、-o/--output、可选 --force

## 环境变量依赖

- CNBLOG_ACCESS_TOKEN
- BGM_ACCESS_TOKEN
- QIREADER_COOKIE
- V2EX_ACCESS_TOKEN
- V2EX_COOKIE
- WEIBO_COOKIE
- ZHIHU_COOKIE
- BILIBILI_COOKIE

## 输出约定

- 输出目录由各子命令的 --output 指定
- 每个条目输出一个 Markdown 文件
- 内容包含 front matter
- 索引默认打印到终端，也可写入单个 Markdown 文件
- 索引文件按模块分组，模块标题为 ##，每轮导出块为 ###

## 增量行为

- 多数模块在发现目标文件已存在时直接结束本轮同步
- 这是一种基于本地文件存在性的剪枝，而不是远端游标持久化
- --force 只在部分模块可用，目前主要是 bangumi、weibo、bilibili

## 已知设计现实

- 项目现在不是通用插件系统，新增平台仍需在 CLI 中手动注册
- IndexWriter 还在入口文件中，尚未独立成公共模块
- 测试覆盖还不完整，当前没有单独的 zhihu、weibo、bilibili、v2ex 测试文件
- 文档和 README 正在向“简单英文使用说明 + 中文内部记忆”分层收敛

