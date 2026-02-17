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

func TestProcessUpdate_StageOrderAndOutput(t *testing.T) {
	order := make([]string, 0)

	p := Pipeline{
		Archive: func(_ context.Context, _ *bot.Bot, _ *models.Update, _ Entity.Config) archiveservice.PersistResult {
			order = append(order, "archive")
			return archiveservice.PersistResult{OK: true, Message: "file.md", SourceLink: "link", MsgText: "content", SourceID: "imbGZo"}
		},
		ResolveTargets: func(_ Entity.Config, _ int64) []int64 {
			order = append(order, "resolve-targets")
			return []int64{1}
		},
		BuildArchiveResponse: func(_ bool, _ string, _ string) string {
			order = append(order, "archive-response")
			return "archive"
		},
		ShouldSync: func(_ Entity.Config, _ string) (bool, string) {
			order = append(order, "should-sync")
			return true, ""
		},
		Dispatch: func(_ Entity.Config, _ string, _ []syncservice.Sender) []syncservice.DispatchResult {
			order = append(order, "dispatch")
			return []syncservice.DispatchResult{{Platform: "BlueSky", Success: true}}
		},
		BuildSyncNotifications: func(_ bool, _ string, _ []syncservice.DispatchResult) []string {
			order = append(order, "sync-notify")
			return []string{"sync-ok"}
		},
		BuildOutboundMessages: func(_ []int64, _ string, _ []string) []notifyservice.OutboundMessage {
			order = append(order, "build-outbound")
			return []notifyservice.OutboundMessage{{ChatID: 1, Text: "archive"}, {ChatID: 1, Text: "sync-ok"}}
		},
		DefaultSenders: func() []syncservice.Sender {
			return nil
		},
	}

	update := &models.Update{Message: &models.Message{Chat: models.Chat{ID: 1}}}
	result := p.ProcessUpdate(context.Background(), nil, update, Entity.Config{})

	expectedOrder := []string{"archive", "resolve-targets", "archive-response", "should-sync", "dispatch", "sync-notify", "build-outbound"}
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

func TestProcessUpdate_WhenSyncDisabled_NoDispatch(t *testing.T) {
	dispatchCalled := false

	p := Pipeline{
		Archive: func(_ context.Context, _ *bot.Bot, _ *models.Update, _ Entity.Config) archiveservice.PersistResult {
			return archiveservice.PersistResult{OK: true, Message: "file.md", SourceLink: "link", MsgText: "content", SourceID: "other"}
		},
		ResolveTargets: func(_ Entity.Config, _ int64) []int64 {
			return []int64{1}
		},
		BuildArchiveResponse: func(_ bool, _ string, _ string) string {
			return "archive"
		},
		ShouldSync: func(_ Entity.Config, _ string) (bool, string) {
			return false, "skip"
		},
		Dispatch: func(_ Entity.Config, _ string, _ []syncservice.Sender) []syncservice.DispatchResult {
			dispatchCalled = true
			return nil
		},
		BuildSyncNotifications: func(syncEnabled bool, _ string, _ []syncservice.DispatchResult) []string {
			if syncEnabled {
				t.Fatalf("sync should be disabled")
			}
			return []string{"skip"}
		},
		BuildOutboundMessages: func(_ []int64, _ string, _ []string) []notifyservice.OutboundMessage {
			return []notifyservice.OutboundMessage{{ChatID: 1, Text: "archive"}, {ChatID: 1, Text: "skip"}}
		},
		DefaultSenders: func() []syncservice.Sender {
			return nil
		},
	}

	update := &models.Update{Message: &models.Message{Chat: models.Chat{ID: 1}}}
	result := p.ProcessUpdate(context.Background(), nil, update, Entity.Config{})

	if dispatchCalled {
		t.Fatalf("dispatch should not be called when sync is disabled")
	}
	if result.SyncEnabled {
		t.Fatalf("expected sync disabled")
	}
	if result.SyncReason != "skip" {
		t.Fatalf("unexpected sync reason: %s", result.SyncReason)
	}
}
