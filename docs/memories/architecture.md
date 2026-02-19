<!--00.记录每个文件的作用-->

# 架构文档

## 文档作用

- 描述系统的核心处理链路与模块边界；
- 作为实现与设计对齐的事实基线；
- 记录“已知实现偏差”并持续追踪关闭状态。

## 文档入口与规范来源（最简）

1. 统一入口：`docs/memories/index.md`；
2. 归档规范唯一源：`docs/memories/archive-markdown-schema.md`；
3. 执行计划目录 `docs/implementation-plans/` 仅用于落地步骤，不定义架构行为。

> 注释：本文件不复写 schema 规则，只引用唯一规范源，避免多处漂移。

## 当前核心链路（简版）

1. Telegram Bot 接收消息；
2. 执行消息落盘（Markdown/JSON）与数据库写入；
3. 根据配置判定是否进入社媒同步；
4. 向目标用户发送处理结果通知。

## 配置驱动规则（冻结）

1. 配置源固定为 `config/config.yaml`；
2. 社媒同步规则由 `socialMediaSync.targetChannel` 控制；
3. 频道匹配策略为精确匹配；
4. 未命中同步规则时，行为为“日志 + 通知”。

## 重构期架构洞察（P0）

### 文件与目录职责（当前 + 目标）

1. `main.go`
   - 当前：入口 + 业务聚合（归档、同步、通知）；
   - 目标：仅保留 CLI 启动与依赖装配。

2. `internal/Entity`
   - 当前：承载配置与核心数据结构；
   - 目标：继续作为公共数据结构中心（冻结决策）。

3. `internal/Database`
   - 当前：数据库连接与持久化入口；
   - 目标：作为去重第一防线（数据库唯一约束优先）的落地点。

4. `pkg/SocialMediaUtils`
   - 当前：各平台同步实现（BlueSky/Mastodon/Twitter）；
   - 目标：逐步收敛为可替换的 provider/adapter 层。

5. `pkg/StrUtils` / `pkg/TgUtils`
   - 当前：文本处理与消息辅助逻辑；
   - 目标：保留为纯逻辑工具，避免混入 I/O 行为。

6. `docs/implementation-plans/implementation-plan-refactor-multi-module.md`
   - 作用：重构主计划与阶段门禁来源（阶段推进唯一依据）。

7. `docs/memories/tech-stack.md`
   - 作用：技术规范与配置生效矩阵，约束重构落地方式。

8. `docs/memories/progress.md`
   - 作用：阶段状态、门禁达成情况、已知偏差关闭记录。

### 分层演进方向

- P1：保持串行执行，先完成“归档/同步/通知”职责拆分；
- P2：在 P1 稳定后引入异步执行，保证行为一致与可回滚。

## 本轮改造后的新增文件作用（阶段2-步骤1）

1. `internal/service/syncservice/service.go`
   - 作用：承载“是否同步”纯逻辑判定与统一分发编排；
   - 边界：不直接依赖 Telegram I/O，不负责通知发送。

2. `internal/service/syncservice/providers.go`
   - 作用：将 BlueSky/Mastodon/Twitter 封装为可替换 Sender 适配器；
   - 边界：只负责平台调用，不处理策略判定。

3. `internal/service/syncservice/service_test.go`
   - 作用：验证同步策略与分发顺序，确保模块可独立测试；
   - 边界：使用假发送器，不触发真实外部网络调用。

4. `internal/Database/messages_test.go`
   - 作用：验证数据库唯一约束优先去重策略；
   - 边界：使用内存 SQLite，不依赖线上数据库文件。

5. `main.go`（本轮边界变化）
   - 变化：移除本地同步判定函数，改为调用 `syncservice`；
   - 意义：主流程开始从“平台细节耦合”向“服务编排”过渡。

## 本轮改造后的新增文件作用（阶段2-步骤2）

1. `internal/service/archiveservice/service.go`
   - 作用：承载归档主流程编排（来源解析、文本选择、模板渲染、文件落盘、数据库写入）；
   - 边界：对外提供 `PersistMessage()`，上层不再直接操作归档细节。

2. `internal/service/archiveservice/service_test.go`
   - 作用：验证归档模块纯逻辑（来源解析、文本选择、模板数据构建）；
   - 边界：不依赖 Telegram 网络与真实文件系统。

