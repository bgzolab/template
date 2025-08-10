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
	ID int64

	Content string // 消息内容

	MessageID   int64        // 用于标识消息来源的唯一ID
	Username    string       // 频道的USERNAME
	MessageUrl  string       // 消息的URL链接
	MessageDate time.Time    // 消息的时间戳
	Attachments []Attachment `gorm:"foreignKey:MessageID"` // 消息附件

	CreatedTime time.Time // 消息存档日期
}

type Attachment struct {
	ID          int64
	MessageID   int64 // 关联的消息ID，并非频道的消息ID
	FilePath    string
	FileSize    int64
	MessageType MessageType
}
