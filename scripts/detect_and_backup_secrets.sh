#!/usr/bin/env bash
# dry-run capable script: 搜索常见敏感文件/关键词并在发现时将备份 copy 移到 /home/bgzo/.trash.bak
# 不会自动提交到 git。默认以 dry-run 模式运行，使用 --run 才会执行移动。

DRY_RUN=1
if [ "$1" == "--run" ]; then
  DRY_RUN=0
fi

WORKDIR="/home/bgzo/.openclaw/workspace"
TRASH_BAK="/home/bgzo/.trash.bak"

mkdir -p "$TRASH_BAK"

# 常见敏感文件和模式
PATTERNS=(".env" "id_rsa" "id_ed25519" "PRIVATE_KEY" "API_KEY" "SECRET=" "TOKEN=")

found=()
for p in "${PATTERNS[@]}"; do
  matches=$(grep -RIl --exclude-dir=.git --exclude-dir=node_modules --binary-files=without-match "$p" "$WORKDIR" 2>/dev/null || true)
  if [ -n "$matches" ]; then
    while IFS= read -r f; do
      found+=("$f")
    done <<< "$matches"
  fi
done

if [ ${#found[@]} -eq 0 ]; then
  echo "No suspected sensitive files found."
  exit 0
fi

echo "Found suspected sensitive files:" 
for f in "${found[@]}"; do
  echo " - $f"
done

if [ $DRY_RUN -eq 1 ]; then
  echo "Dry-run mode: no files will be moved. To execute moving, run: $0 --run"
  exit 0
fi

# 执行移动
for f in "${found[@]}"; do
  base=$(basename "$f")
  ts=$(date +%Y%m%d%H%M%S)
  dest="$TRASH_BAK/${base}.$ts.bak"
  echo "Moving $f -> $dest"
  mv "$f" "$dest"
done

echo "Backup complete. Notifying user..."
# TODO: hook to notification (telegram) — currently just stdout
