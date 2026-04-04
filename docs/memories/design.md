---
title: 项目设计
created: 2026-04-04
modified: 2026-04-04T21:49:49
description: 给后续 LLM 提供「可执行、可验证、可迭代」的上下文。先做最小可用版本（MVP），不要过度设计；所有章节都要能直接映射为任务。
tags: 
  - ai-notes
---

# VXNA Alternatives

This is a replacement for https://www.v2ex.com/xna, for the following reasons:

1. No censor, or small censor;
2. More open, more transparent;

The latest blog collected by v2ex is https://www.v2ex.com/xna/s/543, yet the public index (https://www.v2ex.com/xna) only shows `472` entries. The 71 missing blogs — removed for unknown reasons — are exactly why this project exists.

## How it works

### Step 1: Discover blogs (OPML maintenance)

- Crawl https://www.v2ex.com/xna sequentially by index number (cumulative integers).
- For each index URL, if the response is **not 404**, parse the HTML page to extract the RSS/Atom feed URL from the `Feed 地址` table row.
- The program automatically maintains `config/rss.opml` with all discovered feed URLs.
- Each OPML entry stores: `title="[#N] Blog Title"`, `xmlUrl` (feed), `htmlUrl` (v2ex source page).
- **Incremental mode** (default, used by GitHub Actions): start from `max known index + 1` read from `htmlUrl` attributes; stop after `max_consecutive_404` consecutive 404s.
- **Full scan mode** (`--start-index 1`): used for the initial bootstrap run.

### Step 2: Fetch articles (every 2 hours via GitHub Actions)

- Read `config/rss.opml`, fetch all feeds.
- Aggregate all articles, sorted by date descending.
- Output to `api/{YYYY}/{MM}/{DD}.json`.

**JSON schema per file:**

```json
[
  {
    "title": "Article title",
    "url": "https://...",
    "date": "2026-04-04T08:00:00Z",
    "description": "Brief summary or excerpt"
  }
]
```

### Step 3: Update README (after each fetch)

- Read last 7 days of `api/` JSON files, deduplicate by URL, sort by date descending (newest first).
- Write results into the `## Last Week Blog` section of `README.md` as a Markdown table.

**Table format:**

| Date | Title | Summary |
| --- | --- | --- |
| YYYY-MM-DD | [title](url) | description (max 150 chars) |

### Error handling

- On fetch failure: print log and skip. No retry, no alert.

### MVP scope

- Deliverable: stable crawl + OPML update + JSON output pipeline.
- Acceptance: monitored by the maintainer for one month.




