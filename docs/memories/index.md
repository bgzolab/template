<!--
唯一入口说明：
1) LLM 必须先读本文件；
2) 规范性规则只在 memories 中定义；
3) implementation-plans 仅用于执行步骤，不可作为规范来源。
-->

# Memories 文档入口（唯一入口）

## 读取顺序（最简）

1. `docs/memories/index.md`（本文件）
2. `docs/memories/archive-markdown-schema-v1.md`（归档规范唯一源）
3. `docs/memories/design-document.md`（设计边界与冻结决策）
4. `docs/memories/architecture.md`（模块职责与链路边界）
5. `docs/memories/tech-stack.md`（技术与配置矩阵）
6. `docs/memories/progress.md`（进度与状态）

## 权威顺序（冲突处理）

1. `archive-markdown-schema-v1.md`（最高优先级）
2. 其他 `memories/*.md`
3. `docs/implementation-plans/*.md`（仅执行计划，不是规范）

> 注释：若规则不在 memories 中，返回“规范上下文不足”，不要自行推断。

## LLM 交互 Prompt 示例（可直接复用）

请先读取 `docs/memories/index.md`，并仅将 memories 目录作为规范来源。归档规则只允许使用 `docs/memories/archive-markdown-schema-v1.md`。implementation-plans 仅用于执行顺序参考，不可用于定义行为。输出保持最简，并在开头给出：NormativeSource、Version、OutOfScope。若一次性切换门禁有任一缺失，直接给出 No-Go 与缺失项。
