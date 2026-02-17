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

- [x] 2026-02-16: 文档对齐：在设计与架构文档中同步“已知实现偏差（常驻）”小节。
    - [x] 已同步到 `docs/design-document.md`
    - [x] 已同步到 `docs/architecture.md`

- [x] 2026-02-16: 多模块重构 P0（文档先行）已落地。
    - [x] 完成 `docs/implementation-plan-refactor-multi-module.md`（重构阶段、步骤、验证、回滚、门禁）；
    - [x] 完成 `docs/tech-stack.md`（重构执行规范：Entity沿用、DB唯一约束优先、串行到异步分阶段）；
    - [x] 完成 `docs/architecture.md`（重构期文件职责与边界说明）；
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

### 已知实现偏差跟踪（常驻）

- [ ] 偏差-01：历史配置与运行实例中可能仍残留 `notification` 配置块，但当前代码未消费该配置。
- [x] 偏差-02：缺少统一“配置生效矩阵”文档，配置字段与运行行为对齐成本较高。（已在 `docs/tech-stack.md` 落地）
- [ ] 偏差-03：社媒平台错误处理目前为粗粒度结果反馈（成功/失败），尚未形成统一分级与重试策略。

