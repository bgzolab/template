# PRECOMMIT.md - Pre-commit setup & notes (Agent-facing prompts in English included)

Agent-facing summary (English)
- Purpose: Prevent accidental commits of secrets by scanning staged files for common sensitive patterns and blocking commits when suspicious content is detected.
- Short workflow: use lightweight local git hook for immediate protection; use pre-commit + detect-secrets for robust, long-term checks.

Files created (for review, not enabled):
- hooks/pre-commit.sample  - Lightweight git hook sample. Copy to .git/hooks/pre-commit and chmod +x to enable.
- .pre-commit-config.yaml  - pre-commit configuration using detect-secrets (baseline mode).
- .secrets.baseline         - placeholder baseline file for detect-secrets (update with scan).

Installation notes (agent-facing English commands)
1) Lightweight hook (manual):
   cp workspace/hooks/pre-commit.sample .git/hooks/pre-commit
   chmod +x .git/hooks/pre-commit

2) pre-commit + detect-secrets (recommended):
   python3 -m pip install --user pre-commit detect-secrets
   detect-secrets scan > .secrets.baseline   # review baseline and whitelist known items
   pre-commit install
   pre-commit run --all-files

Behavior notes (English)
- detect-secrets supports a baseline file to reduce false positives. Maintain the baseline after reviewing scan results.
- To temporarily bypass checks: git commit --no-verify (not recommended unless user explicitly allows).

User-facing notes (中文)
- 轻量级钩子已在 workspace/hooks/pre-commit.sample 提供。预配置不会自动启用，需用户手动安装。

(If you want, I can run a scan to generate a baseline; I will only run it after you confirm.)