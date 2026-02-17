package pipelineservice

import (
	"context"
	"reflect"
	"testing"

	"github.com/go-telegram/bot"
	"github.com/go-telegram/bot/models"

	"telegram-message-sync-bot/internal/Entity"
	"telegram-message-sync-bot/internal/service/archiveservice"
	"telegram-message-sync-bot/internal/service/notifyservice"
	"telegram-message-sync-bot/internal/service/syncservice"
)

type fakeArchiveStage struct {
	run func(ctx context.Context, b *bot.Bot, update *models.Update, config Entity.Config) archiveservice.PersistResult
}

func (f fakeArchiveStage) Run(ctx context.Context, b *bot.Bot, update *models.Update, config Entity.Config) archiveservice.PersistResult {
	return f.run(ctx, b, update, config)
}

type fakeSyncStage struct {
	run func(config Entity.Config, persistResult archiveservice.PersistResult) (bool, string, []syncservice.DispatchResult)
}

func (f fakeSyncStage) Run(config Entity.Config, persistResult archiveservice.PersistResult) (bool, string, []syncservice.DispatchResult) {
	return f.run(config, persistResult)
}

type fakeNotifyStage struct {
	run func(config Entity.Config, update *models.Update, persistResult archiveservice.PersistResult, syncEnabled bool, syncReason string, dispatchResults []syncservice.DispatchResult) []notifyservice.OutboundMessage
}

func (f fakeNotifyStage) Run(config Entity.Config, update *models.Update, persistResult archiveservice.PersistResult, syncEnabled bool, syncReason string, dispatchResults []syncservice.DispatchResult) []notifyservice.OutboundMessage {
	return f.run(config, update, persistResult, syncEnabled, syncReason, dispatchResults)
}

func TestProcessUpdate_StageOrderAndOutput(t *testing.T) {
	order := make([]string, 0)

	p := Pipeline{
		ArchiveStage: fakeArchiveStage{run: func(_ context.Context, _ *bot.Bot, _ *models.Update, _ Entity.Config) archiveservice.PersistResult {
			order = append(order, "archive")
			return archiveservice.PersistResult{OK: true, Message: "file.md", SourceLink: "link", MsgText: "content", SourceID: "imbGZo"}
		}},
		SyncStage: fakeSyncStage{run: func(_ Entity.Config, _ archiveservice.PersistResult) (bool, string, []syncservice.DispatchResult) {
			order = append(order, "sync")
			return true, "", []syncservice.DispatchResult{{Platform: "BlueSky", Success: true}}
		}},
		NotifyStage: fakeNotifyStage{run: func(_ Entity.Config, _ *models.Update, _ archiveservice.PersistResult, _ bool, _ string, _ []syncservice.DispatchResult) []notifyservice.OutboundMessage {
			order = append(order, "notify")
			return []notifyservice.OutboundMessage{{ChatID: 1, Text: "archive"}, {ChatID: 1, Text: "sync-ok"}}
		}},
	}

	update := &models.Update{Message: &models.Message{Chat: models.Chat{ID: 1}}}
	result := p.ProcessUpdate(context.Background(), nil, update, Entity.Config{})

	expectedOrder := []string{"archive", "sync", "notify"}
	if !reflect.DeepEqual(order, expectedOrder) {
		t.Fatalf("unexpected stage order: %+v", order)
	}

	if len(result.OutboundMessages) != 2 {
		t.Fatalf("unexpected outbound size: %d", len(result.OutboundMessages))
	}
	if !result.SyncEnabled {
		t.Fatalf("expected sync enabled")
	}
}

func TestProcessUpdate_WhenSyncDisabled_StillNotify(t *testing.T) {
	notifyCalled := false

	p := Pipeline{
		ArchiveStage: fakeArchiveStage{run: func(_ context.Context, _ *bot.Bot, _ *models.Update, _ Entity.Config) archiveservice.PersistResult {
			return archiveservice.PersistResult{OK: true, Message: "file.md", SourceLink: "link", MsgText: "content", SourceID: "other"}
		}},
		SyncStage: fakeSyncStage{run: func(_ Entity.Config, _ archiveservice.PersistResult) (bool, string, []syncservice.DispatchResult) {
			return false, "skip", nil
		}},
		NotifyStage: fakeNotifyStage{run: func(_ Entity.Config, _ *models.Update, _ archiveservice.PersistResult, syncEnabled bool, syncReason string, _ []syncservice.DispatchResult) []notifyservice.OutboundMessage {
			notifyCalled = true
			if syncEnabled {
				t.Fatalf("sync should be disabled")
			}
			if syncReason != "skip" {
				t.Fatalf("unexpected sync reason: %s", syncReason)
			}
			return []notifyservice.OutboundMessage{{ChatID: 1, Text: "archive"}, {ChatID: 1, Text: "skip"}}
		}},
	}

	update := &models.Update{Message: &models.Message{Chat: models.Chat{ID: 1}}}
	result := p.ProcessUpdate(context.Background(), nil, update, Entity.Config{})

	if !notifyCalled {
		t.Fatalf("notify stage should be called when sync is disabled")
	}
	if result.SyncEnabled {
		t.Fatalf("expected sync disabled")
	}
	if result.SyncReason != "skip" {
		t.Fatalf("unexpected sync reason: %s", result.SyncReason)
	}
}

func TestProcessUpdate_NilUpdate_ReturnEmpty(t *testing.T) {
	p := NewDefaultPipeline()
	result := p.ProcessUpdate(context.Background(), nil, nil, Entity.Config{})
	if result.PersistResult.OK {
		t.Fatalf("expected empty result when update is nil")
	}
	if len(result.OutboundMessages) != 0 {
		t.Fatalf("expected no outbound messages for nil update")
	}
}
