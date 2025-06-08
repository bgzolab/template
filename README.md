# Telegram message sync bot


## Roadmap

### Message Archive

#### Rich text from Telegram #gtd/done

#### Media Download from Telegram #gtd/done

#### Notification #gtd/done

### Database Support #gtd/doing

SQLite

### Sync Social Media #gtd/doing

So why?

1. I don't like the online service.
2. I need self-host & local & privacy.

- Target: https://github.com/leaperone/MultiPost-Extension
- Global
  - [x] Telegram
  - [x] Twitter
  - [x] Mastodon
  - [x] BlueSky
  - [ ] Instagram
  - [ ] Facebook
  - [ ] Thread
  - [ ] Reddit
- Chinese
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

![](https://raw.githack.com/bGZo/assets/dev/2025/202503011548103.png)

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
