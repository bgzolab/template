package Entity

import (
	"time"
)

type MessageType string

const (
	TextMessage  MessageType = "text"
	ImageMessage MessageType = "image"
	FileMessage  MessageType = "file"
	VideoMessage MessageType = "video"
)

type Message struct {
	ID          int64
	SenderID    string
	ReceiverID  string
	Content     string
	MediaPath   string
	MessageType MessageType
	Timestamp   time.Time
	Attachments []Attachment `gorm:"foreignKey:MessageID"`
}

type Attachment struct {
	ID        int64
	MessageID int64
	FilePath  string
	FileSize  int64
	MimeType  string
}
