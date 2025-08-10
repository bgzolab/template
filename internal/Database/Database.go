package Database

import (
	"database/sql"
	"fmt"
	"log"
	"path/filepath"

	_ "modernc.org/sqlite"
)

var DB *sql.DB

func InitDB(dataDir string) error {
	dbPath := filepath.Join(dataDir, "archive.db")

	var err error
	DB, err = sql.Open("sqlite", dbPath)
	if err != nil {
		return fmt.Errorf("failed to open database: %w", err)
	}

	if err := DB.Ping(); err != nil {
		return fmt.Errorf("failed to connect to database: %w", err)
	}

	if err := createTables(); err != nil {
		return fmt.Errorf("failed to create tables: %w", err)
	}

	log.Println("Database initialized successfully")
	return nil
}

func createTables() error {
	queries := []string{
		`CREATE TABLE IF NOT EXISTS messages (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			sender_id TEXT NOT NULL,
			sender_name TEXT NOT NULL,
			receiver_id TEXT NOT NULL,
			receiver_name TEXT NOT NULL,
			content TEXT,
			media_path TEXT,
			message_type TEXT NOT NULL,
			timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
		)`,
		`CREATE TABLE IF NOT EXISTS attachments (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			message_id INTEGER NOT NULL,
			file_path TEXT NOT NULL,
			file_size INTEGER,
			mime_type TEXT,
			FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE
		)`,
	}

	for _, query := range queries {
		if _, err := DB.Exec(query); err != nil {
			return fmt.Errorf("failed to execute query %q: %w", query, err)
		}
	}
	return nil
}

func CloseDB() {
	if DB != nil {
		DB.Close()
	}
}
