---
title: 项目架构
created: 2026-03-30T00:00:00
modified: 2026-03-30T00:00:00
description: bGZo 个人网站（astro-demo）整体架构——目录结构、模块划分、数据流与调用关系。
tags:
  - ai-notes
---

## 项目概况

- **仓库名**：`astro-demo`（工作目录 `/home/bgzo/workspaces/playground/astro-demo`）
- **站点域名**：`https://bgzo.github.io`（由 GitHub Actions 自动部署到 `bGZo/bgzo.github.io`）
- **工作分支**：`2025/10/blog-astro`（main 分支为部署目标）
- **构建产物**：`dist/client/`（静态 HTML + JS + CSS），并附带 `.nojekyll` 和 `CNAME`

## 目录结构

```
astro-demo/
├── .github/
│   ├── copilot-instructions.md   # Copilot 全局规则（本文件是最高优先级）
│   ├── instructions/             # 语言/框架专项指令（markdown.instructions.md 等）
│   ├── agents/                   # VS Code Copilot 自定义 Agent 模式
│   ├── prompts/                  # /slash 预制提示词
│   ├── ISSUE_TEMPLATE/           # GitHub Issue 模板
│   └── workflows/deploy.yml      # CI/CD：push 到工作分支自动构建并推送到 GitHub Pages
├── docs/
│   ├── implementation-plans/     # 每次需求/BUG 的实施记录（历史文档，带日期前缀）
│   └── memories/                 # LLM 必读上下文（Living Documents）
│       ├── architecture.md       # 本文件：整体架构
│       ├── design.md             # 功能设计与页面规划
│       └── tech-stack.md         # 技术栈选择与编码规范
├── public/
│   └── repo_stats.json           # Labs 页面的 GitHub 仓库统计缓存（静态 JSON）
├── src/
│   ├── assets/
│   │   ├── css/                  # 全局样式：normalize、main、admonition、talk-*
│   │   └── icon/                 # SVG 社交图标（github、telegram、bluesky 等）
│   ├── components/
│   │   ├── Header.astro          # 全站导航栏；读取 nav.ts；外部链接 target=_blank
│   │   ├── Footer.astro          # 页脚
│   │   ├── Page.astro            # 通用内容容器（max-w-2xl，无阴影）
│   │   ├── Article.astro         # 博客文章容器（prose 样式，有阴影）
│   │   ├── ChatPanel.vue         # 首页第二屏：AI/搜索对话框（Vue 组件）
│   │   ├── Labs.vue              # Labs 页：GitHub 仓库浏览（Vue 组件，数据来自 repo_stats.json）
│   │   ├── profile/
│   │   │   ├── Location.vue      # 地理位置图标（Vue）
│   │   │   └── Language.vue      # 语言图标（Vue）
│   │   ├── talks/
│   │   │   ├── List.astro        # Talks 频道帖子列表；分页（before/after 游标）
│   │   │   └── Item.astro        # 单条 Telegram 帖子渲染
│   │   └── tools/
│   │       ├── DoublePinYinDecode.vue
│   │       ├── FruitYouShouldEat.vue
│   │       ├── StringEscape.vue
│   │       └── UrlScheme.vue
│   ├── config/
│   │   ├── nav.ts                # 导航配置；external:true 表示外部链接
│   │   └── profile.ts            # 站主信息（头像、名字、社交账号等）
│   ├── content/
│   │   ├── config.ts             # Astro Content Collections 定义（blog 集合）
│   │   └── blog/                 # Markdown 博客文章；front-matter 含 title/created/modified/category/tags
│   ├── layouts/
│   │   └── Home.astro            # 全站唯一 HTML 壳（head、GA、normalize/main CSS）
│   ├── lib/
│   │   ├── dayjs.js              # dayjs 封装
│   │   ├── env.js                # 跨环境读取 env 变量的工具函数
│   │   ├── prism.js              # PrismJS 代码高亮
│   │   └── telegram/index.js     # Telegram 频道数据抓取（scraping t.me，带 LRU 缓存 5min/50MB）
│   ├── middleware.js             # 注入 SITE_URL/RSS_URL 到 locals；设置 Cache-Control、Speculation-Rules
│   ├── env.d.ts                  # TypeScript 环境声明
│   └── pages/
│       ├── index.astro           # 首页（第一屏：个人信息；第二屏：ChatPanel）
│       ├── blog.astro            # 博客列表（按年分组，支持 category 筛选）
│       ├── tools.astro           # 工具聚合页（动态扫描 tools/*.astro）
│       ├── labs.astro            # Labs/Playground（渲染 Labs.vue）
│       ├── blog/[slug].astro     # 博客文章详情（SSG getStaticPaths）
│       ├── talks/                # Telegram 频道镜像（index/before/after 分页）
│       ├── tools/                # 各工具独立页面
│       └── rules/prefetch.json.js # Speculation Rules API 响应
├── astro.config.ts              # Astro 配置（Vue、Tailwind、Partytown、Node adapter、Markdown 插件）
├── tailwind.config.js           # Tailwind（content 扫描 src/**/*.{astro,js,ts,vue}）
├── package.json                 # 包管理器：bun；scripts: dev/build/preview
├── tsconfig.json
├── CNAME                        # GitHub Pages 自定义域名
└── .nojekyll                    # 禁止 GitHub Pages Jekyll 处理
```

