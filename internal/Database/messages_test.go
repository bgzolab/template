package Database

import (
	"testing"
	"time"

	"gorm.io/driver/sqlite"
	"gorm.io/gorm"

	"telegram-message-sync-bot/internal/Entity"
)

func setupTestDB(t *testing.T) {
	t.Helper()

	db, err := gorm.Open(sqlite.Open(":memory:"), &gorm.Config{})
	if err != nil {
		t.Fatalf("failed to open in-memory sqlite: %v", err)
	}

	err = db.AutoMigrate(&Entity.Message{}, &Entity.Attachment{})
	if err != nil {
		t.Fatalf("failed to migrate schema: %v", err)
	}

	DB = db
}

func TestSaveMessage_DuplicateBySourceUniqueIndex(t *testing.T) {
	setupTestDB(t)

	msg1 := &Entity.Message{
		MessageID:   1001,
		Username:    "imbGZo",
		Content:     "first",
		MessageUrl:  "https://t.me/imbGZo/1001",
		MessageDate: time.Now(),
		CreatedTime: time.Now(),
	}

	_, err := SaveMessage(msg1)
	if err != nil {
		t.Fatalf("first save should succeed, got err: %v", err)
	}

	msg2 := &Entity.Message{
		MessageID:   1001,
		Username:    "imbGZo",
		Content:     "duplicate",
		MessageUrl:  "https://t.me/imbGZo/1001",
		MessageDate: time.Now(),
		CreatedTime: time.Now(),
	}

	_, err = SaveMessage(msg2)
	if err == nil {
		t.Fatalf("duplicate save should fail by unique constraint")
	}

	if !IsDuplicateMessageError(err) {
		t.Fatalf("expected duplicate error recognizer to return true, got err: %v", err)
	}
}

func TestSaveMessage_DifferentSourceCanCoexist(t *testing.T) {
	setupTestDB(t)

	msg1 := &Entity.Message{
		MessageID:   1001,
		Username:    "imbGZo",
		Content:     "first",
		MessageUrl:  "https://t.me/imbGZo/1001",
		MessageDate: time.Now(),
		CreatedTime: time.Now(),
	}

	msg2 := &Entity.Message{
		MessageID:   1001,
		Username:    "anotherChannel",
		Content:     "second",
		MessageUrl:  "https://t.me/anotherChannel/1001",
		MessageDate: time.Now(),
		CreatedTime: time.Now(),
	}

	if _, err := SaveMessage(msg1); err != nil {
		t.Fatalf("first save should succeed, got err: %v", err)
	}

	if _, err := SaveMessage(msg2); err != nil {
		t.Fatalf("second save with different source should succeed, got err: %v", err)
	}
}
