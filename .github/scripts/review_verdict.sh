#!/usr/bin/env bash
#
# Prints the id of the review verdict comment posted by this run, if one exists.
#
# A verdict comment must be:
#   - authored by github-actions[bot],
#   - created after the run started (a stale comment from an earlier run does
#     not count),
#   - containing the `结论：` verdict signature, and
#   - linking back to this run in its footer (`/actions/runs/<run id>`), so a
#     comment from a cancelled run that lands late cannot satisfy the check.
#
# Exits non-zero when the lookup itself fails, so callers can fail closed.

set -euo pipefail

pr_number="$1"
run_started_at="$2"

for attempt in 1 2 3; do
  if output=$(gh api \
    "repos/${GITHUB_REPOSITORY}/issues/${pr_number}/comments?per_page=100&sort=created&direction=desc" \
    --jq ".[] | select(.user.login == \"github-actions[bot]\" and .created_at >= \"${run_started_at}\" and (.body | contains(\"结论：\")) and (.body | contains(\"/actions/runs/${GITHUB_RUN_ID}\"))) | .id"); then
    echo "${output}"
    exit 0
  fi

  if [ "$attempt" -lt 3 ]; then
    echo "verdict lookup attempt ${attempt} failed; retrying" >&2
    sleep 2
  else
    echo "verdict lookup failed after ${attempt} attempts" >&2
  fi
done

exit 1
