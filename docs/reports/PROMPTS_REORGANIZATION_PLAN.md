---
title: Prompts 重组方案 - 兼容 Copilot 发现机制
created: 2026-02-21
modified: 2026-02-21
description: 设计既能按语言分类又能被 Copilot 识别的组织方案
tags: [organization, copilot, architecture]
---

# Prompts 重组方案

## 问题分析

### Copilot 的文件发现限制

| 目录 | 支持嵌套? | Copilot 识别 | 现状 |
|------|----------|-------------|------|
| `.github/agents/` | ❌ | ✅ 平级文件全部识别 | 现有 4 个 agents |
| `.github/instructions/` | ❌ | ✅ 平级文件全部识别 | 现有 2 个 instructions |
| `.github/prompts/` | ❌ | ❌ **只识别根目录** | 47 个 prompts 无法分类 |

**关键发现**: Copilot 无法识别 `.github/prompts/` 的子目录中的 `*.prompt.md` 文件！

---

## 推荐方案：混合分层架构

### 核心思路

1. **`.github/prompts/`** - 保持平级（根目录）
   - 存放所有 **基础通用 prompts** 
   - 必须在根目录，让 Copilot 识别

2. **`.github/agents/`** - 转换为 Agent
   - 把常用 prompts 转换为 `*.agent.md`
   - 提供交互式体验

3. **`.github/instructions/`** - 创建语言特定指令
   - 新增 `{language}.instructions.md` 文件
   - 自动加载语言特定的规则（Copilot 自动识别）

4. **`docs/prompts-index/`** - 新建索引文档（可选）
   - 为用户提供按语言/功能的导航
   - 不影响 Copilot 发现，仅供人工查阅

---

## 实施方案

### 方案 A：最小侵入（推荐）

```
.github/
├── agents/
│   ├── prd.agent.md                    # ✅ 现有
│   ├── implementation-plan.agent.md    # ✅ 现有
│   ├── github-actions-expert.agent.md  # ✅ 现有
│   ├── debug.agent.md                  # ✅ 现有
│   ├── test-planning.agent.md          # 🆕 转换自 breakdown-test.prompt.md
│   └── refactor-plan.agent.md          # 🆕 转换自 refactor-plan.prompt.md
│
├── instructions/
│   ├── markdown.instructions.md        # ✅ 现有
│   ├── taming-copilot.instructions.md  # ✅ 现有
│   ├── java.instructions.md            # 🆕 Java 生态指令
│   ├── typescript.instructions.md      # 🆕 TypeScript 生态指令
│   ├── python.instructions.md          # 🆕 Python 生态指令
│   └── sql.instructions.md             # 🆕 SQL 指令
│
└── prompts/
    ├── create-specification.prompt.md              # ✅ 保留
    ├── update-specification.prompt.md              # ✅ 保留
    ├── create-architectural-decision-record.prompt.md  # ✅ 保留
    ├── create-oo-component-documentation.prompt.md # ✅ 保留
    ├── create-github-action-workflow-specification.prompt.md  # ✅ 保留
    ├── create-readme.prompt.md                     # ✅ 保留
    ├── create-tldr-page.prompt.md                  # ✅ 保留
    ├── documentation-writer.prompt.md              # ✅ 保留
    ├── devops-rollout-plan.prompt.md               # ✅ 保留
    ├── mkdocs-translations.prompt.md               # ✅ 保留
    ├── review-and-refactor.prompt.md               # ✅ 保留
    ├── add-educational-comments.prompt.md          # ✅ 保留
    ├── write-coding-standards-from-file.prompt.md  # ✅ 保留
    ├── model-recommendation.prompt.md              # ✅ 保留
    ├── ai-prompt-engineering-safety-review.prompt.md # ✅ 保留
    ├── repo-story-time.prompt.md                   # ✅ 保留
    │
    ├── java-docs.prompt.md                         # ✅ 保留（语言特定）
    ├── java-junit.prompt.md                        # ✅ 保留
    ├── java-springboot.prompt.md                   # ✅ 保留
    ├── java-refactoring-extract-method.prompt.md   # ✅ 保留
    ├── java-refactoring-remove-parameter.prompt.md # ✅ 保留
    ├── kotlin-springboot.prompt.md                 # ✅ 保留
    ├── javascript-typescript-jest.prompt.md        # ✅ 保留
    ├── pytest-coverage.prompt.md                   # ✅ 保留
    ├── sql-code-review.prompt.md                   # ✅ 保留
    ├── sql-optimization.prompt.md                  # ✅ 保留
    │
    └── _deprecated/                                # 📁 (或移到其他地方备份)
        ├── breakdown-epic-pm.prompt.md             # ❌ 删除
        ├── breakdown-feature-prd.prompt.md         # ❌ 删除
        ├── create-implementation-plan.prompt.md    # ❌ 删除
        ├── ... (其他重复文件)
```

**优势**:
- ✅ `.github/prompts/` 保持平级结构，Copilot 识别所有文件
- ✅ 语言特定规则转为 `.instructions.md`，Copilot 自动按文件类型加载
- ✅ 常用工作流转为 Agent，提供更好的交互体验
- ✅ 最小化改动，风险低

---

### 方案 B：完全分离（理想但不可行）

```
# ❌ 不可行 - Copilot 无法识别子目录
.github/prompts/
├── core/
├── languages/java/
├── languages/typescript/
└── ...
```

**问题**: Copilot 无法发现 `languages/java/` 中的文件

---

## 转换清单

### 删除（被 Agent 覆盖）

