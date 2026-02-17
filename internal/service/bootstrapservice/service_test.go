package bootstrapservice

import (
	"os"
	"path/filepath"
	"testing"

	"telegram-message-sync-bot/internal/Entity"
)

func TestLoadConfig_Success(t *testing.T) {
	tempDir := t.TempDir()
	configPath := filepath.Join(tempDir, "config.yaml")

	content := `token: test-token
output:
  json: true
  json_dir: /tmp/json
  person_dir: /tmp/person
  channel_dir: /tmp/channel
log:
  enable: true
  dir: /tmp/log
template:
  dir: /tmp/template.txt
targetUserList:
  - 1001
socialMediaSync:
  enable: true
  targetChannel:
    - "imbGZo"
`

	if err := os.WriteFile(configPath, []byte(content), 0644); err != nil {
		t.Fatalf("failed to write config: %v", err)
	}

	config, err := LoadConfig(configPath)
	if err != nil {
		t.Fatalf("expected load config success, got err: %v", err)
	}

	if config.Token != "test-token" {
		t.Fatalf("unexpected token: %s", config.Token)
	}
	if config.Log.Dir != "/tmp/log" {
		t.Fatalf("unexpected log dir: %s", config.Log.Dir)
	}
	if len(config.SocialMediaSync.TargetChannel) != 1 || config.SocialMediaSync.TargetChannel[0] != "imbGZo" {
		t.Fatalf("unexpected target channels: %+v", config.SocialMediaSync.TargetChannel)
	}
}

func TestLoadConfig_FileNotFound(t *testing.T) {
	_, err := LoadConfig(filepath.Join(t.TempDir(), "missing.yaml"))
	if err == nil {
		t.Fatalf("expected error when config file does not exist")
	}
}

func TestInitRuntime_Success(t *testing.T) {
	tempDir := t.TempDir()
	config := Entity.Config{}
	config.Log.Dir = tempDir

	if err := InitRuntime(config); err != nil {
		t.Fatalf("expected init runtime success, got err: %v", err)
	}

	if _, err := os.Stat(filepath.Join(tempDir, "bot.log")); err != nil {
		t.Fatalf("expected bot.log to exist, got err: %v", err)
	}

	if _, err := os.Stat(filepath.Join(tempDir, "archive.db")); err != nil {
		t.Fatalf("expected archive.db to exist, got err: %v", err)
	}
}
