// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: false }, // 生产环境关闭 devtools
  modules: ['@nuxtjs/tailwindcss'],

  // 静态站点生成配置
  nitro: {
    prerender: {
      routes: ['/']
    }
  },

  // GitHub Pages 配置 - 修复本地测试路径问题
  app: {
    baseURL: process.env.NUXT_APP_BASE_URL || (process.env.NODE_ENV === 'production' ? '/playground/' : '/'),
    buildAssetsDir: '/assets/'
  },

  // 关闭 SSR，启用静态生成
  ssr: false,

  // 构建配置
  build: {
    analyze: false
  },

  // 运行时配置
  runtimeConfig: {
    public: {
      apiBase: '/api'
    }
  },

  // 生成配置
  generate: {
    fallback: '404.html'
  }
})
