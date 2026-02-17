package Database

import (
	"strings"
	"telegram-message-sync-bot/internal/Entity"
)

// 保存消息及附件
func SaveMessage(msg *Entity.Message) (int64, error) {
	err := DB.Create(msg).Error
	if err != nil {
		return 0, err
	}
	return msg.ID, nil
}

func IsDuplicateMessageError(err error) bool {
	if err == nil {
		return false
	}

	errMsg := err.Error()
	return strings.Contains(errMsg, "UNIQUE constraint failed") || strings.Contains(errMsg, "duplicated key")
}

// 按ID查找消息（含附件）
func GetMessageByID(id int64) (*Entity.Message, error) {
	var msg Entity.Message
	err := DB.Preload("Attachments").First(&msg, id).Error
	if err != nil {
		return nil, err
	}
	return &msg, nil
}

// 按用户查找消息（含附件）
func GetMessagesByUser(userID string, limit int) ([]Entity.Message, error) {
	var msgs []Entity.Message
	err := DB.Preload("Attachments").
		Where("sender_id = ? OR receiver_id = ?", userID, userID).
		Order("timestamp DESC").
		Limit(limit).
		Find(&msgs).Error
	if err != nil {
		return nil, err
	}
	return msgs, nil
}

// 更新消息内容
func UpdateMessage(msg *Entity.Message) error {
	return DB.Save(msg).Error
}

// 删除消息及附件
func DeleteMessage(id int64) error {
	// 先删除附件
	DB.Where("message_id = ?", id).Delete(&Entity.Attachment{})
	return DB.Delete(&Entity.Message{}, id).Error
}
