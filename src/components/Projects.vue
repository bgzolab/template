<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <!-- <div class="max-w-7xl mx-auto py-6">  -->
      <!-- px-4 sm:px-6 lg:px-8  -->
      <!-- <h1 class="text-3xl font-bold text-gray-900">
        bGZo's Playground
      </h1> -->
      <!-- <p class="mt-2 text-gray-600">
        一共探索、实现了 {{ displayedRepos.length }} 个小想法，希望对你有用 ✨
      </p>
    </div> -->

          <!-- Statistics Summary -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-bold text-gray-900 mb-4">统计摘要</h2>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="text-center">
            <div class="text-2xl font-bold text-blue-600">{{ repoStats?.length || 0 }}</div>
            <div class="text-sm text-gray-500">总分支数</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-green-600">{{ totalCommits }}</div>
            <div class="text-sm text-gray-500">总提交数</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-purple-600">{{ branchesWithReadme }}</div>
            <div class="text-sm text-gray-500">包含 README</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-orange-600">{{ activeProjects }}</div>
            <div class="text-sm text-gray-500">活跃项目</div>
          </div>
        </div>
      </div>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto py-8">
      <!-- px-4 sm:px-6 lg:px-8  -->
      <!-- Loading State -->
      <div v-if="pending" class="flex justify-center items-center h-64">
        <div class="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
        <p class="ml-4 text-gray-600">正在加载数据...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center py-12">
        <div class="text-red-600 text-xl">
          加载数据时出错: {{ error }}
        </div>
        <button @click="refreshData" class="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
          重新加载
        </button>
      </div>

      <!-- Search and Filter -->
      <div v-else class="mb-6">
        <div class="flex flex-col sm:flex-row gap-4">
          <input
            v-model="searchQuery"
            placeholder="搜索项目名称或分支..."
            class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
          <select
            v-model="filterOption"
            class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">所有分支</option>
            <option value="with-readme">包含 README</option>
            <option value="active">活跃项目</option>
          </select>
        </div>
      </div>

      <!-- Repository Cards Grid -->
      <div v-if="!pending && !error" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-6">
        <div
          v-for="repo in paginatedRepos"
          :key="repo.branch"
          class="bg-white rounded-2xl shadow-md hover:shadow-lg transition-all duration-300 overflow-hidden"
          :class="{ 'cursor-pointer group': hasReadme(repo) }"
          @click="hasReadme(repo) ? openReadmeModal(repo) : null"
        >
          <!-- Card Header -->
          <div class="p-6 border-b border-gray-200">
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <h3 class="text-lg font-semibold text-gray-900"
                    :class="{ 'group-hover:text-blue-600 transition-colors duration-200': hasReadme(repo) }"
                    :title="repo.name">
                  {{ repo.name || repo.branch }}
                </h3>
                <p class="text-sm text-gray-500 mt-1 truncate" :title="repo.branch">
                  {{ repo.branch }}
                </p>
                <div class="mt-3 flex items-center space-x-4 text-sm text-gray-500">
                  <span class="flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                    </svg>
                    {{ repo.commit_count }} commits
                  </span>
                </div>
              </div>
              <div class="flex-shrink-0">
                <span :class="getStatusBadgeClass(repo)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                  {{ getStatusText(repo) }}
                </span>
              </div>
            </div>
          </div>

          <!-- Latest Commit Info -->
          <div class="p-6 border-b border-gray-200">
            <h4 class="text-sm font-medium text-gray-900 mb-3">最新提交</h4>
            <div class="space-y-2">
              <p class="text-sm text-gray-800 font-medium line-clamp-2" :title="repo.latest_commit.message">
                {{ repo.latest_commit.message }}
              </p>
              <div class="flex items-center justify-between text-xs text-gray-500">
                <span class="flex items-center">
                  <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"></path>
                  </svg>
                  {{ repo.latest_commit.author }}
                </span>
                <span>{{ formatDate(repo.latest_commit.date) }}</span>
              </div>
              <code class="text-xs bg-gray-100 px-2 py-1 rounded font-mono">
                {{ repo.latest_commit.sha.substring(0, 8) }}
              </code>
            </div>
          </div>

          <!-- Card Footer -->
          <div class="px-6 py-3 bg-gray-50 border-t border-gray-200">
            <div class="flex items-center justify-between">
              <span class="text-xs text-gray-500">
                {{ formatDate(repo.latest_commit.date) }}
              </span>
              <a
                :href="`https://github.com/bGZo/playground/tree/${repo.branch}`"
                target="_blank"
                class="text-xs text-blue-600 hover:text-blue-800 font-medium flex items-center"
                @click.stop
              >
                查看源码
                <svg class="w-3 h-3 ml-1" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z"></path>
                  <path d="M5 5a2 2 0 00-2 2v8a2 2 0 002 2h8a2 2 0 002-2v-1a1 1 0 10-2 0v1H5V7h1a1 1 0 000-2H5z"></path>
                </svg>
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="!pending && !error && displayedRepos.length > itemsPerPage" class="mt-8 flex justify-center">
        <nav class="flex items-center space-x-2">
          <button
            @click="currentPage = Math.max(1, currentPage - 1)"
            :disabled="currentPage === 1"
            class="px-3 py-2 text-sm bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            上一页
          </button>

          <span class="px-4 py-2 text-sm text-gray-700">
            第 {{ currentPage }} 页，共 {{ totalPages }} 页
          </span>

          <button
            @click="currentPage = Math.min(totalPages, currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="px-3 py-2 text-sm bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            下一页
          </button>
        </nav>
      </div>


    </main>

    <!-- README Modal -->
    <div v-if="showReadmeModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50" @click="closeReadmeModal">
      <div class="bg-white rounded-lg max-w-4xl max-h-[90vh] w-full overflow-hidden" @click.stop>
        <!-- Modal Header -->
        <div class="flex items-center justify-between p-6 border-b border-gray-200">
          <div>
            <h3 class="text-lg font-semibold text-gray-900">
              {{ selectedRepo?.name || selectedRepo?.branch }}
            </h3>
            <p class="text-sm text-gray-500 mt-1">{{ selectedRepo?.branch }}</p>
          </div>
          <button
            @click="closeReadmeModal"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>

        <!-- Modal Content -->
        <div class="p-6 overflow-y-auto max-h-[calc(90vh-140px)]">
          <div v-if="selectedRepo?.readme && selectedRepo.readme.trim()"
               class="prose prose-slate max-w-none"
               v-html="renderMarkdown(selectedRepo.readme)">
          </div>
          <div v-else class="text-center py-12 text-gray-500">
            <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
            <p class="text-lg">暂无 README 文件</p>
          </div>
        </div>

        <!-- Modal Footer -->
        <div class="px-6 py-4 border-t border-gray-200 bg-gray-50">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-4 text-sm text-gray-500">
              <span>{{ selectedRepo?.commit_count }} commits</span>
              <span>{{ formatDate(selectedRepo?.latest_commit?.date) }}</span>
            </div>
            <a
              :href="`https://github.com/bGZo/playground/tree/${selectedRepo?.branch}`"
              target="_blank"
              class="inline-flex items-center px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 transition-colors"
            >
              查看源码
              <svg class="w-4 h-4 ml-2" fill="currentColor" viewBox="0 0 20 20">
                <path d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z"></path>
                <path d="M5 5a2 2 0 00-2 2v8a2 2 0 002 2h8a2 2 0 002-2v-1a1 1 0 10-2 0v1H5V7h1a1 1 0 000-2H5z"></path>
              </svg>
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, nextTick } from 'vue'
import { marked } from 'marked'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'

