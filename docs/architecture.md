<!--00.记录每个文件的作用-->

# 架构文档

## 文档作用

- 描述系统的核心处理链路与模块边界；
- 作为实现与设计对齐的事实基线；
- 记录“已知实现偏差”并持续追踪关闭状态。

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

6. `docs/implementation-plan-refactor-multi-module.md`
   - 作用：重构主计划与阶段门禁来源（阶段推进唯一依据）。

7. `docs/tech-stack.md`
   - 作用：技术规范与配置生效矩阵，约束重构落地方式。

8. `docs/progress.md`
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

## 已知实现偏差（常驻）

> 本小节用于记录“架构目标与当前实现”的差异，修复后需在 `docs/progress.md` 标注关闭。

### 偏差清单

1. 历史配置与运行实例中可能仍残留 `notification` 配置块，但当前代码未消费该配置；
2. 缺少统一“配置生效矩阵”文档，配置字段与运行行为对齐成本较高；
3. 社媒平台错误处理目前为粗粒度结果反馈（成功/失败），尚未形成统一分级与重试策略。
