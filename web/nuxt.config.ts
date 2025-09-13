// https://nuxt.com/docs/api/configuration/nuxt-config

// 方式 1: 直接在配置文件顶部声明变量
const isDev = process.env.NODE_ENV !== 'production'
const REPO_NAME = process.env.NUXT_REPO_NAME || 'playground'
const BASE_PATH = process.env.NUXT_PUBLIC_BASE_URL || (isDev ? '/' : '/')

// Vercel 特定配置
const isVercel = process.env.VERCEL === '1'

export default defineNuxtConfig({
  // 基础配置
  devtools: { enabled: false },

  // 模块配置
  modules: ['@nuxtjs/tailwindcss'],

  // 完全禁用 SSR，启用纯 SPA
  ssr: false,

  // 应用配置
  app: {
    // Vercel 部署使用根路径，GitHub Pages 使用子路径
    baseURL: isVercel ? '/' : BASE_PATH,

    head: {
      title: "bGZo's Playground",
      meta: [
        { name: 'description', content: "Show what I've built recently" },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' }
      ]
    }
  },

  // 运行时配置 - 可以在应用中访问这些变量
  runtimeConfig: {
    // 私有配置（只在服务端可用）
    githubToken: process.env.NUXT_GITHUB_TOKEN,

    // 公共配置（客户端也可用）
    public: {
      baseURL: isVercel ? '/' : BASE_PATH,
      repoName: REPO_NAME,
      apiBase: '/api',
      isVercel: isVercel
    }
  },

  // Nitro 配置 - 针对 Vercel 优化
  nitro: {
    preset: isVercel ? 'vercel' : 'github-pages',
    prerender: {
      routes: ['/']
    },
    // Vercel 特定配置
    vercel: {
      functions: {
        maxDuration: 30
      }
    }
  },

  // Vercel 构建优化
  vite: {
    build: {
      rollupOptions: {
        output: {
          manualChunks: {
            vendor: ['marked', 'highlight.js'],
            ui: ['@tailwindcss/typography']
          }
        }
      }
    }
  }

})