export default {
  name: 'App',
  setup() {
    // 配置 marked
    marked.setOptions({
      highlight: function(code, lang) {
        if (lang && hljs.getLanguage(lang)) {
          try {
            return hljs.highlight(code, { language: lang }).value
          } catch (__) {}
        }
        return hljs.highlightAuto(code).value
      },
      breaks: true,
      gfm: true
    })

    // 响应式数据
    const repoStats = ref([])
    const pending = ref(true)
    const error = ref(null)
    const searchQuery = ref('')
    const filterOption = ref('all')
    const currentPage = ref(1)
    const itemsPerPage = 12
    const showReadmeModal = ref(false)
    const selectedRepo = ref(null)

    // 通过 Vite 的 BASE_URL 适配根路径或子路径
    const baseURL = (import.meta.env && import.meta.env.BASE_URL) || '/'

    // 计算属性
    const displayedRepos = computed(() => {
      let filtered = repoStats.value

      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(repo =>
          (repo.name && repo.name.toLowerCase().includes(query)) ||
          (repo.branch && repo.branch.toLowerCase().includes(query))
        )
      }

      if (filterOption.value === 'with-readme') {
        filtered = filtered.filter(repo => repo.readme && repo.readme.trim())
      } else if (filterOption.value === 'active') {
        const oneYearAgo = new Date()
        oneYearAgo.setFullYear(oneYearAgo.getFullYear() - 1)
        filtered = filtered.filter(repo => {
          if (!repo.latest_commit || !repo.latest_commit.date) return false
          const commitDate = new Date(repo.latest_commit.date)
          return commitDate > oneYearAgo
        })
      }

      return filtered
    })

    const totalPages = computed(() => {
      return Math.max(1, Math.ceil(displayedRepos.value.length / itemsPerPage))
    })

    const paginatedRepos = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage
      const end = start + itemsPerPage
      return displayedRepos.value.slice(start, end)
    })

    const totalCommits = computed(() => {
      if (!repoStats.value || !Array.isArray(repoStats.value)) return 0
      return repoStats.value.reduce((sum, repo) => sum + (repo.commit_count || 0), 0)
    })

    const branchesWithReadme = computed(() => {
      if (!repoStats.value || !Array.isArray(repoStats.value)) return 0
      return repoStats.value.filter(repo => repo.readme && repo.readme.trim()).length
    })

    const activeProjects = computed(() => {
      if (!repoStats.value || !Array.isArray(repoStats.value)) return 0

      const oneYearAgo = new Date()
      oneYearAgo.setFullYear(oneYearAgo.getFullYear() - 1)

      return repoStats.value.filter(repo => {
        if (!repo.latest_commit || !repo.latest_commit.date) return false
        const commitDate = new Date(repo.latest_commit.date)
        return commitDate > oneYearAgo
      }).length
    })

    // 方法
    const loadData = async () => {
      try {
        const response = await fetch(`${baseURL}/repo_stats.json`)
        if (response.ok) {
          const data = await response.json()
          repoStats.value = Array.isArray(data) ? data : []
        } else {
          error.value = 'Failed to load data'
        }
      } catch (e) {
        error.value = e.message
      } finally {
        pending.value = false
      }
    }

    const refreshData = () => {
      pending.value = true
      error.value = null
      loadData()
    }

    const hasReadme = (repo) => {
      return repo.readme && repo.readme.trim().length > 0
    }

    const formatDate = (dateString) => {
      if (!dateString) return '未知日期'
      try {
        return new Date(dateString).toLocaleDateString('zh-CN', {
          year: 'numeric',
          month: 'short',
          day: 'numeric'
        })
      } catch (e) {
        return '无效日期'
      }
    }

    const getStatusBadgeClass = (repo) => {
      if (!repo || !repo.latest_commit || !repo.latest_commit.date) {
        return 'bg-gray-100 text-gray-800'
      }

      try {
        const oneYearAgo = new Date()
        oneYearAgo.setFullYear(oneYearAgo.getFullYear() - 1)
        const commitDate = new Date(repo.latest_commit.date)

        if (commitDate > oneYearAgo) {
          return 'bg-green-100 text-green-800'
        } else {
          return 'bg-gray-100 text-gray-800'
        }
      } catch (e) {
        return 'bg-gray-100 text-gray-800'
      }
    }

    const getStatusText = (repo) => {
      if (!repo || !repo.latest_commit || !repo.latest_commit.date) {
        return 'Unknown'
      }

      try {
        const oneYearAgo = new Date()
        oneYearAgo.setFullYear(oneYearAgo.getFullYear() - 1)
        const commitDate = new Date(repo.latest_commit.date)

        return commitDate > oneYearAgo ? 'Active' : 'Archived'
      } catch (e) {
        return 'Unknown'
      }
    }

    const openReadmeModal = (repo) => {
      if (!hasReadme(repo)) return

      selectedRepo.value = repo
      showReadmeModal.value = true
      document.body.style.overflow = 'hidden'
    }

    const closeReadmeModal = () => {
      showReadmeModal.value = false
      selectedRepo.value = null
      document.body.style.overflow = 'auto'
    }

    const renderMarkdown = (content) => {
      if (!content) return ''
      try {
        return marked(content)
      } catch (e) {
        console.error('Markdown rendering error:', e)
        return '<pre>' + content + '</pre>'
      }
    }

    // 生命周期
    onMounted(() => {
      loadData()

      // 键盘事件监听
      const handleKeydown = (e) => {
        if (e.key === 'Escape' && showReadmeModal.value) {
          closeReadmeModal()
        }
      }

      document.addEventListener('keydown', handleKeydown)

      return () => {
        document.removeEventListener('keydown', handleKeydown)
        document.body.style.overflow = 'auto'
      }
    })

    return {
      repoStats,
      pending,
      error,
      searchQuery,
      filterOption,
      currentPage,
      itemsPerPage,
      showReadmeModal,
      selectedRepo,
      displayedRepos,
      totalPages,
      paginatedRepos,
      totalCommits,
      branchesWithReadme,
      activeProjects,
      refreshData,
      hasReadme,
      formatDate,
      getStatusBadgeClass,
      getStatusText,
      openReadmeModal,
      closeReadmeModal,
      renderMarkdown
    }
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>