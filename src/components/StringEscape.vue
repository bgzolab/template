<template>
  <!-- <div class="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg"> -->
  <h1 class="text-3xl font-bold text-gray-800 mb-2">字符串转义工具</h1>
  <p class="text-gray-600 mb-6">支持多种编码格式的双向转义转换</p>

  <!-- 输入区域 -->
  <div class="mb-6">
    <label class="block text-sm font-medium text-gray-700 mb-2">原始字符串：</label>
    <textarea v-model="inputText" rows="4"
      class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-mono text-sm resize-vertical"
      placeholder="输入原始字符串，点击左侧进行转义"></textarea>
  </div>

  <!-- 操作控制区域 -->
  <div class="flex flex-col sm:flex-row items-center gap-4 mb-6 p-4 bg-gray-50 rounded-lg">
    <button @click="processString('encode')"
      class="px-6 py-2 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
      :disabled="!inputText.trim()">
      转义
    </button>

    <div class="flex items-center gap-2">
      <label class="text-sm font-medium text-gray-700">转义模式：</label>
      <select v-model="escapeMode"
        class="px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm">
        <option value="html">HTML 实体</option>
        <option value="url">URL 编码</option>
        <option value="uri">URI 编码</option>
        <option value="json">JSON 转义</option>
        <option value="base64">Base64</option>
      </select>
    </div>

    <button @click="processString('decode')"
      class="px-6 py-2 bg-green-600 text-white font-medium rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
      :disabled="!outputText.trim()">
      反转义
    </button>
  </div>

  <!-- 输出区域 -->
  <div class="mb-6">
    <label class="block text-sm font-medium text-gray-700 mb-2">转义字符串：</label>
    <textarea v-model="outputText" rows="4"
      class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-mono text-sm resize-vertical"
      placeholder="输入转义字符串，点击右侧按钮进行恢复"></textarea>
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
  <!-- </div> -->
</template>

<script setup lang="ts">
import { ref } from 'vue';

const inputText = ref('');
const outputText = ref('');
const escapeMode = ref('html');
const errorMessage = ref('');

// HTML 实体编码/解码
const htmlEncode = (str: string): string => {
  const textarea = document.createElement('textarea');
  textarea.textContent = str;
  return textarea.innerHTML;
};

const htmlDecode = (str: string): string => {
  const textarea = document.createElement('textarea');
  textarea.innerHTML = str;
  return textarea.value;
};

// 处理字符串转换
const processString = (operate: string) => {
  errorMessage.value = '';

  try {
    let result = '';
    if (operate === 'encode') {
      const input = inputText.value;
      // console.log('Encoding with mode:', escapeMode.value);
      // 编码
      switch (escapeMode.value) {
        case 'html':
          result = htmlEncode(input);
          break;
        case 'url':
          result = encodeURIComponent(input);
          break;
        case 'uri':
          result = encodeURI(input);
          break;
        case 'json':
          result = JSON.stringify(input);
          break;
        case 'base64':
          result = btoa(unescape(encodeURIComponent(input)));
          break;
        default:
          result = input;
      }
      outputText.value = result;
    } else if (operate === 'decode') {
      // console.log('Decoding with mode:', escapeMode.value);
      const output = outputText.value;
      // 解码
      switch (escapeMode.value) {
        case 'html':
          result = htmlDecode(output);
          break;
        case 'url':
          result = decodeURIComponent(output);
          break;
        case 'uri':
          result = decodeURI(output);
          break;
        case 'json':
          result = JSON.parse(output);
          break;
        case 'base64':
          result = decodeURIComponent(escape(atob(output)));
          break;
        default:
          result = output;
      }
      inputText.value = result;
    }
  } catch (error) {
    errorMessage.value = `转换失败: ${error instanceof Error ? error.message : '未知错误'}`;
    outputText.value = '';
  }
};
</script>