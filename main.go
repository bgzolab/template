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
		bot.WithMessageTextHandler("/status", bot.MatchTypeExact, versionHandler),
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
			{Command: "start", Description: "Start bot"},
			{Command: "status", Description: "Check bot status"},
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
	if update.Message == nil {
		return
	}
	ok, msg := persistMessage(update)
	if !ok {
		logger.Println(msg)
	} else {
		b.SendMessage(ctx, &bot.SendMessageParams{
			ChatID: update.Message.Chat.ID,
			Text:   fmt.Sprintf("信息已备案至: %s!", msg),
		})
	}
}

func versionHandler(ctx context.Context, b *bot.Bot, update *models.Update) {
	b.SendMessage(ctx, &bot.SendMessageParams{
		ChatID: update.Message.Chat.ID,
		Text:   "I'm working!",
	})
}

func startHandler(ctx context.Context, b *bot.Bot, update *models.Update) {
	b.SendMessage(ctx, &bot.SendMessageParams{
		ChatID: update.Message.Chat.ID,
		Text:   "Hello world!",
	})
}

func persistMessage(update *models.Update) (bool, string) {
	if update.Message == nil {
		return false, "接受消息为空"
	}

	title := fmt.Sprintf("chat_%d.md", update.Message.Chat.ID)
	msgText := update.Message.Text
	if msgText == "" {
		msgText = update.Message.Caption
	}
	sourceLink := ""
	sourceDate := time.Now()

	if update.Message.ForwardOrigin != nil && update.Message.ForwardOrigin.Type == "channel" {
		// 消息为转发，特殊处理
		origin := update.Message.ForwardOrigin.MessageOriginChannel
		title = origin.Chat.Title

		sourceLink = fmt.Sprintf("https://t.me/%s/%d",
			origin.Chat.Username,
			origin.MessageID)
		sourceDate = time.Unix(int64(origin.Date), 0)
	}

	file, err := os.OpenFile(fmt.Sprintf("%s.md", title),
		os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		logger.Println("Error opening file for writing: ", err)
		return false, "无法打开文件以写入"
	}

	logCommandline := fmt.Sprintf("ChatID: %d, User: %s, Message: %s",
		update.Message.Chat.ID,
		title,
		msgText,
	)
	logger.Print(logCommandline)

	defer file.Close() // 关闭时会刷新缓冲区

	logMarkdown := fmt.Sprintf("\n## %s\n\n%s\n\n%s\n",
		sourceDate.Format("2006-01-02 15:04:05"),
		msgText,
		sourceLink,
	)

	_, err = file.WriteString(logMarkdown)
	if err != nil {
		logger.Println("Error writing to file: ", err)
		return false, "写入文件失败"
	}

	file.Sync() // 强制写入磁盘
	return true, title
}
