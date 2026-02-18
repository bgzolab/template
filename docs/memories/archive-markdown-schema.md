<!--
规范定位：
1) 本文件是归档结构唯一规范源；
2) 其他文档只能引用，不能复制并改写本规范；
3) 规则变更必须先改本文件，再同步引用文件。
-->

# Archive Markdown Schema（唯一规范源）

## 1. 规范标识

- NormativeSource: `docs/memories/archive-markdown-schema.md`
- Version: `md`
- Scope: Telegram 消息归档到 Markdown 的最小字段强一致规范

## 2. 目录与分桶规则（来源优先 + 按消息存档）

- 分桶优先级：按来源分桶（`channel` / `person`）。
- 路径规则：`<base_dir>/<source_bucket>/<source_id>/<message_id>.md`
- `message_id`：固定使用 Telegram `message_id`。
- `source_id` 规则：
  1) 优先频道 username；
  2) 没有 username 时使用 chat_id 字符串（例如 `-1002509087128`）；
  3) 统一小写；
  4) 最大长度 128，超限直接报错并进入通知阶段。

> 注释：路径中的 `source_bucket/source_id/message_id` 必须与 Front Matter 一致。

## 3. Front Matter 必填字段（最小强一致）

以下字段为必填，缺任一字段即视为无效归档记录：

1. `schema_version`（固定值：`md`）
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
2. 路径一致：文件所在 `source_bucket/source_id/message_id` 与 Front Matter 一致；
3. 内容一致：`content_sha256` 必须匹配写入正文；
4. 版本一致：`schema_version != md` 视为不合规。

## 5. 一次性切换阈值（One-shot Cutover Threshold）

### 5.1 这是什么（What）

一次性切换阈值是“是否允许单次切换到新归档结构”的门禁集合。

### 5.2 为什么需要（Why）

防止在准备不足时做不可逆切换，避免出现批量不一致或回滚困难。

### 5.3 如何判定（How）

只有以下门禁 **全部通过**，才允许 Go；否则 No-Go：

1. 功能门禁：核心链路回归通过（归档/同步/通知关键路径）；
2. 数据门禁：必填字段完整 + `(chat_id, message_id)` 无冲突；
3. 完整性门禁：迁移后双向核对通过（仅比较 `(chat_id, message_id)`）；
4. 运维门禁：旧归档删除前已生成备份 `archives/260218-old-markdown-archives.zip`；
5. 审批门禁：负责人签字确认（以本文件版本为准）。

> 注释：一次性切换采用“全有或全无”原则，不使用灰度/双写过渡。

## 6. 切换期读写与迁移策略

1. 写入：直接写新路径 `source_id/message_id.md`；
2. 读取：先读新路径，读不到再读旧路径 `source_id.md`；
3. 迁移：以数据库为主，一次性全量补齐本地（已存在跳过、缺失补齐）；
4. 迁移范围：仅 `archives` 下规范文件；
5. 迁移完成后：删除旧模式单文件（删除前必须已完成 zip 备份）；
6. 迁移中出现约束错误：必须将具体报错原因传递给通知阶段。

## 7. 非目标

- 不定义灰度切换策略；
- 不定义多版本并行写入；
- 不引入本文件之外的第二规范源。
