package Database

import (
	"database/sql"
	"fmt"
	"telegram-message-sync-bot/internal/Entity"
)

func SaveMessage(msg *Entity.Message) (int64, error) {
	tx, err := DB.Begin()
	if err != nil {
		return 0, fmt.Errorf("failed to begin transaction: %w", err)
	}
	defer func() {
		if err != nil {
			err := tx.Rollback()
			if err != nil {
				return
			}
		}
	}()

	// 插入主消息
	result, err := tx.Exec(`
		INSERT INTO messages (sender_id, receiver_id, content, media_path, message_type, timestamp)
		VALUES (?, ?, ?, ?, ?, ?)`,
		msg.SenderID, msg.ReceiverID, msg.Content, msg.MediaPath, msg.MessageType, msg.Timestamp,
	)

	if err != nil {
		return 0, fmt.Errorf("failed to insert message: %w", err)
	}

	msgID, err := result.LastInsertId()
	if err != nil {
		return 0, fmt.Errorf("failed to get last insert ID: %w", err)
	}

	// 插入附件
	for _, attachment := range msg.Attachments {
		_, err := tx.Exec(`
			INSERT INTO attachments (message_id, file_path, file_size, mime_type)
			VALUES (?, ?, ?, ?)`,
			msgID, attachment.FilePath, attachment.FileSize, attachment.MimeType,
		)
		if err != nil {
			return 0, fmt.Errorf("failed to insert attachment: %w", err)
		}
	}

	if err := tx.Commit(); err != nil {
		return 0, fmt.Errorf("failed to commit transaction: %w", err)
	}

	return msgID, nil
}

func GetMessagesByUser(userID string, limit int) ([]Entity.Message, error) {
	rows, err := DB.Query(`
		SELECT m.id, m.sender_id, m.receiver_id, m.content, m.media_path, m.message_type, m.timestamp,
		       a.id, a.file_path, a.file_size, a.mime_type
		FROM messages m
		LEFT JOIN attachments a ON m.id = a.message_id
		WHERE m.sender_id = ? OR m.receiver_id = ?
		ORDER BY m.timestamp DESC
		LIMIT ?`, userID, userID, limit)

	if err != nil {
		return nil, fmt.Errorf("failed to query messages: %w", err)
	}
	defer rows.Close()

	messagesMap := make(map[int64]*Entity.Message)

	for rows.Next() {
		var msg Entity.Message
		var _ Entity.Attachment
		var attachmentID sql.NullInt64
		var filePath, mimeType sql.NullString
		var fileSize sql.NullInt64

		err := rows.Scan(
			&msg.ID, &msg.SenderID, &msg.ReceiverID, &msg.Content,
			&msg.MediaPath, &msg.MessageType, &msg.Timestamp,
			&attachmentID, &filePath, &fileSize, &mimeType,
		)

		if err != nil {
			return nil, fmt.Errorf("failed to scan message: %w", err)
		}

		if existingMsg, ok := messagesMap[msg.ID]; ok {
			if attachmentID.Valid {
				attachment := Entity.Attachment{
					ID:       attachmentID.Int64,
					FilePath: filePath.String,
					FileSize: fileSize.Int64,
					MimeType: mimeType.String,
				}
				existingMsg.Attachments = append(existingMsg.Attachments, attachment)
			}
		} else {
			if attachmentID.Valid {
				attachment := Entity.Attachment{
					ID:       attachmentID.Int64,
					FilePath: filePath.String,
					FileSize: fileSize.Int64,
					MimeType: mimeType.String,
				}
				msg.Attachments = append(msg.Attachments, attachment)
			}
			messagesMap[msg.ID] = &msg
		}
	}

	messages := make([]Entity.Message, 0, len(messagesMap))
	for _, msg := range messagesMap {
		messages = append(messages, *msg)
	}

	return messages, nil
}
