package syncservice

import (
	"telegram-message-sync-bot/internal/Entity"
	"telegram-message-sync-bot/pkg/SocialMediaUtils"
)

type blueSkySender struct{}

func (blueSkySender) Name() string {
	return "BlueSky"
}

func (blueSkySender) Send(config Entity.Config, message string) bool {
	return SocialMediaUtils.SendBlueSky(config, message)
}

type mastodonSender struct{}

func (mastodonSender) Name() string {
	return "Mastodon"
}

func (mastodonSender) Send(config Entity.Config, message string) bool {
	return SocialMediaUtils.SendMastodon(config, message)
}

type twitterSender struct{}

func (twitterSender) Name() string {
	return "Twitter"
}

func (twitterSender) Send(config Entity.Config, message string) bool {
	return SocialMediaUtils.SendTwitter(config, message)
}

func DefaultSenders() []Sender {
	return []Sender{
		blueSkySender{},
		mastodonSender{},
		twitterSender{},
	}
}
