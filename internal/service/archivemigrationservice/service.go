package archivemigrationservice

import (
	"bytes"
	"fmt"
	"html/template"
	"os"
	"path/filepath"
	"strconv"
	"strings"

	"telegram-message-sync-bot/internal/Database"
	"telegram-message-sync-bot/internal/Entity"
	"telegram-message-sync-bot/internal/service/archiveservice"
)

type BackfillStats struct {
	DBTotal            int
	FilesCreated       int
	FilesSkipped       int
	MissingFromArchive int
	OrphanInArchive    int
}

// BackfillFromDatabase 按数据库全量补齐归档文件，并执行迁移后键集合核对。
// 当前核对键使用 (source_id, message_id)。
func BackfillFromDatabase(config Entity.Config) (BackfillStats, error) {
	stats := BackfillStats{}

	tmplData, err := os.ReadFile(config.Template.Dir)
	if err != nil {
		return stats, fmt.Errorf("读取模板失败: %w", err)
	}
	tmpl, err := template.New("archive").Parse(string(tmplData))
	if err != nil {
		return stats, fmt.Errorf("解析模板失败: %w", err)
	}

	msgs, err := Database.ListMessages()
	if err != nil {
		return stats, fmt.Errorf("读取数据库消息失败: %w", err)
	}

	stats.DBTotal = len(msgs)
	expectedKeys := make(map[string]struct{}, len(msgs))

	for _, msg := range msgs {
		sourceID := normalizeSourceID(msg.Username)
		archiveRoot := resolveArchiveRoot(config, msg)
		outputDir := filepath.Join(archiveRoot, sourceID)
		fileName := fmt.Sprintf("%d.md", msg.MessageID)
		fullPath := filepath.Join(outputDir, fileName)

		expectedKeys[buildKey(sourceID, msg.MessageID)] = struct{}{}

		if _, statErr := os.Stat(fullPath); statErr == nil {
			stats.FilesSkipped++
			continue
		} else if !os.IsNotExist(statErr) {
			return stats, fmt.Errorf("检查归档文件失败: %w", statErr)
		}

		frontMatter := archiveservice.BuildFrontMatter(archiveservice.SourceMeta{
			SourceLink: msg.MessageUrl,
			SourceDate: msg.MessageDate,
			MessageID:  int(msg.MessageID),
		}, msg.Content, msg.CreatedTime)

		tplData := archiveservice.BuildTemplateData(
			msg.MessageDate,
			renderAttachmentMarkdown(msg.Attachments),
			msg.Content,
			msg.MessageUrl,
			msg.CreatedTime,
		)

		var buf bytes.Buffer
		if execErr := tmpl.Execute(&buf, tplData); execErr != nil {
			return stats, fmt.Errorf("渲染模板失败: %w", execErr)
		}

		content := frontMatter + "\n" + strings.TrimLeft(buf.String(), "\n")
		if mkdirErr := os.MkdirAll(outputDir, 0o755); mkdirErr != nil {
			return stats, fmt.Errorf("创建目录失败: %w", mkdirErr)
		}
		if writeErr := os.WriteFile(fullPath, []byte(content), 0o644); writeErr != nil {
			return stats, fmt.Errorf("写入归档文件失败: %w", writeErr)
		}

		stats.FilesCreated++
	}

	actualKeys, err := collectArchiveKeys(config)
	if err != nil {
		return stats, err
	}

	for key := range expectedKeys {
		if _, ok := actualKeys[key]; !ok {
			stats.MissingFromArchive++
		}
	}
	for key := range actualKeys {
		if _, ok := expectedKeys[key]; !ok {
			stats.OrphanInArchive++
		}
	}

	if stats.MissingFromArchive > 0 || stats.OrphanInArchive > 0 {
		return stats, fmt.Errorf(
			"迁移后核对失败: missing=%d orphan=%d",
			stats.MissingFromArchive,
			stats.OrphanInArchive,
		)
	}

	return stats, nil
}

func resolveArchiveRoot(config Entity.Config, msg Entity.Message) string {
	if msg.MessageUrl != "" {
		return config.Output.ChannelDir
	}
	return config.Output.PersonDir
}

func normalizeSourceID(sourceID string) string {
	return strings.ToLower(strings.TrimSpace(sourceID))
}

func buildKey(sourceID string, messageID int64) string {
	return sourceID + "#" + strconv.FormatInt(messageID, 10)
}

func renderAttachmentMarkdown(assets []Entity.Attachment) string {
	if len(assets) == 0 {
		return ""
	}

	var b strings.Builder
	for _, a := range assets {
		if a.FilePath == "" {
			continue
		}
		b.WriteString("![](")
		b.WriteString(a.FilePath)
		b.WriteString(") ")
	}
	return b.String()
}

func collectArchiveKeys(config Entity.Config) (map[string]struct{}, error) {
	keys := map[string]struct{}{}
	bases := []string{config.Output.PersonDir, config.Output.ChannelDir}

	for _, base := range bases {
		entries, err := os.ReadDir(base)
		if err != nil {
			if os.IsNotExist(err) {
				continue
			}
			return nil, fmt.Errorf("读取归档目录失败: %w", err)
		}

		for _, sourceDir := range entries {
			if !sourceDir.IsDir() {
				continue
			}

			sourceID := normalizeSourceID(sourceDir.Name())
			messageFiles, err := os.ReadDir(filepath.Join(base, sourceDir.Name()))
			if err != nil {
				return nil, fmt.Errorf("读取来源目录失败: %w", err)
			}

			for _, f := range messageFiles {
				if f.IsDir() {
					continue
				}
				if filepath.Ext(f.Name()) != ".md" {
					continue
				}

				idPart := strings.TrimSuffix(f.Name(), ".md")
				messageID, parseErr := strconv.ParseInt(idPart, 10, 64)
				if parseErr != nil {
					continue
				}

				keys[buildKey(sourceID, messageID)] = struct{}{}
			}
		}
	}

	return keys, nil
}