## 数据流

```
[Markdown 文件] → Astro Content Collections → blog.astro / [slug].astro
[Telegram API / t.me scraping] → lib/telegram/index.js (LRU cache) → talks/
[public/repo_stats.json] → Labs.vue（静态 JSON 直接渲染）
[profile.ts + nav.ts] → Header.astro + index.astro（配置驱动）
[middleware.js] → 所有页面 Astro.locals（SITE_URL、RSS_URL、Cache-Control）
```

## 页面与路由

| 路由           | 文件                      | 渲染方式 | 说明                                |
| -------------- | ------------------------- | -------- | ----------------------------------- |
| `/`            | `pages/index.astro`       | SSG      | 首页（个人信息 + ChatPanel 第二屏） |
| `/blog`        | `pages/blog.astro`        | SSG      | 博客列表，按年/category 筛选        |
| `/blog/[slug]` | `pages/blog/[slug].astro` | SSG      | 文章详情，reading time              |
| `/talks`       | `pages/talks/index.astro` | SSR      | Telegram 频道镜像，游标分页         |
| `/tools`       | `pages/tools.astro`       | SSG      | 工具聚合页，动态扫描工具子页        |
| `/tools/*`     | `pages/tools/*.astro`     | SSG      | 单个工具页                          |
| `/labs`        | `pages/labs.astro`        | SSG      | GitHub 仓库展示                     |

> Blog 和 Talks 导航链接当前重定向到外部域名（`blog.bgzo.cc` / `cast.bgzo.cc`），内部路由暂时保留但不在导航中展示。

## CI/CD 流程

```
push → 2025/10/blog-astro
  └─ .github/workflows/deploy.yml
       ├─ bun install --frozen-lockfile
       ├─ bun run build (NODE_ENV=production)
       │    └─ bunx astro build → dist/client/
       └─ git push → bGZo/bgzo.github.io (main)
```

## 关键约束

- `adapter: node({ mode: 'standalone' })`：服务器端适配器仅用于 SSR 页面（talks），其余静态输出。
- `site` 在开发环境为 `http://127.0.0.1:4321`，生产为 `https://bgzo.github.io`。
- `SITE_URL` 通过 `middleware.js` 注入 `Astro.locals`，所有组件统一从此读取，不硬编码。
- Speculation Rules API 通过 `rules/prefetch.json.js` + `middleware.js` 的 `Speculation-Rules` Header 驱动预加载。

