package bootstrapservice

import (
	"fmt"
	"os"
	"path/filepath"
	"telegram-message-sync-bot/internal/Database"
	"telegram-message-sync-bot/internal/Entity"
	"telegram-message-sync-bot/pkg/LogUtils"

	"gopkg.in/yaml.v3"
)

// LoadConfig 负责从 YAML 文件加载应用配置并反序列化为统一配置对象。
// 这样做的原因是将配置读取逻辑从入口层剥离，便于独立测试与复用。
func LoadConfig(configFile string) (Entity.Config, error) {
	data, err := os.ReadFile(configFile)
	if err != nil {
		return Entity.Config{}, fmt.Errorf("读取配置文件失败: %w", err)
	}

	var config Entity.Config
	if err = yaml.Unmarshal(data, &config); err != nil {
		return Entity.Config{}, fmt.Errorf("解析配置失败: %w", err)
	}

	return config, nil
}

// InitRuntime 负责初始化应用运行时依赖（日志系统、数据库连接）。
// 这样做的原因是把“启动装配”集中在单点，避免 main 承担过多基础设施细节。
func InitRuntime(config Entity.Config) error {
	LogUtils.InitLogger(config.Log.Dir)
	if err := Database.InitORMDB(filepath.Join(config.Log.Dir)); err != nil {
		return fmt.Errorf("初始化数据库失败: %w", err)
	}
	return nil
}
