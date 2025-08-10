package SocialMediaUtils

import (
	"context"
	"fmt"
	"log"
	"telegram-message-sync-bot/internal/Entity"

	"github.com/mattn/go-mastodon"
)

func initMastodon(config Entity.Config) mastodon.Config {
	if config.SocialMediaSync.Mastodon.Enabled == false {
		log.Println("Mastodon is not enabled in the configuration.")
		return mastodon.Config{}
	}
	Mastodon := config.SocialMediaSync.Mastodon
	return mastodon.Config{
		Server:       Mastodon.Instance,
		ClientID:     Mastodon.ClientId,
		ClientSecret: Mastodon.ClientSecret,
		AccessToken:  Mastodon.AccessToken,
	}
}

func SendMastodon(globalConfig Entity.Config, Message string) bool {
	config := initMastodon(globalConfig)

	// Create the client
	c := mastodon.NewClient(&config)

	// Post a toot
	visibility := "public"

	toot := mastodon.Toot{
		Status:     Message,
		Visibility: visibility,
	}

	post, err := c.PostStatus(context.Background(), &toot)
	if err != nil {
		log.Fatalf("%#v\n", err)
		return false
	}

	fmt.Println("My new post is:", post)
	return true
}
