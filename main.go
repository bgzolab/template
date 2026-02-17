package main

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"os/signal"
	"path/filepath"
	"telegram-message-sync-bot/internal/Entity"
	"telegram-message-sync-bot/internal/Handler"
	"telegram-message-sync-bot/internal/service/bootstrapservice"
	"telegram-message-sync-bot/internal/service/pipelineservice"
	"telegram-message-sync-bot/pkg/FileUtils"
	"telegram-message-sync-bot/pkg/LogUtils"
	"time"

	"github.com/go-telegram/bot"
	"github.com/go-telegram/bot/models"
	"github.com/spf13/cobra"
)

// 全局配置
var globalConfig Entity.Config

// start 启动 Telegram Bot
func start(botToken string) {
	ctx, cancel := signal.NotifyContext(context.Background(), os.Interrupt)
	defer cancel()

	opts := []bot.Option{
		bot.WithDefaultHandler(defalutHandler),
		bot.WithMessageTextHandler("/start", bot.MatchTypeExact, Handler.Start),
		bot.WithMessageTextHandler("/status", bot.MatchTypeExact, Handler.Version),
	}

	b, err := bot.New(botToken, opts...)
	if err != nil {
		LogUtils.GetLogger().Fatal(err)
	}

	_, err = b.SetMyCommands(ctx, &bot.SetMyCommandsParams{
		Commands: []models.BotCommand{
			{Command: "start", Description: "Start bot"},
			{Command: "status", Description: "Check bot status"},
		},
	})
	if err != nil {
		LogUtils.GetLogger().Fatalf("设置命令失败: %v", err)
	}

	b.Start(ctx)
}

/** 消息默认处理器，默认缓存所有消息
 */
func defalutHandler(ctx context.Context, b *bot.Bot, update *models.Update) {
	if update.Message == nil {
		return
	}

	if globalConfig.Output.JSON {
		persistJSON(update)
	}

	pipeline := pipelineservice.NewDefaultPipeline()
	result := pipeline.ProcessUpdate(ctx, b, update, globalConfig)

	if !result.PersistResult.OK {
		LogUtils.GetLogger().Println(result.PersistResult.Message)
	}
	if !result.SyncEnabled {
		LogUtils.GetLogger().Println(result.SyncReason)
	}

	for _, outbound := range result.OutboundMessages {
		_, _ = b.SendMessage(ctx, &bot.SendMessageParams{
			ChatID: outbound.ChatID,
			Text:   outbound.Text,
		})
	}
}

func persistJSON(update *models.Update) (bool, string) {
	if update.Message == nil {
		return false, "接受消息为空"
	}

	// 使用 json.Marshal 将对象转换为 JSON 字符串
	jsonData, errJson := json.Marshal(update)
	if errJson != nil {
		fmt.Println("转换 JSON 失败:", errJson)
		return false, "转换 JSON 失败"
	}

	// 使用时间戳生成唯一文件名
	timestamp := time.Now().Format("20060102_150405") + fmt.Sprintf("_%d", time.Now().UnixNano()%1e6)

	FileUtils.OutputString(filepath.Join(globalConfig.Output.JsonDir, time.Now().Format("20060102")),
		fmt.Sprintf("%s%s", timestamp, ".json"),
		string(jsonData))

	return true, "JSON序列化成功"
}

func main() {
	var configFile string

	var cmdSync = &cobra.Command{
		Use:   "sync",
		Short: "Sync the message from tg bot",
		Long:  `Sync the message from tg bot.`,
		Args:  cobra.MinimumNArgs(0),
		Run: func(cmd *cobra.Command, args []string) {
			loadedConfig, err := bootstrapservice.LoadConfig(configFile)
			if err != nil {
				fmt.Printf("加载配置失败: %v\n", err)
				return
			}

			globalConfig = loadedConfig
			fmt.Printf("解析配置成功: 配置内容: %+v\n", globalConfig)

			err = bootstrapservice.InitRuntime(globalConfig)
			if err != nil {
				fmt.Printf("初始化运行时失败: %v\n", err)
				LogUtils.GetLogger().Println(err)
				return
			}

			start(globalConfig.Token)
		},
	}

	cmdSync.Flags().StringVarP(&configFile, "config", "c", "./config/config.yaml", "config for bot.")
	err := cmdSync.MarkFlagRequired("config")
	if err != nil {
		return
	}

	var rootCmd = &cobra.Command{Use: "sync"}
	rootCmd.AddCommand(cmdSync)
	err = rootCmd.Execute()
	if err != nil {
		return
	}

	//message := "Hello world from script!"
	//fmt.Println(SocialMediaUtils.SendBlueSky(globalConfig, message))
	//fmt.Println(SocialMediaUtils.SendTwitter(globalConfig, message))
	//fmt.Println(SocialMediaUtils.SendMastodon(globalConfig, message))

}
