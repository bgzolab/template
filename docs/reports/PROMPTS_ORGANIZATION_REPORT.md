---
ai: true
title: Prompts 整理与初筛报告
created: 2026-02-21T00:00:00
modified: 2026-02-21T00:00:00
author: Copilot
description: 对 .github/prompts 文件夹中所有提示词的整理、去重和优化建议
tags: [organization, prompts, documentation]
---

# Prompts 整理与初筛报告

## 📊 总体概览

**总文件数**: 47 个 prompt 文件  
**已有 Agent**: 2 个（prd.agent.md、implementation-plan.agent.md）  
**分析完成度**: 14+ 个关键文件已详细阅读  

---

## 🎯 核心发现

### ✅ 重合度高的 Prompts（建议合并或删除）

#### 1️⃣ **需求文档（PRD）相关 - 可以统一为 Agent**

| 文件 | 功能 | 重合度 | 建议 |
|------|------|--------|------|
| `breakdown-epic-pm.prompt.md` | 创建 Epic PRD | 高 | ❌ 删除（被 prd.agent.md 覆盖） |
| `breakdown-feature-prd.prompt.md` | 创建 Feature PRD | 高 | ❌ 删除（被 prd.agent.md 覆盖） |
| `create-specification.prompt.md` | 创建规范（Infrastructure-level） | 中 | ⚠️ 保留但补充用途说明 |
| `update-specification.prompt.md` | 更新规范 | 中 | 可转换为 Agent 扩展 |

**原因**: 你的 `prd.agent.md` 已经包含了完整的 PRD 生成流程（澄清问题 → 分析 → 生成），包括 Epic 和 Feature 两个层级。这两个 breakdown 文件功能重复。

---

#### 2️⃣ **实现计划相关 - 完全重合**

| 文件 | 功能 | 重合度 | 建议 |
|------|------|--------|------|
| `create-implementation-plan.prompt.md` | 创建实现计划 | 很高 | ❌ 删除（被 implementation-plan.agent.md 覆盖） |
| `update-implementation-plan.prompt.md` | 更新实现计划 | 很高 | ❌ 删除 |
| `breakdown-feature-implementation.prompt.md` | Feature 级实现计划 | 很高 | ❌ 删除 |
| `breakdown-plan.prompt.md` | GitHub Project Planning | 高 | ✅ 保留（但重命名为 project-planning） |

**原因**: `implementation-plan.agent.md` 的模板和 `create-implementation-plan.prompt.md` 几乎完全相同，包括前置条件、执行上下文、模板结构等。三个 breakdown 文件都是生成相同格式的实现计划。

---

#### 3️⃣ **分解（Breakdown）系列 - 同一个概念的多个表达**

| 文件 | 功能 | 重合度 | 建议 |
|------|------|--------|------|
| `breakdown-epic-arch.prompt.md` | Epic 架构分解 | 中 | 保留但转专题（建筑决策记录） |
| `breakdown-test.prompt.md` | 测试规划 | 低 | ✅ 保留（独有功能） |

---

### ⚠️ 可以简化的 Prompts

#### GitHub Issues 创建相关

| 文件 | 功能 | 建议 |
|------|------|------|
| `create-github-issue-feature-from-specification.prompt.md` | 从规范创建 Issue | 简化为单一规范 Issue 创建脚本 |
| `create-github-issues-feature-from-implementation-plan.prompt.md` | 从计划创建 Issues | 可集成到 implementation-plan.agent.md 后续步骤 |
| `create-github-issues-for-unmet-specification-requirements.prompt.md` | 创建未实现的需求 Issue | 可删除（专有场景） |
| `create-github-pull-request-from-specification.prompt.md` | 从规范创建 PR | 太专有，建议删除 |

**建议**: 统一为一个 `create-github-issues.prompt.md`，支持三种输入源（PRD、实现计划、规范）。

---

#### 赋能（Enabler）和其他框架

| 文件 | 功能 | 建议 |
|------|-----|------|
| `structured-autonomy-generate.prompt.md` | 生成代码 | 保留（代码生成框架） |
| `structured-autonomy-implement.prompt.md` | 实现特性 | 保留（实现框架） |
| `structured-autonomy-plan.prompt.md` | 规划框架 | ✅ 保留（轻量级规划，与 implementation-plan 互补） |

---

### 📚 建议保留的 Prompts（独有价值）

#### 最佳实践和工程相关

| 文件 | 原因 |
|------|------|
| `breakdown-test.prompt.md` | 完整的 ISTQB + ISO 25010 测试规划框架 |
| `refactor-plan.prompt.md` | 重构特定的计划结构（与实现计划不同） |
| `create-architectural-decision-record.prompt.md` | ADR 文档生成 |
| `create-oo-component-documentation.prompt.md` | OO 组件文档 |
| `create-github-action-workflow-specification.prompt.md` | CI/CD 工作流规范 |
| `devops-rollout-plan.prompt.md` | DevOps 特定流程 |

#### 语言和框架特定的 Prompts

| 类别 | 文件 | 推荐 |
|------|------|------|
| Java | `java-docs.md`, `java-junit.md`, `java-springboot.md`, `java-refactoring-*.md` | ✅ 保留所有 |
| Kotlin | `kotlin-springboot.md` | ✅ 保留 |
| JavaScript/TypeScript | `javascript-typescript-jest.md` | ✅ 保留 |
| Python | `pytest-coverage.md` | ✅ 保留 |
| SQL | `sql-code-review.md`, `sql-optimization.md` | ✅ 保留 |

