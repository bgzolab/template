package archiveservice

import (
	"strings"
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

func TestNormalizeFrontMatterContent_ReplacesAllNewlines(t *testing.T) {
	input := "line1\nline2\r\nline3\rline4"
	got := normalizeFrontMatterContent(input)
	if got != "line1 line2 line3 line4" {
		t.Fatalf("unexpected normalized content: %s", got)
	}
}

func TestTruncateForFrontMatter(t *testing.T) {
	if got := truncateForFrontMatter("abc", 10); got != "abc" {
		t.Fatalf("expected original string when shorter, got: %s", got)
	}
	if got := truncateForFrontMatter("abcdef", 3); got != "abc" {
		t.Fatalf("expected truncation to 3, got: %s", got)
	}
}

func TestBuildFrontMatter_MandatoryFields(t *testing.T) {
	meta := SourceMeta{
		SourceLink: "https://t.me/channel/100",
		SourceDate: time.Date(2025, 1, 18, 16, 58, 21, 0, time.UTC),
		MessageID:  100,
	}
	archivedAt := time.Date(2025, 1, 19, 10, 20, 30, 0, time.UTC)
	content := "第一行\n第二行"

	fm := BuildFrontMatter(meta, content, archivedAt)

	checks := []string{
		"---",
		"title: \"100-第一行 第二行\"",
		"aliases:",
		"- \"100-第一行 第二行\"",
		"created: 2025-01-18T16:58:21",
		"modified: 2025-01-19T10:20:30",
		"comments: true",
		"draft: true",
		"description: \"第一行 第二行\"",
		"source: \"https://t.me/channel/100\"",
		"tags: []",
	}

	for _, check := range checks {
		if !strings.Contains(fm, check) {
			t.Fatalf("front matter missing expected snippet: %s\nactual:\n%s", check, fm)
		}
	}
}

func TestBuildFrontMatter_SourceCanBeEmpty(t *testing.T) {
	meta := SourceMeta{SourceLink: "", SourceDate: time.Date(2025, 1, 18, 16, 58, 21, 0, time.UTC), MessageID: 1}
	fm := BuildFrontMatter(meta, "hello", time.Date(2025, 1, 19, 10, 20, 30, 0, time.UTC))
	if !strings.Contains(fm, "source: \"\"") {
		t.Fatalf("expected empty source field, got:\n%s", fm)
	}
}