3. `main.go`（本轮边界变化）
   - 变化：归档改为调用 `archiveservice.PersistMessage()`，入口继续向装配层收敛；
   - 意义：归档与同步均已具备服务化入口，后续可继续拆分通知模块。

## 本轮改造后的新增文件作用（阶段2-步骤3）

1. `internal/service/notifyservice/service.go`
   - 作用：承载通知编排逻辑（目标聊天解析、归档通知构建、同步通知构建、批量消息展开）；
   - 边界：不直接执行 Telegram 发送，仅产出待发送消息列表。

2. `internal/service/notifyservice/service_test.go`
   - 作用：验证通知模块纯逻辑，确保通知策略可独立测试；
   - 边界：不依赖 bot 实例与网络 I/O。

3. `main.go`（本轮边界变化）
   - 变化：由 `notifyservice` 统一生成待发送消息，主流程只负责发送；
   - 意义：主入口进一步收敛为编排层，为后续“启动装配模块化”做准备。

## 本轮改造后的新增文件作用（阶段2-步骤4）

1. `internal/service/bootstrapservice/service.go`
   - 作用：承载启动装配逻辑（配置加载、日志初始化、数据库初始化）；
   - 边界：不参与消息处理业务，仅负责运行时依赖准备。

2. `internal/service/bootstrapservice/service_test.go`
   - 作用：验证配置加载与运行时初始化逻辑可独立测试；
   - 边界：使用临时目录，不依赖线上配置与固定环境。

3. `main.go`（本轮边界变化）
   - 变化：入口改为调用 `bootstrapservice.LoadConfig()` 与 `bootstrapservice.InitRuntime()`；
   - 意义：main 更接近“装配 + 启动”，为后续 pipeline 化主流程做准备。

## 本轮改造后的新增文件作用（阶段2-步骤5）

1. `internal/service/pipelineservice/service.go`
   - 作用：提供串行 pipeline 骨架，统一编排 archive -> sync -> notify 的处理顺序；
   - 边界：仅负责 stage 调度与结果聚合，不直接执行消息发送。

2. `internal/service/pipelineservice/service_test.go`
   - 作用：验证 pipeline 阶段顺序与分支行为（同步关闭时不分发）；
   - 边界：使用可注入函数替身，不依赖外部网络。

3. `main.go`（本轮边界变化）
   - 变化：默认处理器调用 `pipeline.ProcessUpdate()`，入口层只保留日志和消息发送；
   - 意义：主流程已从“手工串联服务”收敛为“可扩展编排骨架”。

## 本轮改造后的新增文件作用（阶段2-步骤6）

1. `internal/service/pipelineservice/service.go`
   - 变化：在 pipeline 内抽离 `ArchiveStage` / `SyncStage` / `NotifyStage` 可替换接口；
   - 意义：主流程从“函数注入编排”升级为“stage 接口编排”，为异步化与失败重试策略留出替换点。

2. `internal/service/pipelineservice/service_test.go`
   - 变化：增加回归与失败场景测试（顺序、同步关闭分支、nil update）；
   - 意义：保证重构后行为稳定，并验证失败场景下流程边界可控。

3. `main.go`（本轮边界变化）
   - 变化：仍只消费 `pipeline.ProcessUpdate()` 结果，无需感知 stage 细节；
   - 意义：入口层与执行策略进一步解耦，后续切换执行模型改动面更小。

## 本轮改造后的新增文件作用（阶段2-步骤7）

1. `internal/service/pipelineservice/service.go`
   - 变化：新增执行模式开关（`serial` / `async_experimental`）与 `SetExecutionMode()` 切换入口；
   - 意义：先提供异步化实验骨架，但默认串行，确保现有语义稳定。

2. `internal/service/pipelineservice/service_test.go`
   - 变化：新增“异步模式与串行模式结果一致”测试与“空模式回退串行”测试；
   - 意义：确保开关存在但不会引入行为漂移，支持后续安全演进。

3. `main.go`（本轮边界变化）
   - 变化：本轮无需改动，继续通过默认串行 pipeline 运行；
   - 意义：把执行策略演进限制在 pipeline 内部，降低入口层变更风险。

## 本轮改造后的新增文件作用（阶段2-步骤8）

1. `internal/Entity/Config.go`
   - 变化：新增 `pipeline.executionMode` 配置字段；
   - 意义：将 pipeline 执行策略切换从代码硬编码升级为配置驱动。

