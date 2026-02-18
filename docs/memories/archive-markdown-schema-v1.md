<!--
规范定位：
1) 本文件是归档结构唯一规范源；
2) 其他文档只能引用，不能复制并改写本规范；
3) 规则变更必须先改本文件，再同步引用文件。
-->

# Archive Markdown Schema v1（唯一规范源）

## 1. 规范标识

- NormativeSource: `docs/memories/archive-markdown-schema-v1.md`
- Version: `md.v1`
- Scope: Telegram 消息归档到 Markdown 的最小字段强一致规范

## 2. 目录与分桶规则（来源优先）

- 分桶优先级：按来源分桶（`channel` / `person`）。
- 路径规则：`<base_dir>/<source_bucket>/<source_id>.md`
- `source_id` 规则：优先频道 username；没有 username 时使用 chat_id 字符串。

> 注释：路径中的 bucket/id 必须与 Front Matter 中字段一致。

## 3. Front Matter 必填字段（最小强一致）

以下字段为必填，缺任一字段即视为无效归档记录：

1. `schema_version`（固定值：`md.v1`）
2. `source_bucket`（`channel` 或 `person`）
3. `source_id`（稳定来源标识）
4. `chat_id`（Telegram chat id，字符串）
5. `message_id`（Telegram message id，整数）
6. `message_ts_utc`（消息时间，RFC3339 UTC）
7. `archive_ts_utc`（归档时间，RFC3339 UTC）
8. `origin_ref`（原始引用，推荐：`chat:<chat_id>#<message_id>`）
9. `content_sha256`（正文规范化后哈希）

## 4. 一致性不变量（必须满足）

1. 唯一键：`(chat_id, message_id)`；
2. 路径一致：文件所在 bucket/id 与 Front Matter 的 `source_bucket/source_id` 一致；
3. 内容一致：`content_sha256` 必须匹配写入正文；
4. 版本一致：`schema_version != md.v1` 视为不合规。

## 5. 一次性切换阈值（One-shot Cutover Threshold）

### 5.1 这是什么（What）

一次性切换阈值是“是否允许单次切换到新归档结构”的门禁集合。

### 5.2 为什么需要（Why）

防止在准备不足时做不可逆切换，避免出现批量不一致或回滚困难。

### 5.3 如何判定（How）

只有以下门禁 **全部通过**，才允许 Go；否则 No-Go：

1. 功能门禁：核心链路回归通过（归档/同步/通知关键路径）；
2. 数据门禁：必填字段完整 + `(chat_id, message_id)` 无冲突；
3. 完整性门禁：抽样校验 `content_sha256` 全部匹配；
4. 运维门禁：备份可用且恢复演练通过；
5. 审批门禁：负责人签字确认（以本文件版本为准）。

> 注释：一次性切换采用“全有或全无”原则，不使用灰度/双写过渡。

## 6. 非目标（v1）

- 不定义灰度切换策略；
- 不定义多版本并行写入；
- 不引入本文件之外的第二规范源。
