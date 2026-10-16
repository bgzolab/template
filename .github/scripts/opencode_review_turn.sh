#!/usr/bin/env bash
# 在既有 opencode 审查会话上追加一个「续跑 / 收尾」回合，并把该回合最后一条
# 助手消息提取成 markdown，供 workflow 作为 PR 评论发布。
#
# 用法：opencode_review_turn.sh <phase> <session_id> <events_json> <text_md>
#   phase=continue  继续审查（普通只读 agent，默认 25 分钟预算）
#   phase=finalize  最后通牒（无工具 agent，默认 15 分钟预算，必须立刻给结论）
#
# 退出码：
#   0  提取到的正文含 `结论：` 签名，可直接作为正式审查评论发布
#   1  回合结束或被强杀，但没有结论签名（text_md 里可能有部分文本可供补救）
#   2  参数/环境错误
#
# 注意：调用方必须先把本脚本复制到工作区之外（RUNNER_TEMP）：opencode 可能切换
# git 分支，脚本自身不能放在会被切走的目录里；通用权限配置脚本同理。
set -uo pipefail

phase="${1:?phase required}"
session_id="${2:?session id required}"
events_file="${3:?events output path required}"
text_file="${4:?text output path required}"

CONTINUE_PROMPT='时间预算提醒：这是同一个审查会话的续跑，此前还没有给出最终审查，本轮最多再给 __BUDGET__。

要求：
1. 立即继续完成这个 PR 的审查，优先覆盖尚未审查的文件、模块和审查维度；继续使用工具阅读代码、检查 diff 和上下文。
2. 发现的问题按原要求记录：P0/P1 为阻塞、P2 为非阻塞，每条包含 文件:行号、问题、原因、修复建议，使用简体中文。
3. 只有当你判断审查已经完整时，才直接输出完整最终审查（同样要包含「未审核到位」小节，全部覆盖则写「无」），并让最后一行恰好是 `结论：LGTM` 或 `结论：BLOCK`。
4. 如果本轮无法审完，不要写计划或进度总结，把剩余时间继续用于审查；后续会有收尾回合强制输出结论。'

FINALIZE_PROMPT='最后通牒：审查时间预算已经全部用尽。现在必须立刻停止剩余的审查工作：不要调用任何工具，不要阅读或查找任何文件，不要再做新的探索。

仅基于本会话里已经完成的审查工作，立即输出最终审查：
1. 按原要求列出已发现的问题（P0/P1 为阻塞、P2 为非阻塞；每条包含 文件:行号、问题、原因、修复建议；简体中文）。
2. 必须单独写出「未审核到位」小节：明确说明哪些文件、模块或审查方面没有来得及覆盖；如果全部覆盖则写「无」。
3. 最后一行必须恰好是 `结论：LGTM` 或 `结论：BLOCK`；只要存在 P0/P1 就必须 BLOCK。
4. 不要以计划、状态说明或后续安排结尾，直接给出最终审查。'

case "${phase}" in
  continue)
    agent="${CONTINUE_AGENT:-ci-readonly}"
    default_timeout="25m"
    prompt="${CONTINUE_PROMPT}"
    ;;
  finalize)
    agent="${FINALIZE_AGENT:-ci-finalize}"
    default_timeout="15m"
    prompt="${FINALIZE_PROMPT}"
    ;;
  *)
    echo "unknown phase: ${phase}" >&2
    exit 2
    ;;
esac

: "${MODEL:?MODEL is required}"
turn_timeout="${TURN_TIMEOUT:-${default_timeout}}"

# 提示语里的预算必须和实际 timeout 一致：只接受 <分钟>m / <小时>h，
# 其它形态（1h30m、1.5h、90s 等）直接快速失败，避免算出无意义甚至错误的预算。
if [[ ! "${turn_timeout}" =~ ^[0-9]+[mh]$ ]]; then
  echo "unsupported TURN_TIMEOUT '${turn_timeout}': expected <minutes>m or <hours>h" >&2
  exit 2
fi
case "${turn_timeout}" in
  *h) turn_budget_label="$((${turn_timeout%h} * 60)) 分钟" ;;
  *m) turn_budget_label="${turn_timeout%m} 分钟" ;;
esac
prompt="${prompt//__BUDGET__/${turn_budget_label}}"

# VARIANT 只被 github handler 读取，opencode run 需要显式传 --variant；
# 未设置时不传，避免空值触发 VariantUnavailableError。
# （${arr[@]+...} 写法兼容 bash 3.2/macOS 本地测试时的 set -u）
variant_args=()
if [ -n "${VARIANT:-}" ]; then
  variant_args=(--variant "${VARIANT}")
fi

# timeout 负责在预算内强杀（先 SIGTERM，20s 后 SIGKILL）：即使 provider 卡死，
# 脚本也能继续解析已经落盘的 JSON 事件流并尽量补救。124/137 是强杀的预期结果。
timeout -k 20s "${turn_timeout}" \
  opencode run \
    --session "${session_id}" \
    --model "${MODEL}" \
    ${variant_args[@]+"${variant_args[@]}"} \
    --agent "${agent}" \
    --auto \
    --format json \
    "${prompt}" \
  > "${events_file}" 2> "${events_file}.err"
turn_status=$?

if [ "${turn_status}" -ne 0 ] && [ "${turn_status}" -ne 124 ] && [ "${turn_status}" -ne 137 ]; then
  echo "opencode run exited with ${turn_status}; salvaging any text already emitted" >&2
  # 尤其需要看 provider 的原始报错（鉴权失败、限流、variant 不可用等）
  tail -n 20 "${events_file}.err" >&2 || true
fi

# 事件流里 text part 只在完成时（time.end）输出一次；取最后一条「含文本的助手
# 消息」，把它的多个 text part 按顺序拼起来。被 timeout 截断的半行 JSON 直接忽略。
python3 - "${events_file}" > "${text_file}" <<'PY'
import json
import sys

path = sys.argv[1]
texts = {}
order = []
try:
    with open(path, encoding="utf-8", errors="replace") as events:
        for line in events:
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("type") != "text":
                continue
            part = event.get("part") or {}
            text = (part.get("text") or "").strip()
            if not text:
                continue
            message_id = part.get("messageID") or ""
            if message_id not in texts:
                texts[message_id] = []
                order.append(message_id)
            texts[message_id].append(text)
except FileNotFoundError:
    pass
except Exception as exc:
    print(f"failed to parse {path}: {exc}", file=sys.stderr)
    raise

if order:
    sys.stdout.write("\n\n".join(texts[order[-1]]))
PY
parse_status=$?

# 解析失败不能和「确实没有结论」混为一谈：明确指出是事件流处理出了问题
if [ "${parse_status}" -ne 0 ]; then
  echo "failed to parse the opencode event stream (python exit ${parse_status}); events file: ${events_file}" >&2
  tail -n 20 "${events_file}.err" >&2 || true
  exit 1
fi

if [ -s "${text_file}" ]; then
  echo "extracted $(wc -c < "${text_file}" | tr -d ' ') bytes of assistant text"
fi

if ! grep -q '结论：' "${text_file}"; then
  echo "no 结论： signature in the extracted assistant text" >&2
  exit 1
fi

# 收尾输出必须交代覆盖范围；模型漏掉时补一条显式提示，避免「看起来全审完了」。
if ! grep -q '未审核到位' "${text_file}"; then
  printf '\n\n---\n\n> ⚠️ 本次收尾输出没有按要求列出「未审核到位」的范围，无法确认审查覆盖率，请人工复核。\n' >> "${text_file}"
fi

exit 0
