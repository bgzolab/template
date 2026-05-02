---
title: 项目架构
created: YYYY-MM-DDTHH:MM:SS
modified: YYYY-MM-DDTHH:MM:SS
description: 架构需要对项目的整体结构进行说明，明确每个文件夹和文件的作用，以及它们之间的关系。需要列出每个文件的作用，以及它们之间的调用关系。如果有数据库，包含完整数据库结构。
tags: 
  - ai-notes
---

## Tree 目录结构

```shell
$ tree . -L 3 
.
├── docs 
│   ├── implementation-plans
│   └── memories # 包含项目的设计文档、技术栈选择和架构说明等内容
│       ├── architecture.md
│       ├── design.md
│       └── tech-stack.md
├── LICENCE
├── README.md
├── src
│   └── parser.py # 解析器主文件，包含数据提取和同步功能的实现
└── venera_dump.json # 从 20575-2273.venera 导出的数据文件，包含用户的观看历史、评分、收藏等信息
```

