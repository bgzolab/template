package SocialMediaUtils

import (
	"github.com/reiver/go-atproto/com/atproto/repo"
	"github.com/reiver/go-atproto/com/atproto/server"
	"telegram-message-sync-bot/internal/Entity"
	"time"
	_ "time"
)

func initBlueSky(config Entity.Config) (username string, password string) {
	if config.SocialMediaSync.BlueSky.Enabled == false {
		return "", ""
	}
	BlueSky := config.SocialMediaSync.BlueSky
	return BlueSky.Identifier, BlueSky.Password
}

func SendBlueSky(config Entity.Config, Message string) bool {
	/**
	 * 开启了二步验证怎么办？
	 */
	var identifier, password = initBlueSky(config)

	var dst server.CreateSessionResponse
	err := server.CreateSession(&dst, identifier, password)
	if nil != err {
		return false
	}
	bearerToken := dst.AccessJWT

	when := time.Now().Format("2006-01-02T15:04:05.999Z")
	post := map[string]any{
		"$type":     "app.bsky.feed.post",
		"text":      Message,
		"createdAt": when,
	}
	var repoName string = identifier
	var collection string = "app.bsky.feed.post"

	recordErr := repo.CreateRecord(&dst, bearerToken, repoName, collection, post)

	if nil != recordErr {
		return false
	}
	return true
}
