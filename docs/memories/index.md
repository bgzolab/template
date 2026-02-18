<!--
唯一入口说明：
1) LLM 必须先读本文件；
2) 规范性规则只在 memories 中定义；
3) implementation-plans 仅用于执行步骤，不可作为规范来源，每次改动后，打开 progress.md 记录你做了什么供后续开发者参考，再把新的架构洞察添加到 architecture.md 中解释每个文件的作用；
4) LLM 在输出该项目文档的过程中，需要作为一个耐心的讲师，把专业知识用普通人都能懂的方式落地，尽量用中文。
-->

# Memories 文档入口（唯一入口）

> 说明：本入口主要用于约束 LLM 读取顺序；人类阅读可按需要跳读。

## 读取顺序（最简）

1. `docs/memories/index.md`：本文件，约束LLM读取顺序与规范来源；
2. `docs/memories/design-document.md`：本项目设计的原因，与关键上下文，包含设计边界与冻结决策；
3. `docs/memories/architecture.md`：模块各个文档的职责与链路边界，每次在实施具体的措施与代码改动后，进行更新；；
4. `docs/memories/progress.md`：进度与状态，每次在实施具体的措施与代码改动后，进行更新；
5. `docs/memories/archive-markdown-schema-v1.md`：本项目专属，归档规范唯一源；

## 权威顺序（冲突处理）

1. `archive-markdown-schema-v1.md`（最高优先级）
2. 其他 `memories/*.md`
3. `docs/implementation-plans/*.md`（仅执行计划，不是规范）

> 注释：若规则不在 memories 中，返回“规范上下文不足”，不要自行推断。

