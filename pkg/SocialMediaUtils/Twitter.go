package SocialMediaUtils

import (
	"context"
	"fmt"
	"log"
	"telegram-message-sync-bot/internal/Entity"

	"github.com/michimani/gotwi/tweet/managetweet"
	"github.com/michimani/gotwi/tweet/managetweet/types"

	"github.com/michimani/gotwi"
)

func initTwitter(config Entity.Config) gotwi.NewClientInput {

	Twitter := config.SocialMediaSync.Twitter
	return gotwi.NewClientInput{
		AuthenticationMethod: gotwi.AuthenMethodOAuth1UserContext,
		OAuthToken:           Twitter.OauthToken,
		OAuthTokenSecret:     Twitter.OauthTokenSecret,
	}
}

func SendTwitter(globalConfig Entity.Config, Message string) bool {
	// 提前返回结果失败
	if globalConfig.SocialMediaSync.Twitter.Enable == false {
		log.Println("Twitter is not enabled in the configuration.")
		return false
	}

	config := initTwitter(globalConfig)
	/**
	* more config for
	* GOTWI_API_KEY
	* GOTWI_API_KEY_SECRET
	 */

	c, err := gotwi.NewClient(&config)
	if err != nil {
		fmt.Println(err)
		return false
	}

	p := &types.CreateInput{
		Text: gotwi.String(Message),
	}

	res, err := managetweet.Create(context.Background(), c, p)
	if err != nil {
		fmt.Println(err.Error())
		return false
	}

	fmt.Printf("[%s] %s\n", gotwi.StringValue(res.Data.ID), gotwi.StringValue(res.Data.Text))
	return true
}
