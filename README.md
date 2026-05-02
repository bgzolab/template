[![Contributors](https://img.shields.io/github/contributors/bGZo/playground.svg?style=for-the-badge)](https://github.com/bGZo/playground/graphs/contributors)
[![Forks](https://img.shields.io/github/forks/bGZo/playground.svg?style=for-the-badge)](https://github.com/bGZo/playground/network/members)
[![Stargazers](https://img.shields.io/github/stars/bGZo/playground.svg?style=for-the-badge)](https://github.com/bGZo/playground/stargazers)
[![Issues](https://img.shields.io/github/issues/bGZo/playground.svg?style=for-the-badge)](https://github.com/bGZo/playground/issues)
[![Licence](https://img.shields.io/github/license/bGZo/playground.svg?style=for-the-badge)](https://github.com/bGZo/playground/blob/template/LICENCE)
[![Telegram](https://img.shields.io/badge/-telegram-black.svg?style=for-the-badge&logo=telegram&colorB=555)](https://t.me/imbGZo)

![Playground Name Screen Shot](https://img.bgzo.cc/2025/202508021439235.JPG)

# Venera Parser for Bangumi

A script to parse the data exported from Bangumi's Venera app, which includes users' watching history, ratings, collections, and more. The parsed data can be used for various purposes such as data analysis, visualization, or migration to other platforms.

## Usage

### Parser

```shell
# 查看摘要
python3 src/parser.py summary 20575-2273.venera

# 导出完整 JSON
python3 src/parser.py dump 20575-2273.venera --include-rows --pretty -o venera_dump.json

# 连 cookie.db 一起解析
# 在上面的命令后追加 --include-cookie-db
```

### Bangumi Sync

```shell
# 安装运行依赖
python3 -m pip install -e .

# dry-run，同步本地 DONE 表到 Bangumi done
export ACCESS_TOKEN="your-token"
python3 src/parser.py sync-bangumi 20575-2273.venera --sync DONE=done --dry-run

# 同步多个表，并输出审计报告
python3 src/parser.py sync-bangumi 20575-2273.venera \
  --sync Doing=doing \
  --sync DONE=done \
  --dry-run \
  --report-output reports/dry-run.json
```

说明：

1. `ACCESS_TOKEN` 只从环境变量读取。
2. `--dry-run` 会执行解析、搜索、匹配和当前收藏读取，但不会发写请求。
3. 当前项目已切换为 `click` CLI，所有自动验收以 `pytest` 为准。

### Tests

```shell
python3 -m pytest
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