```
❌ breakdown-epic-pm.prompt.md
❌ breakdown-feature-prd.prompt.md
❌ create-implementation-plan.prompt.md
❌ update-implementation-plan.prompt.md
❌ breakdown-feature-implementation.prompt.md
❌ breakdown-plan.prompt.md
❌ create-github-issue-feature-from-specification.prompt.md
❌ create-github-issues-feature-from-implementation-plan.prompt.md
❌ create-github-issues-for-unmet-specification-requirements.prompt.md
❌ create-github-pull-request-from-specification.prompt.md
```

### 转换为 Agent（高价值 prompts）

```
breakdown-test.prompt.md
  → test-planning.agent.md (完整的 ISTQB + ISO 25010 测试规划)

refactor-plan.prompt.md
  → refactor-plan.agent.md (多文件重构的安全序列规划)

structured-autonomy-plan.prompt.md
  → structured-autonomy-plan.agent.md (轻量级规划框架)
```

### 新建语言特定 Instructions 文件

```
🆕 java.instructions.md
   - 统合所有 java-*.prompt.md 的最佳实践
   - Spring Boot, JUnit, 重构模式

🆕 typescript.instructions.md
   - JavaScript/TypeScript 最佳实践
   - Jest, 测试策略

🆕 python.instructions.md
   - Python 开发标准
   - pytest, 代码质量

🆕 sql.instructions.md
   - SQL 审查和优化标准
   - 性能指南
```

---

## 导航和发现

### 1. 更新 `.github/README.md` 或新建导航文件

```markdown
# Copilot 工具导航

## 🤖 Agents（交互式工作流）
- `@prd` - 创建产品需求文档
- `@implementation-plan` - 创建实现计划
- `@test-planning` - 测试规划
- `@refactor-plan` - 重构计划
- `@github-actions-expert` - GitHub Actions 专家

## 📝 Prompts（通用提示词）
按功能分类：

### 文档
- `create-readme.prompt.md`
- `create-tldr-page.prompt.md`
- `create-oo-component-documentation.prompt.md`

### 架构和设计
- `create-architectural-decision-record.prompt.md`
- `create-github-action-workflow-specification.prompt.md`
- `create-specification.prompt.md`

### 语言特定
- Java: `java-docs.md`, `java-junit.md`, `java-springboot.md`, `java-refactoring-*.md`
- TypeScript: `javascript-typescript-jest.prompt.md`
- Python: `pytest-coverage.prompt.md`
- SQL: `sql-code-review.md`, `sql-optimization.md`
- Kotlin: `kotlin-springboot.prompt.md`

### 代码质量
- `review-and-refactor.prompt.md`
- `add-educational-comments.prompt.md`
- `write-coding-standards-from-file.prompt.md`

### DevOps 和工具
- `devops-rollout-plan.prompt.md`
- `mkdocs-translations.prompt.md`

## 🎯 Instructions（自动加载）
- `markdown.instructions.md` - Markdown 标准
- `taming-copilot.instructions.md` - Copilot 控制规则
- `java.instructions.md` - Java 生态
- `typescript.instructions.md` - TypeScript 生态
- `python.instructions.md` - Python 生态
- `sql.instructions.md` - SQL 标准
```

### 2. 在 VSCode 中启用 Prompt 快速访问

创建 `.vscode/copilot.json` (或在 settings.json 中添加):

```json
{
  "github.copilot.prompts": {
    "enabled": true,
    "showInContextMenu": true
  }
}
```

---

## 实施步骤（按顺序）

### Phase 1: 创建新文件（不删除任何东西）

```bash
# 1. 创建新 Agents
touch .github/agents/test-planning.agent.md
touch .github/agents/refactor-plan.agent.md

# 2. 创建语言特定 Instructions
touch .github/instructions/java.instructions.md
touch .github/instructions/typescript.instructions.md
touch .github/instructions/python.instructions.md
touch .github/instructions/sql.instructions.md

# 3. 创建导航文档
touch .github/PROMPTS_NAVIGATION.md
```

### Phase 2: 填充内容

- 将高价值 prompts 转换为 Agent（带有交互式工作流）
- 将语言特定的 prompts 内容整合到 Instructions

### Phase 3: 验证

```bash
# 检查所有文件是否被识别
ls -la .github/prompts/*.prompt.md | wc -l
ls -la .github/agents/*.agent.md
ls -la .github/instructions/*.instructions.md
```

### Phase 4: 清理

```bash
# 移动重复的 prompts 到备份
mkdir .github/prompts/_archive
# 或删除（建议先备份）
```

---

## 对比：各方案收益

| 方面 | 方案 A (推荐) | 方案 B (不可行) |
|------|-------------|-------------|
| Copilot 发现 | ✅ 100% | ❌ 0% |
| 文件组织 | ⚠️ 平级但有命名规范 | ✅ 完美分类 |
| 维护成本 | ✅ 低 | ❌ 高 |
| 可行性 | ✅ 立即实施 | ❌ 需等待 Copilot 改进 |
| 用户体验 | ✅ 好（Agent + 导航） | ❌ 差（无法识别） |

---

## 所需工具/配置更新

### 如果支持 `applyTo` 规则

可以在 Instructions 中添加 `applyTo` 规则：

```yaml
---
description: "Java Spring Boot best practices"
applyTo: "**/*.java"
---
```

这样 Copilot 会在编辑 Java 文件时自动应用这套规则。

---

## 总结

**最终方案**：
1. ✅ `.github/prompts/` 保持平级（Copilot 要求）
2. ✅ 创建 4-6 个语言特定的 `.instructions.md`
3. ✅ 把 2-3 个高价值 prompts 转为 Agent
4. ✅ 删除 10+ 个重复的 prompts
5. ✅ 添加导航文档供人工查阅

**最终结果**: 
- ✅ Copilot 能识别所有文件
- ✅ 用户能按语言/功能快速找到相关工具
- ✅ 消除 40%+ 的冗余
- ✅ 维护成本显著降低

