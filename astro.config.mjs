// @ts-check
import { defineConfig } from 'astro/config';
import vue from '@astrojs/vue'; 
import tailwind from '@astrojs/tailwind';

// https://astro.build/config
export default defineConfig({
  integrations: [
    // 集成Vue
    vue(),
    // 集成 Tailwind
    tailwind(),
  ]
});
