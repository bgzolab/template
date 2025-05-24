package entity

/** 与配置文件一一对应
 */
type Config struct {
	Output struct {
		JSON       bool   `yaml:"json"`
		JsonDir    string `yaml:"json_dir"`
		PersonDir  string `yaml:"person_dir"`
		ChannelDir string `yaml:"channel_dir"`
	} `yaml:"output"`

	Log struct {
		Enable bool   `yaml:"enable"`
		Dir    string `yaml:"dir"`
	} `yaml:"log"`

	Template struct {
		Dir string `yaml:"dir"`
	} `yaml:"template"`

	Token string `yaml:"token"`

	TargetUserList []int64 `yaml:"targetUserList"`
}
