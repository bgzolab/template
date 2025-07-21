package main

import (
	"database/sql"
	"fmt"
	"log"

	_ "github.com/mattn/go-sqlite3"
)

type User struct {
	ID   int
	Name string
	Age  int
}

func main() {
	// 连接到 SQLite 数据库（如果数据库不存在会自动创建）
	db, err := sql.Open("sqlite3", "./example.db")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	// 测试连接
	err = db.Ping()
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("成功连接到 SQLite 数据库!")

	// 创建表
	createTableSQL := `CREATE TABLE IF NOT EXISTS users (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		name TEXT NOT NULL,
		age INTEGER
	);`

	_, err = db.Exec(createTableSQL)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("成功创建 users 表!")

	// 插入数据
	insertSQL := `INSERT INTO users (name, age) VALUES (?, ?)`
	statement, err := db.Prepare(insertSQL)
	if err != nil {
		log.Fatal(err)
	}
	defer statement.Close()

	// 插入几条示例数据
	users := []User{
		{Name: "张三", Age: 25},
		{Name: "李四", Age: 30},
		{Name: "王五", Age: 28},
	}

	for _, user := range users {
		_, err = statement.Exec(user.Name, user.Age)
		if err != nil {
			log.Fatal(err)
		}
	}
	fmt.Println("成功插入示例数据!")

	// 查询数据
	querySQL := `SELECT id, name, age FROM users`
	rows, err := db.Query(querySQL)
	if err != nil {
		log.Fatal(err)
	}
	defer rows.Close()

	fmt.Println("\n查询结果:")
	fmt.Println("ID\t姓名\t年龄")
	fmt.Println("----------------")

	for rows.Next() {
		var user User
		err = rows.Scan(&user.ID, &user.Name, &user.Age)
		if err != nil {
			log.Fatal(err)
		}
		fmt.Printf("%d\t%s\t%d\n", user.ID, user.Name, user.Age)
	}

	// 检查遍历过程中是否有错误
	err = rows.Err()
	if err != nil {
		log.Fatal(err)
	}

	// 示例：根据条件查询
	fmt.Println("\n年龄大于 26 的用户:")
	fmt.Println("ID\t姓名\t年龄")
	fmt.Println("----------------")

	queryWithCondition := `SELECT id, name, age FROM users WHERE age > ?`
	rows2, err := db.Query(queryWithCondition, 26)
	if err != nil {
		log.Fatal(err)
	}
	defer rows2.Close()

	for rows2.Next() {
		var user User
		err = rows2.Scan(&user.ID, &user.Name, &user.Age)
		if err != nil {
			log.Fatal(err)
		}
		fmt.Printf("%d\t%s\t%d\n", user.ID, user.Name, user.Age)
	}

	// 示例：更新数据
	updateSQL := `UPDATE users SET age = ? WHERE name = ?`
	result, err := db.Exec(updateSQL, 32, "张三")
	if err != nil {
		log.Fatal(err)
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("\n更新操作影响了 %d 行数据\n", rowsAffected)

	fmt.Println("\n数据库操作完成!")
}
