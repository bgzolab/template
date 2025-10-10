<template>
  <h1 class="text-3xl font-bold text-gray-800 mb-2">双拼解码工具</h1>
  <p class="text-gray-600 mb-6">将双拼编码还原为完整拼音（小鹤双拼方案）</p>

  <!-- 输入区域 -->
  <div class="mb-6">
    <label class="block text-sm font-medium text-gray-700 mb-2">双拼字符串：</label>
    <textarea v-model="inputText" rows="3"
      class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-mono text-sm resize-vertical"
      placeholder="输入双拼字符串，如：nihc,jbtmtmqihfhc"></textarea>
  </div>

  <!-- 操作控制区域 -->
  <div class="flex flex-col sm:flex-row items-center gap-4 mb-6 p-4 rounded-lg">
    <button @click="decodeDoublePinYin"
      class="px-6 py-2 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
      :disabled="!inputText.trim()">
      解码
    </button>

    <button @click="clearAll"
      class="px-6 py-2 bg-gray-600 text-white font-medium rounded-md hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors duration-200">
      清空
    </button>
  </div>

  <!-- 输出区域 -->
  <div class="mb-6">
    <label class="block text-sm font-medium text-gray-700 mb-2">解码结果：</label>
    <textarea v-model="outputText" rows="3"
      class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-mono text-sm resize-vertical"
      placeholder="解码后的完整拼音将显示在这里" readonly></textarea>
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
      <li>• 输入双拼编码字符串，每两个字母代表一个音节的声母和韵母</li>
      <li>• 支持逗号分隔多个词组，如：nihc,jbtmtmqihfhc</li>
      <li>• 使用小鹤双拼方案进行解码</li>
      <li>• 输出格式：ni'hao, jin'tian'tian'qi'hen'hao</li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

// 小鹤双拼标准韵母码表（单字母）
const doublePinYinMap: Record<string, string> = {
  q: 'iu',
  w: 'ei',
  e: 'e',
  r: 'uan',
  t: 'ue', // üe
  y: 'iao',
  u: 'u',
  i: 'i',
  o: 'o', //uo
  p: 'ie',
  a: 'a',
  s: 'ong', //'iong'
  d: 'ai',
  f: 'en',
  g: 'eng',
  h: 'ang',
  j: 'an',
  k: 'uai',   //ing
  l: 'uang',  //iang
  z: 'ou',
  x: 'ua',    //ia
  c: 'ao',
  v: 'ui',    //ü
  b: 'in',
  n: 'iao',
  m: 'ian'
};


// 小鹤双拼声母码表（单字母）
const consonantMap: Record<string, string> = {
  q: 'q',
  w: 'w',
  e: 'e',
  r: 'r',
  t: 't',
  y: 'y',
  u: 'sh',
  i: 'ch',
  o: 'o',
  p: 'p',
  a: 'a',
  s: 's',
  d: 'd',
  f: 'f',
  g: 'g',
  h: 'h',
  j: 'j',
  k: 'k',
  l: 'l',
  z: 'z',
  x: 'x',
  c: 'c',
  v: 'zh',
  b: 'b',
  n: 'n',
  m: 'm'
};

// 解码逻辑：每两个字母为一组，首字母查声母，次字母查韵母

const inputText = ref('');
const outputText = ref('');
const errorMessage = ref('');

// 解码双拼字符串
const decodeDoublePinYin = () => {
  errorMessage.value = '';
  outputText.value = '';

  try {
    const input = inputText.value.trim();
    if (!input) {
      errorMessage.value = '请输入双拼字符串';
      return;
    }

    // 按逗号分割词组
    const groups = input.split(',');
    const decodedGroups: string[] = [];

    for (const group of groups) {
      const syllables = decodeGroup(group.trim());
      if (syllables.length > 0) {
        decodedGroups.push(syllables.join("'"));
      }
    }

    if (decodedGroups.length === 0) {
      errorMessage.value = '解码失败：无法识别的双拼编码';
      return;
    }

    outputText.value = decodedGroups.join(', ');

  } catch (error) {
    errorMessage.value = `解码失败: ${error instanceof Error ? error.message : '未知错误'}`;
  }
};

// 解码单个词组
const decodeGroup = (group: string): string[] => {
  const syllables: string[] = [];
  let i = 0;

  while (i < group.length) {
    // 每两个字符作为一个音节
    if (i + 1 >= group.length) {
      throw new Error(`无效的双拼编码：${group}，长度必须为偶数`);
    }

    const consonantCode = group[i];
    const vowelCode = group[i + 1];
    const syllableCode = consonantCode + vowelCode;

    // 获取声母
    const consonant = consonantMap[consonantCode];
    if (!consonant) {
      throw new Error(`未知的声母编码：${consonantCode}`);
    }

    // 获取韵母
    const vowel = doublePinYinMap[vowelCode];
    if (!vowel) {
      throw new Error(`未知的韵母编码：${vowelCode}`);
    }

    // 组合完整拼音
    const fullSyllable = consonant + vowel;
    syllables.push(fullSyllable);

    i += 2;
  }

  return syllables;
};

// 清空所有内容
const clearAll = () => {
  inputText.value = '';
  outputText.value = '';
  errorMessage.value = '';
};
</script>