package archiveservice

import (
	"bytes"
	"context"
	"fmt"
	"html/template"
	"net/http"
	"os"
	"path/filepath"
	"strconv"
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
	OutputPath  string
	ArchiveRoot string
	SourceID    string
	FileName    string
	SourceLink  string
	SourceDate  time.Time
	MessageID   int
}

// PersistMessage 负责执行“单条消息归档”完整编排：解析来源、渲染模板、落盘、入库。
// 这样做的原因是把归档用例从入口层抽离，降低 main 复杂度，并让归档逻辑可独立测试与复用。
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
			file := persistFile(ctx, b, highestResolutionPhoto.FileID, meta.SourceID, meta.ArchiveRoot, Entity.ImageMessage)
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

	archiveNow := time.Now()
	data := BuildTemplateData(meta.SourceDate, photoLink, msgText, meta.SourceLink, archiveNow)

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
	frontMatter := BuildFrontMatter(meta, msgText, archiveNow)
	contentWithFrontMatter := frontMatter + "\n" + strings.TrimLeft(buf.String(), "\n")

	FileUtils.OutputString(meta.OutputPath, meta.FileName, contentWithFrontMatter)

	savedMsg := Entity.Message{
		Content: msgText,

		MessageID:   int64(meta.MessageID),
		Username:    meta.SourceID,
		MessageUrl:  meta.SourceLink,
		MessageDate: meta.SourceDate,
		Attachments: assets,

		CreatedTime: archiveNow,
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

// BuildFrontMatter 生成强制 Front Matter。
// 规则：
// 1) title/aliases/description 基于正文摘要；
// 2) 摘要计算前先把所有 \n 替换为空格；
// 3) 时间格式固定为 yyyy-MM-ddTHH:mm:ss（不带时区后缀）。
func BuildFrontMatter(meta SourceMeta, content string, archivedAt time.Time) string {
	normalized := normalizeFrontMatterContent(content)
	titleSummary := truncateForFrontMatter(normalized, 50)
	descSummary := truncateForFrontMatter(normalized, 100)

	title := fmt.Sprintf("%d-%s", meta.MessageID, titleSummary)
	source := meta.SourceLink
	created := formatFrontMatterTime(meta.SourceDate)
	modified := formatFrontMatterTime(archivedAt)

	return strings.Join([]string{
		"---",
		fmt.Sprintf("title: %s", quoteYAMLString(title)),
		"aliases:",
		fmt.Sprintf("- %s", quoteYAMLString(title)),
		fmt.Sprintf("created: %s", created),
		fmt.Sprintf("modified: %s", modified),
		"comments: true",
		"draft: true",
		fmt.Sprintf("description: %s", quoteYAMLString(descSummary)),
		fmt.Sprintf("source: %s", quoteYAMLString(source)),
		"tags: []",
		"---",
	}, "\n")
}

func normalizeFrontMatterContent(content string) string {
	replaced := strings.ReplaceAll(content, "\r\n", "\n")
	replaced = strings.ReplaceAll(replaced, "\r", "\n")
	return strings.ReplaceAll(replaced, "\n", " ")
}

func truncateForFrontMatter(text string, maxRunes int) string {
	if maxRunes <= 0 {
		return ""
	}
	runes := []rune(text)
	if len(runes) <= maxRunes {
		return text
	}
	return string(runes[:maxRunes])
}

func formatFrontMatterTime(t time.Time) string {
	return t.Format("2006-01-02T15:04:05")
}

func quoteYAMLString(s string) string {
	return strconv.Quote(s)
}

// ResolveSourceMeta 将 Telegram 原始消息转换为统一来源元信息（来源ID、文件名、落盘路径、消息链接等）。
// 这样做的原因是统一“私聊消息/频道转发消息”的分支处理，避免上层重复判断来源类型。
func ResolveSourceMeta(update *models.Update, config Entity.Config) SourceMeta {
	meta := SourceMeta{
		ArchiveRoot: config.Output.PersonDir,
		SourceID:    fmt.Sprintf("%d", update.Message.Chat.ID),
		SourceDate:  time.Now(),
		MessageID:   update.Message.ID,
	}

	if update.Message.ForwardOrigin != nil && update.Message.ForwardOrigin.Type == "channel" {
		meta.ArchiveRoot = config.Output.ChannelDir
		origin := update.Message.ForwardOrigin.MessageOriginChannel

		if origin.Chat.Username != "" {
			meta.SourceID = origin.Chat.Username
		} else {
			meta.SourceID = fmt.Sprintf("%d", origin.Chat.ID)
		}

		meta.SourceLink = fmt.Sprintf("https://t.me/%s/%d", meta.SourceID, origin.MessageID)
		meta.SourceDate = time.Unix(int64(origin.Date), 0)
		meta.MessageID = origin.MessageID
	}

	// 步骤1：仅切换归档写入路径到 source_id/message_id.md。
	meta.OutputPath = filepath.Join(meta.ArchiveRoot, meta.SourceID)
	meta.FileName = fmt.Sprintf("%d.md", meta.MessageID)

	return meta
}

// SelectMsgText 统一提取消息正文：优先 Text，回退 Caption，并处理标签转义和文本链接格式化。
// 这样做的原因是把文本处理规则集中，保证归档内容在不同消息类型下行为一致。
func SelectMsgText(update *models.Update) string {
	msgText := update.Message.Text
	msgEntities := update.Message.Entities
	if msgText == "" {
		msgText = update.Message.Caption
		msgEntities = update.Message.CaptionEntities
	}
	return StrUtils.EscapeHashtags(TgUtils.HandleMsgLink(msgText, msgEntities))
}

// BuildTemplateData 生成模板渲染所需字段，统一时间格式和变量命名。
// 这样做的原因是将模板数据构建从 I/O 逻辑中分离，方便测试与后续模板演进。
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

// formatDownloadedFiles 将下载后的媒体路径格式化为 Markdown 图片片段。
// 这样做的原因是隔离展示格式拼接逻辑，避免散落在归档主流程中。
func formatDownloadedFiles(files []string) string {
	var builder strings.Builder
	for _, file := range files {
		builder.WriteString("![](")
		builder.WriteString(file)
		builder.WriteString(") ")
	}
	return builder.String()
}

// persistFile 下载并保存 Telegram 媒体文件，返回可入库的附件元数据。
// 这样做的原因是把媒体 I/O 细节封装在单点，减少归档主流程的噪音与耦合。
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
