# 让我们快乐地点格子

![](https://raw.githack.com/bGZo/assets/dev/2025/202508021025451.png)


## Quick Start

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

## 参考项目

- https://github.com/LCMs-YoRHa/From-Bangumi-to-Obsidian
- https://github.com/BGmi/BGmi

## License

All code is licensed under the AGPL-3.0 license.
