# Template: everything based here.

[![Contributors](https://img.shields.io/github/contributors/bgzolab/template.svg?style=for-the-badge)](https://github.com/bgzolab/template/graphs/contributors)
[![Forks](https://img.shields.io/github/forks/bgzolab/template.svg?style=for-the-badge)](https://github.com/bgzolab/template/network/members)
[![Stargazers](https://img.shields.io/github/stars/bgzolab/template.svg?style=for-the-badge)](https://github.com/bgzolab/template/stargazers)
[![Issues](https://img.shields.io/github/issues/bgzolab/template.svg?style=for-the-badge)](https://github.com/bgzolab/template/issues)
[![Licence](https://img.shields.io/github/license/bgzolab/template.svg?style=for-the-badge)](https://github.com/bgzolab/template/blob/template/LICENCE)
[![Telegram](https://img.shields.io/badge/-telegram-black.svg?style=for-the-badge&logo=telegram&colorB=555)](https://t.me/imbGZo)

![template Name Screen Shot](https://pub-89c11651a8434f18a530bd6f93e399da.r2.dev/2025/1753254271482.JPG)

A template repository for my projects, whch contains a basic structure and some common files used in all my projects.

You can use this template to create your own projects by forking it or cloning it.

## Getting Started

Before you start, make sure you have Git installed on your machine. You can download it from [here](https://git-scm.com/downloads).

Add the remote repository:

```shell
git remote add origin git@github.com:bgzolab/template.git
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

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://github.com/bgzolab/template)_

## CI / GitHub Actions

The repo ships with a few GitHub Actions workflows under `.github/workflows/`:

- `opencode-review.yaml` — PR review by opencode.
- `opencode-comment.yaml` — on-demand opencode runs triggered by `/oc` comments.
- `pr-agent-review.yaml` — PR review by [PR-Agent](https://github.com/the-pr-agent/pr-agent), an OpenAI-format third-party tool.

### PR-Agent backed by opencode-go

PR-Agent calls opencode-go's OpenAI-compatible endpoint instead of OpenAI
itself; the model/token config is inlined in the workflow via `SECTION__KEY` env
vars (PR-Agent uses no env prefix). It needs these repository settings:

| Setting | Kind | Example |
| --- | --- | --- |
| `OPENCODE_API_BASE` | Repo **variable** | `https://opencode-go.example.com/v1` |
| `OPENCODE_API_KEY` | Repo **secret** | same key used by the opencode workflows |
| `GITHUB_TOKEN` | Auto | GitHub Actions token |

> Note: PR-Agent's runner reads `OPENAI_KEY` (single underscore) directly and it
> overrides any `OPENAI_KEY` repo/org secret. The workflow sets
> `OPENAI_KEY` to `OPENCODE_API_KEY`, so an existing `OPENAI_KEY` secret is ignored.

The action is event-driven and auto-runs on PR events; it posts its review as a
comment on the pull request.

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

<a href="https://github.com/bgzolab/template/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=bgzolab/template" alt="contrib.rocks image" />
</a>

## License

All code is licensed under the AGPL-3.0 license. See `LICENSE` for more information.