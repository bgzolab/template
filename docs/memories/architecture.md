# 项目架构

## 前置要求：项目结构与含义

架构需要对项目的整体结构进行说明，明确每个文件夹和文件的作用，以及它们之间的关系。以下是项目的部分架构设计，要求有：

1) 通过 Tree 结构展示每个文件的作用。
2) 每个文件的作用要清晰、具体，最好列出调用结构。

## 项目结构

```shell
.
├── config # 配置文件夹，存放一些平台的模板文件等
│   └── bangumi_template.md # 这个是bangumi平台的模板文件，用户可以根据自己的需求修改这个文件来改变导出的markdown文件的格式
├── docs # 文档文件夹，存放一些项目相关的文档
│   ├── implementation-plans # 实现计划，记录一些功能的实现思路和计划
│   └── memories # 记忆文件夹，记录一些项目的设计思路、架构等
├── export-env.sh # 导出环境变量的脚本，用户可以运行这个脚本来导出`.env`文件中的环境变量
├── LICENCE 
├── poetry.lock
├── publish.sh # 发布脚本，用户可以运行这个脚本来发布这个项目到PyPI
├── pyproject.toml # Poetry的配置文件，记录项目的依赖和一些项目信息
├── README.md 
├── requirements.txt
├── src
│   ├── bangumi # bangumi平台接口，获取相关分页数据；
│   ├── bilibili # bilibili平台接口，获取相关分页数据；
│   ├── cnblog # 博客园平台接口，获取相关分页数据；
│   ├── demo # demo文件夹，存放一些demo代码，新增一个平台可以从这里复制开始；
│   ├── entity # 实体类文件夹（待改造）
│   ├── export_to_obsidian.py # 导出主程序，用户可以运行这个程序来导出数据到markdown文件
│   ├── qireader # qireader平台接口，获取相关分页数据；
│   ├── utils # 工具类文件夹，存放一些公共的工具函数
│   ├── v2ex # v2ex平台接口，获取相关分页数据；
│   ├── weibo # 微博平台接口，获取相关分页数据；
│   └── zhihu # 知乎平台接口，获取相关分页数据；
└── tests
    ├── test_bangumi.py # bangumi平台的测试文件，测试bangumi平台接口的功能是否正常
    ├── test_cnblog.py # 博客园平台的测试文件，测试博客园平台接口的功能是否正常
    ├── test_qireader.py # qireader平台的测试文件，测试qireader平台接口的功能是否正常
    └── test_utils.py # 工具类的测试文件，测试工具类函数的功能是否正常
```

