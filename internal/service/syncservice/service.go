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

// ShouldSync 根据配置和来源ID判定当前消息是否应进入社媒同步。
// 这样做的原因是将策略判断集中管理，确保“配置驱动”规则在全链路一致生效。
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

// ContainsExactTarget 执行目标频道精确匹配，不做模糊匹配。
// 这样做的原因是保持规则可预测，避免误同步到非目标频道。
func ContainsExactTarget(targetChannels []string, sourceID string) bool {
	for _, channel := range targetChannels {
		if channel == sourceID {
			return true
		}
	}
	return false
}

// Dispatch 统一调度多个 Sender 并汇总结果，不关心具体平台实现。
// 这样做的原因是解耦“分发编排”和“平台细节”，便于扩展新平台与测试替身注入。
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
