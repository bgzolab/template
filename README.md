## Dependencies

```shell
go mod init sqlite-connect-go 
go get github.com/mattn/go-sqlite3 
# 如果你想使用 GORM 作为 ORM 框架，可以添加以下依赖
go get -u gorm.io/gorm
go get -u gorm.io/driver/sqlite
```


## Notes

### ORM 
```shell
Go 也有类似于 MyBatis 的 ORM 框架，可以简化数据库操作，常用的有：

- `GORM`：功能强大，支持多种数据库，语法类似于 ActiveRecord。
- `ent`：由 Facebook 开发，类型安全，适合大型项目。
- `xorm`：简单易用，支持多种数据库。
- `sqlx`：对标准库的扩展，支持结构体映射，但不是全功能 ORM。

这些框架可以让你用结构体和方法操作数据库，减少手写 SQL。推荐初学者使用 `GORM`，文档齐全，社区活跃。
```

