---
title: 项目功能设计
created: 2026-03-30T00:00:00
modified: 2026-03-30T00:00:00
description: bGZo 个人网站功能设计、现有页面规划与待办迭代项［可执行、可验证、可迭代］。
tags:
  - ai-notes
---

## 首页（`/`）

### 第一屏：个人介绍

- 头像（Gravatar），右下角叠加 `💬` 状态图标（绿色脆冲动画）
- 点击图标或底部 `↓` 箭头平滑滚动到第二屏
- 展示：姓名、地理、语言、个人简介、社交图标行

### 第二屏：ChatPanel 对话框（Vue 3）

**文件**：`src/components/ChatPanel.vue`

**功能**：
- 顶部如常见 IM 应用的聊天头部示例
- 左侧气泡：展示固定文案「有什么想聊的？…」
- 右侧气泡：实时预览用户输入内容
- `textarea`：Enter 发送 / Shift+Enter 换行
- 引擎选择器（pill 按鈕组）：
  - 传统搜索：Google、Bing（个按鈕灰色）
  - AI 搜索：Perplexity、ChatGPT、Grok（按鈕紫色）
- 发送：`window.open(engineURL + encodeURIComponent(query), '_blank')`
- 左下角图例说明两种引擎分组色彩含义

## 博客（`/blog`）

> 导航链接已修改为外部跳转到 `https://blog.bgzo.cc/`。内部页面和路由结构保留但不通过导航暴露。

- 内容来自 `src/content/blog/` Markdown 文件
- 列表页按年分组、支持 category 下拉筛选
- 详情页 `/blog/[slug]` 展示 title、created、modified、阅读时间
- 页面样式：`Article.astro`（prose + 阴影）+ `admonition.css`

## Talks（`/talks`）

> 导航链接已修改为外部跳转到 `https://cast.bgzo.cc/`。内部页面保留。

- 数据源：scraping `t.me/imbgzo`（Telegram 公开频道）
- `lib/telegram/index.js`：cheerio 解析 HTML + PrismJS 代码高亮 + LRU Cache（5 min / 50 MB）
- 支持：图片、视频、音频、贴纸、链接弹窗预览
- 分页策略：before/after 游标（即帖子 ID ）
- 使用 SOCKS/HTTPS 代理支持（环境变量配置）

## Tools（`/tools`）

- **双拼音解码**：`DoublePinYinDecode.vue`
- **应吃什么水果**：`FruitYouShouldEat.vue`
- **字符串转义**：`StringEscape.vue`
- **URL Scheme 工具**：`UrlScheme.vue`
- 各工具有独立的 `/tools/[name]` 页面
- `tools.astro` 通过 `import.meta.glob` 动态扫描工具子页汇集列表
- 页面同时汇集了含外部工具的友情链接

## Labs（`/labs`）

- 展示 `bGZo/playground` 仓库所有分支的箱子项目
- 数据来自 `public/repo_stats.json`（GitHub Actions 定期生成，不是实时 API）
- `Labs.vue`：展示统计概览（分支数、源修改数、README 数、活跃项目数）+ 搜索过滤 + 卡片列表

## 导航配置（`src/config/nav.ts`）

```ts
{ name: "Blog",  path: "https://blog.bgzo.cc/", external: true }  // 外部
{ name: "Talks", path: "https://cast.bgzo.cc/", external: true }  // 外部
{ name: "Tools", path: "/tools" }  // 内部
{ name: "Labs",  path: "/labs"  }  // 内部
```

`Header.astro` 根据 `external` 标志分支渲染：外部链接不拼接 SITE_URL、新标签页打开。

## 待迭代项

- Blog / Talks 内部路由暂时保留（未来内容迁移完成后恢复导航入口）
- Talks 页面图片点击放大的 popover 实现（已在 Item.astro 中有框架）
