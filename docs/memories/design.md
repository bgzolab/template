---
title: 项目设计
created: 2026-04-04
description: 给后续 LLM 提供「可执行、可验证、可迭代」的上下文。先做最小可用版本（MVP），不要过度设计；所有章节都要能直接映射为任务。。
tags: 
  - ai-notes
---

# VXNA Alternatives

This is a replace for https://www.v2ex.com/xna, because some reason:

1. No sensor, or small sensor;
2. More open, more transparent;

We can see the lastest blog been collected by v2ex is https://www.v2ex.com/xna/s/543. And the number of index(https://www.v2ex.com/xna) is just `472`.

So, where is those blog gone?

We don't know how they going, so there is it.


## How and what this works

1. We collect the blog urls from https://www.v2ex.com/xna daily, then we will give a specific opml file for those indiviual blogs.
2. Then we fetch those blogs every single 2 hours via github aciton, then output the articles title, url, date and description to api folder with json format.
3. In eariler verison, we don't provide a github page, just care about above workflow stable.




