package notifyservice

import (
	"testing"

	"telegram-message-sync-bot/internal/Entity"
	"telegram-message-sync-bot/internal/service/syncservice"
)

func TestResolveTargetChatIDs_WithConfiguredTargets(t *testing.T) {
	config := Entity.Config{}
	config.TargetUserList = []int64{1001, 1002}

	chatIDs := ResolveTargetChatIDs(config, 999)
	if len(chatIDs) != 2 || chatIDs[0] != 1001 || chatIDs[1] != 1002 {
		t.Fatalf("unexpected chatIDs: %+v", chatIDs)
	}
}

func TestResolveTargetChatIDs_WithFallback(t *testing.T) {
	config := Entity.Config{}

	chatIDs := ResolveTargetChatIDs(config, 999)
	if len(chatIDs) != 1 || chatIDs[0] != 999 {
		t.Fatalf("unexpected fallback chatIDs: %+v", chatIDs)
	}
}

func TestBuildArchiveResponse(t *testing.T) {
	successText := BuildArchiveResponse(true, "link", "file.md")
	if successText != "link\n消息已备案至: file.md!" {
		t.Fatalf("unexpected success text: %s", successText)
	}

	failText := BuildArchiveResponse(false, "link", "err")
	if failText != "link\n消息备份出现异常: err!" {
		t.Fatalf("unexpected fail text: %s", failText)
	}
}

func TestBuildSyncNotifications(t *testing.T) {
	whenDisabled := BuildSyncNotifications(false, "skip reason", nil)
	if len(whenDisabled) != 1 || whenDisabled[0] != "skip reason" {
		t.Fatalf("unexpected disabled notifications: %+v", whenDisabled)
	}

	results := []syncservice.DispatchResult{
		{Platform: "BlueSky", Success: true},
		{Platform: "Twitter", Success: false},
	}
	whenEnabled := BuildSyncNotifications(true, "", results)
	if len(whenEnabled) != 2 {
		t.Fatalf("unexpected enabled notification size: %d", len(whenEnabled))
	}
	if whenEnabled[0] != "消息已同步至 BlueSky!" {
		t.Fatalf("unexpected first notification: %s", whenEnabled[0])
	}
	if whenEnabled[1] != "同步 Twitter 失败" {
		t.Fatalf("unexpected second notification: %s", whenEnabled[1])
	}
}

func TestBuildOutboundMessages(t *testing.T) {
	chatIDs := []int64{1, 2}
	archive := "archive"
	syncTexts := []string{"s1", "s2"}

	msgs := BuildOutboundMessages(chatIDs, archive, syncTexts)
	if len(msgs) != 6 {
		t.Fatalf("unexpected outbound size: %d", len(msgs))
	}

	if msgs[0].ChatID != 1 || msgs[0].Text != "archive" {
		t.Fatalf("unexpected first msg: %+v", msgs[0])
	}
	if msgs[1].ChatID != 1 || msgs[1].Text != "s1" {
		t.Fatalf("unexpected second msg: %+v", msgs[1])
	}
	if msgs[2].ChatID != 1 || msgs[2].Text != "s2" {
		t.Fatalf("unexpected third msg: %+v", msgs[2])
	}
	if msgs[3].ChatID != 2 || msgs[3].Text != "archive" {
		t.Fatalf("unexpected fourth msg: %+v", msgs[3])
	}
}
