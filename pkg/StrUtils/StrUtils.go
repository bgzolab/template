package StrUtils

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

// SearchInFile 读取文件并搜索目标字符串
func SearchInFile(filePath, searchString string) bool {
	// 尝试打开文件
	file, err := os.Open(filePath)
	if err != nil {
		if os.IsNotExist(err) {
			fmt.Println("文件不存在")
			return false
		}
		fmt.Printf("打开文件失败: %v\n", err)
		return false
	}
	defer file.Close()

	// 使用 bufio 逐行读取文件
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		if strings.Contains(scanner.Text(), searchString) {
			return true
		}
	}

	// 检查读取文件时的错误
	if err := scanner.Err(); err != nil {
		fmt.Printf("读取文件时出错: %v\n", err)
		return false
	}

	fmt.Println("未找到匹配内容")
	return false
}

func EscapeHashtags(text string) string {
	return strings.ReplaceAll(text, "#", "\\#")
}
