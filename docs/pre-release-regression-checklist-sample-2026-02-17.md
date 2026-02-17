# 发布前回归检查样例记录（2026-02-17，演练）

> 说明：本记录由模板 `docs/pre-release-regression-checklist.md` 复制并回填，用于阶段2-步骤11的真实演练留痕。

## 基本信息

- 版本/分支：main（本地工作区）
- 检查日期：2026-02-17
- 执行人：维护者（匿名）
- 关联改动（PR/提交）：阶段2-步骤10~11（回归模板化 + 演练回填）

## 配置与启动检查

- [x] 配置文件可读取（`config/config.yaml`）
- [ ] `pipeline.executionMode=serial` 启动成功
- [ ] `pipeline.executionMode=async_experimental` 启动成功
- [x] `pipeline.executionMode` 设为未知值时可回退到串行（由 `pipelineservice` 回归测试覆盖）

## 关键链路回归

- [ ] 归档链路正常：消息可落盘（Markdown/JSON）并入库
- [ ] 同步链路正常：目标频道命中时触发分发
- [ ] 同步关闭分支正常：`socialMediaSync.enable=false` 时仅输出跳过通知
- [ ] 频道未命中分支正常：不触发平台分发，仅输出跳过通知
- [ ] 通知链路正常：归档通知 + 同步通知顺序符合预期

## 模块测试回归

- [x] `go test ./internal/service/pipelineservice`
- [x] `go test ./internal/service/bootstrapservice`
- [x] `go test ./internal/service/notifyservice`
- [x] `go test ./internal/service/archiveservice`
- [x] `go test ./internal/service/syncservice`
- [x] `go test ./internal/Database`

## 结果记录

- 回归结论：不通过（仅完成模块级回归，未完成启动与关键链路手工验证）
- 失败项：配置启动双模式验证、关键链路 5 项未执行
- 风险说明：若直接发布，可能存在“配置可解析但实际运行链路未复核”的发布风险
- 处理建议：补做一次端到端手工链路检查后再执行发布确认

## 审核与发布

- [x] 已同步更新 `docs/progress.md`
- [ ] 已同步更新 `docs/architecture.md`（如涉及边界变化）
- [ ] 已确认可发布
