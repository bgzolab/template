package syncservice

import (
	"telegram-message-sync-bot/internal/Entity"
	"testing"
)

type fakeSender struct {
	name    string
	success bool
}

func (f fakeSender) Name() string {
	return f.name
}

func (f fakeSender) Send(_ Entity.Config, _ string) bool {
	return f.success
}

func TestShouldSync_Disabled(t *testing.T) {
	config := Entity.Config{}
	config.SocialMediaSync.Enable = false

	ok, reason := ShouldSync(config, "imbGZo")
	if ok {
		t.Fatalf("expected false when sync disabled")
	}
	if reason == "" {
		t.Fatalf("expected non-empty reason when sync disabled")
	}
}

func TestShouldSync_EmptyTargetChannels(t *testing.T) {
	config := Entity.Config{}
	config.SocialMediaSync.Enable = true

	ok, reason := ShouldSync(config, "imbGZo")
	if ok {
		t.Fatalf("expected false when targetChannel is empty")
	}
	if reason == "" {
		t.Fatalf("expected non-empty reason when targetChannel is empty")
	}
}

func TestShouldSync_HitTargetChannel(t *testing.T) {
	config := Entity.Config{}
	config.SocialMediaSync.Enable = true
	config.SocialMediaSync.TargetChannel = []string{"imbGZo", "another"}

	ok, reason := ShouldSync(config, "imbGZo")
	if !ok {
		t.Fatalf("expected true when source matches targetChannel, got reason: %s", reason)
	}
	if reason != "" {
		t.Fatalf("expected empty reason on match, got: %s", reason)
	}
}

func TestShouldSync_MissTargetChannel(t *testing.T) {
	config := Entity.Config{}
	config.SocialMediaSync.Enable = true
	config.SocialMediaSync.TargetChannel = []string{"imbGZo"}

	ok, reason := ShouldSync(config, "other")
	if ok {
		t.Fatalf("expected false when source does not match targetChannel")
	}
	if reason == "" {
		t.Fatalf("expected non-empty reason when source does not match")
	}
}

func TestDispatch_KeepOrderAndResults(t *testing.T) {
	config := Entity.Config{}
	senders := []Sender{
		fakeSender{name: "BlueSky", success: true},
		fakeSender{name: "Mastodon", success: false},
		nil,
		fakeSender{name: "Twitter", success: true},
	}

	results := Dispatch(config, "hello", senders)
	if len(results) != 3 {
		t.Fatalf("expected 3 results (nil sender skipped), got %d", len(results))
	}

	if results[0].Platform != "BlueSky" || !results[0].Success {
		t.Fatalf("unexpected first result: %+v", results[0])
	}

	if results[1].Platform != "Mastodon" || results[1].Success {
		t.Fatalf("unexpected second result: %+v", results[1])
	}

	if results[2].Platform != "Twitter" || !results[2].Success {
		t.Fatalf("unexpected third result: %+v", results[2])
	}
}
