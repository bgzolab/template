[![Contributors](https://img.shields.io/github/contributors/bGZo/playground.svg?style=for-the-badge)](https://github.com/bGZo/playground/graphs/contributors)
[![Forks](https://img.shields.io/github/forks/bGZo/playground.svg?style=for-the-badge)](https://github.com/bGZo/playground/network/members)
[![Stargazers](https://img.shields.io/github/stars/bGZo/playground.svg?style=for-the-badge)](https://github.com/bGZo/playground/stargazers)
[![Issues](https://img.shields.io/github/issues/bGZo/playground.svg?style=for-the-badge)](https://github.com/bGZo/playground/issues)
[![Licence](https://img.shields.io/github/license/bGZo/playground.svg?style=for-the-badge)](https://github.com/bGZo/playground/blob/template/LICENCE)
[![Telegram](https://img.shields.io/badge/-telegram-black.svg?style=for-the-badge&logo=telegram&colorB=555)](https://t.me/imbGZo)

# Export all your data into Obsidian

> Your data is your asset, you should own it. 

This tool exports your saved data to Markdown files for Obsidian.

- Export data from many sites into local Markdown files.
- Keep one simple CLI for all modules.
- Write an optional index file in Markdown.

Now this tool had supported following modules:

1. bangumi
2. bilibili
3. cnblog
4. qireader
5. v2ex
6. weibo
7. zhihu

## Quick start

You can install from PyPI:

```shell
pipx install export_to_obsidian
```

Or install from this repo:

```shell
pip install -e .
```

Put your token or cookie values in .env, then load them:

```shell
chmod +x ./export-env.sh
source ./export-env.sh
```

Main env vars used by the current modules:

- CNBLOG_ACCESS_TOKEN
- BGM_ACCESS_TOKEN
- QIREADER_COOKIE
- V2EX_ACCESS_TOKEN
- V2EX_COOKIE
- WEIBO_COOKIE
- ZHIHU_COOKIE
- BILIBILI_COOKIE

## Basic usage

```shell
eto <command> [options]
eto --index-file <path> <command> [options]
```

`--index-file` is a top-level option. Put it before the subcommand.

If you do not use `--index-file`, the index is printed to the terminal.
If you use `--index-file`, the index is written to one Markdown file.

## Command examples

### cnblog

```shell
eto cnblog -o output/cnblog
```

### bangumi

Use `config/bangumi_template.md` as the template file.

```shell
eto bangumi -t config/bangumi_template.md -s 1 -o output/bangumi
eto bangumi -t config/bangumi_template.md -s 2 -o output/bangumi
eto bangumi -t config/bangumi_template.md -s 3 -o output/bangumi
eto bangumi -t config/bangumi_template.md -s 4 -o output/bangumi
```

You can also set one collection type:

```shell
eto bangumi -t config/bangumi_template.md -s 2 -c 3 -o output/bangumi
```

### qireader

```shell
eto qireader -t your-tag -o output/qireader
```

### v2ex

```shell
eto v2ex -o output/v2ex
```

### zhihu

```shell
eto zhihu -c your-collection-id -o output/zhihu
```

### weibo

```shell
eto weibo -u your-user-id -o output/weibo
```

### bilibili

```shell
eto bilibili -f your-fav-id -o output/bilibili
```

## Index file

Example:

```shell
eto --index-file output/index/export-index.md zhihu -c your-collection-id -o output/zhihu
eto --index-file output/index/export-index.md bilibili -f your-fav-id -o output/bilibili
```

The file is grouped by module name.
One module keeps one `##` section.
Each export run adds one `###` block under that module.

Example output:

```markdown
## zhihu

### export index

- [[~zhihu-entry-1|First saved item]]
- [[~zhihu-entry-2|Second saved item]]

## bilibili

### export index

- [[~BV1xxxxxx|One saved video]]
```

<!--
## Vibe Coding

### GitHub copilot

Make sure to keep `.github/instructions` folder clean and simplest, or it may make context understanding and code generation worse, such as, `agent`, `instructions` and `prompts` should not conflict each other.

The **priority** of them should be like this:

Personal Instructions > Repository Instructions > Agent > Prompts > Your messages.

And get the template for GitHub Copilot from https://github.com/doggy8088/github-copilot-configs/tree/main/.github


## Common Steps:

- Read the documentation in `docs/memories` to understand the project structure, design and tech stack.
- Check the features in `docs/implementation-plans` to see if there are any questions or clarifications needed.
- Plan the simplest implementation steps in `docs/implementation-plans`, then list it append to the existing plans, and make every step clear enough for anyone to pick up and execute, and also make sure to include the verification steps for each implementation step.
- Then start implementation based on the plan step by step, and you should make sure keep these things:
  - Only when the verification steps are passed, you can move on to the next step, otherwise you should fix the problems until the verification steps are passed.
  - Link the related files, functions, or types in the codebase as much as possible, and also link the related plans if there are any. 
  - Make sure to record progress and what you have done in every step in the plan and things in other files.
  - Update the documents in `docs/memories` if there are any design changes or tech stack changes during the implementation.


## Roadmap

I use obdisian to manage roadmap of this project, and I will update it here when I have a clear plan for the next steps.

- [x] Add basic structure and files[^template-inspired].
- [x] Add Vibe coding support [^vibe-coding-inspired].

[^template-inspired]: Template inspired by https://github.com/kelseyhightower/nocode, https://github.com/othneildrew/Best-README-Template

[^vibe-coding-inspired]: https://github.com/tukuaiai/vibe-coding-cn

See the [open issues](https://github.com/bGZo/playground/issues) for a full list of proposed features (and known issues).
-->

## Output

Files are written as Markdown files in your output folder.
The project also writes front matter, so the files work well in Obsidian.


## Testing

Run all tests:

```shell
PYTHONPATH=src pytest tests -q
```

Run one test file:

```shell
PYTHONPATH=src pytest tests/test_utils.py -q
```

In VS Code, you can also use the debug and test settings in .vscode/launch.json.

## Contributing


Any contributions made are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'feat(module):add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Top contributors:

<a href="https://github.com/bGZo/playground/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=bGZo/playground" alt="contrib.rocks image" />
</a>

## License

All code is licensed under the AGPL-3.0 license. See `LICENSE` for more information.
