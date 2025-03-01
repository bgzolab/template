# Telegram bot go version

## Quick Start
1. rename `.env.bak` to `.env`.
2. Input your bot BOT_TOKEN.
3. Then run following:
```bash
# install dep
go mod tidy
# run
go run main.go
```

## TODO
Tg bot api go version have many implements via: https://core.telegram.org/bots/api
- [ ] Dockfile
- [ ] Webhook
- [ ] Middlewares

## Develop

```bash
# install dep
go get github.com/joho/godotenv
```

## Build

```shell
go build -o mybot main.go
```

## Run background

```shell
nohup ./mybot > bot.log 2>&1 &     
```


```bash
 sudo vim /lib/systemd/system/tgbot@.service 
```

```bash
[Unit]
Description=tgbot for %i.
After=network.target

[Service]
Type=simple
User=%i
Restart=on-abort
Environment=DISPLAY=:0
ExecStart=/home/bgzo/opt/sunshine.AppImage

[Install]
# WantedBy=multi-user.target
WantedBy=graphical-session.target

```
