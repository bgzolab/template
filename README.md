## Dependencies

```shell
go mod init sqlite-connect-go 
go get github.com/mattn/go-sqlite3 
# 如果你想使用 GORM 作为 ORM 框架，可以添加以下依赖
go get -u gorm.io/gorm
go get -u gorm.io/driver/sqlite
```


## Notes

### GORM

```shell
我日常用 Java 比较多，Java 有 Mybatis 这样的ORM。 Golang 是否有类似的 ORM？
```

Go 也有类似于 MyBatis 的 ORM 框架，可以简化数据库操作，常用的有：

- `GORM`：功能强大，支持多种数据库，语法类似于 ActiveRecord。
- `ent`：由 Facebook 开发，类型安全，适合大型项目。
- `xorm`：简单易用，支持多种数据库。
- `sqlx`：对标准库的扩展，支持结构体映射，但不是全功能 ORM。

这些框架可以让你用结构体和方法操作数据库，减少手写 SQL。推荐初学者使用 `GORM`，文档齐全，社区活跃。


#### 初始化

```go
err = db.AutoMigrate(&User{}, &Order{})
```

1. AutoMigrate 用于自动创建或更新表结构，适合初始化数据库时使用。
   它会根据结构体自动建表或调整字段，但不会删除字段或表。初始化时可以直接用它。
2. 如果需要更复杂的迁移逻辑（如删除字段、重命名等），可以使用 gorm 的 Migrate 方法或手动编写 SQL。
3. AutoMigrate 只会创建表和字段，不会删除或修改现有字段。
4. 如果表已经存在，AutoMigrate 会跳过创建。
5. 如果需要删除表或字段，可以使用 db.Migrator().DropTable() 或 db.Migrator().DropColumn()。
6. 目前 GORM 官方只支持手动传入所有模型到 AutoMigrate，没有自动扫描所有结构体的功能。
   常见做法是统一管理模型，比如定义一个 models 包，集中注册所有模型，然后在初始化时统一传入。

> [!tip] 
> 没有 Spring 那样自动注入的容器的功能


#### 控制事务

> [!tip]
> 没有 Spring 注解那样自动捕捉异常回滚的的功能，需要显式控制事务。

##### 并发事务

```go
package main

import (
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
	"log"
	"sync"
)

type User struct {
	ID   uint   `gorm:"primaryKey"`
	Name string
	Age  int
}

func main() {
	db, err := gorm.Open(sqlite.Open("example.db"), &gorm.Config{})
	if err != nil {
		log.Fatal("无法连接到数据库:", err)
	}

	// 自动迁移
	err = db.AutoMigrate(&User{})
	if err != nil {
		log.Fatal("迁移失败:", err)
	}

	// 并发事务处理
	var wg sync.WaitGroup
	for i := 0; i < 10; i++ {
		wg.Add(1)
		go func(i int) {
			defer wg.Done()
			tx := db.Begin()
			defer func() {
				if r := recover(); r != nil {
					tx.Rollback()
					log.Println("事务回滚:", r)
				}
			}()

			user := User{Name: "用户" + string(i), Age: 20 + i}
			if err := tx.Create(&user).Error; err != nil {
				tx.Rollback()
				log.Println("插入失败，事务回滚:", err)
				return
			}

			if err := tx.Commit().Error; err != nil {
				log.Println("提交失败:", err)
			} else {
				log.Println("事务成功")
			}
		}(i)
	}
	wg.Wait()
}
```

#### 乐观锁


```go
package main

import (
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
	"log"
)

type User struct {
	ID      uint   `gorm:"primaryKey"`
	Name    string
	Age     int
	Version int `gorm:"version"` // 乐观锁字段
}

func main() {
	db, err := gorm.Open(sqlite.Open("example.db"), &gorm.Config{})
	if err != nil {
		log.Fatal("无法连接到数据库:", err)
	}

	// 自动迁移
	err = db.AutoMigrate(&User{})
	if err != nil {
		log.Fatal("迁移失败:", err)
	}

	// 插入数据
	user := User{Name: "张三", Age: 25}
	db.Create(&user)

	// 模拟更新操作
	err = db.Model(&user).Where("version = ?", user.Version).Updates(User{Age: 30}).Error
	if err != nil {
		log.Println("更新失败，可能是版本冲突:", err)
	} else {
		log.Println("更新成功")
	}
}
```

1. Version 字段：用于记录版本号，每次更新时自动递增。
2. 条件更新：通过 WHERE version = ? 确保只有版本号匹配的数据才能被更新。
3. 冲突处理：如果版本号不匹配，更新操作会失败，可以捕获错误并处理。

#### 悲观锁

```go
package main

import (
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
	"log"
)

type User struct {
	ID   uint   `gorm:"primaryKey"`
	Name string
	Age  int
}

func main() {
	db, err := gorm.Open(sqlite.Open("example.db"), &gorm.Config{})
	if err != nil {
		log.Fatal("无法连接到数据库:", err)
	}

	// 自动迁移
	err = db.AutoMigrate(&User{})
	if err != nil {
		log.Fatal("迁移失败:", err)
	}

	// 插入测试数据
	db.Create(&User{Name: "张三", Age: 25})

	// 开始事务
	tx := db.Begin()

	// 使用悲观锁查询
	var user User
	err = tx.Raw("SELECT * FROM users WHERE id = ? FOR UPDATE", 1).Scan(&user).Error
	if err != nil {
		tx.Rollback()
		log.Println("查询失败:", err)
		return
	}

	// 更新数据
	user.Age = 30
	err = tx.Save(&user).Error
	if err != nil {
		tx.Rollback()
		log.Println("更新失败:", err)
		return
	}

	// 提交事务
	err = tx.Commit().Error
	if err != nil {
		log.Println("提交失败:", err)
	} else {
		log.Println("事务成功")
	}
}
```

1. FOR UPDATE：在查询时锁定记录，其他事务无法修改这些记录。
2. 事务管理：悲观锁需要在事务中使用，否则锁定无效。 
3. 适用场景：适合高并发场景，确保数据一致性。
