[![Contributors](https://img.shields.io/github/contributors/bGZo/playground.svg?style=for-the-badge)](https://github.com/bGZo/playground/graphs/contributors)
[![Forks](https://img.shields.io/github/forks/bGZo/playground.svg?style=for-the-badge)](https://github.com/bGZo/playground/network/members)
[![Stargazers](https://img.shields.io/github/stars/bGZo/playground.svg?style=for-the-badge)](https://github.com/bGZo/playground/stargazers)
[![Issues](https://img.shields.io/github/issues/bGZo/playground.svg?style=for-the-badge)](https://github.com/bGZo/playground/issues)
[![Licence](https://img.shields.io/github/license/bGZo/playground.svg?style=for-the-badge)](https://github.com/bGZo/playground/blob/template/LICENCE)
[![Telegram](https://img.shields.io/badge/-telegram-black.svg?style=for-the-badge&logo=telegram&colorB=555)](https://t.me/imbGZo)

![Playground Name Screen Shot](https://img.bgzo.cc/2025/202508021439235.JPG)

# Playground

Here is a template repository for my projects. It contains a basic structure and some common files that I use in all my projects. You can use this template to create your own projects by forking it or cloning it.

## Getting Started

Before you start, make sure you have Git installed on your machine. You can download it from [here](https://git-scm.com/downloads).

## Getting Started

Before you start, make sure you have Git installed on your machine. You can download it from [here](https://git-scm.com/downloads).

```python
pipx install export_to_obsidian
```

Fetch the `template` branch from the remote repository:

```shell
git fetch origin template
```

Merge the `template` branch into your local repository to get started:

```shell
git merge origin/template --allow-unrelated-histories
```

## Usage

### 索引输出控制

所有导出子命令现在都支持统一的索引输出文件参数。

通用格式：

```shell
eto <subcommand> [subcommand options]
eto --index-file <index-file-path> <subcommand> [subcommand options]
```

必要说明：

- `--index-file` 是顶层参数，必须写在子命令前。
- 未指定 `--index-file` 时，索引会继续直接打印到控制台。
- 指定 `--index-file` 时，索引会输出为一个 Markdown 文件。
- 索引文件按模块分组，每个模块只有一个二级标题，例如 `## zhihu`、`## bilibili`。
- 同一个模块多次执行时，不会重复创建二级标题；新一轮导出内容会按执行顺序追加到该模块已有内容后面。
- 如果执行顺序是 `zhihu -> bilibili -> zhihu`，最终文档中会保留两个二级标题，且第二次 `zhihu` 的内容会追加到第一个 `## zhihu` 分节的末尾。
- 每次导出会在所属模块下生成一个三级标题块，默认标题为 `### 输出index`、`### 导出index` 或 `### 导出完成index`，下面紧跟本次导出的条目列表。
- 当前支持这些子命令：`cnblog`、`bangumi`、`qireader`、`v2ex`、`zhihu`、`weibo`、`bilibili`。

示例：

```shell
eto cnblog --output output/cnblog
eto --index-file output/index/cnblog-index.md cnblog --output output/cnblog
eto --index-file output/index/export-index.md zhihu -c xxx -o ./zhihu/
eto --index-file output/index/export-index.md bilibili -f xxx -o ./bilibili/
eto --index-file output/index/export-index.md zhihu -c xxx -o ./zhihu/
```

索引文件示例：

```markdown
## zhihu

### 输出index

- [[~zhihu-entry-1|第一篇知乎收藏]]
- [[~zhihu-entry-2|第二篇知乎收藏]]

### 输出index

- [[~zhihu-entry-3|第三篇知乎收藏]]

## bilibili

### 输出index

- [[~BV1xxxxxx|某个收藏视频]]
```

### 博客园

_For more examples, please refer to the [Documentation](https://github.com/bGZo/playground)_

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

## Testing In VS Code

项目已经提供可直接使用的 VS Code 调试配置，位置在 .vscode/launch.json。

使用方式：

- 在 VS Code 中先选择项目的 Python 解释器，建议使用 Poetry 环境。
- 如果需要平台凭证，先按前文说明准备 .env，并确保调试配置能读到它。
- 打开 Run and Debug 面板后，可直接选择各个 CLI 配置，例如 `CLI: cnblog 导出`、`CLI: zhihu 导出`、`CLI: bilibili 导出`。
- 其中 `qireader`、`bilibili` 等配置里的示例参数需要按你的实际 tag、fid 或 collection 值修改后再运行。
- 测试调试可直接选择 `Pytest: 当前测试文件`，或者运行指定测试文件与 `Pytest: 全部测试`。

命令行测试范例：

```shell
PYTHONPATH=src pytest tests -q
PYTHONPATH=src pytest tests/test_utils.py -q
```

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
