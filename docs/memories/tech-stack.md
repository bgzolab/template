---
title: 技术栈选择与规范
created: 2026-03-30T00:00:00
modified: 2026-03-30T00:00:00
description: bGZo 个人网站技术栈选择和编码规范。
tags:
  - ai-notes
---

## 核心技术栈

| 层       | 技术                                     | 版本 / 备注                     |
| -------- | ---------------------------------------- | ------------------------------- |
| 框架     | [Astro](https://astro.build)             | ^5.14.1；multi-island 架构      |
| UI 组件  | Vue 3 (`@astrojs/vue`)                   | ^5.1.1；`client:load` 水化      |
| 样式     | Tailwind CSS + `@tailwindcss/typography` | ^3.4.18                         |
| 包管理   | Bun                                      | `packageManager: bun@1.2.23`    |
| 适配器   | `@astrojs/node` standalone               | ^9.4.4；SSR 页面支持            |
| 分析     | Google Analytics (Partytown)             | `@astrojs/partytown` 隔离大脚本 |
| Markdown | remark 插件链                            | 见下文                          |
| 部署     | GitHub Actions → GitHub Pages            | `bGZo/bgzo.github.io`           |

## Markdown 处理链

- `remark-toc`：自动生成目录（`heading: "目录"`）
- `remarkReadingTime`：计算阅读时间，结果写入 frontmatter.minutesRead
- `remark-github-beta-blockquote-admonitions`：支持 Obsidian 风格的 Callout（`[!NOTE]` 等）
- `remarkAutoToc`：自定义插件，当前已注释居默认关闭

## 技术选型原则

1. **首选标准库 / 框架内置能力**，不引入多余依赖。
2. Astro 组件优先；需要交互状态时才引入 Vue。
3. Tailwind 类名直接写在模板中，不新建单独 CSS 文件。 
4. 所有外链加 `rel="noopener noreferrer"` + `target="_blank"`。

## 通用编码原则

1. **严格禁止使用 Emoji**。
2. 模块化，禁止单体巨文件（> 1000 行就拆分）。
3. 任何操作必须在仓库内可追溯，禁止在 `/tmp` 黑笼操作。
4. 注释只写「为什么」，不写「是什么」。
5. 新功能/修复必须最小化修改，不操作与需求无关的代码。

## Blog 文章 Frontmatter 规范

```yaml
---
title: 文章标题
created: 2023-07-08T11:15:56   # 创建时间
modified: 2025-06-29T23:51:45  # 最后修改时间
category: weekly               # 分类（weekly / essay / note 等）
tags: [weekly/1143]            # 标签数组
type: writing                  # 类型
---
```

## 常用命令

```bash
bun run dev      # 开发服务器（NODE_ENV=development）
bun run build    # 生产构建 → dist/client/
bun run preview  # 预览构建产物
```

