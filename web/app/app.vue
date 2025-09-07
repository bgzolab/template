<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <h1 class="text-3xl font-bold text-gray-900">
          GitHub 仓库统计仪表板
        </h1>
        <p class="mt-2 text-gray-600">
          展示 {{ displayedRepos.length }} 个分支的详细信息
        </p>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
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
            placeholder="搜索分支名称..."
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
      <div v-if="!pending && !error" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="repo in paginatedRepos"
          :key="repo.branch"
          class="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden"
        >
          <!-- Card Header -->
          <div class="p-6 border-b border-gray-200">
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <h3 class="text-lg font-semibold text-gray-900 truncate" :title="repo.branch">
                  {{ repo.branch }}
                </h3>
                <div class="mt-2 flex items-center space-x-4 text-sm text-gray-500">
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

          <!-- README Preview -->
          <div class="p-6">
            <h4 class="text-sm font-medium text-gray-900 mb-3">README 预览</h4>
            <div class="text-sm text-gray-600">
              <div v-if="repo.readme && repo.readme.trim()" class="space-y-2">
                <p class="line-clamp-3">
                  {{ getReadmePreview(repo.readme) }}
                </p>
                <button
                  v-if="repo.readme.length > 150"
                  @click="toggleReadme(repo.branch)"
                  class="text-blue-600 hover:text-blue-800 text-xs font-medium"
                >
                  {{ expandedReadmes[repo.branch] ? '收起' : '展开更多' }}
                </button>
                <!-- Expanded README (懒加载) -->
                <div v-if="expandedReadmes[repo.branch]" class="mt-3 p-3 bg-gray-50 rounded text-xs max-h-64 overflow-y-auto">
                  <pre class="whitespace-pre-wrap">{{ truncateReadme(repo.readme) }}</pre>
                </div>
              </div>
              <p v-else class="text-gray-400 italic">
                暂无 README 文件
              </p>
            </div>
          </div>

          <!-- Card Footer -->
          <div class="px-6 py-3 bg-gray-50 border-t border-gray-200">
            <div class="flex items-center justify-between">
              <span class="text-xs text-gray-500">
                分支: {{ repo.branch.split('/').pop() }}
              </span>
              <a
                :href="`https://github.com/bGZo/playground/tree/${repo.branch}`"
                target="_blank"
                class="text-xs text-blue-600 hover:text-blue-800 font-medium flex items-center"
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

      <!-- Statistics Summary -->
      <div class="mt-12 bg-white rounded-lg shadow-md p-6">
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
    </main>
  </div>
</template>

<script setup>
// 设置页面标题
useHead({
  title: 'GitHub 仓库统计仪表板',
  meta: [
    { name: 'description', content: '展示 GitHub 仓库的分支统计信息' }
  ]
})

// 获取仓库统计数据 - 移除 await，让它异步加载
const { data: repoStats, pending, error, refresh } = useFetch('/repo_stats.json', {
  server: false, // 只在客户端加载
  default: () => [], // 提供默认值
  transform: (data) => {
    if (!data || !Array.isArray(data)) return []
    // 预处理数据，截断过长的 README 内容以节省内存
    return data.map(repo => ({
      ...repo,
      readme: repo.readme ? (repo.readme.length > 5000 ? repo.readme.substring(0, 5000) + '...' : repo.readme) : ''
    }))
  }
})

// 响应式数据
const expandedReadmes = ref({})
const searchQuery = ref('')
const filterOption = ref('all')
const currentPage = ref(1)
const itemsPerPage = 12

// 计算属性
const displayedRepos = computed(() => {
  if (!repoStats.value || !Array.isArray(repoStats.value)) return []

  let filtered = repoStats.value

  // 搜索过滤
  if (searchQuery.value) {
    filtered = filtered.filter(repo =>
      repo.branch && repo.branch.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }

  // 类型过滤
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

// 监听搜索和过滤变化，重置页面
watch([searchQuery, filterOption], () => {
  currentPage.value = 1
})

// 方法
const refreshData = () => {
  refresh()
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

const getReadmePreview = (readme) => {
  if (!readme) return ''
  const cleaned = readme.replace(/[\r\n]+/g, ' ').trim()
  return cleaned.length > 150 ? cleaned.substring(0, 150) + '...' : cleaned
}

const truncateReadme = (readme) => {
  if (!readme) return ''
  // 限制展开的 README 长度，避免性能问题
  return readme.length > 2000 ? readme.substring(0, 2000) + '\n\n... (内容过长，已截断)' : readme
}

const toggleReadme = (branch) => {
  if (!branch) return
  expandedReadmes.value[branch] = !expandedReadmes.value[branch]
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
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