2. `internal/service/pipelineservice/service.go`
   - 变化：新增 `ResolveExecutionMode()` 统一解析模式并处理回退；
   - 意义：确保未知配置不会破坏行为，默认回退串行模式。

3. `main.go`（本轮边界变化）
   - 变化：在创建 pipeline 后按配置设置执行模式；
   - 意义：入口层仅负责读取配置并注入执行策略，保持语义稳定。

## 本轮改造后的新增文件作用（阶段2-步骤9）

1. `config/config.yaml`
   - 变化：新增 `pipeline.executionMode` 示例配置；
   - 意义：执行模式切换从“代码控制”升级为“配置可见、可操作”。

2. `docs/memories/tech-stack.md`
   - 变化：新增 Pipeline 模式切换运行说明与最小端到端回归清单；
   - 意义：把“如何切换”和“如何验证”标准化，降低后续维护成本。

3. `README.md`
   - 变化：新增 Pipeline 模式说明，便于快速上手；
   - 意义：外部开发者无需翻源码即可理解模式开关的基本用法。

## 本轮改造后的新增文件作用（阶段2-步骤10）

1. `docs/pre-release-regression-checklist.md`
   - 作用：提供发布前回归执行记录模板（配置检查、链路回归、测试回归、审核发布）；
   - 意义：把“回归清单”升级为“可追踪记录”，降低发布遗漏风险。

2. `docs/memories/tech-stack.md`
   - 变化：新增模板入口与使用说明；
   - 意义：让发布前检查流程有统一入口，减少沟通成本。

## 已知实现偏差（常驻）

> 本小节用于记录“架构目标与当前实现”的差异，修复后需在 `docs/memories/progress.md` 标注关闭。

### 偏差清单

1. 历史配置与运行实例中可能仍残留 `notification` 配置块，但当前代码未消费该配置；
2. 缺少统一“配置生效矩阵”文档，配置字段与运行行为对齐成本较高；
3. 社媒平台错误处理目前为粗粒度结果反馈（成功/失败），尚未形成统一分级与重试策略。

## 本轮新增架构洞察（2026-02-18：文档先行，切换前）

1. 归档路径模型已冻结为 `source_id/message_id.md`，并覆盖 `channel/person` 两个分桶。
2. 切换期链路职责：
   - 写入：只写新路径；
   - 读取：先新后旧；
   - 迁移：以 DB 为主，一次性全量补齐本地；
   - 删除：旧单文件必须在 zip 备份完成后再删除。
3. 迁移期错误传播：`source_id` 约束失败等错误必须可被通知阶段消费并展示具体原因。
4. 双向核对口径已冻结为 `(chat_id, message_id)`。

## 本轮新增架构洞察（2026-02-18：代码阶段步骤1）

1. `internal/service/archiveservice/service.go`
   - 变化：仅切换归档写入路径到 `source_id/message_id.md`；
   - 变化：`SourceMeta` 新增 `ArchiveRoot`，用于保持媒体资源仍写在来源分桶根路径；
   - 边界：本轮未实现读兼容（先新后旧）与迁移逻辑。

2. `internal/service/archiveservice/service_test.go`
   - 变化：补充路径断言，确保私聊与频道场景都落在 `source_id/message_id.md`；
   - 意义：先锁定步骤1行为，后续步骤在此基础上增量推进。

## 本轮新增架构洞察（2026-02-19：Front Matter 约束冻结）

1. 归档输出不再只要求“可写入”，还要求 Front Matter 模板字段完整输出；
2. 时间字段格式冻结为 `YYYY-MM-DDTHH:mm:ss`（无时区后缀）；
3. 标题/别名/描述的截断链路固定为：先 `\n` 归一化为空格，再做 `sub(0,50/100)`；
4. `source` 在 person 场景允许空字符串，channel 场景优先构造可访问链接。

## 本轮新增架构洞察（2026-02-19：Front Matter 逻辑落地）

1. `internal/service/archiveservice/service.go`
   - 变化：归档落盘前统一生成强制 Front Matter，并与模板正文拼接输出；
   - 变化：时间字段与持久化时间共享同一归档时间点，降低字段漂移风险；
   - 变化：摘要生成链路固定为“换行归一化 -> 截断 -> 组装字段”。

2. `internal/service/archiveservice/service_test.go`
   - 变化：新增 Front Matter 规则测试（字段完整性、时间格式、换行处理、空 source）；
   - 意义：为步骤2前提供稳定回归基线，避免后续兼容读取改造引入格式回退。
