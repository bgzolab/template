<!--02.技术栈选择与规范
生成一套规则来正确引导大模型，包括但不限于：

1. 输出最简单但最健壮的技术栈；
2. 注重模块化（多文件）和禁止单体巨文件（monolith）
3. 写任何代码前必须完整阅读 docs/@architecture.md（包含完整数据库结构）
4. 写任何代码前必须完整阅读 docs/@design-document.md
5. 每完成一个重大功能或里程碑后，必须更新 docs/@architecture.md
-->

# 技术栈选择与规范

## 当前技术栈选择

- Golang
- Gorm
- Sqlite
- Telebot
- CLI
  - https://github.com/spf13/cobra
- Social media API
  - Twitter
    - http://github.com/michimani/gotwi
  - Mastodon
    - http://github.com/mattn/go-mastodon
  - BlueSky
    - http://github.com/reiver/go-atproto

## 配置生效矩阵（2026-02）

> 目标：明确 `config/config.yaml` 字段是否被当前代码消费，降低“配置写了但不生效”的认知成本。

| 配置路径 | 当前状态 | 消费位置（代码） | 说明 |
|---|---|---|---|
| `token` | 生效 | `main.go` -> `start(globalConfig.Token)` | Telegram Bot 启动凭据 |
| `output.json` | 生效 | `main.go` -> `if globalConfig.Output.JSON { persistJSON(update) }` | 控制是否输出原始 JSON |
| `output.json_dir` | 生效 | `main.go` -> `persistJSON()` | JSON 输出目录 |
| `output.person_dir` | 生效 | `internal/service/archiveservice/service.go` -> `PersistMessage()` | 私聊消息 Markdown 存档目录 |
| `output.channel_dir` | 生效 | `internal/service/archiveservice/service.go` -> `PersistMessage()` | 频道消息 Markdown 存档目录 |
| `log.enable` | 未生效（预留） | 无直接消费 | 当前仅使用 `log.dir` 初始化日志 |
| `log.dir` | 生效 | `internal/service/bootstrapservice/service.go` -> `InitRuntime()` | 日志与 SQLite 路径基准目录 |
| `template.dir` | 生效 | `internal/service/archiveservice/service.go` -> `PersistMessage()` | Markdown 模板文件路径 |
| `targetUserList` | 生效 | `internal/service/notifyservice/service.go` -> `ResolveTargetChatIDs()` | 通知目标用户列表，空时回退消息来源聊天 |
| `pipeline.executionMode` | 生效（默认串行） | `internal/service/pipelineservice/service.go` -> `ResolveExecutionMode()` + `main.go` -> `SetExecutionMode()` | Pipeline 执行模式开关（`serial`/`async_experimental`） |
| `socialMediaSync.enable` | 生效 | `internal/service/syncservice/service.go` -> `ShouldSync()` | 社媒同步总开关 |
| `socialMediaSync.targetChannel` | 生效 | `internal/service/syncservice/service.go` -> `ShouldSync()` + `ContainsExactTarget()` | 频道精确匹配触发同步 |
| `socialMediaSync.mastodon.*` | 生效 | `pkg/SocialMediaUtils/Mastodon.go` | Mastodon 同步配置 |
| `socialMediaSync.twitter.*` | 生效 | `pkg/SocialMediaUtils/Twitter.go` | Twitter 同步配置 |
| `socialMediaSync.bluesky.*` | 生效 | `pkg/SocialMediaUtils/BlueSky.go` | BlueSky 同步配置 |
| `notification.*` | 废弃（目标删除） | 无直接消费 | 历史遗留配置，不再作为设计目标 |

## 配置治理规则

1. 文档默认以 `config/config.yaml` 为唯一配置源；
2. 新增配置项必须同步更新本矩阵，否则视为未完成；
3. 废弃配置项必须在矩阵中标注“废弃”并给出迁移/删除状态；
4. 每次里程碑发布后，需同步更新 `docs/architecture.md` 与 `docs/progress.md`。

## 重构执行规范（2026-02）

1. 公共数据结构统一沿用 `internal/Entity`，禁止平行定义重复实体；
2. 去重策略以数据库唯一约束为第一防线，应用层判重作为补偿；
3. 执行模型按“串行 -> 异步”分阶段演进，禁止一步到位切换；
4. 入口层（CLI/启动）只做装配，不承载归档与同步业务逻辑；
5. 模块边界遵循单职责原则：Archive、Sync、Notify 不混写在同一模块；
6. 每个重构步骤必须绑定独立测试（执行方式 + 通过标准 + 失败处理）；
7. 新增平台必须通过 Provider/适配层扩展，禁止修改核心 pipeline 主干；
8. 单文件建议不超过 300 行，如无必要，超限必须拆分并记录拆分理由；
9.  每个关键函数（主要指抽离出来的业务模块函数）必须添加函数注释，至少说明“做什么、为什么这么做”，优先使用中文；测试函数可不强制。
10. 阶段2准入采用“10项清单全通过”门禁，未通过不得进入代码改造。

## 阶段门禁说明

- P0（文档落地）完成后，需验证：实施计划、技术规范、进度记录、架构洞察四份文档均已更新；
- 仅在“9项清单全通过 + 用户批准”后，允许启动 P1（代码结构拆分）。

## Pipeline 模式切换运行说明（2026-02）

### 配置示例

在 `config/config.yaml` 中设置：

- `pipeline.executionMode: serial`（默认，稳定）
- `pipeline.executionMode: async_experimental`（实验）

### 启动方式

沿用既有命令：

- `./tg sync -c ./config/config.yaml`

程序会在启动后按 `pipeline.executionMode` 解析执行模式；未知值会自动回退到 `serial`。

## 最小端到端回归清单（Pipeline 模式）

1. **配置解析回归**
  - 将 `pipeline.executionMode` 设为 `serial`，确认可正常启动。
2. **实验模式等价回归**
  - 将 `pipeline.executionMode` 设为 `async_experimental`，确认同一输入消息下输出行为与 `serial` 等价（归档、同步通知数量、通知顺序一致）。
3. **未知模式回退回归**
  - 将 `pipeline.executionMode` 设为未知值（如 `foo`），确认自动回退串行且不报致命错误。
4. **同步关闭分支回归**
  - 配置 `socialMediaSync.enable: false`，确认仍产生归档通知且同步通知为“跳过原因”。
5. **目标频道未命中回归**
  - 保持 `socialMediaSync.enable: true`，发送非目标频道消息，确认不触发平台分发，仅输出跳过通知。
6. **核心模块测试回归**
  - 执行：`go test ./internal/service/pipelineservice ./internal/service/bootstrapservice ./internal/service/notifyservice ./internal/service/archiveservice ./internal/service/syncservice ./internal/Database`

## 发布前检查模板

- 可复用模板见 [docs/pre-release-regression-checklist.md](docs/pre-release-regression-checklist.md)
- 每次准备发布前，建议复制一份模板并填写“基本信息 + 结果记录 + 审核与发布”。

