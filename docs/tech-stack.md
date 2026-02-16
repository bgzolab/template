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

