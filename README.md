# 博客批量下载器

一般来说，我读人家的博客都是从存档开始的，因为里面不会有太多的内容。甚至连简短的 Beirf 都没有，就是个标题。

但是很多博客并没有提供这个页面，我又没有办法真的写信给人家说“请你把存档页面放出来”，所以我就只能写了这个脚本。

脚本的原理很简单，就是用 Sitemap.xml 来获取博客的所有文章链接，然后再逐个下载。

## 参考

1. https://gist.github.com/NoWorries/d8d2946d626df0061616db307beeb6d2#file-sitemap_crawler-py-L7
2. https://github.com/hristovskii/sitemap-crawler-python
3. https://github.com/GateNLP/ultimate-sitemap-parser
4. https://github.com/clydesantiago/site-to-md

当然还有反向生成的库，用的人比较多，如：

- https://github.com/c4software/python-sitemap