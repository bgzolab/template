package TgUtils

import (
	"fmt"
	"github.com/go-telegram/bot/models"
	"github.com/rivo/uniseg"
	"strings"
	"unicode"
)

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

func HandleMsgLink(msg string, entities []models.MessageEntity) string {
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
