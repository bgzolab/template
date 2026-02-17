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

type ProcessResult struct {
	PersistResult    archiveservice.PersistResult
	SyncEnabled      bool
	SyncReason       string
	OutboundMessages []notifyservice.OutboundMessage
}

type Pipeline struct {
	Archive                func(ctx context.Context, b *bot.Bot, update *models.Update, config Entity.Config) archiveservice.PersistResult
	ResolveTargets         func(config Entity.Config, fallbackChatID int64) []int64
	BuildArchiveResponse   func(ok bool, sourceLink, message string) string
	ShouldSync             func(config Entity.Config, sourceID string) (bool, string)
	Dispatch               func(config Entity.Config, message string, senders []syncservice.Sender) []syncservice.DispatchResult
	BuildSyncNotifications func(syncEnabled bool, syncReason string, results []syncservice.DispatchResult) []string
	BuildOutboundMessages  func(chatIDs []int64, archiveResponse string, syncNotifications []string) []notifyservice.OutboundMessage
	DefaultSenders         func() []syncservice.Sender
}

// NewDefaultPipeline 构建默认串行 pipeline：archive -> sync -> notify。
// 这样做的原因是把主流程编排集中到单点，main 只保留入口与发送动作。
func NewDefaultPipeline() Pipeline {
	return Pipeline{
		Archive:                archiveservice.PersistMessage,
		ResolveTargets:         notifyservice.ResolveTargetChatIDs,
		BuildArchiveResponse:   notifyservice.BuildArchiveResponse,
		ShouldSync:             syncservice.ShouldSync,
		Dispatch:               syncservice.Dispatch,
		BuildSyncNotifications: notifyservice.BuildSyncNotifications,
		BuildOutboundMessages:  notifyservice.BuildOutboundMessages,
		DefaultSenders:         syncservice.DefaultSenders,
	}
}

// ProcessUpdate 以固定顺序执行串行 stage，并返回统一处理结果。
// 这样做的原因是稳定阶段边界，为后续异步化改造提供可替换骨架。
func (p Pipeline) ProcessUpdate(ctx context.Context, b *bot.Bot, update *models.Update, config Entity.Config) ProcessResult {
	if update == nil || update.Message == nil {
		return ProcessResult{}
	}

	persistResult := p.Archive(ctx, b, update, config)
	targetChatIDs := p.ResolveTargets(config, update.Message.Chat.ID)
	archiveResponse := p.BuildArchiveResponse(persistResult.OK, persistResult.SourceLink, persistResult.Message)

	syncEnabled, syncReason := p.ShouldSync(config, persistResult.SourceID)
	results := make([]syncservice.DispatchResult, 0)
	if syncEnabled {
		results = p.Dispatch(config, persistResult.MsgText, p.DefaultSenders())
	}

	syncNotifications := p.BuildSyncNotifications(syncEnabled, syncReason, results)
	outboundMessages := p.BuildOutboundMessages(targetChatIDs, archiveResponse, syncNotifications)

	return ProcessResult{
		PersistResult:    persistResult,
		SyncEnabled:      syncEnabled,
		SyncReason:       syncReason,
		OutboundMessages: outboundMessages,
	}
}
