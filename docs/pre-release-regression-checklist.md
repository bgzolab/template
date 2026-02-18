# 发布前回归检查模板（可复用）

> 用途：在发布前统一记录回归执行情况，减少“改动通过但未覆盖关键路径”的风险。
> 规范来源：`docs/memories/archive-markdown-schema-v1.md`（本文件只做检查记录，不定义规则）。

## 基本信息

- 版本/分支：
- 检查日期：
- 执行人：
- 关联改动（PR/提交）：

## 配置与启动检查

- [ ] 配置文件可读取（`config/config.yaml`）
- [ ] `pipeline.executionMode=serial` 启动成功
- [ ] `pipeline.executionMode=async_experimental` 启动成功
- [ ] `pipeline.executionMode` 设为未知值时可回退到串行

## 关键链路回归

- [ ] 归档链路正常：消息可落盘（Markdown/JSON）并入库
- [ ] 同步链路正常：目标频道命中时触发分发
- [ ] 同步关闭分支正常：`socialMediaSync.enable=false` 时仅输出跳过通知
- [ ] 频道未命中分支正常：不触发平台分发，仅输出跳过通知
- [ ] 通知链路正常：归档通知 + 同步通知顺序符合预期

## 模块测试回归

- [ ] `go test ./internal/service/pipelineservice`
- [ ] `go test ./internal/service/bootstrapservice`
- [ ] `go test ./internal/service/notifyservice`
- [ ] `go test ./internal/service/archiveservice`
- [ ] `go test ./internal/service/syncservice`
- [ ] `go test ./internal/Database`

## 结果记录

- 回归结论：通过 / 不通过
- 一次性切换结论：Go / No-Go（按 schema v1 门禁）
- 失败项：
- 风险说明：
- 处理建议：

## 审核与发布

- [ ] 已同步更新 `docs/memories/progress.md`
- [ ] 已同步更新 `docs/memories/architecture.md`（如涉及边界变化）
- [ ] 已确认可发布
