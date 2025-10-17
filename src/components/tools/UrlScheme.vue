<template>
  <h1 class="text-3xl font-bold text-gray-800 mb-2">URL Scheme 转换工具</h1>
  <p class="text-gray-600 mb-6">将传统 URL 转换为可直接跳转应用的 URL Scheme</p>

  <!-- 输入区域 -->
  <div class="mb-6">
    <label class="block text-sm font-medium text-gray-700 mb-2">输入 URL（每行一个）：</label>
    <textarea v-model="inputText" rows="4"
      class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-mono text-sm resize-vertical"
      placeholder="输入 URL，如：&#10;https://www.pixiv.net/users/89849713&#10;https://twitter.com/username"></textarea>
  </div>

  <!-- 操作控制区域 -->
  <div class="flex flex-col sm:flex-row items-center gap-4 mb-6 p-4 rounded-lg">
    <div class="flex items-center gap-2">
      <label class="text-sm font-medium text-gray-700">转换规则：</label>
      <select v-model="selectedRule"
        class="px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm">
        <option v-for="rule in rules" :key="rule.key" :value="rule.key">{{ rule.name }}</option>
      </select>
    </div>

    <button @click="convertUrls"
      class="px-6 py-2 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed
      "
      :disabled="!inputText.trim()">
      转换
    </button>

    <button @click="clearAll"
      class="px-6 py-2 bg-gray-600 text-white font-medium rounded-md hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors duration-200">
      清空
    </button>
  </div>

  <!-- 输出区域 -->
  <div class="mb-6">
    <div v-if="outputSchemes.length > 0" class="space-y-2">
    <label class="block text-sm font-medium text-gray-700 mb-2">转换结果：</label>
      <div v-for="(scheme, index) in outputSchemes" :key="index"
        class="p-3 bg-gray-50 border border-gray-200 rounded-md">
        <div class="flex items-center justify-between">
          <span class="font-mono text-sm text-gray-800 break-all">{{ scheme }}</span>
<!-- 
            :disabled="testedSchemes[index]"
