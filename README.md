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


