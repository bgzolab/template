package main

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"os/signal"
	"path/filepath"
	"telegram-message-sync-bot/internal/Database"
	"telegram-message-sync-bot/internal/Entity"
	"telegram-message-sync-bot/internal/Handler"
	"telegram-message-sync-bot/internal/service/archiveservice"
	"telegram-message-sync-bot/internal/service/notifyservice"
	"telegram-message-sync-bot/internal/service/syncservice"
	"telegram-message-sync-bot/pkg/FileUtils"
	"telegram-message-sync-bot/pkg/LogUtils"
	"time"

	"github.com/go-telegram/bot"
	"github.com/go-telegram/bot/models"
	"github.com/spf13/cobra"
	"gopkg.in/yaml.v3"
)

// 全局配置
var globalConfig Entity.Config

func initSetting(configFile string) {
	data, err := os.ReadFile(configFile)
	if err != nil {
		fmt.Printf("读取配置文件失败: %v", err)
	}
	err = yaml.Unmarshal(data, &globalConfig)
	if err != nil {
		fmt.Printf("解析配置失败: %v", err)
	}
	fmt.Printf("解析配置成功: 配置内容: %+v\n", globalConfig)
}

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

	persistResult := archiveservice.PersistMessage(ctx, b, update, globalConfig)
	targetChatIDs := notifyservice.ResolveTargetChatIDs(globalConfig, update.Message.Chat.ID)
	archiveResponse := notifyservice.BuildArchiveResponse(persistResult.OK, persistResult.SourceLink, persistResult.Message)
	if !persistResult.OK {
		LogUtils.GetLogger().Println(persistResult.Message)
	}

	syncEnabled, syncReason := syncservice.ShouldSync(globalConfig, persistResult.SourceID)
	if !syncEnabled {
		LogUtils.GetLogger().Println(syncReason)
	}

	results := make([]syncservice.DispatchResult, 0)
	if syncEnabled {
		results = syncservice.Dispatch(globalConfig, persistResult.MsgText, syncservice.DefaultSenders())
	}

	syncNotifications := notifyservice.BuildSyncNotifications(syncEnabled, syncReason, results)
	outboundMessages := notifyservice.BuildOutboundMessages(targetChatIDs, archiveResponse, syncNotifications)

	for _, outbound := range outboundMessages {
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
			// 初始化配置
			initSetting(configFile)
			// 初始化日志
			LogUtils.InitLogger(globalConfig.Log.Dir)
			// 初始化数据目录
			err := Database.InitORMDB(filepath.Join(globalConfig.Log.Dir))
			if err != nil {
				LogUtils.GetLogger().Println(err)
			}
			// 启动机器人
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
