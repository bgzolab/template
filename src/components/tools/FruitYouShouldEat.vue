<template>
  <div class="w-full">
    <!-- 头部信息 -->
    <div class="mb-8">
      <div class="mb-4 p-4 bg-white rounded-lg border border-gray-200 shadow-sm">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-xl font-semibold text-gray-900 mb-1">当前月份</h2>
            <p class="text-sm text-gray-600">{{ currentMonthName }} ({{ currentMonth }}月)</p>
          </div>
          <div class="text-4xl">📅</div>
        </div>
      </div>
    </div>

    <!-- 本月当季水果 -->
    <div class="mb-8 p-6 bg-white rounded-lg border border-gray-200 shadow-sm">
      <h2 class="text-lg font-semibold text-gray-900 mb-4 flex items-center">
        <span class="mr-2">🌟</span>
        本月推荐水果
      </h2>
      <div v-if="currentSeasonFruits.length > 0" class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-3">
        <div v-for="fruit in currentSeasonFruits" :key="fruit.id"
             class="p-3 bg-gray-50 rounded-lg text-center hover:bg-gray-100 transition-colors">
          <div class="text-3xl mb-1">{{ fruit.emoji }}</div>
          <div class="text-sm font-medium text-gray-700">{{ fruit.name }}</div>
        </div>
      </div>
      <div v-else class="text-center text-gray-500 py-6">
        本月暂无推荐水果
      </div>
    </div>

    <!-- 时间线说明 -->
    <div class="mb-4">
      <h2 class="text-lg font-semibold text-gray-900 mb-2">全年水果时令表</h2>
      <p class="text-sm text-gray-600">从当前月份向未来12个月的水果成熟时间线</p>
    </div>

    <!-- 时间线 - 纵向布局 -->
    <div class="space-y-6">
      <div v-for="month in displayMonths" :key="month.index"
           class="bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden">
        <!-- 月份头部 -->
        <div class="px-4 py-3 border-b border-gray-200 flex items-center justify-between"
             :class="month.isCurrent ? 'bg-blue-50' : 'bg-gray-50'">
          <div class="flex items-center space-x-3">
            <div class="text-2xl font-bold"
                 :class="month.isCurrent ? 'text-blue-600' : 'text-gray-700'">
              {{ month.name }}
            </div>
            <div v-if="month.isCurrent" 
                 class="px-2 py-1 bg-blue-100 text-blue-700 text-xs font-medium rounded-full">
              当前月份
            </div>
          </div>
          <div class="text-sm text-gray-500">{{ month.year }}年</div>
        </div>

        <!-- 该月水果列表 -->
        <div class="p-4">
          <div v-if="getFruitsInMonth(month.realMonth).length > 0" 
               class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
            <div v-for="fruit in getFruitsInMonth(month.realMonth)" :key="fruit.id"
                 class="flex items-center space-x-2 p-2 rounded-lg hover:bg-gray-50 transition-colors">
              <span class="text-2xl">{{ fruit.emoji }}</span>
              <span class="text-sm font-medium text-gray-700">{{ fruit.name }}</span>
            </div>
          </div>
          <div v-else class="text-center py-4 text-gray-400 text-sm">
            本月暂无应季水果
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// 月份名称映射
const monthNames = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']

// 当前日期
const currentDate = ref(new Date())
const currentMonth = computed(() => currentDate.value.getMonth() + 1)
const currentMonthName = computed(() => monthNames[currentDate.value.getMonth()])

// 显示的月份列表（从当前月开始的12个月）
const displayMonths = computed(() => {
  const months = []
  const now = new Date()
  
  for (let i = 0; i < 12; i++) {
    const date = new Date(now.getFullYear(), now.getMonth() + i, 1)
    const monthIndex = date.getMonth() + 1
    months.push({
      index: i,
      realMonth: monthIndex,
      name: monthNames[date.getMonth()],
      year: date.getFullYear(),
      isCurrent: i === 0
    })
  }
  
  return months
})

