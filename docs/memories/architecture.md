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
├── .github
│   ├── agents # 智能体，copilot 左下角可选择
│   ├── copilot-instructions.md # 项目全局生效
│   ├── instructions # 项目默认加载指令
│   ├── ISSUE_TEMPLATE # 项目 issue 模板
│   ├── prompts # 使用slash 调用的预制提示词
│   └── workflows # GitHub CI/CD
├── docs # 项目文档，包含项目的设计文档、架构文档、技术栈规范、实施计划等
│   ├── implementation-plans # 项目的实施计划，每次修BUG、新增改能全部记录在这里，包含每个功能的分步指令和验证正确性的测试
│   └── memories # 项目的记忆库，包含项目的设计文档、架构文档、技术栈规范等，是 LLM 必须加载的上下文；
│       ├── architecture.md # 项目架构设计文档，包含项目的整体架构设计、模块划分、数据库结构等；
│       ├── design.md # 项目设计文档，包含项目的功能设计、接口设计、数据流设计等；
│       └── tech-stack.md # 项目技术栈规范，包含项目的技术栈选择、编码规范、测试规范等；
├── LICENCE # 项目许可证，包含项目的开源许可证信息
└── README.md # 项目自述文件，包含项目的简介、安装使用说明、贡献指南等
```

