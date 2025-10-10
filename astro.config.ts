// @ts-check
import { defineConfig } from 'astro/config';
import vue from '@astrojs/vue';
import tailwind from '@astrojs/tailwind';
import node from '@astrojs/node';
import remarkAdmonitions from 'remark-github-beta-blockquote-admonitions'


// Markdown Reading Time
import getReadingTime from 'reading-time';
import { toString } from 'mdast-util-to-string';
export function remarkReadingTime() {
  return function (tree: any, { data }: { data: any }) {
    const textOnPage = toString(tree);
    const readingTime = getReadingTime(textOnPage);
    // readingTime.text will give us minutes read as a friendly string,
    // i.e. "3 min read"
    data.astro.frontmatter.minutesRead = readingTime.text;
  };
}

// Markdown Callouts
const raConfig = {
  classNameMaps: {
    block: (title: string) => "admonition " + title.toLowerCase(),
    title: "admonition-title",
  },
  titleFilter: (title: string) => {
    return title.match(/\[![^\]]+\]/g);
  },
};


import remarkToc from 'remark-toc';

// 自动为博客文章生成目录的插件
function remarkAutoToc() {
  return function (tree: any, file: any) {
    // 检查是否是博客文章（可以通过文件名或其他方式判断）
    const isBlogPost = file.history[0]?.includes('/blog/') || file.history[0]?.includes('content/blog');
    
    if (!isBlogPost) return;

    // 在文档开头插入目录占位符
    const tocNode = {
      type: 'paragraph',
      children: [
        {
          type: 'text',
          value: '![[toc]]'
        }
      ]
    };

    // 将目录插入到文档开头（在frontmatter之后）
    tree.children.unshift(tocNode);
  };
}
// https://astro.build/config
export default defineConfig({
  // [option]: build for github pages
  // via: https://docs.astro.build/en/guides/deploy/github/
  site: process.env.NODE_ENV === 'development' ? 'http://127.0.0.1:4321' : 'https://bgzo.github.io',
  base: '/github-pages',

  integrations: [
    // 集成Vue
    vue(),
    // 集成 Tailwind
    tailwind(),
  ],

  adapter: node({
    mode: 'standalone'
  }),
  // 省略
  markdown: {
    remarkPlugins: [
      // remarkMath,
      // remarkUnwrapImages,
      // 自动生成目录（只对博客文章）
      remarkAutoToc,
      // 处理目录占位符
      [remarkToc, { tight: true, ordered: true, heading: "目录" }],
      // remarkMarkPlus,
      // 阅读时间
      remarkReadingTime,
      // Callouts
      // @ts-expect-error:next-line
      [remarkAdmonitions, raConfig],
    ],
  },
});