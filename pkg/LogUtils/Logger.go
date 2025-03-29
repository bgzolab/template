package LogUtils

import (
	"io"
	"log"
	"os"
	"path/filepath"
)

var logger *log.Logger

// 统一的初始化方法
func InitLogger(logPath string) {
	output := filepath.Join(logPath, "bot.log")
	logFile, err := os.OpenFile(output, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		log.Fatalf("无法打开日志文件: %v", err)
	}

	multiWriter := io.MultiWriter(os.Stdout, logFile)
	logger = log.New(multiWriter, "[Bot] ", log.LstdFlags|log.Lshortfile)
	logger.Println("Logger 初始化完成")
}

// 获取 logger，提供给外部或其他包内使用
func GetLogger() *log.Logger {
	if logger == nil {
		log.Println("警告: Logger 未初始化，使用默认控制台输出")
		logger = log.New(os.Stdout, "[Bot] ", log.Ldate|log.Ltime|log.Lshortfile)
	}
	return logger
}
