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
| `output.person_dir` | 生效 | `main.go` -> `persistMessage()` | 私聊消息 Markdown 存档目录 |
| `output.channel_dir` | 生效 | `main.go` -> `persistMessage()` | 频道消息 Markdown 存档目录 |
| `log.enable` | 未生效（预留） | 无直接消费 | 当前仅使用 `log.dir` 初始化日志 |
| `log.dir` | 生效 | `main.go` -> `LogUtils.InitLogger(globalConfig.Log.Dir)` | 日志与 SQLite 路径基准目录 |
| `template.dir` | 生效 | `main.go` -> `persistMessage()` | Markdown 模板文件路径 |
| `targetUserList` | 生效 | `main.go` -> `defalutHandler()` | 通知目标用户列表，空时回退消息来源聊天 |
| `socialMediaSync.enable` | 生效 | `main.go` -> `shouldSyncToSocial()` | 社媒同步总开关 |
| `socialMediaSync.targetChannel` | 生效 | `main.go` -> `shouldSyncToSocial()` + `containsExactChannel()` | 频道精确匹配触发同步 |
| `socialMediaSync.mastodon.*` | 生效 | `pkg/SocialMediaUtils/Mastodon.go` | Mastodon 同步配置 |
| `socialMediaSync.twitter.*` | 生效 | `pkg/SocialMediaUtils/Twitter.go` | Twitter 同步配置 |
| `socialMediaSync.bluesky.*` | 生效 | `pkg/SocialMediaUtils/BlueSky.go` | BlueSky 同步配置 |
| `notification.*` | 废弃（目标删除） | 无直接消费 | 历史遗留配置，不再作为设计目标 |

## 配置治理规则

1. 文档默认以 `config/config.yaml` 为唯一配置源；
2. 新增配置项必须同步更新本矩阵，否则视为未完成；
3. 废弃配置项必须在矩阵中标注“废弃”并给出迁移/删除状态；
4. 每次里程碑发布后，需同步更新 `docs/architecture.md` 与 `docs/progress.md`。

