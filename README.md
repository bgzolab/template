<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![project_license][license-shield]][license-url]
![Size][size-shield]

[contributors-shield]: https://img.shields.io/github/contributors/bGZo/playground.svg?style=for-the-badge
[contributors-url]: https://github.com/bGZo/playground/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/bGZo/playground.svg?style=for-the-badge
[forks-url]: https://github.com/bGZo/playground/network/members
[stars-shield]: https://img.shields.io/github/stars/bGZo/playground.svg?style=for-the-badge
[stars-url]: https://github.com/bGZo/playground/stargazers
[issues-shield]: https://img.shields.io/github/issues/bGZo/playground.svg?style=for-the-badge
[issues-url]: https://github.com/bGZo/playground/issues
[license-shield]: https://img.shields.io/github/license/bGZo/playground.svg?style=for-the-badge
[license-url]: https://github.com/bGZo/playground/blob/template/LICENCE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[size-shield]: https://img.shields.io/github/repo-size/bGZo/playground?style=for-the-badge



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/bGZo/playground">
    <img src="https://raw.githack.com/bGZo/assets/dev/2026/20260214095756842.webp" alt="Logo is from: https://siddhantkhare.com/writing/ai-fatigue-is-real">
  </a>
<h1 align="center">Telegram message sync bot</h1>
  <p align="center">
    A telegram bot for archiving messages from bots and syncing them to social media.
    <br />
    <a href="https://github.com/bGZo/playground"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/bGZo/playground">View Demo</a>
    &middot;
    <a href="https://github.com/bGZo/playground/issues/new?labels=bug">Report Bug</a>
    &middot;
    <a href="https://github.com/bGZo/playground/issues/new?labels=enhancement">Request Feature</a>
  </p>
</div>


<!-- ABOUT THE PROJECT -->
## About The Project

![](https://raw.githack.com/bGZo/assets/dev/2025/202503011548103.png)

This is a telegram bot for archiving message from bot and sync to social media.

Of course, you can use it as a simple telegram bot for syncing message from telegram.

- Golang
- Gorm
- Sqlite
- Telebot
- Social media API

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Why

Telegram have a great API and contents than other social media. There's less bot, business and ads.

So I spend a lot of time on it. The messges saved in `SavedMessage` is not enough. You should manage what you read. And post what you think to more social media.

That's what this bot do.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

```shell
# install dependencies
go mod tidy

# build the result
go build -o tg main.go

# give the right to run. 
chmod +x ./tg

# run bot
./tg sync -c ./config/config.yaml
```

### Optional: run in background using nohup

```shell
nohup ./tg sync -c ./config/config.yaml > bot.log 2>&1 &

# kill background
pkill -f tg
```

### Optional: run in background using nohup

```shell
sudo vim /lib/systemd/system/tg@.service
```

Add following config:

```shell
[Unit]
Description=tg message sync bot for %i.
After=network.target

[Service]
Type=simple
User=%i
Restart=on-abort
Environment=http_proxy=192.168.31.20:10800
Environment=https_proxy=192.168.31.20:10800
ExecStart=/home/bgzo/workspaces/telegram-message-sync/tg sync -c /home/bgzo/workspaces/telegram-message-sync/config/config.yaml

[Install]
# WantedBy=multi-user.target
WantedBy=graphical-session.target
```

Then restart systemd and enable `tg@username`

```shell
systemctl daemon-reload
systenctl start tg@bgzo
systenctl enable tg@bgzo
```

_For more examples, please refer to the [Documentation](https://github.com/bGZo/playground)_


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ROADMAP -->
## Roadmap

- [x] Messages archive
  - [x] Rich text from Telegram
  - [x] Media download
- [x] Notification
- [x] Database supported(sqlite)
- [ ] Sync social media (beta)
  - [x] Twitter
  - [x] Mastodon
  - [x] BlueSky
  - [ ] Instagram
  - [ ] Facebook
  - [ ] Thread
  - [ ] Reddit
  - [ ] Douban
  - [ ] Okjike
  - [ ] Weibo
  - [ ] Douyin
  - [ ] Bilibili
  - [ ] Xiaohongshu
  - [ ] Coolapk
  - [ ] Zhihu
  - [ ] V2Ex


<p align="right">(<a href="#readme-top">back to top</a>)</p>


## ALternatives

- https://github.com/leaperone/MultiPost-Extension

<!-- CONTRIBUTING -->
## Contributing

Any contributions made are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- CONTRIBUTING -->
### Top contributors:

<a href="https://github.com/bGZo/playground/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=bGZo/playground" alt="contrib.rocks image" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

All code is licensed under the AGPL-3.0 license. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

- Telegram: @imbGZo

<p align="right">(<a href="#readme-top">back to top</a>)</p>

