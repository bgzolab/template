# Telegram message sync bot

![](https://raw.githack.com/bGZo/assets/dev/2025/202503011548103.png)


This is a telegram bot for archiving message from bot and sync to social media.

Of course, you can use it as a simple telegram bot for syncing message from telegram.

## Why

Telegram have a great API and contents than other social media. There's less bot, business and ads.

So I spend a lot of time on it. The messges saved in `SavedMessage` is not enough. You should manage what you read. And post what you think to more social media.

That's what this bot do.

## How 

- Golang
- Gorm
- Sqlite
- Telebot
- Social media API
- Vibe code

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

## Quick start

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

## ALternatives

- https://github.com/leaperone/MultiPost-Extension

