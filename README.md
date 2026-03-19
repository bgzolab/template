[![Contributors](https://img.shields.io/github/contributors/bGZo/playground.svg?style=for-the-badge)](https://github.com/bGZo/playground/graphs/contributors)
[![Forks](https://img.shields.io/github/forks/bGZo/playground.svg?style=for-the-badge)](https://github.com/bGZo/playground/network/members)
[![Stargazers](https://img.shields.io/github/stars/bGZo/playground.svg?style=for-the-badge)](https://github.com/bGZo/playground/stargazers)
[![Issues](https://img.shields.io/github/issues/bGZo/playground.svg?style=for-the-badge)](https://github.com/bGZo/playground/issues)
[![Licence](https://img.shields.io/github/license/bGZo/playground.svg?style=for-the-badge)](https://github.com/bGZo/playground/blob/template/LICENCE)
[![Telegram](https://img.shields.io/badge/-telegram-black.svg?style=for-the-badge&logo=telegram&colorB=555)](https://t.me/imbGZo)

# 让我们快乐地点格子

![](https://raw.githack.com/bGZo/assets/dev/2025/202508021025451.png)


## Getting Started

需要 Bangumi 的 `access_token`，可以从 https://next.bgm.tv/demo/access-token 获取。

如果从命令行中运行，需要声明环境变量，IDE 中请配置 Environment Variables。以 nix 类系统为例：

```shell
# 必填
export BGM_ACCESS_TOKEN=xxx

# 可选
export http_proxy=192.168.31.20:10800
export https_proxy=192.168.31.20:10800

# 安装本项目
pipx install bangumi_recovery
```

### 往季新番点格子

```shell
bgm-click-server
```

### 恢复数据（克隆账号）

```python
bgm-clone dandelion_fs
```

### 删除时间线

```shell
bgm-timeline-delete bool
```

## 参考项目

- https://github.com/LCMs-YoRHa/From-Bangumi-to-Obsidian
- https://github.com/BGmi/BGmi


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
