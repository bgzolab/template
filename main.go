package main

import (
	"context"
	"fmt"
	"github.com/go-telegram/bot"
	"github.com/go-telegram/bot/models"
	"github.com/joho/godotenv"
	"io"
	"log"
	"os"
	"os/signal"
	"time"
)

var logger *log.Logger

func init() {
	// 初始化日志
	logFile, err := os.OpenFile("bot.log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		log.Fatal("无法创建日志文件: ", err)
	}
	multiWriter := io.MultiWriter(os.Stdout, logFile)
	logger = log.New(multiWriter, "[Bot] ", log.LstdFlags|log.Lshortfile)
}

func main() {
	ctx, cancel := signal.NotifyContext(context.Background(), os.Interrupt)
	defer cancel()

	opts := []bot.Option{
		bot.WithDefaultHandler(handler),
		bot.WithMessageTextHandler("/start", bot.MatchTypeExact, startHandler),
		bot.WithMessageTextHandler("/version", bot.MatchTypeExact, versionHandler),
	}

	// 加载 .env 文件
	if err := godotenv.Load(); err != nil {
		logger.Println("加载环境变量失败:", err)
		return
	}

	botToken := os.Getenv("TG_BOT_TOKEN")
	if botToken == "" {
		logger.Println("TG_BOT_TOKEN 未设置")
		return
	}

	b, err := bot.New(botToken, opts...)
	if err != nil {
		logger.Fatal(err)
	}

	_, err = b.SetMyCommands(ctx, &bot.SetMyCommandsParams{
		Commands: []models.BotCommand{
			{Command: "start", Description: "Hello world!"},
			{Command: "version", Description: "I'm working!"},
		},
	})
	if err != nil {
		logger.Fatalf("设置命令失败: %v", err)
	}

	b.Start(ctx)
}

/** 消息默认处理器，默认缓存所有消息
 */
func handler(ctx context.Context, b *bot.Bot, update *models.Update) {
	logMessage(update)
}

func versionHandler(ctx context.Context, b *bot.Bot, update *models.Update) {
	logMessage(update)
	b.SendMessage(ctx, &bot.SendMessageParams{
		ChatID: update.Message.Chat.ID,
		Text:   "I'm working!",
	})
}

func startHandler(ctx context.Context, b *bot.Bot, update *models.Update) {
	logMessage(update)
	b.SendMessage(ctx, &bot.SendMessageParams{
		ChatID: update.Message.Chat.ID,
		Text:   "Hello world!",
	})
}

func logMessage(update *models.Update) {
	if update.Message == nil {
		return
	}
	logEntry := fmt.Sprintf("ChatID: %d, User: %s, Message: %s",
		update.Message.Chat.ID,
		update.Message.From.Username,
		update.Message.Text,
	)
	logger.Println(logEntry)
	persistMessage(update)
}

func persistMessage(update *models.Update) {
	if update.Message == nil {
		return
	}

	var fileName string
	sourceLink := ""
	sourceDate := time.Now()

	if update.Message.ForwardOrigin != nil && update.Message.ForwardOrigin.Type == "channel" {
		// 消息为转发，进入特殊处理
		origin := update.Message.ForwardOrigin.MessageOriginChannel

		fileName = fmt.Sprintf("%s.md", origin.Chat.Title)
		sourceLink = fmt.Sprintf("https://t.me/%s/%d",
			origin.Chat.Username,
			origin.MessageID)
		sourceDate = time.Unix(int64(origin.Date), 0)
	} else {
		fileName = fmt.Sprintf("chat_%d.md", update.Message.Chat.ID)
	}

	file, err := os.OpenFile(fileName, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		logger.Println("Error opening file for writing: ", err)
		return
	}

	defer file.Close() // 关闭时会刷新缓冲区

	logEntry := fmt.Sprintf("\n## %s\n\n%s\n\n%s\n",
		sourceDate.Format("2006-01-02 15:04:05"),
		update.Message.Text,
		sourceLink,
	)

	_, err = file.WriteString(logEntry)
	if err != nil {
		logger.Println("Error writing to file: ", err)
		return
	}

	file.Sync() // 强制写入磁盘
}
