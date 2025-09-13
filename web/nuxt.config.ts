// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  // 基础配置
  devtools: { enabled: false },

  // 模块配置
  modules: ['@nuxtjs/tailwindcss'],

  // 完全禁用 SSR，启用纯 SPA
  ssr: false,

  // 应用配置
  app: {
    // baseURL: process.env.NODE_ENV === 'production' ? '/playground/' : '/',
    baseURL: '/playground/',  // <-- 一定要和仓库名一致
    head: {
      title: "bGZo's Playground",
      meta: [
        { name: 'description', content: "Show what I've built recently" }
      ]
    }
  },

  // Nitro 配置 - 静态预设
  nitro: {
    preset: 'github-pages'
  },

  // 路由配置
  router: {
    options: {
      hashMode: false
    }
  },

  // https://stackoverflow.com/questions/77618435/building-nuxt-ionic-app-give-me-error-not-initialization-typeerror-cannot-read
  experimental:{
    payloadExtraction: false
  },

})
