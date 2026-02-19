package archiveservice

import (
	"testing"
	"time"

	"github.com/go-telegram/bot/models"

	"telegram-message-sync-bot/internal/Entity"
)

func TestResolveSourceMeta_DefaultPrivateMessage(t *testing.T) {
	update := &models.Update{
		Message: &models.Message{
			ID:   99,
			Chat: models.Chat{ID: 12345},
		},
	}

	config := Entity.Config{}
	config.Output.PersonDir = "/person"
	config.Output.ChannelDir = "/channel"

	meta := ResolveSourceMeta(update, config)
	if meta.OutputPath != "/person/12345" {
		t.Fatalf("expected person output path /person/12345, got: %s", meta.OutputPath)
	}
	if meta.SourceID != "12345" {
		t.Fatalf("expected sourceID=12345, got: %s", meta.SourceID)
	}
	if meta.FileName != "99.md" {
		t.Fatalf("expected fileName=99.md, got: %s", meta.FileName)
	}
	if meta.SourceLink != "" {
		t.Fatalf("expected empty source link for private message, got: %s", meta.SourceLink)
	}
}

func TestResolveSourceMeta_ForwardedChannelWithUsername(t *testing.T) {
	update := &models.Update{
		Message: &models.Message{
			ID:   1,
			Chat: models.Chat{ID: 10},
			ForwardOrigin: &models.MessageOrigin{
				Type: "channel",
				MessageOriginChannel: &models.MessageOriginChannel{
					Date:      int(time.Unix(1700000000, 0).Unix()),
					MessageID: 321,
					Chat: models.Chat{
						ID:       -1001,
						Username: "imbGZo",
					},
				},
			},
		},
	}

	config := Entity.Config{}
	config.Output.PersonDir = "/person"
	config.Output.ChannelDir = "/channel"

	meta := ResolveSourceMeta(update, config)
	if meta.OutputPath != "/channel/imbGZo" {
		t.Fatalf("expected channel output path /channel/imbGZo, got: %s", meta.OutputPath)
	}
	if meta.SourceID != "imbGZo" {
		t.Fatalf("expected sourceID=imbGZo, got: %s", meta.SourceID)
	}
	if meta.FileName != "321.md" {
		t.Fatalf("expected fileName=321.md, got: %s", meta.FileName)
	}
	if meta.SourceLink != "https://t.me/imbGZo/321" {
		t.Fatalf("unexpected source link: %s", meta.SourceLink)
	}
	if meta.MessageID != 321 {
		t.Fatalf("expected messageID=321, got: %d", meta.MessageID)
	}
}

func TestSelectMsgText_FallbackToCaption(t *testing.T) {
	update := &models.Update{
		Message: &models.Message{
			Text:    "",
			Caption: "hello #tag",
		},
	}

	text := SelectMsgText(update)
	if text != "hello \\#tag" {
		t.Fatalf("unexpected selected text: %s", text)
	}
}

func TestBuildTemplateData_ContainsExpectedKeys(t *testing.T) {
	sourceDate := time.Date(2026, 2, 17, 10, 0, 0, 0, time.UTC)
	now := time.Date(2026, 2, 17, 11, 0, 0, 0, time.UTC)

	data := BuildTemplateData(sourceDate, "photo", "content", "link", now)

	if data["photo"] != "photo" {
		t.Fatalf("expected photo field")
	}
	if data["content"] != "content" {
		t.Fatalf("expected content field")
	}
	if data["sourceTelegram"] != "link" {
		t.Fatalf("expected sourceTelegram field")
	}
	if data["title"] == "" || data["date"] == "" || data["now"] == "" {
		t.Fatalf("expected non-empty formatted time fields")
	}
}
