<template>
  <div class="w-full">
    <!-- 本月推荐 -->
    <div class="mb-8 p-6 bg-white rounded-lg border border-gray-200 shadow-sm">
      <h2 class="text-base font-semibold text-gray-900 mb-4">
        本月推荐 · {{ currentMonthName }}
      </h2>
      <div v-if="currentSeasonFruits.length > 0" class="flex flex-wrap gap-3">
        <div v-for="fruit in currentSeasonFruits" :key="fruit.id"
             class="relative flex items-center space-x-2 px-3 py-2 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
             :title="getBadgeTitle(fruit)">
          <!-- Badge group (top-right) -->
          <div class="absolute -top-2 -right-2 flex items-center space-x-1">
            <span v-if="isNewThisMonth(fruit)" class="bg-green-600 text-white text-xs font-semibold px-2 py-0.5 rounded-full">New</span>
            <span v-if="willEndNextMonth(fruit)" class="bg-orange-500 text-white text-xs font-semibold px-2 py-0.5 rounded-full">Exp</span>
          </div>
          <span class="text-xl">{{ fruit.emoji }}</span>
          <span class="text-sm font-medium text-gray-700">{{ fruit.name }}</span>
        </div>
      </div>
      <div v-else class="text-center text-gray-500 py-4 text-sm">
        本月暂无推荐水果
      </div>
    </div>

    <!-- 时间线 -->
    <div class="relative">
      <!-- 时间轴线 -->
      <div class="absolute left-[60px] top-0 bottom-0 w-px bg-gray-200"></div>
      
      <!-- 时间线项目 -->
      <div class="space-y-0">
        <div v-for="month in displayMonths" :key="month.index" class="relative flex">
          <!-- 左侧：月份标签 -->
          <div class="flex-shrink-0 w-[60px] pt-6 pr-4 text-right">
            <div class="text-sm font-medium"
                 :class="month.isCurrent ? 'text-blue-600' : 'text-gray-500'">
              {{ month.name }}
            </div>
            <div v-if="month.showYear" class="text-xs text-gray-400 mt-0.5">
              {{ month.year }}
            </div>
          </div>

          <!-- 时间轴节点 -->
          <div class="absolute left-[60px] top-6 transform -translate-x-1/2 z-10">
            <div class="w-3 h-3 rounded-full border-2"
                 :class="month.isCurrent 
                   ? 'bg-blue-600 border-blue-600' 
                   : 'bg-white border-gray-300'">
            </div>
          </div>

          <!-- 右侧：水果卡片 -->
          <div class="flex-1 pl-6 pb-6">
            <div v-if="getFruitsInMonth(month.realMonth).length > 0"
                 class="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
              <div class="flex flex-wrap gap-2">
                <div v-for="fruit in getFruitsInMonth(month.realMonth)" :key="fruit.id"
                     class="flex items-center space-x-1.5 px-2.5 py-1.5 bg-gray-50 rounded hover:bg-gray-100 transition-colors">
                  <span class="text-lg">{{ fruit.emoji }}</span>
                  <span class="text-sm text-gray-700">{{ fruit.name }}</span>
                </div>
              </div>
            </div>
            <div v-else class="text-sm text-gray-400 pt-1">
              暂无应季水果
            </div>
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
  const currentYear = now.getFullYear()
  
  for (let i = 0; i < 12; i++) {
    const date = new Date(now.getFullYear(), now.getMonth() + i, 1)
    const monthIndex = date.getMonth() + 1
    const year = date.getFullYear()
    
    // 显示年份的条件：
    // 1. 第一个月总是显示年份
    // 2. 1月时显示年份（新年）
    // 3. 年份变化时显示年份
    const showYear = i === 0 || monthIndex === 1 || (i > 0 && year !== months[i - 1].year)
    
    months.push({
      index: i,
      realMonth: monthIndex,
      name: monthNames[date.getMonth()],
      year: year,
      isCurrent: i === 0,
      showYear: showYear
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
  { id: 26, name: '柚子', emoji: '🟡', months: [9, 10, 11, 12, 1] },
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

// 上个月和下个月
const prevMonth = computed(() => ((currentMonth.value + 10) % 12) + 1) // -1 month
const nextMonth = computed(() => (currentMonth.value % 12) + 1) // +1 month

// 判断水果是否本月是首次出现（new）
const isNewThisMonth = (fruit) => {
  // 如果水果成熟月份包含本月，但不包含上个月，则视为本月新上市
  return fruit.months.includes(currentMonth.value) && !fruit.months.includes(prevMonth.value)
}

// 判断水果是否将在下个月过季（即本月有，下个月没有）
const willEndNextMonth = (fruit) => {
  return fruit.months.includes(currentMonth.value) && !fruit.months.includes(nextMonth.value)
}

// Badge 提示文本
const getBadgeTitle = (fruit) => {
  if (isNewThisMonth(fruit) && willEndNextMonth(fruit)) {
    return '本月新上市，并可能下月结束'
  }
  if (isNewThisMonth(fruit)) return '本月新上市'
  if (willEndNextMonth(fruit)) return '下月将过季'
  return ''
}

// 获取指定月份的水果
const getFruitsInMonth = (month) => {
  return fruits.value.filter(fruit => fruit.months.includes(month))
}
</script>

<style scoped>
/* 无需额外样式 */
</style>
