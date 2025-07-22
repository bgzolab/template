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
	models := []interface{}{
		&User{},
		&Order{},
		// 其他模型
	}
	err = db.AutoMigrate(models...)
	if err != nil {
		log.Fatal("迁移失败:", err)
	}

	// 开始事务
	tx := db.Begin()

	// 插入数据
	users := []User{
		{Name: "张三", Age: 25},
		{Name: "李四", Age: 30},
		{Name: "王五", Age: 28},
	}
	for _, user := range users {
		if err := tx.Create(&user).Error; err != nil {
			tx.Rollback() // 回滚事务
			log.Println("插入失败，事务回滚:", err)
			return
		}
	}

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

	// 更新用户
	if err := tx.Model(&User{}).Where("name = ?", "李四").Update("age", 35).Error; err != nil {
		tx.Rollback() // 回滚事务
		log.Println("更新失败，事务回滚:", err)
		return
	}

	// 提交事务
	if err := tx.Commit().Error; err != nil {
		log.Println("提交失败:", err)
	} else {
		log.Println("事务成功")
	}

}

func createTransaction() {
	db, err := gorm.Open(sqlite.Open("example.db"), &gorm.Config{})
	if err != nil {
		log.Fatal("无法连接到数据库:", err)
	}

	// 使用事务
	err = db.Transaction(func(tx *gorm.DB) error {
		// 插入用户
		user := User{Name: "张三", Age: 25}
		if err := tx.Create(&user).Error; err != nil {
			return err // 回滚事务
		}

		// 更新用户
		if err := tx.Model(&User{}).Where("name = ?", "张三").Update("age", 30).Error; err != nil {
			return err // 回滚事务
		}

		// 如果没有错误，事务会自动提交
		return nil
	})

	if err != nil {
		log.Println("事务失败:", err)
	} else {
		log.Println("事务成功")
	}
}
