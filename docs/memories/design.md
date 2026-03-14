# 项目设计

## 前置要求：设计原则

1. 目标：给后续 agent 提供「可执行、可验证、可迭代」的上下文。
2. 要求：先做最小可用版本（MVP），不要过度设计；所有章节都要能直接映射为任务。

# Export all data into Obsidian

All data is your asset, you should own it. This tool helps you export data from various platforms into markdown files that can be easily imported and managed by Obsidian.

## Core Design

Only export, no deletion; because if there are expansion needs in the future, you can export repeatedly, otherwise your data will face the risk of permanent loss.

## Alternatives

- Telegram via: https://github.com/bGZo/telegram-message-sync-bot
- Snipd via: https://github.com/bGZo/snipd-podcast-format-for-obsidian/
