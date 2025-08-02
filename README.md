# 让我们快乐地点格子

![](https://raw.githack.com/bGZo/assets/dev/2025/202508021025451.png)

> [!note]
> `access_token` for https://bgm.tv/ required, you can get it from https://next.bgm.tv/demo/access-token
> export it on your `.env` file as `BGM_ACCESS_TOKEN`.

## Roadmap

- [x] 恢复数据
  - [x] 从 SingleFile 中恢复数据 250728
    - 下载了历史备份，需要这次一次性上传上去
  - [x] 克隆旧账号 250731
    - 多个账号的问题，需要从对应账号里面拉数据；
  - ~~从时间线恢复数据~~
- [x] 往季新番批量标记 250801
  - API 使用： https://github.com/bangumi-data/bangumi-data, 大力感谢
  - 数据结构展示： https://github.com/bangumi-data/bangumi-data/blob/master/data/items/1943/04.json
- [ ] 每日轮训删除时间线
  - 可以用这个 API： https://bgm.tv/feed/user/bool/timeline

## Quick Start

```shell
git clone -b 2025/07/bangumi-recovery-scripts --single-branch git@github.com:bGZo/playground.git
cd playground
pip install -r requirements.txt
cd web
python3 main_web.py
```

## 参考项目

- https://github.com/LCMs-YoRHa/From-Bangumi-to-Obsidian
- https://github.com/BGmi/BGmi

## License

All code is licensed under the AGPL-3.0 license.
