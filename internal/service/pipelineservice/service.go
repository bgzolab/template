package pipelineservice

import (
	"context"

	"github.com/go-telegram/bot"
	"github.com/go-telegram/bot/models"

	"telegram-message-sync-bot/internal/Entity"
	"telegram-message-sync-bot/internal/service/archiveservice"
	"telegram-message-sync-bot/internal/service/notifyservice"
	"telegram-message-sync-bot/internal/service/syncservice"
)

// ArchiveStage 定义归档阶段可替换接口。
// 这样做的原因是让归档实现可按需替换（例如异步任务、重试包装器），而不影响主流程编排。
type ArchiveStage interface {
	Run(ctx context.Context, b *bot.Bot, update *models.Update, config Entity.Config) archiveservice.PersistResult
}

// SyncStage 定义同步阶段可替换接口。
// 这样做的原因是把同步策略判定与分发执行封装为独立阶段，后续可替换为异步实现。
type SyncStage interface {
	Run(config Entity.Config, persistResult archiveservice.PersistResult) (bool, string, []syncservice.DispatchResult)
}

// NotifyStage 定义通知阶段可替换接口。
// 这样做的原因是把消息展开与通知编排独立出来，便于切换发送策略（串行/异步队列）。
type NotifyStage interface {
	Run(config Entity.Config, update *models.Update, persistResult archiveservice.PersistResult, syncEnabled bool, syncReason string, dispatchResults []syncservice.DispatchResult) []notifyservice.OutboundMessage
}

type ProcessResult struct {
	PersistResult    archiveservice.PersistResult
	SyncEnabled      bool
	SyncReason       string
	OutboundMessages []notifyservice.OutboundMessage
}

type Pipeline struct {
	ArchiveStage ArchiveStage
	SyncStage    SyncStage
	NotifyStage  NotifyStage
}

type defaultArchiveStage struct{}

func (defaultArchiveStage) Run(ctx context.Context, b *bot.Bot, update *models.Update, config Entity.Config) archiveservice.PersistResult {
	return archiveservice.PersistMessage(ctx, b, update, config)
}

type defaultSyncStage struct{}

func (defaultSyncStage) Run(config Entity.Config, persistResult archiveservice.PersistResult) (bool, string, []syncservice.DispatchResult) {
	syncEnabled, syncReason := syncservice.ShouldSync(config, persistResult.SourceID)
	results := make([]syncservice.DispatchResult, 0)
	if syncEnabled {
		results = syncservice.Dispatch(config, persistResult.MsgText, syncservice.DefaultSenders())
	}
	return syncEnabled, syncReason, results
}

type defaultNotifyStage struct{}

func (defaultNotifyStage) Run(config Entity.Config, update *models.Update, persistResult archiveservice.PersistResult, syncEnabled bool, syncReason string, dispatchResults []syncservice.DispatchResult) []notifyservice.OutboundMessage {
	targetChatIDs := notifyservice.ResolveTargetChatIDs(config, update.Message.Chat.ID)
	archiveResponse := notifyservice.BuildArchiveResponse(persistResult.OK, persistResult.SourceLink, persistResult.Message)
	syncNotifications := notifyservice.BuildSyncNotifications(syncEnabled, syncReason, dispatchResults)
	return notifyservice.BuildOutboundMessages(targetChatIDs, archiveResponse, syncNotifications)
}

// NewDefaultPipeline 构建默认串行 pipeline：archive -> sync -> notify。
// 这样做的原因是把主流程编排集中到单点，main 只保留入口与发送动作。
func NewDefaultPipeline() Pipeline {
	return Pipeline{
		ArchiveStage: defaultArchiveStage{},
		SyncStage:    defaultSyncStage{},
		NotifyStage:  defaultNotifyStage{},
	}
}

// ProcessUpdate 以固定顺序执行串行 stage，并返回统一处理结果。
// 这样做的原因是稳定阶段边界，为后续异步化改造提供可替换骨架。
func (p Pipeline) ProcessUpdate(ctx context.Context, b *bot.Bot, update *models.Update, config Entity.Config) ProcessResult {
	if update == nil || update.Message == nil {
		return ProcessResult{}
	}

	persistResult := p.ArchiveStage.Run(ctx, b, update, config)
	syncEnabled, syncReason, results := p.SyncStage.Run(config, persistResult)
	outboundMessages := p.NotifyStage.Run(config, update, persistResult, syncEnabled, syncReason, results)

	return ProcessResult{
		PersistResult:    persistResult,
		SyncEnabled:      syncEnabled,
		SyncReason:       syncReason,
		OutboundMessages: outboundMessages,
	}
}
