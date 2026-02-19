package archivemigrationservice

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
	"time"

	"gorm.io/driver/sqlite"
	"gorm.io/gorm"

	"telegram-message-sync-bot/internal/Database"
	"telegram-message-sync-bot/internal/Entity"
)

func TestBackfillFromDatabase_CreatesMissingFilesAndVerifies(t *testing.T) {
	tmp := t.TempDir()
	personDir := filepath.Join(tmp, "person")
	channelDir := filepath.Join(tmp, "channel")
	templatePath := filepath.Join(tmp, "template.txt")

	if err := os.WriteFile(templatePath, []byte("{{.content}}\n{{.sourceTelegram}}"), 0o644); err != nil {
		t.Fatalf("failed to write template: %v", err)
	}

	setupInMemoryDB(t)

	now := time.Date(2026, 2, 19, 11, 0, 0, 0, time.UTC)
	seedMessages := []Entity.Message{
		{MessageID: 101, Username: "MyChannel", MessageUrl: "https://t.me/mychannel/101", Content: "hello channel", MessageDate: now, CreatedTime: now},
		{MessageID: 202, Username: "12345", MessageUrl: "", Content: "hello person", MessageDate: now, CreatedTime: now},
	}
	for _, m := range seedMessages {
		msg := m
		if _, err := Database.SaveMessage(&msg); err != nil {
			t.Fatalf("failed to seed message: %v", err)
		}
	}

	var cfg Entity.Config
	cfg.Output.PersonDir = personDir
	cfg.Output.ChannelDir = channelDir
	cfg.Template.Dir = templatePath

	stats, err := BackfillFromDatabase(cfg)
	if err != nil {
		t.Fatalf("backfill failed: %v", err)
	}

	if stats.DBTotal != 2 || stats.FilesCreated != 2 || stats.FilesSkipped != 0 {
		t.Fatalf("unexpected stats: %+v", stats)
	}
	if stats.MissingFromArchive != 0 || stats.OrphanInArchive != 0 {
		t.Fatalf("verify should pass, stats: %+v", stats)
	}

	channelFile := filepath.Join(channelDir, "mychannel", "101.md")
	personFile := filepath.Join(personDir, "12345", "202.md")

	assertFileContains(t, channelFile, "title: \"101-hello channel\"")
	assertFileContains(t, channelFile, "source: \"https://t.me/mychannel/101\"")
	assertFileContains(t, personFile, "source: \"\"")
}

func TestBackfillFromDatabase_SkipsExistingFile(t *testing.T) {
	tmp := t.TempDir()
	personDir := filepath.Join(tmp, "person")
	channelDir := filepath.Join(tmp, "channel")
	templatePath := filepath.Join(tmp, "template.txt")

	if err := os.WriteFile(templatePath, []byte("{{.content}}"), 0o644); err != nil {
		t.Fatalf("failed to write template: %v", err)
	}

	setupInMemoryDB(t)

	now := time.Date(2026, 2, 19, 11, 0, 0, 0, time.UTC)
	msg := Entity.Message{MessageID: 303, Username: "12345", MessageUrl: "", Content: "existing", MessageDate: now, CreatedTime: now}
	if _, err := Database.SaveMessage(&msg); err != nil {
		t.Fatalf("failed to seed message: %v", err)
	}

	existingDir := filepath.Join(personDir, "12345")
	if err := os.MkdirAll(existingDir, 0o755); err != nil {
		t.Fatalf("failed to create existing dir: %v", err)
	}
	if err := os.WriteFile(filepath.Join(existingDir, "303.md"), []byte("already here"), 0o644); err != nil {
		t.Fatalf("failed to write existing file: %v", err)
	}

	var cfg Entity.Config
	cfg.Output.PersonDir = personDir
	cfg.Output.ChannelDir = channelDir
	cfg.Template.Dir = templatePath

	stats, err := BackfillFromDatabase(cfg)
	if err != nil {
		t.Fatalf("backfill failed: %v", err)
	}

	if stats.FilesSkipped != 1 || stats.FilesCreated != 0 {
		t.Fatalf("expected skip existing behavior, got stats: %+v", stats)
	}
}

func TestBackfillFromDatabase_VerifyDetectsOrphan(t *testing.T) {
	tmp := t.TempDir()
	personDir := filepath.Join(tmp, "person")
	channelDir := filepath.Join(tmp, "channel")
	templatePath := filepath.Join(tmp, "template.txt")

	if err := os.WriteFile(templatePath, []byte("{{.content}}"), 0o644); err != nil {
		t.Fatalf("failed to write template: %v", err)
	}

	setupInMemoryDB(t)

	now := time.Date(2026, 2, 19, 11, 0, 0, 0, time.UTC)
	msg := Entity.Message{MessageID: 404, Username: "12345", MessageUrl: "", Content: "one", MessageDate: now, CreatedTime: now}
	if _, err := Database.SaveMessage(&msg); err != nil {
		t.Fatalf("failed to seed message: %v", err)
	}

	orphanDir := filepath.Join(personDir, "12345")
	if err := os.MkdirAll(orphanDir, 0o755); err != nil {
		t.Fatalf("failed to create orphan dir: %v", err)
	}
	if err := os.WriteFile(filepath.Join(orphanDir, "999.md"), []byte("orphan"), 0o644); err != nil {
		t.Fatalf("failed to write orphan file: %v", err)
	}

	var cfg Entity.Config
	cfg.Output.PersonDir = personDir
	cfg.Output.ChannelDir = channelDir
	cfg.Template.Dir = templatePath

	stats, err := BackfillFromDatabase(cfg)
	if err == nil {
		t.Fatalf("expected verify failure due to orphan file, got nil error")
	}
	if !strings.Contains(err.Error(), "orphan=1") {
		t.Fatalf("unexpected verify error: %v", err)
	}
	if stats.OrphanInArchive != 1 {
		t.Fatalf("expected orphan count 1, got stats: %+v", stats)
	}
}

func setupInMemoryDB(t *testing.T) {
	t.Helper()
	db, err := gorm.Open(sqlite.Open(":memory:"), &gorm.Config{})
	if err != nil {
		t.Fatalf("failed to open sqlite memory db: %v", err)
	}
	if err := db.AutoMigrate(&Entity.Message{}, &Entity.Attachment{}); err != nil {
		t.Fatalf("failed to migrate tables: %v", err)
	}
	Database.DB = db
}

func assertFileContains(t *testing.T, filePath string, expected string) {
	t.Helper()
	b, err := os.ReadFile(filePath)
	if err != nil {
		t.Fatalf("failed to read file %s: %v", filePath, err)
	}
	if !strings.Contains(string(b), expected) {
		t.Fatalf("file %s missing expected snippet: %s\ncontent:\n%s", filePath, expected, string(b))
	}
}
