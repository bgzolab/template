package FileUtils

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"telegram-message-sync-bot/pkg/LogUtils"
)

func OutputString(filePath string, fileName string, context string) (bool, string) {
	exists, message, saveFile, file := checkExists(filePath, fileName)
	if !exists {
		return false, fmt.Sprintf("验证路径失败, %v", message)
	}
	defer file.Close() // 关闭时会刷新缓冲区

	// 输出字符串
	_, err := file.WriteString(context)
	if err != nil {
		LogUtils.GetLogger().Println("Error writing to file: ", err)
		return false, fmt.Sprintf("写入文件失败, %v", err)
	}
	// 强制写入磁盘
	file.Sync()
	return true, saveFile
}

func OutputResponse(filePath string, fileName string, resp *http.Response) (bool, string) {
	exists, msg, filePath, file := checkExists(filePath, fileName)
	if !exists {
		return false, fmt.Sprintf("验证路径失败, %v", msg)
	}

	defer resp.Body.Close()
	defer file.Close()

	// 保存到本地
	_, err := io.Copy(file, resp.Body)
	if err != nil {
		LogUtils.GetLogger().Println("保存文件失败: %v", err)
		return false, fmt.Sprintf("保存文件失败: %v", err)
	}

	// 记录文件路径
	LogUtils.GetLogger().Printf("文件下载成功: %s\n", filePath)
	return true, filePath
}

func checkExists(filePath string, fileName string) (bool, string, string, *os.File) {
	saveFile := filepath.Join(filePath, fileName)
	// 确保输出目录存在
	err := os.MkdirAll(filePath, os.ModePerm) // 创建目录
	if err != nil {
		LogUtils.GetLogger().Println("创建目录失败:", filePath, err)
		return false, "创建目录失败", saveFile, nil
	}
	// 打开文件
	file, err := os.OpenFile(saveFile, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		LogUtils.GetLogger().Println("Error opening file for writing: ", err)
		return false, "无法打开文件以写入", saveFile, nil
	}
	return true, "", saveFile, file
}
