package main

import (
	"context"
	"fmt"
	"github.com/go-telegram/bot"
	"github.com/go-telegram/bot/models"
	"github.com/rivo/uniseg"
	"github.com/spf13/cobra"
	"io"
	"log"
	"os"
	"os/signal"
	"path/filepath"
	"strings"
	"time"
	"unicode"
)

var logger *log.Logger
var outputPath string

func initLog() {
	output := filepath.Join(outputPath, "bot.log")
	err := os.MkdirAll(outputPath, os.ModePerm) // 创建目录
	if err != nil {
		log.Println("Error creating directory:", outputPath, err)
	}

	// 初始化日志
	logFile, err := os.OpenFile(output, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		log.Fatal("无法创建日志文件: ", err)
	}
	multiWriter := io.MultiWriter(os.Stdout, logFile)
	logger = log.New(multiWriter, "[Bot] ", log.LstdFlags|log.Lshortfile)
}

func start(botToken string) {
	ctx, cancel := signal.NotifyContext(context.Background(), os.Interrupt)
	defer cancel()

	opts := []bot.Option{
		bot.WithDefaultHandler(handler),
		bot.WithMessageTextHandler("/start", bot.MatchTypeExact, startHandler),
		bot.WithMessageTextHandler("/status", bot.MatchTypeExact, versionHandler),
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
	msgText := selectMsgText(update)
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

	output := filepath.Join(outputPath, fmt.Sprintf("%s.md", title))

	// 确保输出目录存在
	err := os.MkdirAll(outputPath, os.ModePerm) // 创建目录
	if err != nil {
		logger.Println("Error creating directory:", outputPath, err)
		return false, "无法创建目录"
	}

	file, err := os.OpenFile(output, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
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

func selectMsgText(update *models.Update) string {
	msgText := update.Message.Text
	msgEntities := update.Message.Entities
	if msgText == "" {
		msgText = update.Message.Caption
		msgEntities = update.Message.CaptionEntities
	}
	return handleMsgLink(msgText, msgEntities)
}

// 判断 `string` 是否是 Emoji
func isEmoji(grapheme string) bool {
	runes := []rune(grapheme)
	if len(runes) > 1 {
		return true // 复合 Emoji（如 👨‍👩‍👧‍👦）
	}
	r := runes[0]
	return (r >= 0x1F600 && r <= 0x1F64F) || // 表情符号 😊
		(r >= 0x1F300 && r <= 0x1F5FF) || // 其他符号 🌀
		(r >= 0x1F680 && r <= 0x1F6FF) || // 交通 🚌
		(r >= 0x1F700 && r <= 0x1F77F) || // 其他 🛐
		(r >= 0x1F900 && r <= 0x1F9FF) || // 动物 🦊
		unicode.Is(unicode.Sk, r) // 符号和变音符
}

func msgToGraphemes(msg string) []string {
	gr := uniseg.NewGraphemes(msg)
	var runeMsg []string
	for gr.Next() {
		runeMsg = append(runeMsg, gr.Str())
	}
	return runeMsg
}

func handleMsgLink(msg string, entities []models.MessageEntity) string {
	if entities == nil || len(entities) == 0 {
		return msg
	}

	// 过滤出超链接
	links := make([]models.MessageEntity, 0, len(entities))
	for _, entity := range entities {
		if entity.Type == models.MessageEntityTypeTextLink {
			links = append(links, entity)
		}
	}
	if len(links) == 0 {
		return msg
	}

	var result strings.Builder
	graphemes := msgToGraphemes(msg)
	linkIndex, tgOffset := 0, 0
	// tgOffset 	tg 识别 emoji 默认占位 2，手工维护以和 offset/length 对齐
	// linkIndex	links 的下标索引

	for i := 0; i < len(graphemes); i++ {
		ch := graphemes[i]
		if linkIndex < len(links) {
			entity := links[linkIndex]
			offset, length := entity.Offset, entity.Length

			if tgOffset == offset {
				result.WriteString("[")
				for j := 0; j < length; j++ {
					if i < len(graphemes) { // NOTE: 防止最后一位偶发的越界问题
						ch = graphemes[i]
					}
					if j != length-1 {
						i++
						if isEmoji(ch) {
							tgOffset += 2 // Telegram 认为 Emoji 长度为 2
							j++           // offset 技术也应该保持相同步长
						} else {
							tgOffset++
						}
					}
					result.WriteString(ch)
				}

				result.WriteString(fmt.Sprintf("](%s)", entity.URL))
				linkIndex++
			} else {
				result.WriteString(ch)
			}
		} else {
			result.WriteString(ch)
		}

		if isEmoji(ch) {
			tgOffset += 2 // Telegram 认为 Emoji 长度为 2
		} else {
			tgOffset++
		}
	}
	return result.String()
}

func main() {
	var BOT_TOKEN string
	var OUTPUT_PATH string

	var cmdSync = &cobra.Command{
		Use:   "sync",
		Short: "Sync the message from tg bot",
		Long:  `Sync the message from tg bot.`,
		Args:  cobra.MinimumNArgs(0),
		Run: func(cmd *cobra.Command, args []string) {
			outputPath = OUTPUT_PATH
			initLog()
			start(BOT_TOKEN)
		},
	}

	cmdSync.Flags().StringVarP(&OUTPUT_PATH, "output", "o", "./archives", "Output file for archive.")
	cmdSync.Flags().StringVarP(&BOT_TOKEN, "token", "t", "", "Token for telegram bot.")
	cmdSync.MarkFlagRequired("token")

	var rootCmd = &cobra.Command{Use: "sync"}
	rootCmd.AddCommand(cmdSync)
	rootCmd.Execute()
}
