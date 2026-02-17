package notifyservice

import (
	"fmt"
	"telegram-message-sync-bot/internal/Entity"
	"telegram-message-sync-bot/internal/service/syncservice"
)

type OutboundMessage struct {
	ChatID int64
	Text   string
}

func ResolveTargetChatIDs(config Entity.Config, fallbackChatID int64) []int64 {
	if len(config.TargetUserList) > 0 {
		return config.TargetUserList
	}
	return []int64{fallbackChatID}
}

func BuildArchiveResponse(ok bool, sourceLink, message string) string {
	if ok {
		return fmt.Sprintf("%s\n消息已备案至: %s!", sourceLink, message)
	}
	return fmt.Sprintf("%s\n消息备份出现异常: %s!", sourceLink, message)
}

func BuildSyncNotifications(syncEnabled bool, syncReason string, results []syncservice.DispatchResult) []string {
	if !syncEnabled {
		return []string{syncReason}
	}

	notifications := make([]string, 0, len(results))
	for _, result := range results {
		if result.Success {
			notifications = append(notifications, fmt.Sprintf("消息已同步至 %s!", result.Platform))
			continue
		}
		notifications = append(notifications, fmt.Sprintf("同步 %s 失败", result.Platform))
	}

	return notifications
}

func BuildOutboundMessages(chatIDs []int64, archiveResponse string, syncNotifications []string) []OutboundMessage {
	outbound := make([]OutboundMessage, 0, len(chatIDs)*(1+len(syncNotifications)))
	for _, chatID := range chatIDs {
		outbound = append(outbound, OutboundMessage{ChatID: chatID, Text: archiveResponse})
		for _, text := range syncNotifications {
			outbound = append(outbound, OutboundMessage{ChatID: chatID, Text: text})
		}
	}
	return outbound
}
