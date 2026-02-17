package archiveservice

import (
	"bytes"
	"context"
	"fmt"
	"html/template"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"telegram-message-sync-bot/internal/Database"
	"telegram-message-sync-bot/internal/Entity"
	"telegram-message-sync-bot/pkg/FileUtils"
	"telegram-message-sync-bot/pkg/LogUtils"
	"telegram-message-sync-bot/pkg/StrUtils"
	"telegram-message-sync-bot/pkg/TgUtils"
	"time"

	"github.com/go-telegram/bot"
	"github.com/go-telegram/bot/models"
)

type PersistResult struct {
	OK         bool
	Message    string
	SourceLink string
	MsgText    string
	SourceID   string
}

type SourceMeta struct {
	OutputPath string
	SourceID   string
	FileName   string
	SourceLink string
	SourceDate time.Time
	MessageID  int
}

func PersistMessage(ctx context.Context, b *bot.Bot, update *models.Update, config Entity.Config) PersistResult {
	if update.Message == nil {
		return PersistResult{OK: false, Message: "接受消息为空"}
	}

	meta := ResolveSourceMeta(update, config)
	msgText := SelectMsgText(update)
	photoLink := ""
	assets := []Entity.Attachment{}

	if meta.SourceLink != "" && StrUtils.SearchInFile(filepath.Join(meta.OutputPath, meta.FileName), meta.SourceLink) {
		return PersistResult{OK: false, Message: "消息已存在", SourceLink: meta.SourceLink, MsgText: msgText, SourceID: meta.SourceID}
	}

	if update.Message.ForwardOrigin != nil && update.Message.ForwardOrigin.Type == "channel" {
		var files []string
		photos := update.Message.Photo
		if len(photos) > 0 {
			highestResolutionPhoto := photos[len(photos)-1]
			file := persistFile(ctx, b, highestResolutionPhoto.FileID, meta.SourceID, meta.OutputPath, Entity.ImageMessage)
			if file != nil {
				files = append(files, file.FilePath)
				assets = append(assets, *file)
			}
			photoLink = formatDownloadedFiles(files)
		}
	}

	logCommandline := fmt.Sprintf("ChatID: %d, Channel: %s, Message: %s",
		update.Message.Chat.ID,
		meta.SourceID,
		msgText,
	)
	LogUtils.GetLogger().Println(logCommandline)

	data := BuildTemplateData(meta.SourceDate, photoLink, msgText, meta.SourceLink, time.Now())

	tmplData, err := os.ReadFile(config.Template.Dir)
	if err != nil {
		return PersistResult{OK: false, Message: fmt.Sprintf("读取模板失败, %v", err), SourceLink: meta.SourceLink, MsgText: msgText, SourceID: meta.SourceID}
	}

	tmpl, err := template.New("example").Parse(string(tmplData))
	if err != nil {
		return PersistResult{OK: false, Message: fmt.Sprintf("解析模板失败, %v", err), SourceLink: meta.SourceLink, MsgText: msgText, SourceID: meta.SourceID}
	}

	var buf bytes.Buffer
	err = tmpl.Execute(&buf, data)
	if err != nil {
		return PersistResult{OK: false, Message: fmt.Sprintf("渲染模板失败, %v", err), SourceLink: meta.SourceLink, MsgText: msgText, SourceID: meta.SourceID}
	}

	FileUtils.OutputString(meta.OutputPath, meta.FileName, buf.String())

	savedMsg := Entity.Message{
		Content: msgText,

		MessageID:   int64(meta.MessageID),
		Username:    meta.SourceID,
		MessageUrl:  meta.SourceLink,
		MessageDate: meta.SourceDate,
		Attachments: assets,

		CreatedTime: time.Now(),
	}

	messageID, err := Database.SaveMessage(&savedMsg)
	if err != nil {
		if Database.IsDuplicateMessageError(err) {
			return PersistResult{OK: false, Message: "消息已存在", SourceLink: meta.SourceLink, MsgText: msgText, SourceID: meta.SourceID}
		}

		LogUtils.GetLogger().Println(err)
		return PersistResult{OK: false, Message: fmt.Sprintf("消息入库失败: %v", err), SourceLink: meta.SourceLink, MsgText: msgText, SourceID: meta.SourceID}
	}

	LogUtils.GetLogger().Printf("Save successful with: %d\n", messageID)
	return PersistResult{OK: true, Message: meta.FileName, SourceLink: meta.SourceLink, MsgText: msgText, SourceID: meta.SourceID}
}

