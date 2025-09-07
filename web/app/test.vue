<template>
  <div class="min-h-screen bg-gray-50 p-8">
    <h1 class="text-3xl font-bold mb-8">GitHub 仓库统计仪表板（测试版）</h1>

    <!-- 简单的加载状态 -->
    <div v-if="loading" class="text-center py-8">
      <p>正在加载数据...</p>
    </div>

    <!-- 错误状态 -->
    <div v-else-if="error" class="text-red-600 text-center py-8">
      <p>加载失败: {{ error }}</p>
      <button @click="loadData" class="mt-4 px-4 py-2 bg-blue-600 text-white rounded">重新加载</button>
    </div>

    <!-- 数据展示 -->
    <div v-else>
      <p class="mb-4">找到 {{ repos.length }} 个分支</p>

      <div class="grid gap-4">
        <div
          v-for="repo in repos"
          :key="repo.branch"
          class="bg-white p-6 rounded-lg shadow"
        >
          <h3 class="text-xl font-semibold mb-2">{{ repo.branch }}</h3>
          <p class="text-gray-600 mb-2">提交数: {{ repo.commit_count }}</p>
          <div class="text-sm text-gray-500">
            <p>最新提交: {{ repo.latest_commit?.message || '无' }}</p>
            <p>作者: {{ repo.latest_commit?.author || '未知' }}</p>
            <p>日期: {{ repo.latest_commit?.date || '未知' }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const repos = ref([])
const loading = ref(true)
const error = ref(null)

const loadData = async () => {
  loading.value = true
  error.value = null

  try {
    const response = await fetch('/repo_stats.json')
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }
    const data = await response.json()
    repos.value = Array.isArray(data) ? data : []
    console.log('加载的数据:', data)
  } catch (e) {
    error.value = e.message
    console.error('加载错误:', e)
  } finally {
    loading.value = false
  }
}

// 页面挂载时加载数据
onMounted(() => {
  loadData()
})
</script>

<style scoped>
/* 基本样式 */
</style>
