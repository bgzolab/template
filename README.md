# Export all your data into Obsidian

Your data is your asset, you should own it. This tool helps you export your data from various platforms into markdown files that can be easily imported and managed by Obsidian.


## Installation

```python
pipx install export_to_obsidian
```

## Use Case

Get your token or cookies from the target platform, then input in `.env.bak` and rename it to `.env`, source it via:

```shell
chmod +x ./export-env.sh
./export-env.sh
```

Then you coud run the command like below to export data to your local folder:


```python
# 博客园
eto cnblog --output output/cnblog
# Bangumi
eto bangumi -t ./config/bangumi_template.md -s 1 -o output/bangumi
```

## License

All code is licensed under the AGPL-3.0 license.
