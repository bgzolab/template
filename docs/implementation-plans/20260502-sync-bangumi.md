---
title: Bangumi 同步功能实施计划
created: 2026-05-02T00:00:00
modified: 2026-05-02T00:00:00
description: 在现有 Venera 数据解析能力之上，实现按指定本地收藏夹表同步到 Bangumi 收藏状态的计划。
tags:
  - implementation-plan
  - bangumi
  - venera
---

## 目标

在现有 `.venera` 解析能力之上，实现一个新的同步命令，满足以下要求：

1. 可以指定同步 `local_favorite.db` 中的一个或多个动态收藏夹表，例如 `Doing`。
2. 可以为每个目标表指定 Bangumi 收藏状态，例如 `在看`、`看过`、`想看`。
3. 通过 Bangumi API 完成交互，使用 `ACCESS_TOKEN` 环境变量认证。
4. 因为 Venera 记录没有 Bangumi subject ID，必须先搜索，再判断当前收藏状态，满足跳过条件时不写入，否则执行更新。

## 结论与约束

上述需求逻辑本身没有问题，但必须接受以下边界，否则实现会不稳：

1. 搜索结果存在歧义，因此“零结果”和“多结果/低置信度结果”必须作为正常跳过分支处理。
2. 同步命令必须幂等，重跑不能导致重复写入或无意义更新。
3. 写入前必须先读 Bangumi 当前收藏状态，只有不一致时才更新。
4. `ACCESS_TOKEN` 只从环境变量读取，不从命令行接收。
5. Bangumi 请求必须设置明确的 `User-Agent`。

## 非目标

本次计划明确不包含：

1. 同步 `history.db` 的阅读进度。
2. 同步评分、评论、标签。
3. 交互式人工挑选搜索结果。
4. 自动修复错误匹配后的回滚系统。

## 实施记录

### 2026-05-02 Step 1 完成

已完成内容：

1. 在 `src/parser.py` 中新增 `sync-bangumi` 子命令。
2. 新增 `--sync <table>=<state>` 参数，并限制状态值为 `wish`、`done`、`doing`、`on_hold`、`dropped`。
3. 新增 `--dry-run` 参数。
4. 修复 `main()` 中 `sync-bangumi` 与既有解析路径的分支控制流。

已通过验收：

1. `sync-bangumi --help` 可显示预期参数。
2. 缺少 `--sync` 时命令会以非零退出。
3. 非法状态值会以非零退出并提示允许值。
4. 合法调用可以进入 `sync-bangumi` 自身执行分支。

### 2026-05-02 Step 2 完成

已完成内容：

1. 新增从 `.venera` 中提取 `local_favorite.db` 的逻辑。
2. 可按 `--sync` 指定的动态表读取收藏记录。
3. 提取结果已统一为结构化同步候选项，包含来源表和目标状态。
4. 不存在的表会返回明确错误，而不是静默跳过。

已通过验收：

1. 样本包中 `Doing` 提取为 74 条，`DONE` 提取为 1 条，与 sqlite 实际行数一致。
2. 指定不存在的表时会输出明确错误并非零退出。
3. 提取出的候选记录已确认包含 `source_table` 和 `target_state`。

### 2026-05-02 Step 3 完成

已完成内容：

1. 新增搜索输入模型 `SyncSearchRequest`。
2. 新增 Bangumi subject 简化模型和匹配结果模型。
3. 实现标题规范化和本地匹配判定函数。
4. 已区分 `matched`、`skipped_no_result`、`skipped_ambiguous`、`skipped_low_confidence` 四类结果。

已通过验收：

1. 本地伪造样本下，唯一精确命中会进入 `matched`。
2. 零结果会进入 `skipped_no_result`。
3. 多结果精确命中会进入 `skipped_ambiguous`。

### 2026-05-02 Step 4 完成

已完成内容：

1. 已将 Bangumi 客户端拆分到 `src/venera_parser_bangumi/sync/bangumi.py`。
2. 已实现搜索条目、读取当前用户收藏、更新收藏状态三个客户端方法。
3. 已固定 `Authorization: Bearer <token>` 和显式 `User-Agent`。
4. `sync-bangumi` 现在会先检查 `ACCESS_TOKEN` 是否存在，再继续后续流程。
5. 已补充 `pytest` 覆盖缺 token、鉴权失败等验收路径。

已通过验收：

1. 未设置 `ACCESS_TOKEN` 时，命令会在发请求前失败。
2. 使用无效 token 时，最小读请求会返回明确的鉴权错误。
3. 使用 `.env` 中有效 token 执行真实 `sync-bangumi --dry-run` 时，认证和搜索链路可正常返回结果。

