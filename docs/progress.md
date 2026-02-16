<!--04.记录已完成步骤：

每次完成一个步骤后，更新这个文件，记录已完成的步骤和下一步计划。这样可以清晰地看到项目的进展和未来的计划。
-->

# 进度记录

## 2025年存档（后补，可更新）

- [x] 2025-02-16: 完成了项目的初始设置，包括:
  - [x] 创建Telegram Bot；
  - [x] 设置Golang环境；
  - [x] 安装必要的依赖库；
  - [x] 完成基本消息存档;
  - [x] 机器人生死状态检测;
  - [x] 机器人日志支持
- [x] 2025-06-09: 存档功能加强；实现了CI的自动发布，打包分发到各个平台；
    - [ ] 特殊文本处理
        - [x] 适配链接、媒体等消息的存档；
        - [x] 按频道来源进行归档
        - [x] 存档反馈成败与否
        - [x] 内容替换：如#标签，否则会产生副作用
        - [x] 超文本格式支持
        - [x] EMOJI 特殊处理
        - [ ] 更多消息格式支持（下划线/加粗文本）
    - [ ] 支持时间排序/倒叙
    - [x] 支持自定义模板
    - [x] 输出 MD YAML header
- [x] 2025-08-09: 实现了社交媒体同步功能，支持将Telegram消息同步到：
	- [x] 同步 Mastodon
	- [x] 同步 BlueSky
	- [x] 同步 Twitter
	- [ ] 连接 Threads
	- [ ] 同步 [Planet](https://staging.v2ex.com/planet)
	- [ ] 更多社交媒体
	- [ ] Instagram
    - [ ] Facebook
    - [ ] Thread
    - [ ] Reddit
    - [ ] Okjike
    - [ ] Douyin
    - [ ] Coolapk
    - [ ] V2Ex
	- [ ] Douban
    - [ ] Jike
    - [ ] Weibo
    - [ ] Zhihu
    - [ ] Bilibili
    - [ ] Xiaohongshu
    - [ ] Tiktok
    - [ ] Kuaishou
	- [ ] 展示社交媒体同步后的消息链接
- [ ] Twitter和Mastodon平台。
- [x] 2025-08-10: 实现了数据库SQLITE的存储。
- [ ] 后台运行
    - [x] NOHUB 运行
    - [ ] SYSTEMCTL 运行
- [ ] Dockerfile

## 2026年进度

