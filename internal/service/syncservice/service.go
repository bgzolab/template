package syncservice

import (
	"fmt"
	"telegram-message-sync-bot/internal/Entity"
)

type Sender interface {
	Name() string
	Send(config Entity.Config, message string) bool
}

type DispatchResult struct {
	Platform string
	Success  bool
}

func ShouldSync(config Entity.Config, sourceID string) (bool, string) {
	if !config.SocialMediaSync.Enable {
		return false, "社媒同步未启用"
	}

	if len(config.SocialMediaSync.TargetChannel) == 0 {
		return false, "社媒同步目标频道为空，跳过同步"
	}

	if !ContainsExactTarget(config.SocialMediaSync.TargetChannel, sourceID) {
		return false, fmt.Sprintf("未命中社媒同步规则，跳过同步: %s", sourceID)
	}

	return true, ""
}

func ContainsExactTarget(targetChannels []string, sourceID string) bool {
	for _, channel := range targetChannels {
		if channel == sourceID {
			return true
		}
	}
	return false
}

func Dispatch(config Entity.Config, message string, senders []Sender) []DispatchResult {
	results := make([]DispatchResult, 0, len(senders))
	for _, sender := range senders {
		if sender == nil {
			continue
		}

		ok := sender.Send(config, message)
		results = append(results, DispatchResult{
			Platform: sender.Name(),
			Success:  ok,
		})
	}
	return results
}