额外观察：

1. 样本 `DONE: 電鋸人` 在真实 API 中落为 `skipped_low_confidence`，这是当前标题别名差异导致的匹配限制，不是客户端或鉴权故障。

### 2026-05-02 Step 5 完成

已完成内容：

1. 已在 `src/venera_parser_bangumi/sync/service.py` 中接线幂等判定流程。
2. 对每个已匹配 subject，会先读取当前收藏状态。
3. 已实现 `already_synced` 跳过分支和实际更新分支。
4. 单条失败不会中断整批结果汇总。

已通过验收：

1. 通过 `pytest` 伪造客户端验证：目标状态一致时不会发送写请求。
2. 通过 `pytest` 伪造客户端验证：状态不一致时会发送一次更新请求。
3. 失败条目会进入 `failed` 计数，而不是使程序提前退出。

说明：

1. 未对真实 Bangumi 账号执行写入 smoke test，以避免未经确认修改用户线上收藏状态。

### 2026-05-02 Step 6 完成

已完成内容：

1. 已实现 `--dry-run`，会执行解析、搜索、匹配和当前状态查询，但不发送写请求。
2. 已实现结果汇总，覆盖 `updated`、`would_update`、`skipped`、`failed`。
3. 已为每条记录保留跳过或失败原因。
4. 已支持通过 `--report-output` 导出 JSON 报告。

已通过验收：

1. `pytest` 已验证 dry-run 仅产生 `would_update`，不会调用写请求。
2. 真实 `.env` dry-run 烟测能输出完整统计摘要并正常结束。
3. 汇总结果中的计数与候选处理结果一致。

### 2026-05-02 Step 7 部分完成

已完成内容：

1. 已更新 `README.md` 的 CLI 用法，补充 `sync-bangumi`、`ACCESS_TOKEN` 和测试命令。
2. 已更新 `docs/memories` 中的架构、设计和技术栈说明。
3. 已将验收基线切换为 `pytest`，手工命令只保留为烟测。

待完成内容：

1. 如果要把该功能视为“真实可用同步”，仍需继续优化跨语言标题匹配，以降低真实样本中的 `skipped_low_confidence`。

## 实施步骤

### 步骤 1：固化 Bangumi 同步命令接口

实现内容：

1. 设计新子命令，例如 `sync-bangumi`。
2. 设计输入参数，至少包括：
	`archive`、`--table`、`--state`、`--dry-run`。
3. 明确 `--table` 可重复传入，支持一次同步多个表。
4. 明确 `--state` 的表达方式。

建议采用以下 CLI 约定：

1. `--table Doing --state doing`
2. `--table DONE --state done`
3. 或者使用成对映射参数，例如 `--sync Doing=doing --sync DONE=done`

推荐最终采用 `--sync <table>=<state>`，原因是它能天然表达“一张表对应一个 Bangumi 状态”，避免参数错位。

验收方案：

1. 运行 `python3 src/parser.py sync-bangumi --help`，帮助文本中出现该命令和所有必需参数。
2. 缺少 `--sync` 时，命令以非零退出并给出明确错误。
3. 传入非法状态值时，命令以非零退出并列出允许值。

### 步骤 2：从 `local_favorite.db` 精确提取候选同步项

实现内容：

1. 在当前解析层之上新增只读提取逻辑，不重复实现 zip 和 sqlite 打开流程。
2. 根据 `--sync` 指定的表名读取动态收藏夹表。
3. 为每条记录提取统一字段，至少包括：
	`source_table`、`id`、`name`、`author`、`type`、`tags`、`translated_tags`。
4. 对不存在的表返回结构化错误，而不是静默忽略。
5. 对列缺失做兼容读取，避免不同表 schema 小差异导致整体失败。

验收方案：

1. 使用样本 `20575-2273.venera` 运行提取路径时，`Doing` 与 `DONE` 的记录数与 sqlite 实际行数一致。
2. 指定不存在的表时，错误信息明确包含表名。
3. 提取结果中每条记录都带有来源表和目标状态，不丢失映射关系。

### 步骤 3：建立 Venera 收藏记录到 Bangumi 搜索请求的映射

实现内容：

1. 将 Venera 记录转换为搜索输入模型。
2. 搜索主关键词优先使用 `name`。
3. 如果后续需要，可追加 `translated_tags`、`author` 作为辅助判断信息，而不是直接拼成搜索词。
4. 设计统一的匹配判定结果类型，至少包括：
	`matched`、`skipped_no_result`、`skipped_ambiguous`、`skipped_low_confidence`。

建议的匹配策略：