#### 文档和工具相关

| 文件 | 原因 |
|------|------|
| `create-readme.md` | 项目 README 生成 |
| `create-tldr-page.md` | 快速参考页面 |
| `documentation-writer.md` | 通用文档编写 |
| `mkdocs-translations.md` | 文档翻译 |
| `readme-blueprint-generator.md` | README 模板生成 |
| `write-coding-standards-from-file.md` | 从代码提取编码标准 |

---

## 🗂️ 推荐的新组织结构

```
.github/prompts/
├── _core/                          # 核心 Agent（现有）
│   ├── prd.agent.md               # ✅ 保留
│   ├── implementation-plan.agent.md # ✅ 保留
│   └── structured-autonomy-*.agent.md  # 转换为 Agent
│
├── documentation/                  # 文档生成提示词
│   ├── create-readme.prompt.md
│   ├── create-tldr-page.prompt.md
│   ├── create-oo-component-documentation.prompt.md
│   ├── documentation-writer.prompt.md
│   └── mkdocs-translations.prompt.md
│
├── engineering/                    # 工程相关提示词
│   ├── refactor-plan.prompt.md
│   ├── breakdown-test.prompt.md
│   ├── create-architectural-decision-record.prompt.md
│   ├── review-and-refactor.prompt.md
│   └── add-educational-comments.prompt.md
│
├── devops/                         # DevOps 相关
│   ├── create-github-action-workflow-specification.prompt.md
│   ├── create-github-issues.prompt.md  # 统一的 Issue 创建
│   └── devops-rollout-plan.prompt.md
│
├── languages/                      # 语言特定提示词
│   ├── java/
│   │   ├── java-docs.prompt.md
│   │   ├── java-junit.prompt.md
│   │   ├── java-springboot.prompt.md
│   │   ├── java-refactoring-extract-method.prompt.md
│   │   └── java-refactoring-remove-parameter.prompt.md
│   ├── kotlin/
│   │   └── kotlin-springboot.prompt.md
│   ├── typescript/
│   │   └── javascript-typescript-jest.prompt.md
│   ├── python/
│   │   └── pytest-coverage.prompt.md
│   └── sql/
│       ├── sql-code-review.prompt.md
│       └── sql-optimization.prompt.md
│
└── deprecated/                     # 建议删除的提示词（保留备份）
    ├── breakdown-epic-pm.prompt.md
    ├── breakdown-feature-prd.prompt.md
    ├── create-implementation-plan.prompt.md
    ├── update-implementation-plan.prompt.md
    ├── breakdown-feature-implementation.prompt.md
    ├── create-github-issue-feature-from-specification.prompt.md
    ├── create-github-issues-feature-from-implementation-plan.prompt.md
    ├── create-github-issues-for-unmet-specification-requirements.prompt.md
    └── create-github-pull-request-from-specification.prompt.md
```

---

## 📋 具体建议清单

### 🔴 立即删除（被 Agent 完全覆盖）

```
❌ breakdown-epic-pm.prompt.md          → 被 prd.agent.md 覆盖
❌ breakdown-feature-prd.prompt.md      → 被 prd.agent.md 覆盖
❌ create-implementation-plan.prompt.md → 被 implementation-plan.agent.md 覆盖
❌ update-implementation-plan.prompt.md → 被 implementation-plan.agent.md 覆盖
❌ breakdown-feature-implementation.prompt.md → 由实现计划 Agent 覆盖
❌ create-github-pull-request-from-specification.prompt.md → 太专有
```

### 🟡 有条件保留

#### update-specification.prompt.md
- 保留，但可转换为 Agent 或集成到规范工作流
- 与 `create-specification.prompt.md` 配对使用

#### create-github-issue-* 系列
- 建议合并为单一 `create-github-issues.prompt.md`
- 根据输入类型（PRD/Plan/Spec）动态调整

#### breakdown-epic-arch.prompt.md
- 转换为 `create-architectural-decision-record.prompt.md`
- 或重名为 `architecture-specification.prompt.md`

### 🟢 保留并优化

所有语言特定、测试、文档、DevOps 相关的提示词都应保留，但建议按目录重新组织。

---

## 📝 实施步骤

### 第 1 步：备份
```bash
mkdir -p .github/prompts/deprecated
# 移动建议删除的文件到 deprecated
```

### 第 2 步：整理结构
```bash
# 创建新目录
mkdir -p .github/prompts/{documentation,engineering,devops,languages/{java,kotlin,typescript,python,sql}}

# 移动相应文件
```

### 第 3 步：创建统一的 Issue 创建 Prompt
- 合并三个 `create-github-issue-*` 文件
- 支持多种输入源

### 第 4 步：更新文档
- 在 README 中说明各目录用途
- 添加促进使用的指引

---

## 📊 整理效果预期

| 指标 | 现状 | 目标 | 效果 |
|------|------|------|------|
| 总文件数 | 47 | ~25-30 | 减少 40% 冗余 |
| 重复 Prompts | 6+ | 0 | 完全去重 |
| 查找难度 | 困难 | 容易 | 结构清晰 |
| 维护成本 | 高 | 低 | 降低维护开销 |

---

## 🔗 相关文件

- [PRD Agent](../.github/agents/prd.agent.md)
- [Implementation Plan Agent](../.github/agents/implementation-plan.agent.md)
- [默认 Copilot 指令](../.github/copilot-instructions.md)

