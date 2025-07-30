# 博客批量下载器

一般来说，我读人家的博客都是从存档开始的，因为里面不会有太多的内容。甚至连简短的 Beirf 都没有，就是个标题。

但是很多博客并没有提供这个页面，我又没有办法真的写信给人家说“请你把存档页面放出来”，所以我就只能写了这个脚本。

脚本的原理很简单，就是用 Sitemap.xml 来获取博客的所有文章链接，然后再逐个下载。

## Roadmap

- [x] 支持 Sitemap 自动匹配
  - https://ultimate-sitemap-parser.readthedocs.io/en/stable/
- [x] 获取 URL 内容
  - ~~想用 crawl4ai，但是依赖浏览器~~
  - [x] trafilatura 提取文章内容，但是失败了
  - [x] BS 直接转换 HTML 全部内容
- [ ] 异步下载文章内容
  - 目前是同步下载，速度很慢
- [x] 支持 Frontmatter
  - [ ] 最好可以做到自定义模板，无需改动代码，自由度更高
- [ ] 支持自定义下载目录
- [x] 支持输出一个 index.md 文件，里面包含所有文章的链接 
   - 用 Wikilink 还是 ==Markdown 链接==？

## 测试网站

1. http://www.hecaitou.com
2. https://cn.apkjam.com

## 参考

参考的项目不限于下面这些：

1. https://gist.github.com/NoWorries/d8d2946d626df0061616db307beeb6d2#file-sitemap_crawler-py-L7
2. https://github.com/hristovskii/sitemap-crawler-python
3. https://github.com/GateNLP/ultimate-sitemap-parser
4. https://github.com/clydesantiago/site-to-md
5. https://github.com/buriy/python-readability


当然还有反向生成的库，用的人比较多，如：

- https://github.com/c4software/python-sitemap