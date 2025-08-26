# Export your data into Obsidian

## Roadmap

只做导出，不做删除；因为如果未来有拓展需求，可以重复导出，否则你的数据将会面临永久丢失的风险。

## Feature

- 增量导出

## Quick Start

```python
pipx install export_to_obsidian
```

## Scope

- [x] 博客园
- [x] Bangumi
- [ ] Social Media Fed
- [ ] V2ex
- [ ] Zhihu
- [ ] Weibo

## Examples

### 博客园

```python
export CNBLOG_ACCESS_TOKEN=xxx
eto cnblog --output output/cnblog
#debug
python3 ./export_to_obsidian.py cnblog --output output/cnblog
```

### Bangumi

```python
export BGM_ACCESS_TOKEN=xxx
eto bangumi -t ./config/bangumi_template.md -s 1 -o output/bangumi
# debug
python3 ./export_to_obsidian.py bangumi -t ./config/bangumi_template.md -s 1 -o output/bangumi
python3 ./export_to_obsidian.py bangumi -t ./config/bangumi_template.md -s 2 -c 3 -o output/bangumi --force
```

## Alternatives

- Telegram via: https://github.com/bGZo/telegram-message-sync-bot
- Snipd via: https://github.com/bGZo/snipd-podcast-format-for-obsidian


## License

All code is licensed under the AGPL-3.0 license.
