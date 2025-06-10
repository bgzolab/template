package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"github.com/go-telegram/bot"
	"github.com/go-telegram/bot/models"
	"github.com/spf13/cobra"
	"gopkg.in/yaml.v3"
	"html/template"
	"net/http"
	"os"
	"os/signal"
	"path/filepath"
	"strings"
	"telegram-message-sync-bot/internal/Handler"
	"telegram-message-sync-bot/internal/entity"
	"telegram-message-sync-bot/pkg/FileUtils"
	"telegram-message-sync-bot/pkg/LogUtils"
	//"telegram-message-sync-bot/pkg/SocialMediaUtils"
	"telegram-message-sync-bot/pkg/StrUtils"
	"telegram-message-sync-bot/pkg/TgUtils"
	"time"
)

// 全局配置
var globalConfig entity.Config

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

	ok, msg, sourceLink := persistMessage(ctx, b, update)
	targetChatIdList := []int64{update.Message.Chat.ID}
	if len(globalConfig.TargetUserList) > 0 {
		targetChatIdList = globalConfig.TargetUserList
	}

	responseTxt := ""
	if !ok {
		LogUtils.GetLogger().Println(msg)
		responseTxt = fmt.Sprintf("%s\n消息备份出现异常: %s!", sourceLink, msg)
	} else {
		responseTxt = fmt.Sprintf("%s\n消息已备案至: %s!", sourceLink, msg)
	}

	for _, chatId := range targetChatIdList {
		_, _ = b.SendMessage(ctx, &bot.SendMessageParams{
			ChatID: chatId,
			Text:   responseTxt,
		})
	}
}

func formatDownloadedFiles(files []string) string {
	var builder strings.Builder
	for _, file := range files {
		builder.WriteString("![](")
		builder.WriteString(file)
		builder.WriteString(") ")
	}
	return builder.String()
}

func persistMessage(ctx context.Context, b *bot.Bot, update *models.Update) (bool, string, string) {
	if update.Message == nil {
		return false, "接受消息为空", ""
	}

	// 默认为私人消息
	outputPath := globalConfig.Output.PersonDir
	sourceId := fmt.Sprintf("%d", update.Message.Chat.ID)
	fileName := fmt.Sprintf("%s.md", sourceId)
	msgText := selectMsgText(update)
	sourceLink := ""
	sourceDate := time.Now()
	photoLink := ""

	if update.Message.ForwardOrigin != nil && update.Message.ForwardOrigin.Type == "channel" {
		// 消息为转发，特殊处理
		outputPath = globalConfig.Output.ChannelDir
		origin := update.Message.ForwardOrigin.MessageOriginChannel

		if origin.Chat.Username != "" {
			sourceId = origin.Chat.Username
			fileName = fmt.Sprintf("%s.md", sourceId)
		} else {
			sourceId = fmt.Sprintf("%d", origin.Chat.ID)
			fileName = fmt.Sprintf("%s.md", sourceId)
		}

		sourceLink = fmt.Sprintf("https://t.me/%s/%d",
			sourceId,
			origin.MessageID)
		sourceDate = time.Unix(int64(origin.Date), 0)

		if StrUtils.SearchInFile(filepath.Join(outputPath, fileName), sourceLink) {
			return false, fmt.Sprint("消息已存在"), sourceLink
		}

		var files []string
		photos := update.Message.Photo
		if len(photos) > 0 {
			highestResolutionPhoto := photos[len(photos)-1]
			file := persistFile(ctx, b, highestResolutionPhoto.FileID, sourceId, outputPath)
			if file != "" {
				files = append(files, file)
			}
		}

		photoLink = formatDownloadedFiles(files)
	}

	logCommandline := fmt.Sprintf("ChatID: %d, Channel: %s, Message: %s",
		update.Message.Chat.ID,
		sourceId,
		msgText,
	)

	LogUtils.GetLogger().Println(logCommandline)

	timeFormat := "2006-01-02 15:04:05"
	data := map[string]interface{}{
		"title":          sourceDate.Format(timeFormat),
		"photo":          photoLink,
		"content":        msgText,
		"sourceTelegram": sourceLink,
		"now":            time.Now().Format(timeFormat),
		"date":           sourceDate.Format(timeFormat),
	}

	// 读取模板文件
	tmplData, err := os.ReadFile(globalConfig.Template.Dir)
	if err != nil {
		return false, fmt.Sprintf("读取模板失败, %v", err), sourceLink
	}

	// 创建并解析模板
	tmpl, err := template.New("example").Parse(string(tmplData))
	if err != nil {
		return false, fmt.Sprintf("解析模板失败, %v", err), sourceLink
	}

	// 使用 bytes.Buffer 捕获渲染结果
	var buf bytes.Buffer
	err = tmpl.Execute(&buf, data)
	if err != nil {
		return false, fmt.Sprintf("渲染模板失败, %v", err), sourceLink
	}

	FileUtils.OutputString(outputPath, fileName, buf.String())

	return true, fileName, sourceLink
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

func persistFile(ctx context.Context, b *bot.Bot, fileID string, dirname string, outputPath string) string {
	// 获取文件信息
	params := bot.GetFileParams{FileID: fileID}
	file, err := b.GetFile(ctx, &params)
	if err != nil {
		LogUtils.GetLogger().Println("获取文件信息失败: %v", err)
		return ""
	}

	// 构造下载 URL
	downloadURL := fmt.Sprintf("https://api.telegram.org/file/bot%s/%s", b.Token(), file.FilePath)

	// 获取文件扩展名
	ext := filepath.Ext(file.FilePath)
	if ext == "" {
		ext = ".dat" // 如果没有扩展名，则存为 .dat
	}

	// 下载文件
	resp, err := http.Get(downloadURL)
	if err != nil {
		LogUtils.GetLogger().Println("下载文件失败: %v", err)
		return ""
	}

	// 使用时间戳生成唯一文件名
	timestamp := time.Now().Format("20060102_150405") + fmt.Sprintf("_%d", time.Now().UnixNano()%1e6)
	FileUtils.OutputResponse(filepath.Join(outputPath, "assets", dirname), fmt.Sprintf("%s%s", timestamp, ext), resp)

	return filepath.Join("assets", dirname, fmt.Sprintf("%s%s", timestamp, ext))
}

func selectMsgText(update *models.Update) string {
	msgText := update.Message.Text
	msgEntities := update.Message.Entities
	if msgText == "" {
		msgText = update.Message.Caption
		msgEntities = update.Message.CaptionEntities
	}
	return StrUtils.EscapeHashtags(TgUtils.HandleMsgLink(msgText, msgEntities))
}

func main() {
	var configFile string

	var cmdSync = &cobra.Command{
		Use:   "sync",
		Short: "Sync the message from tg bot",
		Long:  `Sync the message from tg bot.`,
		Args:  cobra.MinimumNArgs(0),
		Run: func(cmd *cobra.Command, args []string) {
			initSetting(configFile)
			LogUtils.InitLogger(globalConfig.Log.Dir)
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
	//fmt.Println(SocialMediaUtils.SendBlueSky(message))
	//fmt.Println(SocialMediaUtils.SendMastodon(message))

}
