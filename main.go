package main

import (
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
	"log"

	_ "github.com/mattn/go-sqlite3"
)

// User 结构体表示用户数据
type User struct {
	ID   uint `gorm:"primaryKey"`
	Name string
	Age  int
}

// Order 结构体表示订单数据
type Order struct {
	ID     uint
	Item   string
	UserID uint
}

func main() {
	// 连接到 SQLite 数据库
	db, err := gorm.Open(sqlite.Open("example.db"), &gorm.Config{})
	if err != nil {
		log.Fatal("无法连接到数据库:", err)
	}

	// 自动迁移（创建表）
	// NOTE:
	// 1. AutoMigrate 用于自动创建或更新表结构，适合初始化数据库时使用。
	//		它会根据结构体自动建表或调整字段，但不会删除字段或表。初始化时可以直接用它。
	err = db.AutoMigrate(&User{}, &Order{})
	if err != nil {
		log.Fatal("迁移失败:", err)
	}

	// 插入数据
	users := []User{
		{Name: "张三", Age: 25},
		{Name: "李四", Age: 30},
		{Name: "王五", Age: 28},
	}
	//for _, user := range users {
	//	db.Create(&user)
	//}

	var result []User
	db.Find(&result)
	log.Println("查询结果:", result)

	// 更新数据
	db.Where("name = ? AND age = ?", "张三", 25).Find(&users).Update("age", 32)
	// 条件查询
	var filteredUsers []User
	db.Where("age > ?", 26).Find(&filteredUsers)
	log.Println("年龄大于 26 的用户:", filteredUsers)

	var usersTarget []User
	db.Preload("Orders").Find(&usersTarget)
	db.Raw("SELECT u.name, o.item FROM users u JOIN orders o ON u.id = o.user_id WHERE o.item = ?", "商品A").Scan(&result)
	log.Println("订单:", result)

}
