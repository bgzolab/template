// @ts-check
import { defineConfig } from 'astro/config';
import vue from '@astrojs/vue';
import tailwind from '@astrojs/tailwind';
import node from '@astrojs/node';

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
  })
});