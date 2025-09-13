// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss'],

  // 启用静态站点生成
  nitro: {
    prerender: {
      routes: ['/']
    }
  },

  // GitHub Pages 配置
  app: {
    baseURL: process.env.NODE_ENV === 'production' ? '/playground/' : '/',
    buildAssetsDir: '/assets/'
  },

  // SSR 配置
  ssr: true,

  // 构建配置
  build: {
    analyze: false
  },

  // 运行时配置
  runtimeConfig: {
    public: {
      apiBase: '/api'
    }
  }
})