// 水果数据 - 基于北半球（特别是中国）的时令
const fruits = ref([
  // 春季水果 (3-5月)
  { id: 1, name: '草莓', emoji: '🍓', months: [1, 2, 3, 4, 5] },
  { id: 2, name: '枇杷', emoji: '🟠', months: [3, 4, 5] },
  { id: 3, name: '桑葚', emoji: '🫐', months: [4, 5, 6] },
  { id: 4, name: '樱桃', emoji: '�', months: [5, 6] },
  { id: 5, name: '青梅', emoji: '🟢', months: [4, 5, 6] },
  
  // 夏季水果 (6-8月)
  { id: 6, name: '荔枝', emoji: '🔴', months: [5, 6, 7] },
  { id: 7, name: '杨梅', emoji: '🔴', months: [6, 7] },
  { id: 8, name: '西瓜', emoji: '🍉', months: [6, 7, 8, 9] },
  { id: 9, name: '桃子', emoji: '�', months: [6, 7, 8] },
  { id: 10, name: '李子', emoji: '🟣', months: [6, 7, 8] },
  { id: 11, name: '杏', emoji: '🟠', months: [6, 7] },
  { id: 12, name: '芒果', emoji: '🥭', months: [6, 7, 8] },
  { id: 13, name: '火龙果', emoji: '🐉', months: [5, 6, 7, 8, 9, 10, 11] },
  { id: 14, name: '哈密瓜', emoji: '🍈', months: [7, 8, 9] },
  { id: 15, name: '香瓜', emoji: '🍈', months: [6, 7, 8] },
  { id: 16, name: '龙眼', emoji: '🟤', months: [7, 8, 9] },
  { id: 17, name: '榴莲', emoji: '🟡', months: [6, 7, 8] },
  { id: 18, name: '山竹', emoji: '🟣', months: [5, 6, 7, 8, 9] },
  { id: 19, name: '黄桃', emoji: '�', months: [7, 8] },
  { id: 20, name: '油桃', emoji: '�', months: [6, 7, 8] },
  { id: 21, name: '蓝莓', emoji: '🫐', months: [6, 7, 8] },
  
  // 秋季水果 (9-11月)
  { id: 22, name: '葡萄', emoji: '🍇', months: [7, 8, 9, 10] },
  { id: 23, name: '石榴', emoji: '🟥', months: [9, 10] },
  { id: 24, name: '梨', emoji: '🍐', months: [8, 9, 10, 11] },
  { id: 25, name: '柿子', emoji: '🟠', months: [9, 10, 11] },
  { id: 26, name: '柚子', emoji: '🟡', months: [9, 10, 11] },
  { id: 27, name: '猕猴桃', emoji: '🥝', months: [9, 10, 11] },
  { id: 28, name: '苹果', emoji: '🍎', months: [9, 10, 11, 12] },
  { id: 29, name: '冬枣', emoji: '🟤', months: [9, 10, 11] },
  { id: 30, name: '板栗', emoji: '🌰', months: [9, 10] },
  { id: 31, name: '核桃', emoji: '🟤', months: [9, 10] },
  { id: 32, name: '山楂', emoji: '🔴', months: [9, 10, 11] },
  
  // 冬季水果 (12-2月)
  { id: 33, name: '橙子', emoji: '🍊', months: [11, 12, 1, 2, 3] },
  { id: 34, name: '柑橘', emoji: '🍊', months: [10, 11, 12, 1, 2] },
  { id: 35, name: '砂糖橘', emoji: '🍊', months: [12, 1, 2] },
  { id: 36, name: '金桔', emoji: '🟡', months: [11, 12, 1] },
  { id: 37, name: '柚子', emoji: '🟡', months: [10, 11, 12, 1] },
  { id: 38, name: '释迦果', emoji: '🟢', months: [11, 12, 1, 2] },
  
  // 全年可得水果
  { id: 39, name: '香蕉', emoji: '🍌', months: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] },
  { id: 40, name: '菠萝', emoji: '🍍', months: [3, 4, 5, 6, 7, 8, 9] },
  { id: 41, name: '木瓜', emoji: '🟡', months: [9, 10, 11, 12, 1, 2] },
  { id: 42, name: '牛油果', emoji: '🥑', months: [3, 4, 5, 6, 7, 8, 9] },
])

// 当季水果
const currentSeasonFruits = computed(() => {
  return fruits.value.filter(fruit => fruit.months.includes(currentMonth.value))
})

// 获取指定月份的水果
const getFruitsInMonth = (month) => {
  return fruits.value.filter(fruit => fruit.months.includes(month))
}
</script>

<style scoped>
/* 自定义滚动条样式 */
.overflow-x-auto::-webkit-scrollbar {
  height: 8px;
}

.overflow-x-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.overflow-x-auto::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.overflow-x-auto::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>