1. 先按标题搜索 subject。
2. 在返回结果中优先比较 `name` 和 `name_cn` 的完全一致。
3. 再比较规范化后的一致性，例如大小写、空格、全半角处理。
4. 如果仍有多个候选，则直接跳过并记录候选列表摘要。

验收方案：

1. 为匹配逻辑准备最小样本，验证“唯一精确命中”会进入 `matched`。
2. 构造零结果样本，验证进入 `skipped_no_result`。
3. 构造多结果样本，验证进入 `skipped_ambiguous`，且不会进入写 API 阶段。

### 步骤 4：实现 Bangumi API 客户端最小封装

实现内容：

1. 新增一个窄接口客户端，只封装本阶段真正需要的调用：
	搜索条目、读取用户收藏、更新用户收藏。
2. 从 `ACCESS_TOKEN` 环境变量读取令牌。
3. 每个请求统一附带：
	`Authorization: Bearer <token>` 和项目专用 `User-Agent`。
4. 统一处理 Bangumi API 错误响应和网络异常。

实现前提：

1. 新版 API 不允许通过 query string 传递 token。
2. 非浏览器客户端需要明确 `User-Agent`。
3. 实际接口路径和响应体字段在落地时用一次 smoke test 最终确认。

验收方案：

1. 未设置 `ACCESS_TOKEN` 时，命令在发请求前失败并提示环境变量缺失。
2. 使用无效 token 时，能输出明确的鉴权失败信息。
3. 使用有效 token 时，最小读请求能够成功返回并被解析。

### 步骤 5：实现收藏状态的幂等判定与更新

实现内容：

1. 对每个已成功匹配的 subject，先读取用户当前收藏状态。
2. 如果当前状态与目标状态一致，则记为 `skipped_already_synced`。
3. 如果不存在收藏或状态不一致，则调用更新接口。
4. 更新后记录最终状态和响应摘要。

建议的 Bangumi 状态映射：

1. `wish` -> `1`
2. `done` -> `2`
3. `doing` -> `3`
4. `on_hold` -> `4`
5. `dropped` -> `5`

验收方案：

1. 对已经是目标状态的条目，重复执行同步时不会再次写入。
2. 对未收藏或状态不一致的条目，会发生一次更新请求并返回成功结果。
3. 更新失败时，失败条目会被记录，且不会阻断已经成功处理的其他条目汇总输出。

### 步骤 6：实现 `--dry-run`、结果汇总和审计输出

实现内容：

1. 增加 `--dry-run`，完整执行解析、搜索、匹配和当前状态查询，但不发送写请求。
2. 输出至少三类结果：
	`updated`、`skipped`、`failed`。
3. 为跳过和失败记录明确原因，例如：
	`no_result`、`ambiguous`、`already_synced`、`auth_error`、`network_error`。
4. 最终打印统计摘要，并在需要时支持导出 JSON 报告。

验收方案：

1. `--dry-run` 下不会产生写请求，但会给出本应更新的条目列表。
2. 真实运行后，结果汇总中的总数等于候选同步项总数。
3. 任意单条失败不会导致统计结果缺失或程序无摘要退出。

### 步骤 7：补充文档和最小回归验证

实现内容：

1. 更新 `README.md`，补充同步命令用法和 `ACCESS_TOKEN` 要求。
2. 更新 `docs/memories` 中涉及的架构、设计、技术栈变化。
3. 补充最小回归验证方式，至少覆盖：
	参数校验、样本解析、dry-run、单条成功同步、幂等跳过。

验收方案：

1. `README.md` 能让新使用者从零完成一次 dry-run。
2. 文档中的命令与实际 CLI 一致。
3. 回归检查通过后，才能将该功能视为完成。

## 建议的实现顺序

严格按以下顺序推进，不要跳步：

1. 先固定 CLI 形态。
2. 再做本地表提取。
3. 再做匹配决策模型。
4. 然后接入 Bangumi 只读 API。
5. 最后开放写入和 dry-run 汇总。

原因很简单：如果前面的输入模型和匹配边界没有稳定，越早接入写 API，越容易误同步。

## 完成定义

只有同时满足以下条件，Bangumi 同步功能才算完成：

1. 能按 `--sync <table>=<state>` 指定一个或多个本地收藏夹表。
2. 能通过 `ACCESS_TOKEN` 完成 Bangumi API 认证。
3. 能对每条记录执行“搜索 -> 判定 -> 读当前状态 -> 必要时更新”的完整流程。
4. 能对零结果、歧义结果和已同步结果做显式跳过。
5. 能通过 `--dry-run` 在不写入的前提下验证整个判定链路。
6. 有清晰的结果摘要和文档说明。

