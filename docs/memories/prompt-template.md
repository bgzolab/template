<!--
用途：统一 LLM 交互提示词，减少上下文误读。
说明：本文件给“人”直接复制使用；不是强制规则文档。
约束：默认只读 memories；implementation-plans 仅在明确要求时读取。
-->

# LLM Prompt 模板（只读 memories 默认版）

## 先说结论（给人看的）

`prompt-template.md` 的意义：
1. 让你每次都能“复制即用”，不用临时重写提示词；
2. 降低 LLM 误读历史计划文档的概率；
3. 保证输出口径稳定（先结论，再变更点）。

## 三个字段的白话解释（可选，不是必须）

- `NormativeSource`：这次任务“最终听谁的”（规范来源）；
- `Version`：按哪个版本执行，避免新旧口径混用；
- `OutOfScope`：这次明确“不做什么”，防止任务跑偏。

> 注释：如果你觉得术语重，可以直接用下面“简版模板（无术语）”。

## 简版模板（无术语，推荐日常使用）

请先读 `docs/memories/index.md`，只把 memories 当作规则来源。
如果 memories 没写清楚，就直接告诉我“信息不足”，不要猜。
这次只做我要求的范围，不额外扩展。
输出请保持：先结论，再改动点。

## LLM 交互 Prompt 示例（可直接复用）

请先读取 `docs/memories/index.md`，并仅将 memories 目录作为规范来源。归档规则只允许使用 `docs/memories/archive-markdown-schema-v1.md`。implementation-plans 仅用于执行顺序参考，不可用于定义行为。输出保持最简，并在开头给出：NormativeSource、Version、OutOfScope。若一次性切换门禁有任一缺失，直接给出 No-Go 与缺失项。

## 模板A：通用实现任务（推荐）

- NormativeSource: `docs/memories/archive-markdown-schema-v1.md`
- Version: `md.v1`
- OutOfScope: 未在 memories 中定义的行为推断

请先读取 `docs/memories/index.md`，并只将 memories 目录视为规范来源。
归档行为只允许依据 `docs/memories/archive-markdown-schema-v1.md`。
`docs/implementation-plans/` 仅用于执行顺序，不可用于定义行为。
输出保持最简：
1) 先给结论；
2) 再给变更点；
3) 若信息不足，直接返回 `INSUFFICIENT_NORMATIVE_CONTEXT` 并列缺失项。

## 模板B：一次性切换评审（Go/No-Go）

- NormativeSource: `docs/memories/archive-markdown-schema-v1.md`
- Version: `md.v1`
- OutOfScope: 灰度/双写过渡策略

请先读取 `docs/memories/index.md` 与 `docs/memories/archive-markdown-schema-v1.md`。
仅按 schema v1 的一次性切换门禁判定：功能、数据、完整性、运维、审批。
若任一门禁缺失或失败，结论必须为 `No-Go`，并列出缺失项/失败项。

## 模板C：仅文档更新任务

- NormativeSource: `docs/memories/index.md`
- Version: `2026-02`
- OutOfScope: 代码改动

只更新文档，不改业务代码。
优先更新 `docs/memories/`；若涉及执行步骤，仅在 `docs/implementation-plans/` 追加计划。
遇到路径冲突时，以 memories 现有路径为准并统一引用。

## 快速检查清单（每次交互前）

1. 是否已声明 `NormativeSource` / `Version` / `OutOfScope`？
2. 是否先读了 `docs/memories/index.md`？
3. 是否把 implementation-plans 当成“执行步骤”而非“规范来源”？
4. 若规则缺失，是否返回了 `INSUFFICIENT_NORMATIVE_CONTEXT`？