func ResolveSourceMeta(update *models.Update, config Entity.Config) SourceMeta {
	meta := SourceMeta{
		OutputPath: config.Output.PersonDir,
		SourceID:   fmt.Sprintf("%d", update.Message.Chat.ID),
		SourceDate: time.Now(),
		MessageID:  update.Message.ID,
	}
	meta.FileName = fmt.Sprintf("%s.md", meta.SourceID)

	if update.Message.ForwardOrigin != nil && update.Message.ForwardOrigin.Type == "channel" {
		meta.OutputPath = config.Output.ChannelDir
		origin := update.Message.ForwardOrigin.MessageOriginChannel

		if origin.Chat.Username != "" {
			meta.SourceID = origin.Chat.Username
		} else {
			meta.SourceID = fmt.Sprintf("%d", origin.Chat.ID)
		}

		meta.FileName = fmt.Sprintf("%s.md", meta.SourceID)
		meta.SourceLink = fmt.Sprintf("https://t.me/%s/%d", meta.SourceID, origin.MessageID)
		meta.SourceDate = time.Unix(int64(origin.Date), 0)
		meta.MessageID = origin.MessageID
	}

	return meta
}

func SelectMsgText(update *models.Update) string {
	msgText := update.Message.Text
	msgEntities := update.Message.Entities
	if msgText == "" {
		msgText = update.Message.Caption
		msgEntities = update.Message.CaptionEntities
	}
	return StrUtils.EscapeHashtags(TgUtils.HandleMsgLink(msgText, msgEntities))
}

func BuildTemplateData(sourceDate time.Time, photoLink, msgText, sourceLink string, now time.Time) map[string]interface{} {
	timeFormat := "2006-01-02 15:04:05"
	return map[string]interface{}{
		"title":          sourceDate.Format(timeFormat),
		"photo":          photoLink,
		"content":        msgText,
		"sourceTelegram": sourceLink,
		"now":            now.Format(timeFormat),
		"date":           sourceDate.Format(timeFormat),
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

func persistFile(ctx context.Context, b *bot.Bot, fileID string, dirname string, outputPath string, messageType Entity.MessageType) *Entity.Attachment {
	params := bot.GetFileParams{FileID: fileID}
	file, err := b.GetFile(ctx, &params)
	if err != nil {
		LogUtils.GetLogger().Printf("获取文件信息失败: %v\n", err)
		return nil
	}

	downloadURL := fmt.Sprintf("https://api.telegram.org/file/bot%s/%s", b.Token(), file.FilePath)

	ext := filepath.Ext(file.FilePath)
	if ext == "" {
		ext = ".dat"
	}

	resp, err := http.Get(downloadURL)
	if err != nil {
		LogUtils.GetLogger().Printf("下载文件失败: %v\n", err)
		return nil
	}

	timestamp := time.Now().Format("20060102_150405") + fmt.Sprintf("_%d", time.Now().UnixNano()%1e6)
	fileName := fmt.Sprintf("%s%s", timestamp, ext)
	fullOutputDir := filepath.Join(outputPath, "assets", dirname)
	fullOutputFilename := filepath.Join(fullOutputDir, fileName)
	relatedPath := filepath.Join("assets", dirname, fileName)

	FileUtils.OutputResponse(fullOutputDir, fmt.Sprintf("%s%s", timestamp, ext), resp)

	size, err := FileUtils.GetFileSize(fullOutputFilename)
	if err != nil {
		size = 0
	}

	return &Entity.Attachment{
		FileName: fileName,
		FilePath: relatedPath,
		FileSize: size,
		Type:     messageType,
	}
}
