<!--04.记录已完成步骤：

每次完成一个步骤后，更新这个文件，记录已完成的步骤和下一步计划。这样可以清晰地看到项目的进展和未来的计划。
-->

# 进度记录

## 2025年存档（后补，可更新）

- [x] 2025-02-16: 完成了项目的初始设置，包括:
  - [x] 创建Telegram Bot；
  - [x] 设置Golang环境；
  - [x] 安装必要的依赖库；
  - [x] 完成基本消息存档;
  - [x] 机器人生死状态检测;
  - [x] 机器人日志支持
- [x] 2025-06-09: 存档功能加强；实现了CI的自动发布，打包分发到各个平台；
    - [ ] 特殊文本处理
        - [x] 适配链接、媒体等消息的存档；
        - [x] 按频道来源进行归档
        - [x] 存档反馈成败与否
        - [x] 内容替换：如#标签，否则会产生副作用
        - [x] 超文本格式支持
        - [x] EMOJI 特殊处理
        - [ ] 更多消息格式支持（下划线/加粗文本）
    - [ ] 支持时间排序/倒叙
    - [x] 支持自定义模板
    - [x] 输出 MD YAML header
- [x] 2025-08-09: 实现了社交媒体同步功能，支持将Telegram消息同步到：
	- [x] 同步 Mastodon
	- [x] 同步 BlueSky
	- [x] 同步 Twitter
	- [ ] 连接 Threads
	- [ ] 同步 [Planet](https://staging.v2ex.com/planet)
	- [ ] 更多社交媒体
	- [ ] Instagram
    - [ ] Facebook
    - [ ] Thread
    - [ ] Reddit
    - [ ] Okjike
    - [ ] Douyin
    - [ ] Coolapk
    - [ ] V2Ex
	- [ ] Douban
    - [ ] Jike
    - [ ] Weibo
    - [ ] Zhihu
    - [ ] Bilibili
    - [ ] Xiaohongshu
    - [ ] Tiktok
    - [ ] Kuaishou
	- [ ] 展示社交媒体同步后的消息链接
- [ ] Twitter和Mastodon平台。
- [x] 2025-08-10: 实现了数据库SQLITE的存储。
- [ ] 后台运行
    - [x] NOHUB 运行
    - [ ] SYSTEMCTL 运行
- [ ] Dockerfile

## 2026年进度

- [x] 2026-02-19: 代码阶段步骤4完成（旧单文件备份与删除，先备份后删除）。
    - [x] 新增 `BackupAndDeleteLegacySingleFiles()`：扫描 `person/channel` 根目录下旧单文件 `source_id.md`；
    - [x] 删除前强制生成备份 `archives/260218-old-markdown-archives.zip`（含 `person/*.md`、`channel/*.md` 条目）；
    - [x] 仅清理旧单文件，不影响新结构目录 `source_id/message_id.md`；
    - [x] 新增单元测试：备份+删除成功、无旧文件时跳过；
    - [x] 验证通过：`go test ./internal/service/archivemigrationservice ./internal/service/archiveservice ./internal/service/pipelineservice ./internal/Database`。

### 下一步（待你确认后执行）

- [ ] 执行端到端迁移演练：步骤2读兼容 + 步骤3补齐 + 步骤4备份删旧联调，并补充 Go/No-Go 记录。

- [x] 2026-02-19: 代码阶段步骤3完成（以 DB 为主全量补齐 + 迁移后核对）。
    - [x] 新增 `archivemigrationservice.BackfillFromDatabase()`：按数据库消息全量补齐 `source_id/message_id.md`；
    - [x] 已实现“已存在跳过、缺失补齐”行为；
    - [x] 已实现迁移后键集合核对（当前实现键为 `(source_id, message_id)`）；
    - [x] 新增迁移服务单元测试：补齐成功、已存在跳过、孤儿文件核对失败；
    - [x] 验证通过：`go test ./internal/service/archivemigrationservice ./internal/service/archiveservice ./internal/service/pipelineservice`。

### 下一步（待你确认后执行）

- [ ] 代码阶段步骤4：实现旧单文件 zip 备份与删除流程（删除前强制备份）。

- [x] 2026-02-19: 代码阶段步骤2完成（切换期读兼容：先新后旧）。
    - [x] `archiveservice` 去重读取链路已改为：先检查新路径 `source_id/message_id.md`；
    - [x] 新路径未命中时，已回退检查旧单文件 `source_id.md`；
    - [x] 新增并通过兼容读取单测（新路径命中、旧路径回退命中、双路径未命中）；
    - [x] 验证通过：`go test ./internal/service/archiveservice ./internal/service/pipelineservice`。

### 下一步（待你确认后执行）

- [ ] 代码阶段步骤3：实现全量补齐（以 DB 为主）与迁移后核对逻辑。

- [x] 2026-02-19: 已补充 Front Matter 生成逻辑与测试（步骤2前置完成）。
    - [x] 在 `archiveservice` 增加强制 Front Matter 生成逻辑（title/aliases/created/modified/comments/draft/description/source/tags）；
    - [x] 时间格式已固定为 `YYYY-MM-DDTHH:mm:ss`（无时区后缀）；
    - [x] 文本摘要规则已实现：先将 `\n` 替换为空格，再执行 50/100 截断，不足长度原样输出；
    - [x] `source` 在无可用链接时已支持空字符串；
    - [x] 新增并通过归档模块单元测试：`go test ./internal/service/archiveservice ./internal/service/pipelineservice`。

### 下一步（待你确认后执行）

- [ ] 开始代码阶段步骤2：实现切换期“先读新路径，读不到回退旧路径”并补测试。

- [x] 2026-02-19: Front Matter 强制模板需求已同步到规范与实施计划。
    - [x] 已在 `archive-markdown-schema.md` 增加强制模板字段定义与计算规则；
    - [x] 已明确时间格式 `YYYY-MM-DDTHH:mm:ss`（无时区后缀）；
    - [x] 已明确截断前换行归一化（`\n` 全部替换为空格）；
    - [x] 已明确 `source` 允许空字符串（person 场景）；
    - [x] 已在实施计划步骤1与步骤3追加对应验证项。

### 下一步（待你验收后执行）

- [ ] 代码阶段步骤2前，先补 Front Matter 生成逻辑单元测试用例清单，再做实现。

- [x] 2026-02-18: 代码阶段步骤1完成（仅归档写路径切换）。
    - [x] `archiveservice.ResolveSourceMeta()` 已将归档写路径切换为 `source_id/message_id.md`；
    - [x] 保持步骤边界：本轮未实现“读新回退旧”、未实现全量迁移与删旧；
    - [x] 已补充并更新归档相关单元测试（路径与文件名断言）；
    - [x] 验证通过：`go test ./internal/service/archiveservice ./internal/service/pipelineservice`。

### 下一步（待你验收后执行）

- [ ] 代码阶段步骤2：实现切换期“先读新路径，读不到回退旧路径”并补测试。

- [x] 2026-02-18: 归档改造改为“文档先行，代码后置”。
    - [x] 已先冻结归档规则：按消息存档 `source_id/message_id.md`；
    - [x] 已明确切换期策略：写新路径，读新失败回退旧路径；
    - [x] 已明确 `source_id` 规则：统一小写，最大长度 128，超限报错并传递到通知阶段；
    - [x] 已明确迁移策略：以数据库为主一次性全量补齐，旧单文件删除前先打包 `archives/260218-old-markdown-archives.zip`；
    - [x] 已明确核对口径：双向核对仅比较 `(chat_id, message_id)`；
    - [x] 已明确迁移范围：仅 `archives` 下规范文件。

### 下一步（待你确认后执行）

- [ ] 代码阶段步骤1（小步）：仅实现“归档写入路径切换到 `source_id/message_id.md`”并补对应单元测试；
- [ ] 暂不实现全量迁移命令与删旧逻辑，等步骤1验收通过后再进入步骤2。

- [x] 2026-02-18: 新增 LLM Prompt 模板并接入 memories 唯一入口。
    - [x] 新增 `docs/prompt-template.md`（通用实现 / 切换评审 / 文档更新 三类模板）；
    - [x] 更新 `docs/memories/index.md` 读取顺序，纳入 Prompt 模板入口；
    - [x] 默认交互策略固定为“先读 memories，再执行任务”。

- [x] 2026-02-18: LLM 文档治理最简方案落地（memories 唯一入口 + schema 唯一规范源）。
    - [x] 新增 `docs/memories/index.md` 作为唯一入口与冲突处理规则；
    - [x] 新增 `docs/memories/archive-markdown-schema.md` 并定义一次性切换阈值门禁；
    - [x] 新增 `docs/implementation-plans/implementation-plan-cutover-threshold.md`，包含强制字段 `NormativeSource/Version/OutOfScope`；
    - [x] 更新 `docs/memories/design-document.md` 与 `docs/memories/architecture.md` 仅做规范引用；
    - [x] 更新 `docs/pre-release-regression-checklist.md`，新增一次性切换结论记录项。


- [x] 2026-02-16: 文档对齐：在设计与架构文档中同步“已知实现偏差（常驻）”小节。
    - [x] 已同步到 `docs/memories/design-document.md`
    - [x] 已同步到 `docs/memories/architecture.md`

- [x] 2026-02-16: 多模块重构 P0（文档先行）已落地。
    - [x] 完成 `docs/implementation-plans/implementation-plan-refactor-multi-module.md`（重构阶段、步骤、验证、回滚、门禁）；
    - [x] 完成 `docs/memories/tech-stack.md`（重构执行规范：Entity沿用、DB唯一约束优先、串行到异步分阶段）；
    - [x] 完成 `docs/memories/architecture.md`（重构期文件职责与边界说明）；
    - [x] 明确阶段2准入：9项清单全通过 + 用户明确批准。

### 重构阶段门禁（阶段2前）

- [ ] 门禁-01：实施计划章节完整且无占位缺失；
- [ ] 门禁-02：冻结决策（Entity沿用/DB唯一约束优先/串行到异步）表述一致；
- [ ] 门禁-03：P0/P1/P2 路线清晰并含验证方式；
- [ ] 门禁-04：技术规范已落地并与实施计划一致；
- [ ] 门禁-05：技术规范明确去重优先数据库唯一约束；
- [ ] 门禁-06：技术规范明确执行模型串行到异步分阶段；
- [ ] 门禁-07：进度文档已记录本轮产出与下一步条件；
- [ ] 门禁-08：架构文档已补充重构期文件职责与边界；
- [ ] 门禁-09：用户已明确批准进入阶段2。

## 2026-02-16（阶段2-步骤1）

- [x] 完成“社媒同步模块化”第一步改造：
    - [x] 新增 `internal/service/syncservice`，抽离同步判定与分发逻辑；
    - [x] `main.go` 改为调用 `syncservice.ShouldSync()` 与 `syncservice.Dispatch()`；
    - [x] 保持现有通知语义（按平台返回成功/失败消息）。

- [x] 落实“数据库唯一约束优先”第一步：
    - [x] 为 `Entity.Message` 增加 `(MessageID, Username)` 复合唯一约束；
    - [x] `Database` 新增重复错误识别函数 `IsDuplicateMessageError()`；
    - [x] 持久化流程在入库重复时返回“消息已存在”。

- [x] 独立模块测试通过：
    - [x] `go test ./internal/service/syncservice`
    - [x] `go test ./internal/Database`

### 下一步（待你验收后执行）

- [ ] 阶段2-步骤2：拆分归档流程（`persistMessage`）为独立服务模块，继续保持串行执行并补齐模块测试。

## 2026-02-17（阶段2-步骤2）

- [x] 完成“归档流程模块化”第二步改造：
    - [x] 新增 `internal/service/archiveservice`，抽离来源解析、文本选择、模板渲染、落盘与入库编排；
    - [x] `main.go` 改为调用 `archiveservice.PersistMessage()`；
    - [x] 保持当前串行执行模型，不引入异步改造。

- [x] 独立模块测试通过：
    - [x] `go test ./internal/service/archiveservice`
    - [x] `go test ./internal/service/syncservice`
    - [x] `go test ./internal/Database`

### 下一步（待你验收后执行）

- [ ] 阶段2-步骤3：继续缩减 `main.go`（入口装配化），并将通知编排提取为独立模块，补齐对应测试。

## 2026-02-17（阶段2-步骤3）

- [x] 完成“通知编排模块化”第三步改造：
    - [x] 新增 `internal/service/notifyservice`，抽离通知目标解析与通知文案编排；
    - [x] `main.go` 改为调用 `notifyservice` 生成待发送消息；
    - [x] 保持当前串行执行模型，不引入异步改造。

- [x] 独立模块测试通过：
    - [x] `go test ./internal/service/notifyservice`
    - [x] `go test ./internal/service/archiveservice`
    - [x] `go test ./internal/service/syncservice`
    - [x] `go test ./internal/Database`

- [x] 入口文件持续瘦身：
    - [x] `main.go` 当前 172 行（满足单文件建议不超过 300 行）。

### 下一步（待你验收后执行）

- [ ] 阶段2-步骤4：继续拆分启动装配（初始化配置/日志/数据库）到独立模块，并补充对应测试。

## 2026-02-17（阶段2-步骤4）

- [x] 完成“启动装配模块化”第四步改造：
    - [x] 新增 `internal/service/bootstrapservice`，抽离配置加载与运行时初始化（日志/数据库）；
    - [x] `main.go` 改为调用 `bootstrapservice.LoadConfig()` 与 `bootstrapservice.InitRuntime()`；
    - [x] 保持当前串行执行模型，不引入异步改造。

- [x] 独立模块测试通过：
    - [x] `go test ./internal/service/bootstrapservice`
    - [x] `go test ./internal/service/notifyservice`
    - [x] `go test ./internal/service/archiveservice`
    - [x] `go test ./internal/service/syncservice`
    - [x] `go test ./internal/Database`

### 下一步（待你验收后执行）

- [ ] 阶段2-步骤5：引入 pipeline 编排骨架（仍保持串行），把主流程从 handler 进一步收敛为 stage 调度并补对应测试。

## 2026-02-17（阶段2-步骤5）

- [x] 完成“串行 pipeline 编排骨架”第五步改造：
    - [x] 新增 `internal/service/pipelineservice`，统一串行编排 archive -> sync -> notify；
    - [x] `main.go` 改为调用 `pipeline.ProcessUpdate()`，主流程仅保留日志与发送动作；
    - [x] 保持当前串行执行模型，不引入异步改造。

- [x] 独立模块测试通过：
    - [x] `go test ./internal/service/pipelineservice`
    - [x] `go test ./internal/service/bootstrapservice`
    - [x] `go test ./internal/service/notifyservice`
    - [x] `go test ./internal/service/archiveservice`
    - [x] `go test ./internal/service/syncservice`
    - [x] `go test ./internal/Database`

### 下一步（待你验收后执行）

- [ ] 阶段2-步骤6：基于 pipeline 抽离可替换 stage 接口（为异步化做准备），并补充回归测试与失败场景测试。

## 2026-02-17（阶段2-步骤6）

- [x] 完成“可替换 stage 接口”第六步改造：
    - [x] 在 `internal/service/pipelineservice` 中抽离 `ArchiveStage` / `SyncStage` / `NotifyStage` 接口；
    - [x] 增加默认 stage 实现并保持现有串行行为不变；
    - [x] `Pipeline` 改为通过 stage 接口编排流程，为后续异步化替换预留扩展点。

- [x] 回归与失败场景测试通过：
    - [x] 验证 stage 执行顺序回归（archive -> sync -> notify）；
    - [x] 验证同步关闭时仍执行通知阶段；
    - [x] 验证 `nil update` 时安全返回空结果。

- [x] 独立模块测试通过：
    - [x] `go test ./internal/service/pipelineservice`
    - [x] `go test ./internal/service/bootstrapservice`
    - [x] `go test ./internal/service/notifyservice`
    - [x] `go test ./internal/service/archiveservice`
    - [x] `go test ./internal/service/syncservice`
    - [x] `go test ./internal/Database`

### 下一步（待你验收后执行）

- [ ] 阶段2-步骤7：在不改业务语义前提下，为 pipeline 增加异步执行实验开关（仅骨架），并补充顺序一致性与回退测试。

## 2026-02-17（阶段2-步骤7）

- [x] 完成“异步执行实验开关骨架”第七步改造：
    - [x] 在 `pipelineservice` 新增执行模式 `serial` / `async_experimental`；
    - [x] 新增 `SetExecutionMode()` 作为模式切换入口；
    - [x] 默认仍为串行模式，保持现有业务语义不变。

- [x] 一致性与回退测试通过：
    - [x] 验证 `async_experimental` 与 `serial` 结果一致；
    - [x] 验证执行模式为空时自动回退到串行模式；
    - [x] 继续保持原有回归与失败场景测试通过。

- [x] 独立模块测试通过：
    - [x] `go test ./internal/service/pipelineservice`
    - [x] `go test ./internal/service/bootstrapservice`
    - [x] `go test ./internal/service/notifyservice`
    - [x] `go test ./internal/service/archiveservice`
    - [x] `go test ./internal/service/syncservice`
    - [x] `go test ./internal/Database`

### 下一步（待你验收后执行）

- [ ] 阶段2-步骤8：引入配置驱动的 pipeline 执行模式（默认串行），并补充“开关开启但行为等价”验证与文档说明。

## 2026-02-17（阶段2-步骤8）

- [x] 完成“配置驱动 pipeline 模式”第八步改造：
    - [x] 在 `internal/Entity/Config.go` 增加 `pipeline.executionMode` 配置字段；
    - [x] 在 `pipelineservice` 增加 `ResolveExecutionMode()`，未知值回退串行；
    - [x] `main.go` 改为按配置设置 pipeline 执行模式。

- [x] 等价性与回退测试通过：
    - [x] 验证配置模式解析（大小写兼容、未知值回退）；
    - [x] 验证配置开启 `async_experimental` 时与串行结果等价；
    - [x] 保持原有回归测试全部通过。

- [x] 独立模块测试通过：
    - [x] `go test ./internal/service/pipelineservice`
    - [x] `go test ./internal/service/bootstrapservice`
    - [x] `go test ./internal/service/notifyservice`
    - [x] `go test ./internal/service/archiveservice`
    - [x] `go test ./internal/service/syncservice`
    - [x] `go test ./internal/Database`

### 下一步（待你验收后执行）

- [ ] 阶段2-步骤9：补充配置示例与运行说明（如何切换 pipeline 模式），并增加最小端到端回归测试清单。

## 2026-02-17（阶段2-步骤9）

- [x] 完成“配置示例与运行说明”第九步改造：
    - [x] 在 `config/config.yaml` 增加 `pipeline.executionMode` 示例配置；
    - [x] 在 `README.md` 增加 Pipeline 模式切换说明；
    - [x] 在 `docs/memories/tech-stack.md` 增加模式切换运行说明。

- [x] 增加最小端到端回归清单：
    - [x] 在 `docs/memories/tech-stack.md` 增加 6 条最小回归清单（模式解析、等价性、回退、分支、测试命令）。

### 下一步（待你验收后执行）

- [ ] 阶段2-步骤10：按回归清单执行一次手工验证记录模板，沉淀为可复用发布前检查项。

## 2026-02-17（阶段2-步骤10）

- [x] 完成“发布前检查项模板化”第十步落地：
    - [x] 新增 `docs/pre-release-regression-checklist.md`，沉淀可复用回归记录模板；
    - [x] 在 `docs/memories/tech-stack.md` 增加模板入口与使用说明；
    - [x] 将配置/链路/测试/发布审核整合为统一检查表。

### 下一步（待你验收后执行）

- [x] 阶段2-步骤11：按模板执行一次真实发布前检查演练，并回填一份样例记录（可匿名）。

## 2026-02-17（阶段2-步骤11）

- [x] 完成“发布前检查演练与样例回填”第十一步落地：
    - [x] 基于模板生成样例记录：`docs/pre-release-regression-checklist-sample-2026-02-17.md`；
    - [x] 完成 1 轮模块回归测试并记录结果（`pipelineservice/bootstrapservice/notifyservice/archiveservice/syncservice/Database`）；
    - [x] 回填“结论/失败项/风险说明/处理建议”四项关键信息。

- [x] 本次演练结论：
    - [x] 模块级测试通过；
    - [x] 发布门禁暂不通过（尚未完成启动模式与关键链路手工验证）。

### 下一步

- [x] 阶段2实施计划链路（步骤1~11）已执行完毕；
- [x] 如需进入发布：补做端到端手工链路检查后，再执行“已确认可发布”；
- [x] 如当前仅以“计划闭环”为目标：本轮可停止。

### 已知实现偏差跟踪（常驻）

- [ ] 偏差-01：历史配置与运行实例中可能仍残留 `notification` 配置块，但当前代码未消费该配置。
- [x] 偏差-02：缺少统一“配置生效矩阵”文档，配置字段与运行行为对齐成本较高。（已在 `docs/memories/tech-stack.md` 落地）
- [ ] 偏差-03：社媒平台错误处理目前为粗粒度结果反馈（成功/失败），尚未形成统一分级与重试策略。

