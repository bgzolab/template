# Telegram message sync bot

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
./tg sync -t TG_BOT_TOKEN
```

### Optional: run in background using nohup

```shell
nohup ./tg sync -t 5883330296:AAFCI0jtgH1iHU1zDaL2p3Hj5Z6fkqaRWaU > bot.log 2>&1 &

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
ExecStart=/home/bgzo/workspaces/telegram-message-sync/tg sync -t 58833029:AAFCI0jiHU1zDaL2p3HaRWaU -o /home/bgzo/workspaces/telegram-message-sync/archives

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
