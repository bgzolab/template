#!/usr/bin/env bash
# 把 opencode CI 的 deny 规则与只读 agent 写到全局配置
# （~/.config/opencode/opencode.json），不要写进仓库目录：opencode 结束时会对
# 「变脏的工作区」执行 git add/commit/push，写进仓库会把自己提交上去。
# review / comment 两个 workflow 共用本脚本，避免安全策略各自漂移。
set -euo pipefail

mkdir -p "$HOME/.config/opencode"
cat > "$HOME/.config/opencode/opencode.json" <<'EOF'
{
  "$schema": "https://opencode.ai/config.json",
  "default_agent": "ci-readonly",
  "permission": {
    "bash": {
      "*": "allow",
      "rm *": "deny",
      "rmdir *": "deny",
      "shred *": "deny",
      "truncate *": "deny",
      "git commit": "deny",
      "git commit *": "deny",
      "git * commit*": "deny",
      "*git commit*": "deny",
      "git push": "deny",
      "git push *": "deny",
      "git * push*": "deny",
      "*git push*": "deny"
    },
    "read": "allow",
    "edit": "deny",
    "glob": "allow",
    "grep": "allow",
    "list": "allow",
    "task": "allow",
    "external_directory": "allow",
    "todowrite": "allow",
    "question": "deny",
    "webfetch": "allow",
    "websearch": "allow",
    "lsp": "allow",
    "doom_loop": "allow",
    "skill": "allow"
  },
  "agent": {
    "ci-readonly": {
      "description": "Read-only CI agent: never writes to the repository",
      "mode": "primary",
      "prompt": "This environment is read-only. Never create, edit, move or delete repository files, including via shell redirection or in-place edits (e.g. '>', '>>', 'tee', 'sed -i', 'cat >', python writes). If code changes are needed, describe them or show a diff in your reply. Never run git commit or git push. Never ask the user questions; there is no one to answer in CI.",
      "tools": {
        "write": false,
        "edit": false,
        "patch": false
      }
    },
    "ci-finalize": {
      "description": "Final-turn CI agent: no tools at all, must summarize the review from session history",
      "mode": "primary",
      "steps": 1,
      "prompt": "You are in the final turn of a timed review: produce the review verdict from the session history only. You have no tools; never attempt a tool call, never read files and never run commands. Obey the user's finalization instruction and finish with a line exactly `结论：LGTM` or `结论：BLOCK`.",
      "tools": {
        "write": false,
        "edit": false,
        "patch": false,
        "bash": false,
        "read": false,
        "glob": false,
        "grep": false,
        "list": false,
        "task": false,
        "webfetch": false,
        "websearch": false,
        "todowrite": false,
        "lsp": false,
        "skill": false
      }
    }
  }
}
EOF