-->
          <button @click="testScheme(index)"
            :class="[
              'ml-2 px-3 py-1 text-xs font-medium rounded focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors duration-200',
              testedSchemes[index]
                ? 'bg-gray-400 text-gray-200'
                : 'bg-green-600 text-white hover:bg-green-700 focus:ring-green-500'
            ]">
            {{ testedSchemes[index] ? '已测试' : '测试' }}
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- 错误提示 -->
  <div v-if="errorMessage" class="p-4 bg-red-50 border border-red-200 rounded-md">
    <div class="flex">
      <div class="flex-shrink-0">
        <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd"
            d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
            clip-rule="evenodd" />
        </svg>
      </div>
      <div class="ml-3">
        <p class="text-sm text-red-800">{{ errorMessage }}</p>
      </div>
    </div>
  </div>

  <!-- 使用说明 -->
  <div class="mt-8 p-4 bg-blue-50 border border-blue-200 rounded-md">
    <h3 class="text-lg font-medium text-blue-800 mb-2">使用说明</h3>
    <ul class="text-sm text-blue-700 space-y-1">
      <li>• 输入每行一个 URL，支持多个 URL</li>
      <li>• 选择对应的转换规则（如 Pixiv、Twitter 等）</li>
      <li>• 点击转换按钮生成 URL Scheme</li>
      <li>• 点击测试按钮可在浏览器中测试跳转</li>
      <li>• 注意：URL Scheme 在移动设备上效果更佳</li>
    </ul>
  </div>

  <!-- 示例测试 -->
  <div class="mt-6 p-4 bg-green-50 border border-green-200 rounded-md">
    <h3 class="text-lg font-medium text-green-800 mb-3">示例测试</h3>
    <p class="text-sm text-green-700 mb-4">点击下方按钮测试常用应用的 URL Scheme：</p>
    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
      <button
        v-for="example in exampleSchemes"
        :key="example.key"
        @click="testExampleScheme(example.scheme)"
        class="px-3 py-2 bg-green-600 text-white text-sm font-medium rounded hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-colors duration-200">
        {{ example.name }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

// 定义转换规则
interface Rule {
  key: string;
  name: string;
  pattern: RegExp;
  replacement: string;
}

interface ExampleScheme {
  key: string;
  name: string;
  scheme: string;
}

const rules: Rule[] = [
  {
    key: 'pixiv',
    name: 'Pixiv',
    pattern: /^https?:\/\/(?:www\.)?pixiv\.net\/users\/(\d+)$/,
    replacement: 'pixiv://users/$1'
  },
  {
    key: 'twitter',
    name: 'Twitter',
    pattern: /^https?:\/\/(?:www\.)?twitter\.com\/(\w+)$/,
    replacement: 'twitter://user?screen_name=$1'
  },
  {
    key: 'instagram',
    name: 'Instagram',
    pattern: /^https?:\/\/(?:www\.)?instagram\.com\/(\w+)$/,
    replacement: 'instagram://user?username=$1'
  },
  {
    key: 'youtube',
    name: 'YouTube',
    pattern: /^https?:\/\/(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)$/,
    replacement: 'youtube://watch?v=$1'
  },
  {
    key: 'github',
    name: 'GitHub',
    pattern: /^https?:\/\/(?:www\.)?github\.com\/([^\/]+)\/([^\/]+)$/,
    replacement: 'github://$1/$2'
  }
];

const exampleSchemes: ExampleScheme[] = [
  { key: '支付宝扫一扫', name: '支付宝扫一扫', scheme: 'alipayqr://platformapi/startapp?saId=10000007' },
  { key: '支付宝付款码', name: '支付宝付款码', scheme: 'alipayqr://platformapi/startapp?saId=20000056' },
  { key: '哈啰扫码', name: '哈啰扫码', scheme: 'hellobike://hellobike.com/scan_qr' },
  { key: '微信扫一扫', name: '微信扫一扫(iOS)', scheme: 'weixin://scanqrcode' },
  { key: 'telegram', name: 'Telegram', scheme: 'tg://resolve?domain=imbgzo' },
];

const inputText = ref('');
const selectedRule = ref('pixiv');
const outputSchemes = ref<string[]>([]);
const errorMessage = ref('');
const testedSchemes = ref<boolean[]>([]);

// 获取当前选中的规则
const currentRule = computed(() => {
  return rules.find(rule => rule.key === selectedRule.value);
});

// 转换 URL
const convertUrls = () => {
  errorMessage.value = '';
  outputSchemes.value = [];
  testedSchemes.value = [];

  try {
    const lines = inputText.value.trim().split('\n').filter(line => line.trim());
    if (lines.length === 0) {
      errorMessage.value = '请输入至少一个 URL';
      return;
    }

    const rule = currentRule.value;
    if (!rule) {
      errorMessage.value = '请选择有效的转换规则';
      return;
    }

    const schemes: string[] = [];
    for (const line of lines) {
      const url = line.trim();
      if (!url) continue;

      const match = url.match(rule.pattern);
      if (match) {
        const scheme = url.replace(rule.pattern, rule.replacement);
        schemes.push(scheme);
      } else {
        errorMessage.value = `URL 格式不匹配规则：${url}`;
        return;
      }
    }

    outputSchemes.value = schemes;
    testedSchemes.value = new Array(schemes.length).fill(false);

  } catch (error) {
    errorMessage.value = `转换失败: ${error instanceof Error ? error.message : '未知错误'}`;
  }
};

// 清空所有内容
const clearAll = () => {
  inputText.value = '';
  outputSchemes.value = [];
  errorMessage.value = '';
  testedSchemes.value = [];
};

// 测试 URL Scheme
const testScheme = (index: number) => {
  testedSchemes.value[index] = true;
  window.open(outputSchemes.value[index], '_blank', 'noopener,noreferrer');
};

// 测试示例 URL Scheme
const testExampleScheme = (scheme: string) => {
  window.open(scheme, '_blank', 'noopener,noreferrer');
};
</script>
